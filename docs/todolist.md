# Skill Ideas Todolist

> Research date: 2026-03-16

---

## Market Research

### What the Skill Ecosystem Looks Like Today

The agent skills market is exploding. As of March 2026:

- **349+ Claude Code skills** catalogued across 12 categories ([OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/best-claude-code-skills-2026))
- **117K weekly installs** for the top official skill (Remotion)
- **89K installs** for `/feature-dev`, the most popular community skill
- **40.9K GitHub stars** for `Superpowers`, the leading multi-agent workflow framework
- **20K stars in a single week** for `agency-agents` after one viral tweet

The market is **dominated by developer workflow tools** (code review, TDD, batch PR automation). The whitespace is in:

1. **Fun / personality** — nothing with charm, humor, or social proof yet
2. **Shareable artifacts** — outputs people *want* to post publicly
3. **Cross-domain** — beyond just writing code
4. **Personalized intelligence** — not generic tools, but tuned to *your* context

### The Viral Formula

| Factor | Example |
|---|---|
| Shareable output | `agency-agents` — one tweet → 20K stars in a week |
| Surprise/delight | `airi` VTuber — 10K stars/week, two weeks running |
| Solves deep friction | `Superpowers` — 40.9K stars enforcing dev discipline |
| Competitive element | GitHub Wrapped, devcard.dev — people compare and share |
| Meta / ecosystem builder | `Remotion Skill` — 117K weekly installs via official partnership |

---

## Skill Ideas (Ranked by Viral Potential)

---

### 1. `code-roast` ⭐ Highest Viral Potential

**Concept:** Brutally (and funnily) roasts your codebase. Generates a shareable "report card" — a letter grade, a list of comedic offenses (e.g., *"your `utils.js` is a graveyard of abandoned dreams"*), and actionable shame.

**Why it goes viral:**
- The output *is* the shareable artifact: screenshot → tweet → retweet loop
- Everyone has embarrassing code they secretly want validated
- Creates team competition: *"My repo got a C+, what did yours get?"*
- The tweet writes itself

**What to build:** Analyzes git history for anti-patterns, scans for code smells (duplicates, magic numbers, long functions, TODO graveyards), generates a witty roast + letter grade. Zero setup — just run it in any repo.

**Virality ceiling:** Very high. Think "RoastMe but for codebases." HN front page material.

---

### 2. `dev-card` — GitHub Wrapped Energy

**Concept:** Analyzes your repos and commits to generate a shareable "Developer Identity Card" — your archetype, top languages, coding patterns, peak hours, and a 1-line personality summary.

**Why it goes viral:**
- Spotify Wrapped / GitHub Wrapped mechanics are proven viral formats
- People love sharing personality archetypes
- Zero-stakes, high-delight
- Works for any developer — massive TAM

**What to build:** Parses `git log`, `git shortstat`, file types, commit message sentiment, and generates a styled markdown or HTML card. Example output: *"Midnight Refactorer. Speaks TypeScript, dreams in shell scripts. 73% of commits happen after 11pm."*

**Virality ceiling:** Extremely high on social. Could become a "post your dev card" meme.

---

### 3. `git-story` — Long-Tail Viral

**Concept:** Turns a repo's git history into a narrative "making of" blog post — the story of how the project was built, with arc, struggles, and insights.

**Why it goes viral:**
- Shareable on dev blogs, LinkedIn, HN, and portfolio sites
- Bridges the gap between building and storytelling (which most devs struggle with)
- The output has standalone value — it's a real, publishable blog post
- Unique: nothing like this exists in the ecosystem yet

**What to build:** Parses `git log --stat`, extracts commit clusters, identifies major phases (prototyping → refactor → scale), synthesizes into a narrative. Outputs a `.md` post ready to publish.

**Virality ceiling:** Strong long-tail. Less explosive but more durable — every new project becomes shareable content.

---

### 4. `one-person-unicorn` — Rides the Dominant 2026 Narrative

**Concept:** Given a product idea, generate a full agentic execution blueprint: which skills to use, which APIs to connect, what Claude can automate vs. what needs a human, and a time estimate (with AI vs. without).

