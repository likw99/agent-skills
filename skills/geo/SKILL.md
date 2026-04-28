---
name: geo
description: Optimize websites, docs, products, and brand presence for Generative Engine Optimization (GEO), AI search visibility, answer-engine citations, and LLM retrieval. Use when the user asks about GEO, AEO, LLMO, ChatGPT Search, Google AI Overviews or AI Mode, Gemini, Perplexity, Claude Search, Microsoft Copilot/Bing AI answers, AI crawler access, robots.txt for AI bots, llms.txt, structured data for AI discovery, citation tracking, or making content easier for AI systems to retrieve, trust, cite, and recommend.
---

# GEO

## Overview

Improve the odds that AI answer engines can access, understand, trust, cite, and accurately summarize a site or product. Treat GEO as practical retrieval and citation engineering: keep SEO fundamentals, add evidence-rich content, clarify entities, allow the right crawlers, and measure citations instead of only clicks.

## Workflow

### 1. Establish the Target

Identify the business goal, target audience, priority engines, and conversion path. If the user provides little context, assume a founder-style MVP goal: fastest path to more qualified AI mentions and citations.

Classify the surface:
- **Docs or developer tool**: prioritize canonical docs, examples, API references, GitHub, package registries, `llms.txt`, and answerable troubleshooting pages.
- **SaaS or AI product**: prioritize use cases, alternatives, comparisons, pricing, integrations, security, changelog, customer proof, and third-party mentions.
- **Ecommerce**: prioritize product feeds, Product schema, availability, price, reviews, images, return/shipping policies, and merchant integrations.
- **Local or services**: prioritize LocalBusiness data, service-area pages, reviews, location facts, testimonials, and consistent directory profiles.

### 2. Build a Baseline

Create a small query set before changing content:
- Branded: `<brand>`, `<brand> pricing`, `<brand> alternatives`, `<brand> reviews`.
- Category: `best <category> for <audience>`, `how to <job-to-be-done>`, `<competitor> alternative`.
- Decision: `<brand> vs <competitor>`, `tools that <capability>`, `which <category> supports <feature>`.
- Support: common errors, integrations, setup, migration, security, compliance, or procurement questions.

For each query, record: engine, answer summary, cited URLs, brand mentions, competitor mentions, sentiment, missing facts, and next action. If live AI search is unavailable, approximate with classic search results, Bing Webmaster Tools, server logs, and competitor citation surfaces.

### 3. Audit Access and Indexability

Check whether the pages AI systems need can be crawled and rendered:
- `robots.txt`, CDN/WAF rules, sitemap, canonical tags, redirects, `noindex`, `nofollow`, `nosnippet`, `max-snippet`, and `data-nosnippet`.
- Allow search/retrieval crawlers intentionally: `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, `Bingbot`, and `Googlebot` where appropriate.
- Treat training crawlers separately from search crawlers. Allowing search visibility does not require allowing every model-training bot.
- Keep important content in visible HTML text. Do not hide key facts only in images, scripts, PDFs, or schema.

### 4. Make Entities Unambiguous

Normalize the brand, product, people, and feature names across owned and third-party surfaces:
- Use consistent names, URLs, descriptions, logos, founder/company facts, social profiles, and `sameAs` links.
- Add accurate Organization, WebSite, Product, SoftwareApplication, LocalBusiness, Article, FAQPage, HowTo, Review, or Dataset schema only when it matches visible content.
- Create one canonical page for each important entity or decision topic. Avoid scattering the best answer across many thin pages.

### 5. Rewrite for Citation

For priority pages, make the content chunkable and evidence-rich:
- Start sections with a direct answer in 2-4 sentences, then add proof.
- Use specific facts, dates, numbers, named entities, comparisons, tables, examples, and primary sources.
- Include original insight: benchmarks, teardown notes, screenshots, experiments, founder experience, customer outcomes, or implementation details.
- Attribute claims with credible citations. Avoid unsupported superlatives like "best" unless backed by criteria.
- Prefer plain headings that match user questions. Avoid keyword stuffing, fluff, and programmatic content that adds no information gain.

### 6. Add Machine-Readable Support

Use these when they fit the site:
- `sitemap.xml` and IndexNow for fresh URL discovery.
- Structured data that accurately mirrors visible text.
- `llms.txt` for a concise Markdown map of the site's most important AI-readable pages. Do not present it as a guaranteed ranking factor; treat it as a useful convention for agents, docs, and direct retrieval.
- Product feeds for commerce surfaces when available, especially if the user sells products and wants ChatGPT shopping visibility.

### 7. Expand Off-Site Proof

AI systems often rely on broader web consensus. Build genuine, verifiable mentions:
- GitHub README, package registry pages, docs portals, integration directories, app marketplaces, review sites, comparison pages, YouTube demos/transcripts, podcasts, launch posts, forums, and reputable publications.
- Keep claims consistent across every profile. Inconsistency hurts entity confidence.
- For founder-speed execution, prioritize 5-10 high-signal surfaces over mass syndication.

### 8. Measure and Iterate

Track visibility as citations and answer share, not only clicks:
- Bing Webmaster Tools AI Performance, Google Search Console, analytics referrals, `utm_source=chatgpt.com`, server logs by user agent, third-party AI visibility tools, and manual query snapshots.
- Re-test the same query set after changes. Record what changed in citations, wording, competitor mentions, and conversion intent.
- Re-prioritize pages where the site is indexed but absent from answers, or where AI answers cite competitors for facts the user can credibly provide better.

## Deliverables

When using this skill, produce whichever artifacts best fit the request:
- GEO audit with prioritized quick wins, high-leverage fixes, and risky assumptions.
- `robots.txt` crawler policy for search, user-fetch, and training bots.
- `llms.txt` or `llms-full.txt` draft.
- Structured data JSON-LD recommendations.
- Page rewrite briefs or direct content edits.
- AI visibility query matrix and measurement plan.
- Founder MVP action plan: what to ship today, this week, and later.

## References

Read [playbook.md](references/playbook.md) for deeper guidance, engine-specific notes, and source-backed principles. Read [templates.md](references/templates.md) for reusable audit, crawler, `llms.txt`, schema, and content rewrite templates.
