# Agent Skills

This repository contains skills for Agents.

## Available Skills

### [llm-daily](skills/llm-daily/SKILL.md)
**Description:** Generates and publishes a daily AI/LLM newsletter by curating research, open-source trends, product launches, and industry news from multiple sources.

**Usage:**
- "Give me today's LLM briefing."
- "Publish today's LLM Daily newsletter."

### [sync-trending](skills/sync-trending/SKILL.md)
**Description:** Monitors technology trends (GitHub, etc.), contextualizes them against the user's project, and autonomously verifies them through installation and testing.

**Usage:**
- "What are trending repos this week?"
- "Sync me on trending tech."

### [code-roast](skills/code-roast/SKILL.md)
**Description:** Roasts a codebase with a brutally honest, funny audit and shareable report card. Grades it A+ to F across 9 shame categories with wit, specific file callouts, and actionable fixes.

**Usage:**
- "Roast my code."
- "How bad is my codebase?"

### [dev-card](skills/dev-card/SKILL.md)
**Description:** Generates a shareable Developer Identity Card from any git repo. Analyzes commit history, language breakdown, and coding patterns to assign a developer archetype (e.g. "The Midnight Architect", "The Dawn Deployer") with a personality tagline and stats.

**Usage:**
- "Make my dev card."
- "What's my developer archetype?"

## Structure
- `skills/`: Source code for skills.
- `specs/`: Design specifications for skills.
