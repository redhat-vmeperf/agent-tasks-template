# SDLC Task Pipeline (Ungated)

This file defines the ungated variant of the SDLC pipeline. It runs the same 7 roles as `.agents/pipelines/SDLC.md` but without human approval gates. All gates are advisory and self-advancing.

When a later gate discovers something that changes architecture, scope, or security posture, the pipeline loops back to Gate 1 with the discovery as new context, re-evaluates, and continues forward. This self-correction loop runs a maximum of 2 times per pipeline invocation.

For the gated pipeline, see `.agents/pipelines/SDLC.md`.

---

## Pipeline Overview

```
 Task Input
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│                   SDLC TASK PIPELINE (UNGATED)               │
│                                                              │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│  │ Gate 1  │   │ Gate 2  │   │ Gate 3  │   │ Gate 4  │       │
│  │ARCHITECT│──►│SEC.ARCH │──►│TEAM LEAD│──►│ENGINEER │       │
│  │  ADR    │   │  SAR    │   │ BRIEF   │   │  IMPL   │       │
│  │ ADVISORY│   │ ADVISORY│   │ADVISORY │   │         │       │
│  └────▲────┘   └─────────┘   └─────────┘   └────┬────┘       │
│       │                                         │            │
│       │        ┌────────────────────────────────┘            │
│       │        │  Discovery changes arch/scope/security?     │
│       │        │  YES ──► LOOP BACK (max 2 cycles)           │
│       │        │  NO  ──► continue                           │
│       │        ▼                                             │
│  ┌────┴────┐   ┌─────────┐   ┌─────────┐                     │
│  │ RE-EVAL │   │ Gate 6  │   │ Gate 5  │                     │
│  │ (loop)  │   │QUALITY  │◄──│CODE REV │◄──── (continue)     │
│  └─────────┘   └─────────┘   └─────────┘                     │
│                     │                                        │
│                ┌────▼────┐                                   │
│                │ Gate 7  │                                   │
│                │SEC.AUDIT│                                   │
│                │ ADVISORY│                                   │
│                └────┬────┘                                   │
│                     │                                        │
└─────────────────────┼────────────────────────────────────────┘
                      │
                      ▼
                CONSOLIDATED REPORT
```

**All gates are ADVISORY.** No gate blocks on human approval. Agents produce artifacts, surface findings, and self-advance.

**Self-correction loop:** When any gate from 4-7 discovers a change to architecture, scope, or security posture, the pipeline loops back to Gate 1 with the discovery as context.

---

## Common Files (All Agents Load First)

Same as the standard SDLC pipeline:

```
.agents/CYNEFIN.md        ← Cynefin framework: classify before responding
.agents/PERSONALITY.md    ← Shared values, lenses, behavioral commitments
.agents/LESSONS.md        ← Accumulated lessons from past sessions
.agents/REQUIREMENTS.md   ← Non-negotiable project requirements
```

Role-specific instructions are in `.agents/roles/` (same roles as standard SDLC).

---

## Advisory Gate Behavior

Each gate follows this protocol:

1. **Load common files** and role-specific instructions (same as standard SDLC)
2. **Produce the gate artifact** (ADR, SAR, Sprint Brief, etc.) exactly as defined in `.agents/pipelines/SDLC.md`
3. **Self-evaluate the artifact** — identify any findings, open questions, or blockers
4. **Record findings** with their severity classifications
5. **Apply the invoker's directions and mitigate findings:**
   - Read the invoker's task description to understand scope and intent
   - Mitigate findings that fall within the invoker's directions
   - Flag findings outside the invoker's scope in the gate artifact
   - If a mitigation changes architecture, scope, or security posture: trigger the Re-Evaluation Protocol
6. **Check for re-evaluation triggers** (Gates 4-7 only) — see Re-Evaluation Protocol
7. **Self-advance** to the next gate without waiting for human approval

### Finding Handling Policy

```
Finding Handling Policy
──────────────────────────────────────────────────────────────────
The invoker's directions determine what gets mitigated.

1. READ the invoker's task description to understand intent
2. MITIGATE findings that fall within the invoker's directions
3. If the invoker's directions are broad (e.g., "build feature X"),
   mitigate all findings encountered — the intent is a complete,
   quality result
4. If the invoker's directions are narrow (e.g., "fix the auth
   vulnerability"), mitigate findings within that scope and FLAG
   findings outside it in the Consolidated Report
5. If a mitigation changes architecture, scope, or security
   posture: trigger the Re-Evaluation Protocol

All findings — mitigated or flagged — surface in the
Consolidated Report with their original severity, resolution
status, and the gate that identified them.
──────────────────────────────────────────────────────────────────
```

---

## Re-Evaluation Protocol