**Why it goes viral:**
- "One-person unicorn" is *the* dominant builder narrative right now
- Feeds the solopreneur/indie hacker community (huge and growing)
- Output is a strategic artifact that people share as proof they're serious
- Could become the canonical "how to build a startup with AI agents" skill

**What to build:** Takes a product description, researches available skills/MCPs, generates a phased plan with specific tool recommendations. Output: a `blueprint.md` people can execute or share.

**Virality ceiling:** Very high with the builder/solopreneur crowd. Could trend beyond the dev community.

---

### 5. `dep-brief` — Personalized Utility with Shareability

**Concept:** `llm-daily` but for *your specific dependencies* — a weekly briefing on CVE exposure, upcoming breaking changes, sunset risk, and upgrade priorities for your exact `package.json` / `requirements.txt`.

**Why it goes viral:**
- Hyper-personalized version of a proven format (daily briefing)
- Solves real anxiety: *"What's about to break in my project?"*
- Shareable output: *"My project has 3 active CVEs and 2 dependencies hitting EOL next month 😬"*
- Natural extension of the `llm-daily` infrastructure already in this repo

**What to build:** Parses dependency files, queries CVE databases and changelogs, synthesizes a weekly `dep_brief_YYYY-MM-DD.md`.

**Virality ceiling:** High in the pragmatic dev community. Strong word-of-mouth.

---

### Dark Horse: `aura`

**Concept:** AI personality profiler for developers. Analyzes your code style, commit messages, PR comments, and README writing to generate your "developer aura" — a personality archetype with a title, a vibe, a strength, and a blind spot.

Example outputs: *"The Quiet Architect"*, *"The Chaos Wizard"*, *"The Premature Optimizer"*

**Why it could explode:** Pure social proof + personality = the most-shared format on the internet. Zero utility friction — just run it and share.

---

## Summary Table

| Skill | Viral Potential | Build Complexity | Whitespace |
|---|---|---|---|
| `code-roast` | ⭐⭐⭐⭐⭐ | Low | High |
| `dev-card` | ⭐⭐⭐⭐⭐ | Low-Medium | High |
| `git-story` | ⭐⭐⭐⭐ | Low | Very High |
| `one-person-unicorn` | ⭐⭐⭐⭐ | Medium | High |
| `dep-brief` | ⭐⭐⭐⭐ | Medium | Medium |
| `aura` | ⭐⭐⭐⭐⭐ | Low | Very High |

**Top pick for max viral speed:** `code-roast`
**Top pick for durable growth:** `dep-brief`

---

## Sources

- [10 Must-Have Skills for Claude in 2026 — Medium](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)
- [awesome-agent-skills — VoltAgent/GitHub](https://github.com/VoltAgent/awesome-agent-skills)
- [Best Claude Code Skills 2026 — TurboDocx](https://www.turbodocx.com/blog/best-claude-code-skills-plugins-mcp-servers)
- [Top 10 Claude Code Skills — Composio](https://composio.dev/content/top-claude-skills)
- [awesome-claude-skills — ComposioHQ/GitHub](https://github.com/ComposioHQ/awesome-claude-skills)
- [Top 8 Claude Skills for Developers — Snyk](https://snyk.io/articles/top-claude-skills-developers/)
- [Best Claude Code Skills 2026: 349 Skills Ranked — OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/best-claude-code-skills-2026)
- [awesome-claude-code — hesreallyhim/GitHub](https://github.com/hesreallyhim/awesome-claude-code)
- [50+ Best MCP Servers for Claude Code 2026 — ClaudeFast](https://claudefa.st/blog/tools/mcp-extensions/best-addons)
- [awesome-claude-code-subagents — VoltAgent/GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Top AI GitHub Repositories in 2026 — ByteByteGo](https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026)
- [GitHub Trending Weekly 2026-03-11: Skills Ecosystem Blooms](https://www.shareuhack.com/en/posts/github-trending-weekly-2026-03-11)
- [Superpowers: Agent Skill Framework — AIToolly](https://aitoolly.com/ai-news/article/2026-03-15-superpowers-a-new-agent-skill-framework-and-software-development-workflow-for-coding-agents)
- [The AI Agent Skills Boom 2026 — SoloBusinessHub](https://www.solobusinesshub.com/trend-watch/ai-agent-skills-boom-2026/)
