---
name: llm-daily
description: >
  Generate and publish a daily AI/LLM newsletter called "LLM Daily" that curates content from
  10+ sources (ArXiv, GitHub Trending, HuggingFace, VentureBeat, TechCrunch, Product Hunt,
  Sequoia Capital). Use when user asks to: generate a newsletter, create today's
  LLM Daily, collect AI news, build an AI newsletter, publish newsletter, or run the daily
  newsletter pipeline. Also triggers on: "llm daily", "daily briefing", "AI newsletter",
  "generate newsletter", "collect news", "publish newsletter".
---

# LLM Daily Newsletter Skill

Generate a professional daily AI/LLM newsletter by collecting data from multiple sources and
synthesizing it into a curated briefing.

## Quick Start

### Step 1: Collect Data

```bash
cd <skill_dir>/scripts
uv run --with requests --with beautifulsoup4 --with feedparser --with huggingface-hub collect.py
```

This runs all collectors (ArXiv, GitHub, HuggingFace, VentureBeat, TechCrunch, Product Hunt,
Sequoia) and outputs `collected_data_YYYY-MM-DD.md` to `scripts/output/`.

Skip specific collectors if they fail or aren't needed:
```bash
uv run --with requests --with beautifulsoup4 --with feedparser --with huggingface-hub collect.py --skip-producthunt --skip-huggingface
```

### Step 2: Generate Newsletter

Read the collected data file, then generate the newsletter using the section prompts below.
Write the final newsletter to `scripts/output/llm_newsletter_YYYY-MM-DD.md`.

### Step 3: Publish (Optional)

Requires `BUTTONDOWN_API_KEY` in the environment:
```bash
cd <skill_dir>/scripts
uv run --with requests publish.py output/llm_newsletter_YYYY-MM-DD.md --status draft
```

Without BUTTONDOWN_API_KEY, the newsletter is still generated locally as a markdown file.

## Newsletter Generation Instructions

After collecting data, generate the newsletter by creating each section below. Read the
collected data markdown file and use it as source material.

### Newsletter Structure

```
# 🔍 LLM DAILY
## Your Daily Briefing on Large Language Models
**{date}**

{stats_line}

---

# HIGHLIGHTS
{3-5 bullet points of key developments}

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

### Section Generation Prompts

Use these prompts when generating each section from the collected data.

#### BUSINESS Section
Source data: VentureBeat, TechCrunch, Sequoia articles.
- Cover: funding rounds, M&A, company announcements, market trends
- Include direct links to original articles
- Include publication dates in (YYYY-MM-DD) format
- Focus on developments from the past 24-48 hours

#### PRODUCTS Section
Source data: Product Hunt.
- Cover: new AI product launches, updates, applications, user feedback
- Include direct links and company attribution
- Specify if startup or established player

#### TECHNOLOGY Section
Source data: GitHub trending repos, HuggingFace models/datasets/spaces.
- Cover: open source projects, new models, developer tools, infrastructure
- Include direct links to GitHub repos and HuggingFace pages
- Note stars, forks, trending metrics
- Highlight distinctive features and technical details

#### RESEARCH Section
Source data: ArXiv papers.
- "Paper of the Day": single most significant paper with title, authors, institutions,
  arXiv link, 2-3 sentence significance explanation, key findings summary
- "Notable Research": 3-5 other papers with title, primary author, arXiv link,
  1-2 sentence summary
- Always include arXiv URLs in format `https://arxiv.org/abs/XXXX.XXXXX`
- Include publication dates in (YYYY-MM-DD) format

#### HIGHLIGHTS Section
Generate after all other sections. Extract 3-5 most important developments as bullet points.
Each bullet: concise (1-2 sentences), specific, using "•" symbol.

#### LOOKING AHEAD Section
1-2 paragraphs identifying emerging trends and predictions. Reference current quarter.
Keep concise (~100 words).

## Data Sources & API Keys

### No API Key Required (always available)
| Source | Type | Data |
|--------|------|------|
| ArXiv | REST/XML | LLM research papers |
| GitHub Trending | Web scraping | Trending AI repositories |
| VentureBeat | RSS feed | AI business news |
| TechCrunch | RSS feed | AI tech news |
| Sequoia Capital | RSS feed | VC insights |

### Optional API Keys
| Source | Env Variable | Purpose |
|--------|-------------|---------|
| HuggingFace | `HF_TOKEN` | Trending models/datasets/spaces (works without token too) |
| GitHub | `GITHUB_TOKEN` | README enrichment, commit history (scraping works without) |
| Product Hunt | `PRODUCTHUNT_API_TOKEN` | AI product launches |
| Buttondown | `BUTTONDOWN_API_KEY` | Email newsletter publishing |

### Email Publishing

Email publishing uses [Buttondown](https://buttondown.email). Set `BUTTONDOWN_API_KEY` in
the environment. Use `--status draft` for review before sending, or `--status scheduled` for
automatic delivery.

Without `BUTTONDOWN_API_KEY`, the skill generates the newsletter as a local markdown file.
The file can be copy-pasted into any email platform.

## CLI Options

```
uv run --with requests --with beautifulsoup4 --with feedparser --with huggingface-hub collect.py [options]

--output-dir PATH      Output directory (default: ./output)
--force-refresh        Force refresh all caches
--skip-arxiv           Skip ArXiv collection
--skip-github          Skip GitHub collection
--skip-huggingface     Skip HuggingFace collection
--skip-venturebeat     Skip VentureBeat collection
--skip-techcrunch      Skip TechCrunch collection
--skip-producthunt     Skip Product Hunt collection
--skip-sequoia         Skip Sequoia Capital collection
--arxiv-days N         ArXiv lookback days (default: 7)
--arxiv-results N      Max ArXiv results per query (default: 50)
--news-days N          News lookback days (default: 7)
--huggingface-limit N  Max HuggingFace items (default: 30)
--producthunt-limit N  Max Product Hunt items (default: 50)
```

## Caching

All collectors cache results locally in `scripts/cache/`. Cache TTL:
- ArXiv, GitHub, HuggingFace, Product Hunt: 24 hours
- VentureBeat, TechCrunch, Sequoia: 12 hours

Use `--force-refresh` to bypass caches.