When any gate from 4-7 discovers something that changes architecture, scope, or security posture, the pipeline loops back to Gate 1.

```
Re-Evaluation Protocol
──────────────────────────────────────────────────────────────────
Trigger conditions (any gate 4-7):
  - A discovery invalidates an assumption in the ADR
  - A security gap not covered by the SAR is found
  - Implementation reveals the approved scope is insufficient
  - A code review or quality finding requires architectural change
  - A security audit finding requires design-level remediation

When triggered:
  1. RECORD the discovery in the current gate artifact
  2. INCREMENT the re-evaluation counter
  3. CHECK: if re-evaluation counter > 2, DO NOT loop back.
     Instead, flag the discovery in the Consolidated Report
     with ⚠ RE-EVALUATION LIMIT REACHED and continue forward
  4. LOOP BACK to Gate 1 with the discovery as additional context:
     - The original task description
     - The discovery that triggered re-evaluation
     - All artifacts produced so far (for reference, not repetition)
  5. Gate 1 (Architect) re-evaluates the ADR in light of the
     discovery, updating it as needed
  6. Gates 2-3 re-evaluate with the updated ADR
  7. Pipeline continues forward from Gate 4

Re-evaluation cycles are tracked in the audit trail:

| Cycle | Triggered at | Discovery | Gates re-run |
|-------|-------------|-----------|--------------|
| 1     | Gate 5      | [summary] | 1-7          |
| 2     | Gate 7      | [summary] | 1-7          |

Maximum re-evaluation cycles: 2 per pipeline invocation.
After 2 cycles, the pipeline completes with remaining findings
flagged in the Consolidated Report.
──────────────────────────────────────────────────────────────────
```

---

## Gate Definitions

Gates 1-7 use the same role files and produce the same artifacts as `.agents/pipelines/SDLC.md`. The only difference is the removal of human approval gates and the addition of the re-evaluation protocol.

### Gate 1: Architecture (Advisory)

```
Role file:   .agents/roles/ARCHITECT.md
Input:       Task description (+ re-evaluation context if looping)
Output:      Architecture Decision Record (ADR)
Gate type:   ADVISORY — self-advancing
```

Produce the ADR per ARCHITECT.md instructions. On re-evaluation cycles, update the existing ADR with the new discovery rather than starting from scratch. Note what changed and why.

### Gate 2: Security Architecture Review (Advisory)

```
Role file:   .agents/roles/SECURITY_ARCHITECT.md
Input:       ADR from Gate 1
Output:      Security Architecture Review (SAR)
Gate type:   ADVISORY — self-advancing
```

Produce the SAR per SECURITY_ARCHITECT.md instructions. Mitigate findings per invoker's directions.

### Gate 3: Team Lead Synthesis (Advisory)

```
Role file:   .agents/roles/TEAM_LEAD.md
Input:       ADR (Gate 1) + SAR (Gate 2)
Output:      Sprint Brief
Gate type:   ADVISORY — self-advancing
```

Synthesize and produce Sprint Brief per TEAM_LEAD.md instructions. Surface unresolved risks. Record go/no-go recommendation (advisory only). Advance.

### Gate 4: Engineering

```
Role file:   .agents/roles/ENGINEER.md
Input:       ADR + SAR + Sprint Brief
Output:      Implementation artifacts + Implementation Report
Gate type:   Same as standard SDLC (no human gate in standard either)
```

Implement per ENGINEER.md instructions. If a discovery changes architecture, scope, or security posture: trigger the Re-Evaluation Protocol.

### Gate 5: Code Review (Advisory)

```
Role file:   .agents/roles/CODE_REVIEWER.md
Input:       Implementation Report + artifacts from Gate 4
Output:      Code Review Report
Gate type:   ADVISORY — self-advancing
```

If a finding requires architectural change: trigger the Re-Evaluation Protocol.

### Gate 6: Quality (Advisory)

```
Role file:   .agents/roles/QUALITY_ENGINEER.md
Input:       Code Review Report (Gate 5) + artifacts
Output:      Quality Report
Gate type:   ADVISORY — self-advancing
```

If an OWASP violation or quality finding requires design-level change: trigger the Re-Evaluation Protocol.

### Gate 7: Security Audit (Advisory)

```
Role file:   .agents/roles/SECURITY_AUDITOR.md
Input:       Quality Report (Gate 6) + all prior artifacts
Output:      Security Audit Report (SAR-Code)
Gate type:   ADVISORY — self-advancing
```

If a Critical finding requires design-level remediation: trigger the Re-Evaluation Protocol.

---

## Consolidated Report

After Gate 7 (and any re-evaluation cycles), produce a Consolidated Report:

