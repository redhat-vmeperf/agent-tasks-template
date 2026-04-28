#!/usr/bin/env python3
"""Verify diagram alignment in markdown files.

Reads markdown files, finds all fenced code blocks containing
box-drawing diagrams, and checks:
  - Line width consistency within each outer box
  - Vertical connector (│) alignment with junction chars (┬ ┴ ┼)
  - Inner box border width matching content width
"""

import argparse
import fnmatch
import sys

BOX_CORNERS = set("┌┐└┘")
JUNCTIONS = set("┬┴┼├┤")
VERT_BARS = set("│|")


def extract_code_blocks(lines):
    """Find all fenced code blocks with their line ranges."""
    blocks = []
    in_fence = False
    start = 0
    prev_text = ""

    for i, line in enumerate(lines):
        if line.startswith("```"):
            if in_fence:
                blocks.append({
                    "start": start,
                    "end": i,
                    "lines": lines[start + 1 : i],
                    "label": prev_text,
                })
                in_fence = False
            else:
                start = i
                in_fence = True
                prev_text = lines[i - 1] if i > 0 else ""

    return blocks


def is_diagram(block_lines):
    """Determine if a code block contains a box-drawing diagram."""
    has_top = False
    has_bottom = False
    has_box_chars = False

    for line in block_lines:
        chars = set(line)
        if chars & (BOX_CORNERS | JUNCTIONS | set("+")):
            has_box_chars = True
        if "┌" in line and "┐" in line:
            has_top = True
        if "└" in line and "┘" in line:
            has_bottom = True
        # ASCII boxes
        if "+" in line and "-" in line:
            plus_positions = [i for i, c in enumerate(line) if c == "+"]
            if len(plus_positions) >= 2:
                has_top = True
                has_bottom = True

    return has_box_chars and has_top and has_bottom


def find_box_groups(dlines):
    """Identify independent box groups by finding contiguous runs of
    lines that start with box characters at column 0. A gap (line that
    doesn't start with a box char, or is empty/short) separates groups."""
    box_chars = set("│┌└├┤+|")
    groups = []
    current_group = []

    for j, line in enumerate(dlines):
        first = line[0] if line else ""
        if first in box_chars:
            current_group.append(j)
        else:
            if current_group:
                groups.append(current_group)
                current_group = []

    if current_group:
        groups.append(current_group)

    return groups


def check_width_consistency(dlines):
    """Check that all lines within each independent box group have
    the same width. Multiple box groups (e.g., stacked separate boxes
    connected by a vertical connector) are checked independently."""
    issues = []
    groups = find_box_groups(dlines)

    if not groups:
        return issues, None

    widths = [len(line) for line in dlines]
    info = {"widths": widths, "groups": []}

    for group_lines in groups:
        # Find the top border within this group
        group_width = None
        top_line = None
        for j in group_lines:
            line = dlines[j]
            if line and (line[0] in ("┌", "├") or
                         (line[0] == "+" and len(line) > 1 and line[1] == "-")):
                group_width = len(line)
                top_line = j
                break

        if group_width is None:
            # No top border found; use the first line's width
            group_width = len(dlines[group_lines[0]])
            top_line = group_lines[0]

        info["groups"].append({"width": group_width, "top_line": top_line,
                               "lines": group_lines})

        for j in group_lines:
            w = len(dlines[j])
            if w != group_width:
                issues.append({
                    "type": "width",
                    "line": j,
                    "expected": group_width,
                    "actual": w,
                    "diff": w - group_width,
                    "group_top": top_line,
                })

    return issues, info


