# Project Instructions

This file provides project-specific instructions for AI/LLM agents working in this repository. Update this file to reflect your project's context, conventions, and requirements.

## Project Overview

[Describe your project here. What does it do? Who is it for?]

## Tech Stack

[List your languages, frameworks, and key dependencies.]

## Development Conventions

[Document your project's coding standards, naming conventions, branching strategy, and any other patterns agents should follow.]

## Agent Configuration

Shared agent configuration is located in `.agents/`:

- `.agents/CYNEFIN.md` — Problem classification framework
- `.agents/PERSONALITY.md` — Shared agent values and behavioral commitments
- `.agents/LESSONS.md` — Lessons learned from past sessions (index)
- `.agents/lessons/` — Themed lesson files (architecture, code-quality, communication, implementation, process, security)
- `.agents/REQUIREMENTS.md` — Non-negotiable project requirements (index)
- `.agents/SECURITY_REVIEW_CHECKLIST.md` — Security review process for external context files
- `.agents/pipelines/` — Pipeline process definitions (SDLC, Jira, Skill Generation)
- `.agents/requirements/` — Individual requirement definitions (REQ-001 through REQ-NNN)
- `.agents/roles/` — Role-specific instructions for each SDLC gate

Platform-specific configuration:

- `.claude/` — Claude Code skills and settings
- `.cursor/` — Cursor IDE rules
- `.opencode/` — OpenCode commands
- `opencode.json` — OpenCode configuration
