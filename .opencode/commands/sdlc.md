---
description: Run the full SDLC pipeline (7 gates) with human approval at each stage
subtask: false
---

Load the `sdlc` skill and execute it with the following arguments: $ARGUMENTS

If no arguments are provided, ask the user to describe the task they want to run through the SDLC pipeline.

Arguments reference:

- `/sdlc <task description>` — Start the full pipeline from Gate 1
- `/sdlc resume:<N> <task>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/sdlc gate:<name>` — Jump to a specific gate (architect, security-arch, team-lead, engineer, review, quality, audit)
- `/sdlc emergency <incident>` — Expedited Chaotic-domain path
