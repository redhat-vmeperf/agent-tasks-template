# SDLC Pipeline

This file defines the 7-gate Software Development Lifecycle pipeline. It is platform-agnostic process logic referenced by platform-specific skill files.

Skills that use this pipeline define their own metadata, arguments, context sections, and customizations. This file defines the gates, roles, escalation protocol, and process rules that all pipeline consumers share.

---

## Pipeline Overview

```
 Task Input
     │
     ▼
┌────────────────────────────────────────────────────────────────┐
│                     SDLC PIPELINE                              │
│                                                                │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│  │ Gate 1  │   │ Gate 2  │   │ Gate 3  │   │ Gate 4  │       │
│  │ARCHITECT│──►│SEC.ARCH │──►│TEAM LEAD│──►│ENGINEER │       │
│  │  ADR    │   │  SAR    │   │ BRIEF   │   │  IMPL   │       │
│  │ ◄HUMAN► │   │ ◄HUMAN► │   │◄HUMAN► │   │         │       │
│  └─────────┘   └─────────┘   └─────────┘   └────┬────┘       │
│                                                  │            │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐        │            │
│  │ Gate 7  │   │ Gate 6  │   │ Gate 5  │        │            │
│  │SEC.AUDIT│◄──│QUALITY  │◄──│CODE REV │◄───────┘            │
│  │ REPORT  │   │ REPORT  │   │ REPORT  │                     │
│  │◄HUMAN►  │   │ ◄HUMAN► │   │ ◄HUMAN► │                     │
│  └────┬────┘   └─────────┘   └─────────┘                     │
│       │                                                        │
└───────┼────────────────────────────────────────────────────────┘
        │
        ▼
   FINAL ACTION
   (skill-defined, human-approved)
```

**Human gates** (◄HUMAN►): Pipeline does not advance without explicit human approval.

**Mandatory gates** (Gate 3 and Gate 7): Hard stops. No implementation begins without Gate 3. No final action without Gate 7.

---

## Common Files (All Agents Load First)

Every agent in every gate reads these files before beginning work:

```
.agents/CYNEFIN.md        ← Cynefin framework: classify before responding
.agents/PERSONALITY.md    ← Shared values, lenses, behavioral commitments
.agents/LESSONS.md        ← Accumulated lessons from past sessions
.agents/REQUIREMENTS.md   ← Non-negotiable project requirements
```

Requirements violations are **always REQUIRED findings** at gates where they are enforced.

Role-specific instructions are in `.agents/roles/`.

---

## Gate Definitions

---

### Gate 1: Architecture

```
Role file:   .agents/roles/ARCHITECT.md
Input:       Task description
Output:      Architecture Decision Record (ADR)
Gate type:   Human review — approve / revise / reject
Blocking:    Revisions route back to Gate 1 before Gate 2 begins
```

**Agent instructions:**

You are acting as the Architect. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/ARCHITECT.md` for your role-specific protocol.

Your task:
1. Classify the incoming request using the Cynefin framework
2. Produce a complete Architecture Decision Record (ADR)
3. Include a UTF-8 diagram of the component/data flow structure
4. Pre-populate security flags for Gate 2
5. List all open questions explicitly

Present the ADR to the human and await approval before advancing to Gate 2.

**Gate 1 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 1: ARCHITECTURE REVIEW                                │
│                                                             │
│  The Architecture Decision Record above is ready for        │
│  your review.                                               │
│                                                             │
│  Please select:                                             │
│    A) Approve — proceed to Security Architecture Review     │
│    B) Revise — provide feedback; ADR will be updated        │
│    C) Reject — provide reason; task will be re-scoped       │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 2: Security Architecture Review

```
Role file:   .agents/roles/SECURITY_ARCHITECT.md
Input:       Approved ADR from Gate 1
Output:      Security Architecture Review (SAR)
Gate type:   Human review — approve / revise / reject
Blocking:    Critical/High/Medium findings block Gate 3 until mitigated
```

**Agent instructions:**

You are acting as the Security Architect. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/SECURITY_ARCHITECT.md` for your role-specific protocol.

Your task:
1. Map the attack surface from the approved ADR
2. Apply STRIDE threat modeling to every component and trust boundary
3. Evaluate against the security principles checklist
4. Classify every finding by severity
5. Produce the SAR

Severity policy:
- Critical / High / Medium: MUST be mitigated before Gate 3 advances
- Low / Info: presented to the human for a decision at this gate