def check_vertical_connectors(dlines):
    """Check that vertical │ aligns with ┬ ┴ ┼ junctions."""
    issues = []

    # Collect all junction positions: col -> [(line, char)]
    junctions = {}
    for j, line in enumerate(dlines):
        for col, ch in enumerate(line):
            if ch in ("┬", "┴", "┼"):
                junctions.setdefault(col, []).append((j, ch))

    # For each junction column, check vertical bars between junctions
    for col in sorted(junctions.keys()):
        juncs = sorted(junctions[col], key=lambda x: x[0])
        for ji in range(len(juncs)):
            junc_line, junc_char = juncs[ji]

            # Determine search range: from this junction to next junction
            # or up to 10 lines if no next junction
            if ji + 1 < len(juncs):
                end_line = juncs[ji + 1][0]
            else:
                end_line = min(junc_line + 15, len(dlines))

            # Only check downward from ┬ and ┼
            if junc_char not in ("┬", "┼"):
                continue

            for between in range(junc_line + 1, end_line):
                if between >= len(dlines):
                    break
                line = dlines[between]

                # Get char at expected column
                char_at_col = line[col] if col < len(line) else " "

                if char_at_col in VERT_BARS:
                    continue  # Correct
                if char_at_col in ("┬", "┴", "┼", "┘", "└", "┐", "┌"):
                    break  # Hit another junction/corner, stop

                # Check for drift: is there a │ nearby?
                for offset in (-2, -1, 1, 2):
                    check_col = col + offset
                    if 0 <= check_col < len(line) and line[check_col] in VERT_BARS:
                        issues.append({
                            "type": "connector_drift",
                            "junction_col": col,
                            "junction_line": junc_line,
                            "junction_char": junc_char,
                            "actual_col": check_col,
                            "drift_line": between,
                            "offset": offset,
                        })
                        break
                else:
                    # No │ at expected col and none nearby — might be
                    # a gap or the connector doesn't extend here
                    # (could be content between boxes). Skip silently.
                    pass

    return issues


def check_inner_boxes(dlines):
    """Check inner box borders match their content line widths."""
    issues = []
    seen = set()

    for j, line in enumerate(dlines):
        for col, ch in enumerate(line):
            # Find inner box tops: ┌ not at column 0
            if ch == "┌" and col > 0:
                # Find matching ┐
                right_col = None
                for c2 in range(col + 1, len(line)):
                    if line[c2] == "┐":
                        right_col = c2
                        break

                if right_col is None:
                    continue

                key = (col, j)
                if key in seen:
                    continue
                seen.add(key)

                border_width = right_col - col + 1

                # Detect multi-column table: top border has ┬
                is_table = any(
                    line[c2] == "┬"
                    for c2 in range(col + 1, right_col)
                )

                # Check content and bottom lines
                for j2 in range(j + 1, min(j + 25, len(dlines))):
                    line2 = dlines[j2]
                    if col >= len(line2):
                        break

                    left_char = line2[col]

                    if left_char == "│":
                        # Content line: find the right-edge │.
                        # For tables with column separators, use the
                        # LAST │ (the table right edge), not the first
                        # (which is an internal column separator).
                        right_edge = None
                        if is_table:
                            for c2 in range(len(line2) - 1, col, -1):
                                if line2[c2] == "│":
                                    right_edge = c2
                                    break
                        else:
                            for c2 in range(col + 1, len(line2)):
                                if line2[c2] == "│":
                                    right_edge = c2
                                    break

                        if right_edge is not None:
                            content_width = right_edge - col + 1
                            if content_width != border_width:
                                issues.append({
                                    "type": "inner_box_mismatch",
                                    "left_col": col,
                                    "border_width": border_width,
                                    "border_line": j,
                                    "content_width": content_width,
                                    "content_line": j2,
                                })
                    elif left_char == "└":
                        # Bottom border: find matching ┘
                        for c2 in range(col + 1, len(line2)):
                            if line2[c2] in ("┘",):
                                bottom_width = c2 - col + 1
                                if bottom_width != border_width:
                                    issues.append({
                                        "type": "inner_box_bottom",
                                        "left_col": col,
                                        "top_width": border_width,
                                        "top_line": j,
                                        "bottom_width": bottom_width,
                                        "bottom_line": j2,
                                    })
                                break
                        break
                    else:
                        break

    return issues


