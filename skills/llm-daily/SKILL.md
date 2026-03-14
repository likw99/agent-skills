---
name: llm-daily
description: >
  Generate and publish a daily AI/LLM newsletter called "LLM Daily" that curates content from
  top sources (ArXiv, GitHub Trending, HuggingFace, VentureBeat, TechCrunch, Product Hunt). 
  Use when user asks to: generate a newsletter, create today's LLM Daily, collect AI news, 
  build an AI newsletter, publish newsletter, or run the daily newsletter pipeline. 
  Also triggers on: "llm daily", "daily briefing", "AI newsletter", "generate newsletter", 
  "collect news", "publish newsletter".
---

# LLM Daily Newsletter Skill

Generate a professional daily AI/LLM newsletter by utilizing the `fetch_sources.py` script to fetch dynamically configured data, and leveraging your LLM capabilities to synthesize it into a curated briefing.

## Workflow

### Step 1: Collect Data

Run the universal collector script to fetch data from all sources defined in `references/sources.yaml`.

```bash
cd <skill_dir>/scripts
uv run --with requests --with feedparser --with pyyaml fetch_sources.py
```

This will parse all RSS feeds, JSON APIs, and XML APIs, generating a single markdown file at `scripts/output/context.md`.

### Step 2: Generate Newsletter

Read the generated `scripts/output/context.md` file using your file reading tools. Then open `references/newsletter_template.md` and follow it exactly when drafting the final newsletter. Use the source context to synthesize a readable briefing, not a raw dump of links.

Write the final newsletter to `scripts/output/llm_newsletter_YYYY-MM-DD.md`.

### Step 3: Publish (Optional)

If the user wants to publish the newsletter and `BUTTONDOWN_API_KEY` is present in the environment:
```bash
cd <skill_dir>/scripts
uv run --with requests publish.py output/llm_newsletter_YYYY-MM-DD.md --status draft
```

Without `BUTTONDOWN_API_KEY`, the newsletter is only generated locally.

---

## Newsletter Structure

The canonical newsletter structure now lives in `references/newsletter_template.md`.

Use that file as the source of truth for:
- the markdown layout
- section order
- scan-friendly formatting rules
- which sections to omit

## Section Generation Prompts

Apply these guidelines when drafting each section based on the collected context.

#### BUSINESS Section
Source data: VentureBeat, TechCrunch.
- Cover: funding rounds, M&A, company announcements, market trends
- Include direct links to original articles using markdown links
- Focus on developments from the past 24-48 hours
- Prefer 3-4 strong items over exhaustive coverage
- Each item should explain both what happened and why it matters

#### PRODUCTS Section
Source data: Product Hunt, Hacker News.
- Cover: new AI product launches, updates, applications, user feedback
- Include direct links and company attribution using markdown links
- Specify if startup or established player
- Keep each item concise and readable for a general technical audience

#### TECHNOLOGY Section
Source data: GitHub Recent Top AI Repos, HuggingFace Trending Models.
- Cover: open source projects, new models, developer tools, infrastructure
- Include direct links to GitHub repos and HuggingFace pages using markdown links
- Highlight distinctive features and technical details
- Focus on the few items that are actually novel or important

#### RESEARCH Section
Source data: ArXiv LLM Papers.
- Do not include a "Paper of the Day" subsection
- Present research as a single "Research" list with the strongest 4-6 papers
- For each paper: include title, primary author (or first author) when available,
  arXiv link, 1-2 sentence summary, and why it matters when that is clear
- Always include arXiv URLs in format `https://arxiv.org/abs/XXXX.XXXXX`

#### HIGHLIGHTS Section
Generate after all other sections. Extract 3-5 most important developments as bullet points.
Each bullet: concise (1-2 sentences), specific, and formatted as a normal markdown bullet using `-`.

## Markdown Style Rules

- Use standard markdown bullets (`-`) and ordered lists (`1.`), not decorative bullets such as `•`
- Use descriptive markdown links instead of raw URLs or separate `Link:` lines
- Prefer title case section headings for readability
- Keep sections skimmable: short paragraphs, short bullets, generous spacing
- Do not include the old stats line below the date
- Do not include a "Looking Ahead" section
- If a section is thin, keep it short instead of padding it with weak items

## Configuration

Data sources are configured in `references/sources.yaml`. To add a new source:
1. Identify if it is an `rss`, `json_api`, or `xml_api`.
2. Add a new entry to `sources.yaml` with the appropriate `parser_config`.
