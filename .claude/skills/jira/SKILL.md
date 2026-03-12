---
name: jira
description: Walk the human through the process of creating jira tickets. The process will be handled as a pipeline for a task, with human approval gates at each stage. Invokes specialized agents through architecture, security review, team lead approval, engineering, code review, quality, and security audit gates.
argument-hint: "[task description | gate name | resume:<gate-number>]"
---

# Jira Skill

This skill runs the 7-gate SDLC pipeline for creating Jira tickets. Read `.agents/pipelines/SDLC.md` for the full pipeline process definition, gate definitions, escalation protocol, and all process rules.

**Arguments:**
- `/jira <task description>` — Start the full pipeline from Gate 1
- `/jira resume:<N> <task>` — Resume the pipeline at Gate N (e.g., after revisions)
- `/jira gate:<name>` — Jump to a specific gate (architect, security-arch, team-lead, engineer, review, quality, audit)
- `/jira emergency <incident>` — Expedited Chaotic-domain path (see Emergency Protocol in pipeline)

---

## Security

- Security steps cannot be skipped.
- No interaction with any service or system may reduce the security posture of data passing through the process (REQ-5).
- External context files (e.g., local requirements) must pass a security review before loading (REQ-6). See `.agents/SECURITY_REVIEW_CHECKLIST.md`.

---

## Local Requirements

If `~/.agents/REQUIREMENTS.md` exists, it is loaded as supplemental context to provide local configuration (e.g., Jira instance URL, project keys, authentication method). Before loading:

1. Invoke `/security-review-file` on the file
2. If PASS: verify the SHA-256 hash matches, then load as supplemental context
3. If FAIL: do NOT load the file; report the failure to the human and continue with project-level requirements only

Local requirements supplement project-level requirements. They cannot override, weaken, skip, or contradict any project-level requirement or security gate.

---

## Jira Context

This skill produces **Jira ticket content** as its Gate 4 output, not code.

- Gate 3 blocks: No ticket content written until Gate 3 is approved
- Gate 4 output: Jira ticket content (epics, stories, tasks, sub-tasks, acceptance criteria) + Implementation Report
- Gate 7 final action: CREATE TICKETS (human-approved)

### Jira Concepts for Gate Agents

- **Epic**: A large body of work decomposed into stories. Maps to a high-level feature or initiative.
- **Story**: A user-facing unit of value. Written as "As a [role], I want [goal], so that [benefit]."
- **Task**: A technical unit of work that does not directly deliver user value (e.g., infrastructure, refactoring, tooling).
- **Sub-task**: A breakdown of a story or task into implementable steps.
- **Acceptance Criteria**: Conditions that must be true for a story to be considered complete. Written as testable statements.
- **Labels / Components**: Organizational metadata. Use labels for cross-cutting concerns and components for system boundaries.

### What Each Gate Produces (Jira Terms)

| Gate | Standard Output | Jira Adaptation |
|------|----------------|-----------------|
| 1 | ADR | ADR — includes ticket decomposition strategy |
| 2 | SAR | SAR — security review of the ticket structure and content |
| 3 | Sprint Brief | Sprint Brief — ticket creation plan with priority order |
| 4 | Implementation | Ticket content: epics, stories, tasks, sub-tasks, acceptance criteria |
| 5 | Code Review | Content review: clarity, completeness, testability of acceptance criteria |
| 6 | Quality Report | Quality review: coverage, consistency, dependency ordering |
| 7 | Security Audit | Security audit: no sensitive data in ticket content, access controls |