```
# Consolidated Report: [Task Name]

Date: YYYY-MM-DD
Pipeline: SDLC Task (Ungated)
Invoker: [human | other]
Recursion depth: [N] (if invoked as subtask)
Re-evaluation cycles: [N] (0, 1, or 2)

## Task Description

[Original task as provided by invoker]

## Re-Evaluation History

[If cycles > 0:]
| Cycle | Triggered at | Discovery | Resolution |
|-------|-------------|-----------|------------|
| 1     | Gate [N]    | [summary] | [how ADR/SAR changed] |

[If cycles = 0: "No re-evaluation cycles required."]

## Gate Summary

| Gate | Role              | Status   | Findings (C/H/M/L/I) | Action Taken |
|------|-------------------|----------|-----------------------|--------------|
| 1    | Architect         | COMPLETE | 0/0/0/0/0             | —            |
| 2    | Security Arch.    | COMPLETE | 0/0/0/0/0             | MITIGATED    |
| 3    | Team Lead         | COMPLETE | —                     | —            |
| 4    | Engineer          | COMPLETE | —                     | —            |
| 5    | Code Reviewer     | COMPLETE | 0/0/0/0/0             | —            |
| 6    | Quality Engineer  | COMPLETE | 0/0/0/0/0             | —            |
| 7    | Security Auditor  | COMPLETE | 0/0/0/0/0             | —            |

## ⚠ Unfixed Findings

[List any findings that were flagged but not fixed (only when
invoker narrowed scope), with gate of origin, severity, and
reason not fixed. If none: "All findings mitigated."]

## ⚠ RE-EVALUATION LIMIT REACHED

[Only present if re-evaluation counter hit 2 and further
re-evaluation was needed but not performed. List the
discoveries that could not be addressed.]

## Key Decisions Made

[Summarize the architectural and security decisions from Gates 1-3]

## Implementation Summary

[Brief summary of what was built/changed from Gate 4]

## Recommendations

[Any recommendations from review gates (5-7) that were not acted on]
```

---

## Audit Trail

Every gate completion appends a timestamped entry to `.sdlc/audit/task-<session-name>.md`. All entries are marked `UNGATED`. Re-evaluation cycles are recorded.

```
| Gate | Agent             | Date       | Status   | Mode    | Cycle |
|------|-------------------|------------|----------|---------|-------|
| 1    | Architect         | YYYY-MM-DD | COMPLETE | UNGATED | 0     |
| 2    | Security Arch.    | YYYY-MM-DD | COMPLETE | UNGATED | 0     |
| ...  | ...               | ...        | ...      | ...     | ...   |
| 5    | Code Reviewer     | YYYY-MM-DD | RE-EVAL  | UNGATED | 0     |
| 1    | Architect         | YYYY-MM-DD | COMPLETE | UNGATED | 1     |
| 2    | Security Arch.    | YYYY-MM-DD | COMPLETE | UNGATED | 1     |
| ...  | ...               | ...        | ...      | ...     | ...   |
```

---

---

## Escalation Protocol (Self-Correcting)

In ungated mode, escalations trigger re-evaluation rather than just flagging:

```
Discovery                         Ungated behavior
─────────────────────────        ─────────────────────────────
Gate 4 discovers ADR error    →  RE-EVALUATE from Gate 1
Gate 4 discovers security gap →  RE-EVALUATE from Gate 1
Gate 5 discovers scope creep  →  RE-EVALUATE from Gate 1
Gate 6 finds OWASP violation  →  RE-EVALUATE from Gate 1
  requiring design change
Gate 7 finds Critical issue   →  RE-EVALUATE from Gate 1
  requiring design change

If re-evaluation counter > 2:
  FLAG in Consolidated Report with
  ⚠ RE-EVALUATION LIMIT REACHED
```

Findings that do NOT change architecture, scope, or security posture are mitigated per the invoker's directions — they do not trigger re-evaluation.

---

## File Reference

```
.agents/
  skills/sdlc-task/
    SKILL.md                     ← Skill definition (this file's parent)
    PIPELINE.md                  ← This file
  roles/                         ← Standard SDLC roles (reused, not copied)
    ARCHITECT.md                 ← Gate 1
    SECURITY_ARCHITECT.md        ← Gate 2
    TEAM_LEAD.md                 ← Gate 3
    ENGINEER.md                  ← Gate 4
    CODE_REVIEWER.md             ← Gate 5
    QUALITY_ENGINEER.md          ← Gate 6
    SECURITY_AUDITOR.md          ← Gate 7

.sdlc/
  audit/task-<session-name>.md   ← Audit trail (auto-created, marked UNGATED)
  sessions/task-<session-name>/  ← Session artifacts (auto-created)
```
