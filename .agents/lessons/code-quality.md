# Lessons: Code Quality and Standards

Patterns for code style, refactoring, naming, and quality expectations.

**Relevant to:** Any agent writing, reviewing, or evaluating code quality and style.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Constants and Defaults

<!-- Session: 2026-03-09 -->
- [Magic Numbers] Human rejected literal integer defaults in test code ("please move these values to some form of constant") -> When adding configurable values with defaults, define them as named constants and use those constants in both production code and tests -> Prevents maintenance burden of updating magic numbers across multiple test sites

## Refactoring

<!-- Session: 2026-03-09 -->
- [Behavioral Preservation] Human directed "retain the current method to preserve the desired behavior" when condensed code changed the behavior -> When refactoring for line count reduction, preserve user-facing behavior exactly; do not change semantics as a side effect of code condensation -> Behavioral changes disguised as refactors will be caught and rejected

## Readability

<!-- Session: 2026-03-09 -->
- [Variable Declarations] Human rejected combining unrelated variable initializations onto single lines ("each variable should be defined on its own line, unless returned by a function as a tuple") -> Do not combine disparate variable declarations for line savings; only use tuple destructuring for values returned together from a function -> Readability trumps line count reduction
