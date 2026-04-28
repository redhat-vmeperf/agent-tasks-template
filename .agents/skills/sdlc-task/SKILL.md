---
name: sdlc-task
description: Run the full SDLC pipeline autonomously without human approval gates — all roles execute, produce artifacts, and self-correct by looping back when discoveries change architecture, scope, or security posture.
generated: true
generated-date: 2026-03-31
source-sessions:
  - skillgen-2026-03-31
triggering-pattern: Autonomous SDLC execution for subtask resolution and lower-ceremony work
last-used: 2026-03-31
capability-scope:
  reads:
    - ".agents/**/*.md"
    - ".sdlc/**/*.md"
    - "src/**"
    - "tests/**"
  writes:
    - ".sdlc/audit/task-*.md"
    - ".sdlc/sessions/task-*/**"
    - "src/**"
    - "tests/**"
  external:
    - "none"
---

# sdlc-task Skill

Platform-agnostic definition for the autonomous (ungated) SDLC pipeline.

This skill runs the same 7 roles as the standard SDLC pipeline (Architect, Security Architect, Team Lead, Engineer, Code Reviewer, Quality Engineer, Security Auditor) but without human approval gates. All gates are advisory — agents produce their artifacts, surface findings, and self-advance.

When a later gate discovers something that changes architecture, scope, or security posture, the pipeline loops back to Gate 1 to re-evaluate with the new information, then continues forward. This makes the pipeline self-improving, not just advisory.

## Behavior

- All 7 roles execute in sequence and produce their standard artifacts
- No gate blocks on human approval — agents self-advance
- Self-correction: discoveries that change architecture, scope, or security posture trigger a loop back to Gate 1 (max 2 re-evaluation cycles to prevent infinite loops)
- Finding mitigation is driven by the invoker's directions — findings within scope are mitigated, findings outside scope are flagged
- Audit trail is mandatory (REQ-2), entries marked as `UNGATED`
- All common files (CYNEFIN.md, PERSONALITY.md, LESSONS.md, REQUIREMENTS.md) are loaded

## Pipeline

See `.agents/skills/sdlc-task/PIPELINE.md` for the full pipeline process definition.

## Invocation Context

This skill may be invoked:

1. Directly by a human for lower-ceremony tasks
2. By any pipeline that needs autonomous SDLC-quality analysis without blocking
