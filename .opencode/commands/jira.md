---
description: Create Jira tickets using a 3-gate pipeline (Plan, Draft, Review) with human approval gates
subtask: false
---

Load the `jira` skill and execute it with the following arguments: $ARGUMENTS

If no arguments are provided, ask the user to describe the task they want to create Jira tickets for.

Arguments reference:
- `/jira <task description>` — Start the pipeline from Gate 1
- `/jira resume:<N> <task>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/jira gate:<name>` — Jump to a specific gate (plan, draft, review)
