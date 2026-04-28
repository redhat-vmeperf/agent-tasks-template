# Jira Pipeline

This file defines the 3-gate Jira ticket creation pipeline. It is a purpose-built pipeline for creating Jira tickets, distilled from the 7-gate SDLC pipeline to eliminate ceremony that does not apply to ticket content.

For tasks that produce code, tests, or deployments, use the SDLC pipeline (`.agents/pipelines/SDLC.md`). For tasks that produce Jira ticket content, use this pipeline.

---

## Pipeline Overview

```
 Task Input
     │
     ▼
┌────────────────────────────────────────────────────────────────┐
│                     JIRA PIPELINE                              │
│                                                                │
│  ┌───────────┐     ┌───────────┐     ┌───────────┐             │
│  │  Gate 1   │     │  Gate 2   │     │  Gate 3   │             │
│  │  PLAN     │────►│  DRAFT    │────►│  REVIEW   │             │
│  │           │     │           │     │           │             │
│  │ Classify  │     │ Write all │     │ Content + │             │
│  │ Decompose │     │ ticket    │     │ security  │             │
│  │ ◄HUMAN►   │     │ content   │     │ ◄HUMAN►   │             │
│  └───────────┘     └───────────┘     └────┬──────┘             │
│                                           │                    │
└───────────────────────────────────────────┼────────────────────┘
                                            │
                                            ▼
                                    CREATE TICKETS
                                    (human-approved)
```

**Human gates** (◄HUMAN►): Pipeline does not advance without explicit human approval.

**Gate 1** is mandatory: no ticket content is drafted until a human approves the plan.

**Gate 3** is mandatory: no tickets are created until a human approves the final review.

---

## Common Files (All Gates Load First)

Every gate reads these files before beginning work:

```
.agents/CYNEFIN.md        <- Cynefin framework: classify before responding
.agents/PERSONALITY.md    <- Shared values, lenses, behavioral commitments
.agents/LESSONS.md        <- Accumulated lessons from past sessions
.agents/REQUIREMENTS.md   <- Non-negotiable project requirements
```

Requirements violations are **always findings** at gates where they are enforced.

---

## Gate Definitions

---

### Gate 1: Plan

```
Input:       Task description
Output:      Ticket Plan
Gate type:   MANDATORY human approval — no drafting begins without this
```

**Agent instructions:**

You are the Planner. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, `.agents/LESSONS.md`, and `.agents/REQUIREMENTS.md` first.

Your task:

1. Classify the incoming request using the Cynefin framework (see `.agents/CYNEFIN.md` for heuristics)
2. Determine the ticket decomposition strategy: what tickets to create, what type each is (epic, story, task, sub-task), how they relate to each other, and what priority order they should be created in
3. Identify security flags: note any areas where ticket content could inadvertently include sensitive data (credentials, internal URLs, infrastructure details, access control specifics)
4. Surface open questions that need human input before drafting
5. Produce the Ticket Plan

**Ticket Plan format:**

```
# Ticket Plan: [Short title]

Date: YYYY-MM-DD
Status: Proposed
Cynefin Domain: [Clear | Complicated | Complex | Chaotic]
Domain Justification: [2-4 sentences]

## Ticket Decomposition

[Describe the planned ticket structure. Use a tree diagram for
hierarchical relationships.]

  EPIC: [title]
  ├── STORY: [title]
  ├── STORY: [title]
  └── TASK: [title]

## Ticket Summary Table

| # | Type  | Summary                    | Priority | Dependencies |
|---|-------|----------------------------|----------|--------------|
| 1 | Epic  | [summary]                  | [H/M/L]  | None         |
| 2 | Story | [summary]                  | [H/M/L]  | #1           |

## Security Flags

  [Flag 1: description of sensitive data risk]
  [Or: "No security flags identified."]

## Open Questions

  ? [Question needing human input]
  [Or: "All questions resolved."]
```

Present the Ticket Plan to the human and await approval before advancing to Gate 2.

**Gate 1 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 1: TICKET PLAN                                        │
│                                                             │
│  The Ticket Plan above is ready for your review.            │
│                                                             │
│  Please select:                                             │
│    A) Approve — proceed to Draft                            │
│    B) Revise — provide feedback; plan will be updated       │
│    C) Reject — provide reason; task will be re-scoped       │
└─────────────────────────────────────────────────────────────┘
```

---

### Gate 2: Draft

```
Input:       Approved Ticket Plan from Gate 1
Output:      Complete ticket content + Draft Report
Gate type:   No direct human gate — output goes to Gate 3
```

**Agent instructions:**

You are the Drafter. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, `.agents/LESSONS.md`, and `.agents/REQUIREMENTS.md` first.

Your task:

1. Write all ticket content exactly as specified in the approved Ticket Plan
2. For each ticket, produce: summary, description, acceptance criteria, labels, and components
3. Follow the Jira content standards below
4. Produce the Draft Report

If you discover that the approved plan contains a gap or error that changes the ticket structure or scope: stop, escalate to Gate 1, do not proceed.

**Jira content standards:**

```
Stories:
  - Written as "As a [role], I want [goal], so that [benefit]"
  - Include acceptance criteria as testable statements
  - Each criterion starts with "Given/When/Then" or is a verifiable condition

Tasks:
  - Description explains what technical work is needed and why
  - Include acceptance criteria as completion conditions

Epics:
  - Description provides high-level context and scope
  - Lists the stories/tasks it contains

Sub-tasks:
  - Brief, actionable descriptions
  - Clear completion condition

All tickets:
  - Summaries are concise (under 80 characters)
  - Descriptions provide enough context to work without side-channel knowledge
  - No sensitive data: no credentials, no internal URLs, no infrastructure
    details beyond what is appropriate for the Jira project's access level
  - Labels and components use existing project conventions where known