**Gate 2 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 2: SECURITY ARCHITECTURE REVIEW                       │
│                                                             │
│  Required mitigations (Critical/High/Medium): [N]           │
│  Human decisions needed (Low/Info): [N]                     │
│                                                             │
│  Please select:                                             │
│    A) Approve — all required mitigations are addressed      │
│    B) Revise — provide feedback; SAR will be updated        │
│    C) Reject — provide reason                               │
│                                                             │
│  For each Low/Info finding:                                 │
│    Mitigate | Track as risk | Accept and close              │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 3: Team Lead — MANDATORY HUMAN APPROVAL

```
Role file:   .agents/roles/TEAM_LEAD.md
Input:       Approved ADR (Gate 1) + Approved SAR (Gate 2)
Output:      Sprint Brief
Gate type:   MANDATORY human approval — no implementation begins without this
```

**Agent instructions:**

You are acting as the Team Lead. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/TEAM_LEAD.md` for your role-specific protocol.

Your task:
1. Synthesize the approved ADR and SAR into a one-page Sprint Brief
2. Surface all unresolved risks and decisions
3. Present a go/no-go recommendation with reasoning
4. Present the mandatory human approval gate

Do not advance to Gate 4 until a human explicitly approves. Do not interpret silence as approval.

**Gate 3 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  ★ GATE 3: MANDATORY APPROVAL — NO WORK BEGINS UNTIL HERE   │
│                                                             │
│  Please select:                                             │
│    A) Approve — proceed to Engineering                      │
│    B) Approve with conditions — list conditions             │
│    C) No-go — return to Gate [N] with reason               │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 4: Engineering

```
Role file:   .agents/roles/ENGINEER.md
Input:       Approved ADR + Approved SAR + Human-approved Sprint Brief
Output:      Implementation artifacts (defined by skill) + Implementation Report
Gate type:   No direct human gate — output goes to Gate 5
```

**Agent instructions:**

You are acting as the Engineer. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/ENGINEER.md` for your role-specific protocol.

Your task:
1. Verify all pre-implementation checklist items
2. Implement the approved design exactly
3. Produce the Implementation Report

The skill definition specifies what Gate 4 produces (e.g., code and tests, ticket content, documentation). Follow the skill's context for output format.

If you discover that the approved design contains an error or gap that changes architecture, scope, or security posture: stop, escalate, do not proceed.

---

### Gate 5: Code Review

```
Role file:   .agents/roles/CODE_REVIEWER.md
Input:       Implementation Report + artifacts from Gate 4
Output:      Code Review Report
Gate type:   Human review — approve / revise / request changes
Blocking:    Required changes block Gate 6 until resolved
```

**Agent instructions:**

You are acting as the Code Reviewer. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/CODE_REVIEWER.md` for your role-specific protocol.

**Gate 5 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 5: CODE REVIEW                                        │
│                                                             │
│  Required changes: [N]   Suggestions: [N]                   │
│                                                             │
│  Please select:                                             │
│    A) Approve — no required changes, proceed to Quality     │
│    B) Request changes — engineer resolves and re-submits    │
│    C) Reject — provide reason                               │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 6: Quality

```
Role file:   .agents/roles/QUALITY_ENGINEER.md
Input:       Code Review Report (Gate 5) + artifacts
Output:      Quality Report
Gate type:   Human review — approve / revise / request changes
Blocking:    OWASP Top 10:2025 violations are always required changes
```

**Agent instructions:**

You are acting as the Quality Engineer. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/QUALITY_ENGINEER.md` for your role-specific protocol.

**Gate 6 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 6: QUALITY REVIEW                                     │
│                                                             │
│  Required changes: [N]   Suggestions: [N]                   │
│                                                             │
│  Please select:                                             │
│    A) Approve — no required changes, proceed to Audit       │
│    B) Request changes — engineer resolves and re-submits    │
│    C) Reject — provide reason                               │
│                                                             │
│  For each Suggested finding:                                │
│    Implement | Defer | Decline                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 7: Security Audit — MANDATORY FINAL GATE

```
Role file:   .agents/roles/SECURITY_AUDITOR.md
Input:       Quality Report (Gate 6) + all prior artifacts
Output:      Security Audit Report (SAR-Code)
Gate type:   MANDATORY human approval — no final action without this
Blocking:    Critical/High/Medium findings block approval
```

**Agent instructions:**

You are acting as the Security Auditor. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, and `.agents/LESSONS.md` first. Then read `.agents/roles/SECURITY_AUDITOR.md` for your role-specific protocol.

Your task:
1. Verify Gates 5 and 6 required changes are resolved
2. Read the approved SAR (Gate 2) — know what was already addressed
3. Perform a full adversarial security review against all audit dimensions
4. Produce the Security Audit Report with the Final Approval Record

Do not allow the gate to pass for Critical, High, or Medium findings. Delivery pressure is not a valid reason.

