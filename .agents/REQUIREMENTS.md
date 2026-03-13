# Project Requirements

This file contains **non-negotiable, project-specific requirements**. They are not suggestions. They are not defaults that can be overridden by convenience or delivery pressure. Every agent reads this file. Every gate enforces it. Violations are REQUIRED findings that block gate advancement.

All agents read this file alongside `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` before beginning any gate work.

Full requirement descriptions are in `.agents/requirements/`. Each file contains the requirement statement, rationale, scope, and enforcement rules.

---

## Requirement Index

| ID    | Requirement                          | Enforced at Gates | Full Description |
|-------|--------------------------------------|-------------------|------------------|
| REQ-1 | Inclusive language (ASWF guide)       | 1–7 (all gates)   | [REQ-001.md](requirements/REQ-001.md) |
| REQ-2 | Full ADR and audit log written to .sdlc at every step | 1–7 (all gates) | [REQ-002.md](requirements/REQ-002.md) |
| REQ-3 | Code file line limit: 500 lines max  | 4, 5, 6           | [REQ-003.md](requirements/REQ-003.md) |
| REQ-4 | Test file line limit: 500 lines max  | 4, 5, 6           | [REQ-004.md](requirements/REQ-004.md) |
| REQ-5 | Security posture preservation        | 1-7 (all gates)   | [REQ-005.md](requirements/REQ-005.md) |
| REQ-6 | External context file security review | 1-7 (all gates)   | [REQ-006.md](requirements/REQ-006.md) |
| REQ-7 | Use .test TLD in all testing contexts | 1-7 (all gates)   | [REQ-007.md](requirements/REQ-007.md) |

---

## Requirements Enforcement Summary

```
Requirements Compliance Matrix
──────────────────────────────────────────────────────────────────────────────
Requirement      Gate 1   Gate 2   Gate 3   Gate 4   Gate 5   Gate 6   Gate 7
                 ARCH     SEC-ARCH TEAM     ENG      CODE REV QUALITY  AUDIT
──────────────────────────────────────────────────────────────────────────────
REQ-1 Inclusive  REQUIRED REQUIRED REQUIRED Enforce  REQUIRED  REQUIRED CRIT
REQ-2 .sdlc      WRITE    WRITE    VERIFY   WRITE    REQUIRED  REQUIRED CRIT
REQ-3 Code 500   —        —        Visible  Enforce  REQUIRED  REQUIRED  —
REQ-4 Test 500   —        —        Visible  Enforce  REQUIRED  REQUIRED  —
REQ-5 Posture   REQUIRED REQUIRED Visible  Enforce  REQUIRED  REQUIRED CRIT
REQ-6 Ext.Review REQUIRED REQUIRED Visible  Enforce  REQUIRED  REQUIRED CRIT
REQ-7 .test TLD  REQUIRED REQUIRED REQUIRED Enforce  REQUIRED  REQUIRED CRIT
──────────────────────────────────────────────────────────────────────────────
WRITE    = Agent must write/update .sdlc/ artifacts — gate cannot advance without them
VERIFY   = Agent must verify .sdlc/ artifacts exist from prior gates — missing = BLOCKED
REQUIRED = Code Reviewer or Quality Engineer finding — blocks gate advancement
CRIT     = Security Auditor finding severity
Visible  = Team Lead surfaces in Sprint Brief
──────────────────────────────────────────────────────────────────────────────
```

---

## Updating This File

This file is maintained by the human stakeholder or principal architect. Changes require:
1. A new ADR documenting the change rationale (Gate 1)
2. Human approval at Gate 3 before the change takes effect
3. A note in `.agents/LESSONS.md` under Cross-Cutting lessons if the change reflects a learned pattern

Agents do not modify this file.
