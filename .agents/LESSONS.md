# Lessons Learned

This file is maintained by the TEAM_LEAD agent at the end of every SDLC session. It captures distilled, principle-level lessons from human feedback during gate interactions. All agents read this file at the start of their gate before producing any artifact.

---

## How to Use This File (All Agents)

Before producing your gate artifact, read the sections relevant to your role. Pre-apply any applicable lessons. You do not need to cite lessons in your output — simply incorporate them.

---

## How to Update This File (TEAM_LEAD, End of Session)

1. Review all human approval comments, revision requests, and rejection reasons from this session's gates.
2. Identify recurring patterns or principles in the feedback — not one-off specifics.
3. Distill each pattern into a single lesson following the format below.
4. Check for duplication with existing lessons. If a lesson already captures the same principle, update it rather than adding a duplicate.
5. Check for contradiction with existing lessons. If a new lesson contradicts an existing one, the newer lesson supersedes it — mark the old entry with `[SUPERSEDED by <date>]` and add the new one.
6. Append new or updated lessons with a session date marker: `<!-- Session: YYYY-MM-DD -->`.
7. Do not record any lesson that would require quoting verbatim code, business logic, domain-specific data models, or any other project-specific implementation detail. All lessons must be generic and transferable to future tasks.

**Lesson format:**
```
- [Gate/Category] Pattern of feedback observed → What to do differently → Why it matters
```

---

## Cross-Cutting Lessons

<!-- Session: 2026-03-04 -->
- [Cross-Cutting] Human approved all gates without revision on first pass → When the change is small, well-scoped, and follows existing patterns, the SDLC pipeline flows efficiently without rework → Proportionality in artifact depth pays off; match analysis depth to change complexity
- [Cross-Cutting] Human used shorthand approval ("A", "continue with implementation") rather than detailed feedback → For low-risk, well-explained changes, concise gate presentations are preferred over exhaustive detail → Keep gate presentations scannable and front-load the verdict

<!-- Session: 2026-03-05 -->
- [Cross-Cutting] Human consistently chose "resolve" over "accept/defer" for all findings at every gate (Gates 2, 5, 6, 7) → This human values comprehensive resolution over shipping velocity; all findings should be fixed, not tracked → In future sessions, consider proactively resolving LOW/INFO findings before presenting them, offering the resolved state for approval rather than asking the human to decide disposition

<!-- Session: 2026-03-05 -->
- [Cross-Cutting] When human requested mitigating one finding at Gate 2, proactively resolving all remaining findings in the same revision pass resulted in immediate approval → When the human escalates any finding, resolve all findings at that severity and below in a single pass rather than waiting for individual decisions → Eliminates multiple revision rounds and aligns with established preference for comprehensive resolution

---

## Gate 1: Architecture

<!-- Session: 2026-03-04 -->
- [Gate 1] Human requested combining two presented options rather than choosing one → When options are complementary rather than mutually exclusive, present the combined approach as a viable option or note combinability explicitly → Saves a revision round when the human sees value in both approaches
- [Gate 1] Human provided three pieces of revision feedback at once (combine options, increase limit, change display location) → Present the ADR in a way that makes each decision point independently revisable → Reduces friction when multiple aspects need adjustment simultaneously

<!-- Session: 2026-03-06 -->
- [Gate 1] Human rejected the recommended "minimal" dependency update option and directed using the "full update" option instead → When presenting dependency update options, prefer recommending the comprehensive approach (full version alignment) over the minimal approach (compatibility shims/feature flags), especially when the full approach is cleaner long-term → This human values clean dependency alignment over minimal blast radius; prevents a revision round at Gate 1

<!-- Session: 2026-03-09 -->
- [Gate 1] Human provided direct answers to all open questions in a single message, then requested removing the Open Questions section entirely → When presenting an ADR with open questions, make them answerable inline (yes/no, pick a value) so the human can resolve them all at once → Reduces revision rounds; do not re-present resolved questions as "open"

---

## Gate 2: Security Architecture

<!-- Session: 2026-03-05 -->
- [Gate 2] Human requested many LOW and INFO findings be escalated to required mitigations → When presenting findings by severity, do not assume human will accept lower-severity items; present all findings with clear mitigation paths so the human can escalate freely → Avoids a revision round where the human must explicitly request what should have been offered

---

## Gate 3: Team Lead / Approval

<!-- Add Gate 3 lessons here -->

---

## Gate 4: Engineering

