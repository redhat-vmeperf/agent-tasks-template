"""
AI-powered pre-commit review hook.

Runs review phases against staged git changes:
  - persona: Condensed 7-persona SDLC review (self-contained prompt)
  - sdlc:    Full SDLC pipeline self-review (references .agents/ files)
  - diagram: Diagram alignment review (runs linter, then AI analysis)

Configuration is primarily via environment variables (see --help).

Exit codes:
  0 = PASS (or CLI not found in non-strict mode)
  1 = FAIL (findings, error, or CLI not found in strict mode)
"""

import argparse
import os
import secrets
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# Named constants
VERDICT_SENTINEL = "## VERDICT:"
VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
BOUNDARY_PLACEHOLDER = "{{DATA_BOUNDARY}}"
BOUNDARY_PREFIX = "===REVIEW_BOUNDARY_"
BOUNDARY_SUFFIX = "==="
MAX_BOUNDARY_ATTEMPTS = 3

# Per-phase configuration: prompt file path and default timeout
PHASE_CONFIG = {
    "persona": {
        "prompt": "scripts/prompts/persona-review.md",
        "timeout": 300,
    },
    "sdlc": {
        "prompt": "scripts/prompts/sdlc-review.md",
        "timeout": 600,
    },
    "diagram": {
        "prompt": "scripts/prompts/diagram-review.md",
        "timeout": 300,
    },
}

# CLI invocation patterns for non-interactive, print-to-stdout mode.
# Prompt is passed via stdin for all patterns.
CLI_PATTERNS = {
    "claude": ["claude", "--print", "-p"],
    "opencode": ["opencode", "--prompt"],
}


def find_repo_root():
    """Walk up from script location to find the repo root (contains .git)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    # Fallback: assume script is in scripts/ under repo root
    return Path(__file__).resolve().parent.parent


def resolve_cli():
    """Determine which AI CLI to use.

    Priority:
      1. AI_REVIEW_CLI environment variable
      2. Auto-detection from PATH
    """
    env_cli = os.environ.get("AI_REVIEW_CLI", "").strip()
    if env_cli:
        return env_cli

    for cli_name in CLI_PATTERNS:
        if shutil.which(cli_name) is not None:
            return cli_name

    return None


def get_staged_diff():
    """Get the staged git diff for review."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--no-color"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return result.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        print(f"Error: failed to get staged diff: {err}", file=sys.stderr)
        return None


def generate_boundary(diff_content):
    """Generate a unique boundary marker that does not appear in the diff.

    SEC-001 mitigation: the boundary is random and verified absent from
    the diff content before use. If the diff contains the generated
    boundary after multiple attempts, fail — the diff may be attempting
    a framing attack. This mirrors the approach in
    .agents/SECURITY_REVIEW_CHECKLIST.md (SEC-001 mitigation).
    """
    for _ in range(MAX_BOUNDARY_ATTEMPTS):
        token = secrets.token_hex(8)
        boundary = f"{BOUNDARY_PREFIX}{token}{BOUNDARY_SUFFIX}"
        if boundary not in diff_content:
            return boundary

    print(
        "Error: could not generate a unique boundary marker after "
        f"{MAX_BOUNDARY_ATTEMPTS} attempts — possible framing attack. "
        "Review the diff manually.",
        file=sys.stderr,
    )
    return None


def extract_markdown_paths_from_diff(diff_content, repo_root):
    """Extract markdown file paths mentioned in a unified diff.

    SEC-002: Resolved paths are validated to be within repo_root
    to prevent path traversal via crafted diff headers.
    """
    paths = set()
    repo_root_resolved = repo_root.resolve()
    for line in diff_content.splitlines():
        if line.startswith("+++ b/") and line.endswith(".md"):
            rel_path = line[6:]  # strip "+++ b/"
            resolved = (repo_root / rel_path).resolve()
            if str(resolved).startswith(str(repo_root_resolved) + os.sep):
                paths.add(rel_path)
    return sorted(paths)


SCRIPT_OUTPUT_PLACEHOLDER = "{{SCRIPT_OUTPUT}}"

DIAGRAM_LINTER_SCRIPT = "scripts/verify-diagram-alignment.py"
# Also excluded in .pre-commit-config.yaml (diagram-alignment hook entry)
DIAGRAM_LINTER_EXCLUDE = ".agents/pipelines/DIAGRAM_ALIGNMENT.md"


