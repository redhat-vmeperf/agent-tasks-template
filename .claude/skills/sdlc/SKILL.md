---
name: sdlc
description: Run the full Software Development Lifecycle pipeline for a task, with human approval gates at each stage. Invokes specialized agents through architecture, security review, team lead approval, engineering, code review, quality, and security audit gates.
argument-hint: "[task description | gate name | resume:<gate-number>]"
---

# SDLC Skill

This skill runs the 7-gate SDLC pipeline for software engineering tasks. Read `.agents/pipelines/SDLC.md` for the full pipeline process definition, gate definitions, escalation protocol, and all process rules.

**Arguments:**

- `/sdlc <task description>` — Start the full pipeline from Gate 1
- `/sdlc resume:<N> <task>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/sdlc gate:<name>` — Jump to a specific gate (architect, security-arch, team-lead, engineer, review, quality, audit)
- `/sdlc emergency <incident>` — Expedited Chaotic-domain path (see Emergency Protocol in pipeline)

---

## SDLC Context

This skill produces **code, tests, and inline documentation** as its Gate 4 output.

- Gate 3 blocks: No code written until Gate 3 is approved
- Gate 4 output: Implementation (code, tests, inline docs) + Implementation Report
- Gate 4 instruction: Write tests alongside the code, not after
- Gate 7 final action: MERGE / DEPLOY (human-approved)

Security of data and access controls:

- Security steps cannot be skipped.
- No interaction with any service or system may reduce the security posture of data passing through the process (REQ-5).
- External context files must pass a security review before loading (REQ-6). See `.agents/SECURITY_REVIEW_CHECKLIST.md`.
