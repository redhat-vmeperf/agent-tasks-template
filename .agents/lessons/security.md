# Lessons: Security Practices

Security-specific patterns for threat modeling, finding severity, boundary design, and audit behavior.

**Relevant to:** Any agent performing threat modeling, security review, audit, or designing trust boundaries and data framing.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Boundary Design

<!-- Session: 2026-03-11 -->
- [Data Framing] Human rejected a content framing delimiter design because the delimiter could be injected into the file itself to break out of the data frame -> When designing data/instruction boundaries, the boundary markers must be verified absent from the data before use; presence of boundary markers in the data is an immediate security failure -> Always verify delimiter uniqueness against content; treat delimiter presence in data as a framing attack

## Attack Surface

<!-- Session: 2026-03-11 -->
- [Hardcoded References] When a skill argument provides an example referencing a specific file path that could itself be a scan or injection target, the example creates a hardcoded assumption -> Skill arguments should only reference files known at runtime, not embed specific paths as examples -> Prevents assumption leakage and reduces attack surface of the skill definition

## Audit Scope

<!-- Session: 2026-03-09 -->
- [Release Validation] Human rejected the final security audit twice to request infrastructure improvements (cargo audit in CI, version bump, edition bump) -> The final security audit is where the human validates the entire release, not just the code diff; be prepared for scope additions that improve the project's security posture or release hygiene -> Final audit rejections are not always about code findings; they can be about build/release process gaps

## Mandatory Coverage

<!-- Session: 2026-03-13 -->
- [Universal Security] Security lessons were marked as optional "read if relevant to your role" alongside other themes -> Security lessons must be mandatory reading for all agents regardless of role, not optional based on perceived relevance -> Security applies to every role and task; no agent should self-select out of security awareness
