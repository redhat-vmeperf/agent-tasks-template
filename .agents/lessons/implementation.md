# Lessons: Implementation and Engineering Practices

Patterns for implementation ordering, dependency management, and engineering workflow.

**Relevant to:** Any agent producing implementation artifacts, creating files, or managing build order.

---

## Lesson Format

```
- [Theme] Pattern observed -> What to do differently -> Why it matters
```

---

## Build Order

<!-- Session: 2026-03-11 -->
- [Dependency Ordering] Human redirected implementation order: "create the shared file first, then present the changes to the consumers" -> When extracting shared logic from multiple files into a new shared artifact, create the shared artifact first before modifying any consumer -> Establishes the dependency before the references; prevents presenting incomplete work where consumers reference a file that does not yet exist
