# agent-tasks-template

A template repository that provides a structured set of tasks, skills, and commands for AI/LLM agents to process. Use this repo as a starting point for new projects that leverage AI-assisted software development workflows.

## Goals

This template provides a framework for AI/LLM agents to follow structured workflows when performing software engineering tasks. The included configuration defines:

- **Agent roles** with specialized responsibilities (architect, engineer, reviewer, etc.)
- **Pipelines** that define multi-gate processes (SDLC, Jira, Diagram Alignment) with human approval gates
- **Skills** that invoke pipelines from platform-specific entry points
- **Pre-commit hooks** with deterministic linting and AI-powered review (persona, diagram, SDLC)
- **Shared context** (personality, lessons learned, requirements) that agents load before each task
- **A Cynefin-based classification system** to match response strategy to problem complexity

## Platform Support

- **Claude Code** — fully supported via `.claude/` configuration
- **Cursor IDE** — fully supported via `.cursor/rules/` configuration
- **OpenCode** — fully supported via `.opencode/` configuration and `opencode.json`

## Quickstart

```bash
mkdir new_project
cd new_project

cat <<EOF | bash
set -ex
REMOTE_NAME=redhat-vmeperf-agent-tasks-template
REMOTE_URL=https://github.com/redhat-vmeperf/agent-tasks-template
REMOTE_FILES=(.agents .claude .cursor .opencode opencode.json AGENTS.md)


git init
cat <<EOI >> .gitignore
.agents
.claude
.cursor
.opencode
opencode.json
EOI

git remote add "\${REMOTE_NAME}" "\${REMOTE_URL}"
git fetch --no-tags "\${REMOTE_NAME}"
git restore --source="\${REMOTE_NAME}/main" -- \${REMOTE_FILES[@]}

claude /sdlc
EOF
```

## Repository Structure

```
.agents/                          Shared agent configuration
  CYNEFIN.md                      Cynefin framework for problem classification
  PERSONALITY.md                  Shared values and behavioral commitments
  LESSONS.md                      Accumulated lessons from past sessions (index)
  REQUIREMENTS.md                 Non-negotiable project requirements (index)
  SECURITY_REVIEW_CHECKLIST.md    Security review process for external context files
  lessons/                        Themed lesson files
    architecture.md               Design decisions and trade-offs
    code-quality.md               Code standards and style
    communication.md              Human interaction and feedback
    implementation.md             Engineering practices
    process.md                    Pipeline efficiency
    security.md                   Security practices (read by all agents)
  pipelines/                      Pipeline process definitions
    SDLC.md                       7-gate software development lifecycle pipeline
    JIRA.md                       3-gate Jira ticket creation pipeline
    SKILLGEN.md                   4-gate skill generation pipeline
    DIAGRAM_ALIGNMENT.md          Diagram alignment verification rules and examples
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
    sdlc-task/SKILL.md            Autonomous SDLC pipeline skill
    jira/SKILL.md                 Jira ticket creation skill
    skillgen/SKILL.md             Automatic skill generation
    security-review-file/SKILL.md Security review for external context files
    diagram-alignment/SKILL.md    Diagram alignment verification skill
  settings.json                   Claude Code settings

.cursor/                          Cursor IDE platform support
  rules/                          Rule definitions
    project.mdc                   Project context (always applied)
    security-guidelines.mdc       Security restrictions (always applied)
    sdlc.mdc                      Full SDLC pipeline rule
    sdlc-task.mdc                 Autonomous SDLC pipeline rule
    jira.mdc                      Jira ticket creation rule
    skillgen.mdc                  Automatic skill generation rule
    security-review-file.mdc      Security review for external context files

.opencode/                        OpenCode platform support
  commands/                       Command definitions
    sdlc.md                       Full SDLC pipeline command
    sdlc-task.md                  Autonomous SDLC pipeline command
    jira.md                       Jira ticket creation command
    skillgen.md                   Automatic skill generation
    security-review-file.md       Security review for external context files
    diagram-alignment.md          Diagram alignment verification command

opencode.json                     OpenCode configuration

scripts/                          CI and pre-commit tooling
  verify-diagram-alignment.py     Deterministic diagram alignment linter
  ai-review.py                    AI-powered pre-commit review hook
  prompts/                        Prompt templates for AI review phases
    persona-review.md             7-persona condensed review prompt
    sdlc-review.md                Full SDLC pipeline review prompt
    diagram-review.md             Diagram alignment review prompt
  update-pinned-shas.py           Updates pinned SHAs in CI and pre-commit configs

.pre-commit-config.yaml           Pre-commit hook configuration
.github/workflows/ci.yml          GitHub Actions CI workflow
```

## License

This project is released under the [Unlicense](LICENSE).
