# Lessons: Communication and Human Interaction

How to present information to the human, what formats they prefer, and how to structure gate artifacts for efficient review.

**Relevant to:** Any agent presenting artifacts for human review, requesting approval, or handling feedback.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Approval Presentation

<!-- Session: 2026-03-04 -->
- [Approval Style] Human used shorthand approval ("A", "continue with implementation") rather than detailed feedback -> For low-risk, well-explained changes, concise gate presentations are preferred over exhaustive detail -> Keep gate presentations scannable and front-load the verdict

## Artifact Structure

<!-- Session: 2026-03-04 -->
- [Revision Handling] Human provided three pieces of revision feedback at once (combine options, increase limit, change display location) -> Present artifacts in a way that makes each decision point independently revisable -> Reduces friction when multiple aspects need adjustment simultaneously

<!-- Session: 2026-03-09 -->
- [Open Questions] Human provided direct answers to all open questions in a single message, then requested removing the Open Questions section entirely -> When presenting an artifact with open questions, make them answerable inline (yes/no, pick a value) so the human can resolve them all at once -> Reduces revision rounds; do not re-present resolved questions as "open"

## Finding Presentation

<!-- Session: 2026-03-05 -->
- [Severity Handling] Human requested many LOW and INFO findings be escalated to required mitigations -> When presenting findings by severity, do not assume human will accept lower-severity items; present all findings with clear mitigation paths so the human can escalate freely -> Avoids a revision round where the human must explicitly request what should have been offered
