# Lessons: Process and Pipeline Efficiency

Patterns for gate flow, finding resolution, proportionality, and reducing revision rounds.

**Relevant to:** Any agent operating within a gated pipeline, handling findings, or managing approval flow.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Proportionality

<!-- Session: 2026-03-04 -->
- [Artifact Depth] Human approved all gates without revision on first pass -> When the change is small, well-scoped, and follows existing patterns, the pipeline flows efficiently without rework -> Proportionality in artifact depth pays off; match analysis depth to change complexity

## Finding Resolution

<!-- Session: 2026-03-05 -->
- [Resolution Preference] Human consistently chose "resolve" over "accept/defer" for all findings at every review stage -> This human values comprehensive resolution over shipping velocity; all findings should be fixed, not tracked -> In future sessions, consider proactively resolving LOW/INFO findings before presenting them, offering the resolved state for approval rather than asking the human to decide disposition

<!-- Session: 2026-03-05 -->
- [Batch Resolution] When human requested mitigating one finding, proactively resolving all remaining findings in the same revision pass resulted in immediate approval -> When the human escalates any finding, resolve all findings at that severity and below in a single pass rather than waiting for individual decisions -> Eliminates multiple revision rounds and aligns with established preference for comprehensive resolution

<!-- Session: 2026-03-05 -->
- [Suggested Findings] Human requested suggested findings be implemented rather than deferred -> When presenting SUGGESTED findings alongside REQUIRED ones, make suggested fixes implementable in the same round; human often prefers "fix it now" over "track for later" -> Present suggested findings with ready-to-apply fixes, not just descriptions

<!-- Session: 2026-03-05 -->
- [Pre-Resolution] Pre-resolving SUGGESTED findings before presenting the review resulted in clean first-pass approval -> The pattern of fixing suggestions before presenting (rather than asking the human to decide) reduces friction and matches this human's preference for immediate resolution -> Continue pre-resolving all non-controversial findings

<!-- Session: 2026-03-05 -->
- [DRY Extraction] Human requested implementing a DRY extraction rather than deferring -> Same pattern as suggested findings: human prefers resolving findings immediately -> When findings have clear, low-risk fixes, implement them before presenting the review rather than offering defer/decline options

<!-- Session: 2026-03-05 -->
- [Audit Findings] Human requested resolving all LOW and INFO audit findings rather than accepting/tracking -> Consistent pattern across all reviews: this human prefers resolving all findings at every severity level -> For future sessions, strongly consider pre-resolving all findings (including LOW/INFO) before presenting a review, or at minimum present them with implemented fixes ready for approval

<!-- Session: 2026-03-11 -->
- [Audit Findings] Human required mitigating all LOW and INFO findings at final audit rather than accepting them -> Reinforces existing pattern: this human expects all findings resolved regardless of severity -> Pre-resolve all findings before presenting the final audit, or present with implemented fixes ready for approval

## Enforcement Scope

<!-- Session: 2026-03-09 -->
- [Cross-Cutting Requirements] Human corrected enforcement scope from a subset of stages to "all stages" for a cross-cutting requirement -> When a requirement governs language, style, or conventions (not just code), it applies at every stage — architecture text, security reviews, and briefs must also comply -> Cross-cutting requirements default to all-stage enforcement unless there is a specific reason to restrict scope

<!-- Session: 2026-03-13 -->
- [Pipeline Independence] Lesson files, shared context, and reusable artifacts must not reference pipeline-specific concepts (gate numbers, pipeline-specific role names) -> Use activity-based or role-based descriptions that apply across any pipeline or command -> Ensures shared artifacts remain usable as new pipelines and skills are added without requiring updates to shared files