```

**Draft Report format:**

```
# Draft Report: [Task Title]

Date: YYYY-MM-DD
Ticket Plan Reference: [date]

## Tickets Drafted

  [N] tickets drafted ([breakdown by type])

## Deviations from Plan

  [If none: "None — draft matches approved plan."]

## Items for Review Attention

  [Flag any areas where acceptance criteria testability is uncertain,
   where descriptions required assumptions, or where security flags
   from the plan needed special handling.]
```

---

### Gate 3: Review

```
Input:       Draft Report + all ticket content from Gate 2
Output:      Review Report
Gate type:   MANDATORY human approval — no tickets created without this
```

**Agent instructions:**

You are the Reviewer. Read `.agents/CYNEFIN.md`, `.agents/PERSONALITY.md`, `.agents/LESSONS.md`, and `.agents/REQUIREMENTS.md` first.

Your task is to review all ticket content across two mandatory dimensions: Content Quality and Security. Both dimensions must be evaluated. Produce the Review Report and present it to the human for final approval.

### Dimension 1: Content Quality

```
Review Checklist
  □ Ticket structure matches the approved plan
  □ Story descriptions follow "As a [role]..." format
  □ Acceptance criteria are testable (verifiable conditions, not vague)
  □ Dependencies between tickets are correctly identified
  □ Priority ordering is logical
  □ Descriptions are self-contained (no side-channel context needed)
  □ Summaries are concise and descriptive
  □ No duplicate content across tickets
  □ Consistent terminology across all tickets
```

### Dimension 2: Security Check

```
Security Checklist
  □ No credentials or secrets in ticket content
  □ No internal URLs or endpoints
  □ No infrastructure details beyond what is appropriate for the
    Jira project's access level
  □ No personally identifiable information (PII)
  □ Security flags from the Ticket Plan are addressed
  □ REQ-1 (inclusive language) compliance verified
  □ REQ-5 (security posture) — no ticket content reduces security posture
```

**Finding classification:**

```
  ✗ REQUIRED    Must be resolved before tickets are created.
  ↑ SUGGESTED   Advisory. Human decides.
  ✓ POSITIVE    Something done well.
```

**Review Report format:**

```
# Review Report: [Task Title]

Date: YYYY-MM-DD
Draft Report Reference: [date]

## Summary

  Tickets reviewed: [N]
  Required changes: [N]
  Suggestions: [N]

## Content Quality

  [Checklist results. Findings listed with classification.]

## Security Check

  [Checklist results. Findings listed with classification.]

## Findings

  [Detailed findings, if any]

  ┌────────────────────────────────────────────────────────┐
  │ RV-001 ✗ REQUIRED                                      │
  │                                                        │
  │ [Description — specific, not vague]                    │
  │ Suggested fix: [actionable guidance]                   │
  └────────────────────────────────────────────────────────┘

## Review Verdict

  Required changes:
    RV-NNN — [one-line description]
    [If none: "None — cleared for ticket creation."]

  Gate status:
    ✓ APPROVED         No required changes
    ⚠ WITH CONDITIONS  Required changes listed above
    ✗ BLOCKED          [N] required changes must be resolved
```

**Gate 3 approval prompt:**

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 3: FINAL REVIEW — MANDATORY APPROVAL                  │
│                                                             │
│  Required changes: [N]   Suggestions: [N]                   │
│                                                             │
│  Please select:                                             │
│    A) Approve — CLEARED FOR TICKET CREATION                 │
│    B) Request changes — drafter resolves and re-submits     │
│    C) Reject — provide reason                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Audit Trail

Every gate completion appends a timestamped entry to the audit trail in `.sdlc/audit/<type>-<session-name>.md`. The session name is derived from the task description, prefixed with a sortable type (e.g., `task-`, `feature-`). Gate artifacts are stored in `.sdlc/sessions/<type>-<session-name>/`.

```
| Gate | Role     | Date       | Status   | Approved by |
|------|----------|------------|----------|-------------|
| 1    | Planner  | YYYY-MM-DD | APPROVED | [name]      |
| 2    | Drafter  | YYYY-MM-DD | COMPLETE | —           |
| 3    | Reviewer | YYYY-MM-DD | APPROVED | [name]      |
```

---

## Escalation Protocol

```
Gate 2 discovers plan error     -> Return to Gate 1
Gate 3 finds required changes   -> Return to Gate 2 for fix,
                                   then re-run Gate 3
```

---

## Cynefin-Adaptive Gate Depth

```
Clear       Lightweight plan. Emphasis on structure, not analysis.
Complicated Full depth. Standard protocol.
Complex     Full depth. Gate 2 may be a probe (draft a subset first).
```

---

## When to Use SDLC Instead

Use the SDLC pipeline (`.agents/pipelines/SDLC.md`) instead of this pipeline when:

- Ticket content describes security-sensitive architecture (access controls, authentication flows, encryption)
- The task involves creating tickets for infrastructure changes that require threat modeling
- The ticket content itself needs STRIDE analysis (e.g., tickets that will contain security requirements)

---

## File Reference

```
.agents/
  CYNEFIN.md                   <- Cynefin framework (all gates)
  PERSONALITY.md               <- Shared persona (all gates)
  LESSONS.md                   <- Accumulated lessons
  REQUIREMENTS.md              <- Non-negotiable project requirements
  SECURITY_REVIEW_CHECKLIST.md <- External file review process (REQ-6)
  pipelines/
    JIRA.md                    <- This file (Jira pipeline)
    SDLC.md                    <- SDLC pipeline (for code tasks)
```
