---
description: Generate new skills automatically from detected workflow patterns using a 4-gate pipeline with human approval gates
subtask: false
---

Load the `skillgen` skill and execute it with the following arguments: $ARGUMENTS

If no arguments are provided, ask the user to describe the skill they want to generate, or describe the recurring workflow pattern they want to codify.

Arguments reference:
- `/skillgen <description>` — Start the pipeline from Gate 1 with a manual skill description
- `/skillgen resume:<N> <skill>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/skillgen gate:<name>` — Jump to a specific gate (analyze, generate, security, activate)
