# Lessons: Architecture and Design Decisions

Patterns for presenting options, structuring ADRs, and making design recommendations.

**Relevant to:** Any agent presenting design options, making architectural recommendations, or structuring trade-off analysis.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Option Presentation

<!-- Session: 2026-03-04 -->
- [Complementary Options] Human requested combining two presented options rather than choosing one -> When options are complementary rather than mutually exclusive, present the combined approach as a viable option or note combinability explicitly -> Saves a revision round when the human sees value in both approaches

## Recommendation Strategy

<!-- Session: 2026-03-06 -->
- [Comprehensive vs. Minimal] Human rejected the recommended "minimal" dependency update option and directed using the "full update" option instead -> When presenting dependency update options, prefer recommending the comprehensive approach (full version alignment) over the minimal approach (compatibility shims/feature flags), especially when the full approach is cleaner long-term -> This human values clean dependency alignment over minimal blast radius; prevents a revision round
