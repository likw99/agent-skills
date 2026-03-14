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

Read the generated `scripts/output/context.md` file using your file reading tools. Using this context, generate the final newsletter based on the **Newsletter Structure** and **Section Generation Prompts** below. 

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

Follow this template exactly:

```markdown
# 🔍 LLM DAILY
## Your Daily Briefing on Large Language Models
**{date}**

{stats_line}

---

# HIGHLIGHTS
{3-5 bullet points of key developments across all sections}

---

# BUSINESS
{funding, M&A, company updates, market analysis}

---

# PRODUCTS
{new releases, updates, applications, community reception}

---

# TECHNOLOGY
{open source projects, models/datasets, developer tools, infrastructure}

---

# RESEARCH
## Paper of the Day
{single most significant paper with full details}

## Notable Research
{3-5 other significant papers}

---

# LOOKING AHEAD
{emerging trends and predictions, 1-2 paragraphs}
```

## Section Generation Prompts

Apply these guidelines when drafting each section based on the collected context.

#### BUSINESS Section
Source data: VentureBeat, TechCrunch.
- Cover: funding rounds, M&A, company announcements, market trends
- Include direct links to original articles
- Focus on developments from the past 24-48 hours

#### PRODUCTS Section
Source data: Product Hunt, Hacker News.
- Cover: new AI product launches, updates, applications, user feedback
- Include direct links and company attribution
- Specify if startup or established player

#### TECHNOLOGY Section
Source data: GitHub Recent Top AI Repos, HuggingFace Trending Models.
- Cover: open source projects, new models, developer tools, infrastructure
- Include direct links to GitHub repos and HuggingFace pages
- Highlight distinctive features and technical details

#### RESEARCH Section
Source data: ArXiv LLM Papers.
- "Paper of the Day": single most significant paper with title, authors, institutions,
  arXiv link, 2-3 sentence significance explanation, key findings summary
- "Notable Research": 3-5 other papers with title, primary author, arXiv link,
  1-2 sentence summary
- Always include arXiv URLs in format `https://arxiv.org/abs/XXXX.XXXXX`

#### HIGHLIGHTS Section
Generate after all other sections. Extract 3-5 most important developments as bullet points.
Each bullet: concise (1-2 sentences), specific, using "•" symbol.

#### LOOKING AHEAD Section
1-2 paragraphs identifying emerging trends and predictions. Reference current quarter.
Keep concise (~100 words).

## Configuration

Data sources are configured in `references/sources.yaml`. To add a new source:
1. Identify if it is an `rss`, `json_api`, or `xml_api`.
2. Add a new entry to `sources.yaml` with the appropriate `parser_config`.