def run_diagram_linter(repo_root, markdown_files):
    """Run the diagram alignment linter on the given files.

    Returns the captured stdout, or a message if no files to check
    or the script is missing.
    """
    script_path = repo_root / DIAGRAM_LINTER_SCRIPT
    if not script_path.exists():
        return f"Warning: linter script not found at {DIAGRAM_LINTER_SCRIPT}"

    # Filter out the excluded file
    files_to_check = [
        f for f in markdown_files if f != DIAGRAM_LINTER_EXCLUDE
    ]
    if not files_to_check:
        return "No markdown files to check (all excluded)."

    # Resolve paths relative to repo root
    resolved = [str(repo_root / f) for f in files_to_check]

    try:
        result = subprocess.run(
            ["python3", str(script_path)] + resolved,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(repo_root),
        )
        # SEC-003: Only include stdout in the prompt. Stderr may contain
        # error messages from malicious filenames and is not data-framed.
        # Stderr is logged separately for developer visibility.
        if result.stderr:
            print(f"Diagram linter stderr: {result.stderr}", file=sys.stderr)
        return result.stdout.strip() if result.stdout.strip() else "No diagrams found."
    except subprocess.TimeoutExpired:
        return "Warning: diagram linter timed out after 60 seconds."
    except OSError as err:
        return f"Warning: failed to run diagram linter: {err}"


def build_prompt(phase, repo_root, diff_content, script_output=None):
    """Build the full prompt by reading the prompt file and appending the diff.

    Per SEC-001, a dynamic boundary is generated at runtime, verified
    absent from the diff, and injected into the prompt template. The
    diff is placed after the boundary marker.

    If script_output is provided and the template contains the
    SCRIPT_OUTPUT_PLACEHOLDER, the output is injected at that location.
    """
    prompt_rel_path = PHASE_CONFIG[phase]["prompt"]
    if not prompt_rel_path:
        print(f"Error: unknown phase '{phase}'", file=sys.stderr)
        return None

    prompt_path = repo_root / prompt_rel_path
    if not prompt_path.exists():
        print(f"Error: prompt file not found: {prompt_path}", file=sys.stderr)
        return None

    try:
        prompt_template = prompt_path.read_text(encoding="utf-8")
    except OSError as err:
        print(f"Error: failed to read prompt file: {err}", file=sys.stderr)
        return None

    # SEC-001: Generate a dynamic boundary verified absent from ALL
    # untrusted content (diff and script output). Both are placed below
    # the boundary in the prompt template.
    all_untrusted = diff_content
    if script_output:
        all_untrusted = script_output + "\n" + diff_content

    boundary = generate_boundary(all_untrusted)
    if boundary is None:
        return None

    # Replace the placeholder in the prompt template with the actual boundary
    prompt = prompt_template.replace(BOUNDARY_PLACEHOLDER, boundary)

    # Inject script output if the template has the placeholder
    if script_output and SCRIPT_OUTPUT_PLACEHOLDER in prompt:
        prompt = prompt.replace(SCRIPT_OUTPUT_PLACEHOLDER, script_output)

    # Append the diff after the template (which ends with the diff section header)
    return f"{prompt}\n{diff_content}\n"


def build_cli_command(cli_name, custom_cli):
    """Build the subprocess command list for the chosen CLI.

    Returns a list of command parts. The prompt is passed via stdin.
    """
    if custom_cli:
        return shlex.split(custom_cli)

    pattern = CLI_PATTERNS.get(cli_name)
    if pattern:
        return list(pattern)

    # Unknown CLI — invoke directly, prompt via stdin
    return [cli_name]


def exit_on_missing_cli(msg, strict):
    """Handle CLI unavailability with strict/permissive behavior."""
    if strict:
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Warning: {msg} — skipping AI review", file=sys.stderr)
        sys.exit(0)


