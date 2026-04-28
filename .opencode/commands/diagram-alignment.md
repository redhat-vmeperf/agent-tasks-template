---
description: Detect and fix visual alignment errors in UTF-8 and ASCII box-drawing diagrams in markdown files
subtask: false
---

Load the `diagram-alignment` skill and execute it against the files: $ARGUMENTS

If no files are provided, ask the user which markdown files to check.

Arguments reference:

- `/diagram-alignment <file.md> [file2.md ...]` — Check and fix specific files
- `/diagram-alignment --check <file.md>` — Check only, do not fix
