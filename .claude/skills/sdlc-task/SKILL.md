---
name: sdlc-task
description: Run the full SDLC pipeline autonomously without human approval gates — all 7 roles execute, self-correct by looping back on discoveries, and produce a consolidated report.
argument-hint: "[task description]"
---

# SDLC Task Skill (Autonomous)

This skill runs the 7-gate SDLC pipeline without human approval gates. Read `.agents/skills/sdlc-task/PIPELINE.md` for the full pipeline process definition.

**Arguments:**
- `/sdlc-task <task description>` — Run the full autonomous pipeline

---

## SDLC Task Context

This skill produces the same artifacts as `/sdlc` — **code, tests, inline documentation, and all gate reports** — but without blocking on human approval at any gate.

- All 7 roles execute in sequence (Architect through Security Auditor)
- All gate artifacts are produced (ADR, SAR, Sprint Brief, Implementation Report, Code Review, Quality Report, Security Audit)
- Self-correction: discoveries that change architecture, scope, or security posture loop back to Gate 1 (max 2 cycles)
- Finding mitigation is driven by the invoker's directions — findings within scope are mitigated, findings outside scope are flagged
- Audit trail entries are marked `UNGATED`
- Output: Consolidated Report summarizing all gates and re-evaluation cycles

Security of data and access controls:
- Security roles still execute their full analysis
- No interaction with any service or system may reduce the security posture of data passing through the process (REQ-5)
- External context files must pass a security review before loading (REQ-6)
