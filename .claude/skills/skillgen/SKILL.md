---
name: skillgen
description: Generate new skills automatically from detected workflow patterns using the 4-gate Skill Generation Pipeline (Analyze, Generate, Security Review, Activate) with human approval gates.
argument-hint: "[skill description | resume:<gate-number>]"
---

# Skill Generation Skill

This skill runs the 4-gate Skill Generation Pipeline for creating new skills from detected workflow patterns. Read `.agents/pipelines/SKILLGEN.md` for the full pipeline process definition, gate definitions, escalation protocol, and all process rules.

**Arguments:**
- `/skillgen <description>` — Start the pipeline from Gate 1 with a manual skill description
- `/skillgen resume:<N> <skill>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/skillgen gate:<name>` — Jump to a specific gate (analyze, generate, security, activate)

---

## Security

- Security steps cannot be skipped.
- No interaction with any service or system may reduce the security posture of data passing through the process (REQ-5).
- Generated skill files must pass the full SECURITY_REVIEW_CHECKLIST.md before activation (REQ-6 equivalent).
- Generated skills are treated as untrusted content until human-approved.

---

## Skill Generation Context

This skill produces **skill definitions, pipeline definitions, role files, and platform entry points** as its output, not code.

- Gate 1 blocks: No skill is generated until a human confirms the detected pattern
- Gate 2 output: Complete skill file set (SKILL.md, PIPELINE.md, roles, platform entries) + Generation Report
- Gate 3 blocks: No skill activates without passing security review
- Gate 4 final action: WRITE FILES + ACTIVATE SKILL (human-approved)
