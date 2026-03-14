# agent-tasks-template

A template repository that provides a structured set of tasks, skills, and commands for AI/LLM agents to process. Use this repo as a starting point for new projects that leverage AI-assisted software development workflows.

## Repository Structure

```
.agents/                          Shared agent configuration
  CYNEFIN.md                      Cynefin framework for problem classification
  PERSONALITY.md                  Shared values and behavioral commitments
  LESSONS.md                      Accumulated lessons from past sessions
  REQUIREMENTS.md                 Non-negotiable project requirements (index)
  SECURITY_REVIEW_CHECKLIST.md    Security review process for external context files
  pipelines/                      Pipeline process definitions
    SDLC.md                       7-gate software development lifecycle pipeline
    JIRA.md                       3-gate Jira ticket creation pipeline
  requirements/                   Individual requirement definitions
    REQ-001.md – REQ-NNN.md       Full requirement statements, rationale, and enforcement
  roles/                          Role-specific instructions
    ARCHITECT.md                  Architecture review
    SECURITY_ARCHITECT.md         Security architecture review
    TEAM_LEAD.md                  Team lead approval
    ENGINEER.md                   Engineering implementation
    CODE_REVIEWER.md              Code review
    QUALITY_ENGINEER.md           Quality review
    SECURITY_AUDITOR.md           Security audit

.claude/                          Claude Code platform support
  skills/                         Skill definitions
    sdlc/SKILL.md                 Full SDLC pipeline skill
    jira/SKILL.md                 Jira ticket creation skill
    security-review-file/SKILL.md Security review for external context files
  settings.json                   Claude Code settings
```

## Goals

This template provides a framework for AI/LLM agents to follow structured workflows when performing software engineering tasks. The included configuration defines:

- **Agent roles** with specialized responsibilities (architect, engineer, reviewer, etc.)
- **Pipelines** that define multi-gate processes (SDLC, Jira) with human approval gates
- **Skills** that invoke pipelines from platform-specific entry points
- **Shared context** (personality, lessons learned, requirements) that agents load before each task
- **A Cynefin-based classification system** to match response strategy to problem complexity

## Platform Support

- **Claude Code** — fully supported via `.claude/` configuration
- **Other platforms** — under consideration

## License

This project is released under the [Unlicense](LICENSE).
