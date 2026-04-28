"""
Resolve version tags to pinned commit SHAs in CI and pre-commit configs.

Updates two files:
  1. .github/workflows/ci.yml — GitHub Actions `uses:` references
  2. .pre-commit-config.yaml  — pre-commit `repo:` / `rev:` references

For each versioned reference, resolves the tag to the latest patch
version within that major version, pins to the commit SHA, and writes
the resolved version in a comment.

Examples:
  CI:         `uses: actions/checkout@v4`
           -> `uses: actions/checkout@abc123...  # v4.3.1`

  pre-commit: `rev: v5.0.0`
           -> `rev: abc123...  # v5.0.0`

Re-running updates to the latest patch within each major version.

Usage:
    python scripts/update-pinned-shas.py

Requires: git on PATH.
"""

import re
import subprocess
import sys
from pathlib import Path

# File paths relative to repo root
WORKFLOW_PATH = ".github/workflows/ci.yml"
PRECOMMIT_PATH = ".pre-commit-config.yaml"

# Patterns
VERSION_TAG_PATTERN = re.compile(r"^v(\d+)(?:\.(\d+)(?:\.(\d+))?)?$")
CI_USES_PATTERN = re.compile(r"^(\s*uses:\s*)([^@]+)@(\S+?)(\s*#.*)?$")
PRECOMMIT_REPO_PATTERN = re.compile(
    r"^(\s*-\s*repo:\s*)https://github\.com/([^\s]+?)(?:\.git)?\s*$"
)
PRECOMMIT_REV_PATTERN = re.compile(r"^(\s*rev:\s*)(\S+?)(\s*#.*)?$")


def find_repo_root():
    """Walk up from script location to find the repo root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def parse_version(tag):
    """Parse a version tag into (major, minor, patch) tuple.

    Returns None if not a version tag.
    """
    match = VERSION_TAG_PATTERN.match(tag)
    if not match:
        return None
    major = int(match.group(1))
    minor = int(match.group(2)) if match.group(2) is not None else 0
    patch = int(match.group(3)) if match.group(3) is not None else 0
    return (major, minor, patch)


def is_sha(value):
    """Check if a string looks like a commit SHA."""
    return len(value) >= 40 and all(c in "0123456789abcdef" for c in value)


def fetch_all_tags(owner_repo):
    """Fetch all tags from a remote repo via git ls-remote."""
    url = f"https://github.com/{owner_repo}.git"

    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as err:
        print(f"    Error: git ls-remote failed: {err}", file=sys.stderr)
        return {}

    if result.returncode != 0:
        print(f"    Error: git ls-remote returned {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(f"    {result.stderr.strip()}", file=sys.stderr)
        return {}

    tags = {}
    for line in result.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ref_sha = parts[0]
        ref_name = parts[1]

        if ref_name.startswith("refs/tags/"):
            tag_name = ref_name[len("refs/tags/"):]
            if tag_name.endswith("^{}"):
                tag_name = tag_name[:-3]
                tags[tag_name] = ref_sha
            elif tag_name not in tags:
                tags[tag_name] = ref_sha

    return tags


def find_latest_in_major(tags, major_version):
    """Find the latest semver tag within a major version."""
    best_version = (-1, -1, -1)
    best_tag = None
    best_sha = None

    for tag_name, sha in tags.items():
        version = parse_version(tag_name)
        if version is None:
            continue
        if version[0] != major_version:
            continue
        if version > best_version:
            best_version = version
            best_tag = tag_name
            best_sha = sha

    return best_tag, best_sha


def resolve_tag(owner_repo, tag):
    """Resolve a tag to the latest patch within its major version."""
    version = parse_version(tag)
    tags = fetch_all_tags(owner_repo)

    if not tags:
        return None, None

    if version is not None:
        resolved_tag, sha = find_latest_in_major(tags, version[0])
        if resolved_tag is not None:
            return resolved_tag, sha

    if tag in tags:
        return tag, tags[tag]

    return None, None


def resolve_and_pin(owner_repo, tag, comment):
    """Resolve a version reference to a pinned SHA.

    Handles both fresh tags and already-pinned SHAs (re-resolves from
    the version in the comment). Returns (resolved_tag, sha) or None
    to signal the reference should be skipped.
    """
    if is_sha(tag):
        if comment.startswith("# "):
            tag = comment[2:].strip()
            print(f"  {owner_repo} (re-resolving from {tag})")
        else:
            print(f"  {owner_repo}@... pinned, no version comment, skipping")
            return None
    else:
        print(f"  {owner_repo}@{tag}")

    resolved_tag, sha = resolve_tag(owner_repo, tag)
    if sha is None:
        print("    FAILED — skipping")
        return None

    print(f"    -> {sha}  # {resolved_tag}")
    return resolved_tag, sha


def update_ci_workflow(repo_root):
    """Update GitHub Actions references in CI workflow."""
    workflow_path = repo_root / WORKFLOW_PATH
    if not workflow_path.exists():
        print(f"  {WORKFLOW_PATH} not found, skipping")
        return 0

    lines = workflow_path.read_text(encoding="utf-8").splitlines(keepends=True)
    updated = 0

    for i, line in enumerate(lines):
        match = CI_USES_PATTERN.match(line.rstrip("\n"))
        if not match:
            continue

        prefix = match.group(1)
        owner_repo = match.group(2)
        tag = match.group(3)
        comment = (match.group(4) or "").strip()

        result = resolve_and_pin(owner_repo, tag, comment)
        if result is None:
            continue

        resolved_tag, sha = result
        lines[i] = f"{prefix}{owner_repo}@{sha}  # {resolved_tag}\n"
        updated += 1

    workflow_path.write_text("".join(lines), encoding="utf-8")
    return updated


def update_precommit_config(repo_root):
    """Update rev: references in pre-commit config."""
    config_path = repo_root / PRECOMMIT_PATH
    if not config_path.exists():
        print(f"  {PRECOMMIT_PATH} not found, skipping")
        return 0

    lines = config_path.read_text(encoding="utf-8").splitlines(keepends=True)
    updated = 0
    current_repo = None

    for i, line in enumerate(lines):
        repo_match = PRECOMMIT_REPO_PATTERN.match(line.rstrip("\n"))
        if repo_match:
            current_repo = repo_match.group(2)
            continue

        rev_match = PRECOMMIT_REV_PATTERN.match(line.rstrip("\n"))
        if not rev_match or current_repo is None:
            continue

        prefix = rev_match.group(1)
        tag = rev_match.group(2)
        comment = (rev_match.group(3) or "").strip()

        result = resolve_and_pin(current_repo, tag, comment)
        if result is None:
            continue

        resolved_tag, sha = result
        lines[i] = f"{prefix}{sha}  # {resolved_tag}\n"
        updated += 1

    config_path.write_text("".join(lines), encoding="utf-8")
    return updated


def main():
    repo_root = find_repo_root()
    total = 0

    print(f"=== {WORKFLOW_PATH} ===\n")
    total += update_ci_workflow(repo_root)

    print(f"\n=== {PRECOMMIT_PATH} ===\n")
    total += update_precommit_config(repo_root)

    print(f"\nUpdated {total} reference(s) total.")
    print(f"Review with: git diff {WORKFLOW_PATH} {PRECOMMIT_PATH}")


if __name__ == "__main__":
    main()