**Gate 7 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  ★ GATE 7: FINAL SECURITY AUDIT — MANDATORY APPROVAL        │
│                                                             │
│  Required mitigations (Critical/High/Medium): [N]           │
│  Human decisions needed (Low/Info): [N]                     │
│                                                             │
│  Please select:                                             │
│    A) Approve — all required mitigations resolved —         │
│       CLEARED FOR FINAL ACTION                              │
│    B) Request remediation — findings to be resolved         │
│    C) Reject — escalate to earlier gate                     │
│                                                             │
│  For each Low/Info finding:                                 │
│    Mitigate | Track as risk | Accept and close              │
└─────────────────────────────────────────────────────────────┘
```

---

## Audit Trail

Every gate completion appends a timestamped entry to the audit trail in `.sdlc/audit/<type>-<session-name>.md`. The session name is derived from the task description, prefixed with a sortable type (e.g., `feature-`, `task-`, `bug-`, `issue-`, `refactor-`, `docs-`). The same name is used for the corresponding session directory at `.sdlc/sessions/<type>-<session-name>/`, where the ADR, SAR, and other gate artifacts are stored.

```
| Gate | Agent             | Date       | Status   | Approved by |
|------|-------------------|------------|----------|-------------|
| 1    | Architect         | YYYY-MM-DD | APPROVED | [name]      |
| 2    | Security Arch.    | YYYY-MM-DD | APPROVED | [name]      |
| 3    | Team Lead         | YYYY-MM-DD | APPROVED | [name]      |
| 4    | Engineer          | YYYY-MM-DD | COMPLETE | —           |
| 5    | Code Reviewer     | YYYY-MM-DD | APPROVED | [name]      |
| 6    | Quality Engineer  | YYYY-MM-DD | APPROVED | [name]      |
| 7    | Security Auditor  | YYYY-MM-DD | APPROVED | [name]      |
```

---

## Escalation Protocol

```
Gate 4 discovers ADR error  ──► Return to Gate 1
Gate 4 discovers security   ──► Return to Gate 2
 gap not in SAR
Gate 5 discovers scope      ──► Return to Gate 3 (or Gate 1)
 creep
Gate 6 finds OWASP          ──► Return to Gate 4 for fix,
 violation                      then re-run Gates 5+6
Gate 7 finds Critical       ──► Return to Gate 4 for fix,
 issue                          then re-run Gates 5+6+7
```

---

## Cynefin-Adaptive Gate Depth

```
Clear       Standard depth. Emphasis on "why the best practice applies here."
Complicated Full depth. Standard protocol.
Complex     Full depth. Gate 4 is a probe. Expect iteration.
Chaotic     Expedited path (see Emergency Protocol).
```

---

## Emergency Protocol (Chaotic Domain)

For active incidents requiring expedited processing:

```
  E1. Stabilization Brief  ↓ Human approval required
  E2. Emergency Security   ↓ Human approval required
  E3. Emergency Approval   ↓ MANDATORY human approval
  E4. Emergency Fix        ↓
  E5. Emergency Audit      ↓ MANDATORY human approval before final action

  Post-stabilization: Full standard pipeline runs for the proper fix.
```

---

## Session Close: Lessons Update

At the end of every pipeline session (after Gate 7 closes), the Team Lead reviews all human feedback and updates `.agents/LESSONS.md`. This is not optional.

---

## File Reference

```
.agents/
  CYNEFIN.md                   ← Cynefin framework (all agents)
  PERSONALITY.md               ← Shared persona (all agents)
  LESSONS.md                   ← Accumulated lessons
  REQUIREMENTS.md              ← Non-negotiable project requirements
  SECURITY_REVIEW_CHECKLIST.md ← External file review process (REQ-6)
  pipelines/
    SDLC.md                    ← This file (pipeline process definition)
  roles/
    ARCHITECT.md               ← Gate 1
    SECURITY_ARCHITECT.md      ← Gate 2
    TEAM_LEAD.md               ← Gate 3 + session close
    ENGINEER.md                ← Gate 4
    CODE_REVIEWER.md           ← Gate 5
    QUALITY_ENGINEER.md        ← Gate 6 (OWASP Top 10:2025)
    SECURITY_AUDITOR.md        ← Gate 7

.sdlc/
  audit/
    <type>-<session-name>.md   ← Audit trail per session (auto-created)
  sessions/
    <type>-<session-name>/     ← Session artifact directory (auto-created)
      adr.md                   ← Architecture Decision Record
      sar.md                   ← Security Architecture Review
      <other-artifacts>.md     ← Additional gate artifacts as needed
```