def invoke_ai_cli(command, prompt, timeout_seconds):
    """Invoke the AI CLI with the prompt and return its stdout.

    The prompt is passed via stdin to avoid shell injection (SEC-001
    mitigation: no shell=True, no string interpolation in command).
    """
    try:
        result = subprocess.run(
            command,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

        if result.returncode != 0:
            print(f"AI CLI returned non-zero exit code: {result.returncode}", file=sys.stderr)
            if result.stderr:
                print(f"AI CLI stderr: {result.stderr}", file=sys.stderr)
            return None

        return result.stdout

    except subprocess.TimeoutExpired:
        print(
            f"Error: AI CLI timed out after {timeout_seconds} seconds",
            file=sys.stderr,
        )
        return None
    except FileNotFoundError:
        print(f"Error: AI CLI command not found: {command[0]}", file=sys.stderr)
        return None
    except OSError as err:
        print(f"Error: failed to invoke AI CLI: {err}", file=sys.stderr)
        return None


def parse_verdict(ai_output):
    """Parse the AI output for a PASS/FAIL verdict.

    SEC-003 mitigation: parse the LAST verdict line in the output,
    not the first. This reduces the impact of injected early verdict
    lines from diff content.

    Returns: ("PASS", reason) or ("FAIL", reason) or (None, error_msg)
    """
    if not ai_output:
        return None, "No output received from AI CLI"

    # Find the last line containing the verdict sentinel
    last_verdict_line = None
    for line in ai_output.splitlines():
        stripped = line.strip()
        if stripped.startswith(VERDICT_SENTINEL):
            last_verdict_line = stripped

    if last_verdict_line is None:
        return None, "No verdict line found in AI output"

    # Extract verdict after the sentinel
    verdict_text = last_verdict_line[len(VERDICT_SENTINEL):].strip()

    if verdict_text.upper().startswith(VERDICT_PASS):
        return VERDICT_PASS, verdict_text

    if verdict_text.upper().startswith(VERDICT_FAIL):
        return VERDICT_FAIL, verdict_text

    return None, f"Unrecognized verdict format: {verdict_text}"


def main():
    """Entry point for the pre-commit hook."""
    parser = argparse.ArgumentParser(
        prog="python3 scripts/ai-review.py",
        description="AI-powered pre-commit review hook.",
        epilog=(
            "Environment variables:\n"
            "  AI_REVIEW_CLI      AI CLI name: claude, opencode, or custom\n"
            "  AI_REVIEW_STRICT   true to fail when CLI unavailable (default: false)\n"
            "  AI_REVIEW_TIMEOUT  Timeout in seconds (overrides per-phase default)\n"
            "  AI_REVIEW_CUSTOM   Custom CLI command (prompt via stdin)\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "phase",
        choices=sorted(PHASE_CONFIG),
        help="Review phase to run",
    )
    args = parser.parse_args()
    phase = args.phase

    repo_root = find_repo_root()

    # Resolve configuration from environment variables
    strict_raw = os.environ.get("AI_REVIEW_STRICT", "false").strip().lower()
    strict = strict_raw in ("true", "yes", "1")

    default_timeout = PHASE_CONFIG[phase]["timeout"]
    timeout_raw = os.environ.get("AI_REVIEW_TIMEOUT", "").strip()
    try:
        timeout_seconds = int(timeout_raw) if timeout_raw else default_timeout
    except ValueError:
        timeout_seconds = default_timeout
    timeout_seconds = max(timeout_seconds, 1)

    custom_cli = os.environ.get("AI_REVIEW_CUSTOM", "").strip()

    # Find the AI CLI
    cli_name = resolve_cli()
    if cli_name is None:
        exit_on_missing_cli(
            "No AI CLI found (checked AI_REVIEW_CLI env, PATH auto-detection)",
            strict,
        )

    # Verify the resolved CLI is actually available on PATH
    cli_executable = CLI_PATTERNS[cli_name][0] if cli_name in CLI_PATTERNS else cli_name
    if not custom_cli and shutil.which(cli_executable) is None:
        exit_on_missing_cli(f"AI CLI '{cli_name}' not found on PATH", strict)

    # Get the staged diff
    diff = get_staged_diff()
    if diff is None:
        print("Error: could not retrieve staged diff", file=sys.stderr)
        sys.exit(1)

    if not diff.strip():
        # No staged changes — nothing to review
        print("No staged changes to review.", file=sys.stderr)
        sys.exit(0)

    # For diagram phase, run the deterministic linter first
    script_output = None
    if phase == "diagram":
        md_files = extract_markdown_paths_from_diff(diff, repo_root)
        if md_files:
            print(f"Running diagram linter on {len(md_files)} file(s)...", file=sys.stderr)
            script_output = run_diagram_linter(repo_root, md_files)
            print(script_output, file=sys.stderr)
        else:
            script_output = "No markdown files in diff."

    # Build the prompt
    prompt = build_prompt(phase, repo_root, diff, script_output=script_output)
    if prompt is None:
        sys.exit(1)

    # Build the CLI command
    command = build_cli_command(cli_name, custom_cli)

    # Invoke the AI CLI
    print(f"Running {phase} review with {cli_name}...", file=sys.stderr)
    ai_output = invoke_ai_cli(command, prompt, timeout_seconds)

    if ai_output is None:
        print("Error: AI CLI invocation failed", file=sys.stderr)
        sys.exit(1)

    # Print the full AI output to stderr for developer visibility
    print("\n--- AI Review Output ---", file=sys.stderr)
    print(ai_output, file=sys.stderr)
    print("--- End AI Review Output ---\n", file=sys.stderr)

    # Parse the verdict (SEC-003: parse LAST verdict line)
    verdict, reason = parse_verdict(ai_output)

    if verdict is None:
        # Fail-safe: unparsable output = FAIL
        print(f"Error: could not parse verdict — {reason}", file=sys.stderr)
        print("Fail-safe: treating unparsable output as FAIL", file=sys.stderr)
        sys.exit(1)

    if verdict == VERDICT_PASS:
        print(f"{phase.upper()} review: PASS", file=sys.stderr)
        sys.exit(0)

    # FAIL
    print(f"{phase.upper()} review: FAIL — {reason}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