<!-- Session: 2026-03-09 -->
- [Gate 4] Human rejected literal integer defaults in test code ("please move these values to some form of constant") → When adding configurable values with defaults, define them as named constants and use those constants in both production code and tests → Prevents maintenance burden of updating magic numbers across multiple test sites

<!-- Session: 2026-03-09 (inclusive-language) -->
- [Gate 4] Human corrected enforcement scope from "4, 5, 6, 7" to "all gates" for a cross-cutting requirement → When a requirement governs language, style, or conventions (not just code), it applies at every gate — architecture text, security reviews, and sprint briefs must also comply → Cross-cutting requirements default to all-gate enforcement unless there is a specific reason to restrict scope

<!-- Session: 2026-03-11 -->
- [Gate 4] Human redirected implementation order: "create the shared file first, then present the changes to the consumers" → When extracting shared logic from multiple files into a new shared artifact, create the shared artifact first before modifying any consumer → Establishes the dependency before the references; prevents presenting incomplete work where consumers reference a file that does not yet exist

---

## Gate 5: Code Review

<!-- Session: 2026-03-05 -->
- [Gate 5] Human requested suggested findings be implemented rather than deferred → When presenting SUGGESTED findings alongside REQUIRED ones, make suggested fixes implementable in the same round; human often prefers "fix it now" over "track for later" → Present suggested findings with ready-to-apply fixes, not just descriptions

<!-- Session: 2026-03-05 -->
- [Gate 5] Pre-resolving SUGGESTED findings before presenting the gate resulted in clean first-pass approval → The pattern of fixing suggestions before presenting (rather than asking the human to decide) reduces gate friction and matches this human's preference for immediate resolution → Continue pre-resolving all non-controversial findings

<!-- Session: 2026-03-09 -->
- [Gate 5] Human directed "retain the current method to preserve the desired behavior" when condensed code changed the behavior → When refactoring for line count reduction, preserve user-facing behavior exactly; do not change semantics as a side effect of code condensation → Behavioral changes disguised as refactors will be caught and rejected
- [Gate 5] Human rejected combining unrelated variable initializations onto single lines ("each variable should be defined on its own line, unless returned by a function as a tuple") → Do not combine disparate variable declarations for line savings; only use tuple destructuring for values returned together from a function → Readability trumps line count reduction

---

## Gate 6: Quality

<!-- Session: 2026-03-05 -->
- [Gate 6] Human requested implementing the DRY extraction (QA-001) rather than deferring → Same pattern as Gate 5: human prefers resolving findings immediately → When findings have clear, low-risk fixes, implement them before presenting the gate rather than offering defer/decline options

---

## Gate 7: Security Audit

<!-- Session: 2026-03-05 -->
- [Gate 7] Human requested resolving all LOW and INFO audit findings rather than accepting/tracking → Consistent pattern across all gates: this human prefers resolving all findings at every severity level → For future sessions, strongly consider pre-resolving all findings (including LOW/INFO) before presenting the gate, or at minimum present them with implemented fixes ready for approval

<!-- Session: 2026-03-09 -->
- [Gate 7] Human rejected Gate 7 twice to request infrastructure improvements (cargo audit in CI, version bump, edition bump) → The final security gate is where the human validates the entire release, not just the code diff; be prepared for scope additions that improve the project's security posture or release hygiene → Gate 7 rejections are not always about code findings; they can be about build/release process gaps

<!-- Session: 2026-03-11 -->
- [Gate 7] Human required mitigating all LOW and INFO findings at Gate 7 rather than accepting them → Reinforces existing pattern: this human expects all findings resolved regardless of severity → Pre-resolve all findings before presenting Gate 7, or present with implemented fixes ready for approval

---

## Cross-Cutting Lessons (continued)

<!-- Session: 2026-03-11 -->
- [Cross-Cutting] When a skill argument provides an example referencing a specific file path that could itself be a scan or injection target, the example creates a hardcoded assumption → Skill arguments should only reference files known at runtime, not embed specific paths as examples → Prevents assumption leakage and reduces attack surface of the skill definition
- [Gate 1] Human rejected a content framing delimiter design because the delimiter could be injected into the file itself to break out of the data frame → When designing data/instruction boundaries, the boundary markers must be verified absent from the data before use; presence of boundary markers in the data is an immediate security failure → Always verify delimiter uniqueness against content; treat delimiter presence in data as a framing attack

---

## Superseded Lessons

<!-- Lessons replaced by newer, more accurate lessons are moved here with their supersession date -->
