# Skill Specification: sync-trending

## Overview
The `sync-trending` skill is designed to keep the user up-to-date with the latest technology trends by monitoring platforms like GitHub Trending. It streamlines the discovery-to-action pipeline into three distinct phases: actively monitoring trends and immediately brainstorming their value against the user's context, autonomously verifying selected technologies through deep-dive testing, and finally generating actionable artifacts to facilitate adoption or reporting.

## Triggers
- "What are trending repos this week?"
- "Check github trending"
- "Any new cool tools for my project?"
- "Sync me on trending tech."

## Capabilities & Workflow

### 1. Monitor, Brainstorm & Summarize
- **Context Awareness:** deeply understand the user's current project (read `README.md`, `package.json` etc.) or general working context (via memory or prompt) *before* fetching trends.
- **Source:** GitHub Trending (https://github.com/trending). Future support for Hugging Face, etc.
- **Action:**
  1. Fetch the trending repositories.
  2. For high-signal repos, immediately brainstorming: "How does this specific tool help [User's Project]?" or "What value does this bring to [User's Role]?"
- **Output:** A consolidated "Contextualized Trend Report". For each top repo, include:
  - **Facts:** Name, URL, Primary Language, Star Velocity.
  - **Contextual Value:** A one-sentence insight on *why* this matters to the user (e.g., "Could replace the legacy logging in ProjectX," "Perfect for that project idea we discussed," "Competitor analysis for the CEO").

### 2. Permission & Deep Dive (Autonomous Verification)
- **Trigger:** User selects a repo from the report.
- **Constraint:** **Strictly** ask for permission before cloning code or executing scripts.
- **Action:**
  - `git clone <repo_url>` into a temporary directory.
  - Analyze `README.md` / `CONTRIBUTING.md` for build instructions.
  - Detect project type (Node, Python, Rust, etc.).
  - Install dependencies and Build/Run (`npm install && npm start`, `cargo run`, etc.).
  - **Verification:** Use `browser_*` tools to visit `localhost` (if web app) or check CLI output to ensure it actually works.
  - **Reporting:** Capture success status, required configuration, and any hurdles encountered.

### 3. Generate Artifacts (Action)
- **Trigger:** Verification complete (Step 2).
- **Action:** Synthesize the "Value" (from Step 1) and "Technical Reality" (from Step 2) into a permanent artifact.
- **Outputs (Select one based on context):**
  - **`TODO.md`:** For integrating the tool into an existing project. Includes specific technical steps found during the deep dive.
  - **`idea.md`:** For starting a new project. Includes the initial "Value" brainstorming and the "How to start" technical guide.
  - **`brief.md`:** A formal summary for external communication (CEO, Board, Team). Focuses on high-level value, market position, and "Verified" status.

## Technical Implementation Details
- **Tools Required:**
  - `web_fetch` / `google_web_search`: To get trending data.
  - `run_shell_command`: For git operations, installation, and running servers.
  - `read_file`: To parse READMEs and user project context.
  - `browser_*`: For verifying web applications.
  - `write_file`: To save the artifacts.

## Example Interaction
**User:** "Any new cool tools for my project?"
**Agent:** (Reads user's project context, Fetches GitHub Trending)
"Here are 3 trending repos that fit your 'AI-powered ToDo app' stack:
1.  **SuperGraph-JS**: (Graph Database) - *Could optimize your complex task relationships.*
2.  **Fast-LLM-Edge**: (Inference) - *Might reduce your cloud API costs by running local models.*
3.  **React-Fancy-UI**: (UI Lib) - *Has the exact 'Cyberpunk' aesthetic you wanted.*

Which one should we test?"
**User:** "Check out Fast-LLM-Edge."
**Agent:** "I will clone `Fast-LLM-Edge` to a temp folder, install it, and try to run the benchmark. Proceed?"
**User:** "Yes."
**Agent:** (Clones, Installs, Runs). "It built successfully and ran the benchmark in 30ms. However, it requires Python 3.11+.
I've generated `idea.md` with the benchmark results and a plan to wrap this in a Docker container for your app."

## Instructions for the Skill File (SKILL.md)
The generated `SKILL.md` must contain:
1.  **YAML Frontmatter:** Name (`sync-trending`) and Description.
2.  **Detailed Procedural Rules:** Step-by-step instructions for the agent to follow the 3-step workflow.
3.  **Safety Guidelines:** strict rules about asking permission before executing code or downloading files.
