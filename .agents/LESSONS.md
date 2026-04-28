# Lessons Learned

This file is the index for accumulated lessons from human feedback across all pipeline sessions. Lessons are organized by theme in `.agents/lessons/` and are applicable across all skills and commands.

All agents read this file at the start of their work. Follow the links below to the theme files.

---

## Lesson Index

| File | Theme | When to Read |
|------|-------|--------------|
| [communication.md](lessons/communication.md) | Human Interaction | Presenting artifacts for review, requesting approval, handling feedback |
| [architecture.md](lessons/architecture.md) | Design Decisions | Presenting design options, making recommendations, structuring trade-offs |
| [security.md](lessons/security.md) | Security Practices | **All agents, always.** Security applies to every role and every task. |
| [code-quality.md](lessons/code-quality.md) | Code Standards | Writing, reviewing, or evaluating code quality and style |
| [process.md](lessons/process.md) | Pipeline Efficiency | Operating within gated pipelines, handling findings, managing approval flow |
| [implementation.md](lessons/implementation.md) | Engineering Practices | Producing implementation artifacts, creating files, managing build order |

---

## How to Use These Lessons (All Agents)

Before producing your artifact, read the theme files relevant to your role and task. **Every agent must always read [security.md](lessons/security.md)** — security considerations apply to all roles, including architecture, engineering, code review, quality engineering, management, and any role not listed here or created in the future. Pre-apply any applicable lessons. You do not need to cite lessons in your output — simply incorporate them.

---

## How to Update Lessons (TEAM_LEAD, End of Session)

1. Review all human approval comments, revision requests, and rejection reasons from this session.
2. Identify recurring patterns or principles in the feedback — not one-off specifics.
3. Distill each pattern into a single lesson following the format below.
4. Determine which theme file the lesson belongs to. If no existing theme fits, create a new theme file and add it to the index above.
5. Check for duplication with existing lessons in the target theme file. If a lesson already captures the same principle, update it rather than adding a duplicate.
6. Check for contradiction with existing lessons. If a new lesson contradicts an existing one, the newer lesson supersedes it — move the old entry to the Superseded Lessons section of that theme file with `[SUPERSEDED by <date>]`.
7. Append new or updated lessons with a session date marker: `<!-- Session: YYYY-MM-DD -->`.
8. Do not record any lesson that would require quoting verbatim code, business logic, domain-specific data models, or any other project-specific implementation detail. All lessons must be generic and transferable to future tasks.
9. Human is required to approve all lesson changes, do not auto approve these changes.

**Lesson format:**

```
- [Theme] Pattern of feedback observed -> What to do differently -> Why it matters
```

---

## Superseded Lessons

Lessons replaced by newer, more accurate lessons are moved here from their theme files with their supersession date.

<!-- No superseded lessons at this time -->