def analyze_diagram(block, diagram_num):
    """Run all checks on a single diagram block."""
    dlines = block["lines"]
    file_line_base = block["start"] + 2  # +1 fence, +1 for 1-indexed
    label = block["label"].strip()[:60]

    print("=" * 70)
    print(f"DIAGRAM {diagram_num} (file line {block['start'] + 1}): {label}")
    print("=" * 70)

    # --- Widths ---
    print("\n--- LINE WIDTHS ---")
    for j, line in enumerate(dlines):
        w = len(line)
        display = line if len(line) <= 72 else line[:69] + "..."
        print(f"  Line {j:3d} (file:{file_line_base + j:3d}): w={w:3d} | {display}")

    width_issues, width_info = check_width_consistency(dlines)
    if width_info:
        groups = width_info.get("groups", [])
        if len(groups) == 1:
            ow = groups[0]["width"]
            print(f"\n  Outer box top width: {ow}")
        else:
            print(f"\n  {len(groups)} independent box group(s) found:")
            for gi, g in enumerate(groups):
                print(f"    Group {gi+1}: width={g['width']}, "
                      f"lines {g['lines'][0]}-{g['lines'][-1]}")
        if width_issues:
            print("  ** WIDTH MISMATCHES:")
            for issue in width_issues:
                print(f"     Line {issue['line']} (file:{file_line_base + issue['line']}): "
                      f"w={issue['actual']}, expected {issue['expected']} "
                      f"(off by {issue['diff']:+d})")
        else:
            if len(groups) == 1:
                print(f"  All outer box lines match width {groups[0]['width']}: OK")
            else:
                print(f"  All box groups internally consistent: OK")

    # --- Connectors ---
    print("\n--- VERTICAL CONNECTORS ---")
    conn_issues = check_vertical_connectors(dlines)
    if conn_issues:
        for issue in conn_issues:
            print(f"  ** DRIFT: {issue['junction_char']} at col {issue['junction_col']} "
                  f"(line {issue['junction_line']}), "
                  f"but │ at col {issue['actual_col']} on line {issue['drift_line']} "
                  f"(off by {issue['offset']:+d})")
    else:
        print("  All vertical connectors aligned: OK")

    # --- Inner boxes ---
    print("\n--- INNER BOX BORDERS ---")
    inner_issues = check_inner_boxes(dlines)
    if inner_issues:
        for issue in inner_issues:
            if issue["type"] == "inner_box_mismatch":
                print(f"  ** MISMATCH at col {issue['left_col']}: "
                      f"border w={issue['border_width']} (line {issue['border_line']}), "
                      f"content w={issue['content_width']} (line {issue['content_line']})")
            elif issue["type"] == "inner_box_bottom":
                print(f"  ** MISMATCH at col {issue['left_col']}: "
                      f"top w={issue['top_width']} (line {issue['top_line']}), "
                      f"bottom w={issue['bottom_width']} (line {issue['bottom_line']})")
    else:
        print("  Inner box borders consistent: OK")

    total = len(width_issues) + len(conn_issues) + len(inner_issues)
    print()
    if total == 0:
        print(f"RESULT: PASS ({len(dlines)} lines, no issues)")
    else:
        print(f"RESULT: FAIL ({total} issue(s) found)")
    print()
    return total


def process_file(file_path, after_only=False):
    """Process a single file. Returns the number of issues found."""
    with open(file_path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    blocks = extract_code_blocks(lines)
    diagrams = [b for b in blocks if is_diagram(b["lines"])]

    if after_only:
        diagrams = [b for b in diagrams if "AFTER" in b["label"].upper()]

    if not diagrams:
        return 0, 0  # (diagrams_checked, issues_found)

    print(f"Found {len(diagrams)} diagram block(s) in {file_path}\n")

    total_issues = 0
    for i, block in enumerate(diagrams):
        total_issues += analyze_diagram(block, i + 1)

    return len(diagrams), total_issues


def is_excluded(file_path, excludes):
    """Check if a file matches any exclude pattern.

    Matches against:
      - Exact path match (as given)
      - Glob against the full path
      - Glob against the basename
    """
    for pattern in excludes:
        if file_path == pattern:
            return True
        if fnmatch.fnmatch(file_path, pattern):
            return True
        basename = file_path.rsplit("/", 1)[-1] if "/" in file_path else file_path
        if fnmatch.fnmatch(basename, pattern):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify diagram alignment in markdown files."
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Markdown files to check",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Exclude files matching an exact path or glob pattern (repeatable)",
    )
    parser.add_argument(
        "--after-only",
        action="store_true",
        help="Only check diagrams that follow an AFTER label",
    )
    args = parser.parse_args()

    # Filter out excluded files
    filtered = []
    for fp in args.files:
        if is_excluded(fp, args.exclude):
            print(f"Skipping excluded file: {fp}")
        else:
            filtered.append(fp)

    if not filtered:
        print("All files excluded — nothing to check.")
        sys.exit(0)

    grand_total_diagrams = 0
    grand_total_issues = 0

    for file_path in filtered:
        diagrams_checked, issues_found = process_file(file_path, args.after_only)
        grand_total_diagrams += diagrams_checked
        grand_total_issues += issues_found

    if grand_total_diagrams > 0:
        print("=" * 70)
        print(f"TOTAL: {grand_total_diagrams} diagram(s) checked across "
              f"{len(filtered)} file(s), {grand_total_issues} issue(s) found")

    sys.exit(1 if grand_total_issues > 0 else 0)


if __name__ == "__main__":
    main()
