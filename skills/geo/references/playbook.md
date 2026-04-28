# GEO Playbook

## Table of Contents

- Core Thesis
- Source-Backed Principles
- Engine Notes
- Content Patterns
- Technical Checklist
- Measurement
- Source Map

## Core Thesis

Generative Engine Optimization is the practice of increasing the chance that AI answer engines retrieve, understand, trust, cite, and accurately recommend a site, product, or brand. It overlaps with SEO, but the success metric shifts from rank and click volume to answer presence, citation share, factual accuracy, sentiment, and downstream conversion.

The practical model:

1. Access: can the engine crawl or fetch the content?
2. Retrieval: does the page match the query and entity clearly enough to be selected?
3. Trust: does the content include evidence, authorship, originality, freshness, and external corroboration?
4. Citation: can a sentence, table, quote, or stat be lifted and cited without ambiguity?
5. Conversion: does the cited answer move the user toward signup, purchase, install, contact, or trust?

## Source-Backed Principles

### Keep SEO Fundamentals

Google says AI Overviews and AI Mode use the same foundational SEO requirements: pages must be indexable and eligible for snippets, and there are no special AI-only schema requirements for those Google Search features. Google also says AI features may use query fan-out across subtopics and sources, so content clusters and specific subtopic pages matter.

Use this as the base layer: crawlable pages, internal links, textual content, page experience, accurate structured data, canonical URLs, and Search Console diagnostics.

### Optimize for Evidence, Not Keyword Density

The KDD 2024 GEO paper found that adding credible sources, quotations, and statistics improved source visibility in generative engine responses, while keyword stuffing performed poorly. The strongest general pattern is evidence density: facts, numbers, cited sources, and clear claims that an AI system can safely reuse.

Use:
- direct answers near the top of each section
- named entities and dates
- comparison tables
- original data or benchmarks
- quotes with attribution
- primary-source links
- clear definitions and scope limits

Avoid:
- vague authority language
- excessive adjectives
- pages that only paraphrase top results
- many thin pages created for every keyword variant
- claims that schema says but visible text does not support

### Build Entity Consensus

Industry correlation studies are not causal proof, but they consistently point toward brand mentions and web-wide corroboration as important AI visibility signals. Treat off-site mentions as entity confidence work: help systems see that the same product, company, founder, use case, and category appear consistently across trusted surfaces.

High-leverage founder surfaces:
- GitHub repo and README
- docs site and package registry
- launch posts
- app/integration directories
- comparison pages
- credible guest posts or interviews
- YouTube demo with transcript
- review platforms relevant to the category
- community answers where disclosure and rules allow participation

### Respect Content Controls

GEO should never assume "allow every AI bot." Separate search inclusion, user-requested fetches, ads validation, and model training. Some bots affect search visibility; others control training. Read current provider docs before editing crawl policy.

## Engine Notes

### Google AI Overviews and AI Mode

For Google Search AI features:
- There are no additional technical requirements beyond Google Search eligibility and snippets.
- Important content should be in crawlable text.
- Structured data should match visible content.
- `nosnippet` and `max-snippet` can limit use as direct input for AI Overviews and AI Mode.
- `Google-Extended` is a control token for Gemini model training and Gemini/Vertex grounding, not a Google Search ranking signal.

### OpenAI and ChatGPT Search

OpenAI separates crawlers:
- `OAI-SearchBot`: search discovery and surfacing in ChatGPT search features.
- `GPTBot`: model training.
- `ChatGPT-User`: user-initiated fetches; not used to determine search inclusion.
- `OAI-AdsBot`: validates ChatGPT ad landing pages.

For visibility in ChatGPT search, do not block `OAI-SearchBot` on important public pages. For commerce, product feeds can provide more accurate and current product data than crawling alone.

### Perplexity

Perplexity documents:
- `PerplexityBot` for surfacing and linking websites in search results, not foundation-model training.
- `Perplexity-User` for user-requested page access.

If a WAF or CDN is present, allow the documented bot user agents and IP ranges for pages intended to appear.

### Anthropic and Claude

Anthropic documents:
- `ClaudeBot` for model training.
- `Claude-SearchBot` for search result quality.
- `Claude-User` for user-directed retrieval.

Blocking search or user retrieval bots may reduce Claude visibility even if blocking training is acceptable.

### Microsoft Copilot and Bing

Bing has explicit AI visibility reporting in Bing Webmaster Tools:
- total citations
- average cited pages
- grounding queries
- page-level citation activity
- visibility trends

Bing recommends improving depth, structure, evidence, freshness, and reducing ambiguity across text, image, and video. Use IndexNow to notify participating engines when important content changes.

### llms.txt

`llms.txt` is a Markdown proposal, not a ratified standard and not a guaranteed ranking factor. Use it when a site has documentation, product pages, API references, or canonical explainers that agents should find quickly.

Good `llms.txt` files:
- live at `/llms.txt`
- start with an H1 name and short description
- group the most important URLs by section
- include brief descriptions
- omit private, stale, duplicate, or low-value pages
- link to Markdown versions where possible

Do not confuse `llms.txt` with `robots.txt`: `robots.txt` controls access; `llms.txt` curates understanding.

## Content Patterns

### Citation-Ready Section

Use this shape for any important topic:

1. Heading phrased like the query.
2. Two to four sentence direct answer.
3. Evidence block with statistics, examples, source links, screenshots, or named cases.
4. Comparison or decision table when users choose between options.
5. "When to use / when not to use" guidance.
6. Date, author, and update note for time-sensitive content.

### Decision Pages

AI answer engines often answer comparison and recommendation queries. Useful pages include:
- `<product> vs <competitor>`
- `<product> alternatives`
- `best <category> for <audience>`
- `<category> pricing`
- `<feature> integration guide`
- `<problem> troubleshooting`
- `security`, `privacy`, `SOC 2`, `data retention`, and `deployment` pages when relevant

Write these pages honestly. A credible "not for everyone" section often improves trust.

### Originality Assets

Create assets competitors cannot copy quickly:
- benchmarks
- teardown screenshots
- real setup walkthroughs
- integration matrices
- pricing calculators
- datasets
- founder field notes
- customer implementation stories
- open-source examples

## Technical Checklist

- Important pages return `200` and canonicalize correctly.
- Robots policy intentionally allows search crawlers needed for AI discovery.
- Training bot policy is explicit and matches the user's preference.
- No accidental `noindex`, `nosnippet`, low `max-snippet`, blocked JS/CSS, or WAF challenge on priority pages.
- Sitemap includes canonical priority pages and current `lastmod`.
- IndexNow is enabled where useful.
- Structured data is valid, specific, and visible on-page.
- Page title and H1 clearly name the entity/topic.
- Main content is not hidden behind client-only rendering or login.
- Images have descriptive alt text and nearby captions.
- Product pages include current price, availability, reviews, images, variants, shipping/return facts, and identifiers when applicable.
- Docs expose Markdown or clean HTML versions when possible.

## Measurement

Track:
- citation count by engine
- cited URLs
- brand mention share
- competitor mention share
- answer sentiment and factual accuracy
- grounding queries
- AI referral sessions and conversions
- server-log hits by AI user agent
- Search Console/Bing Webmaster changes after releases

Use a stable query matrix and retest on a schedule. GEO changes are noisy; compare snapshots over time instead of trusting one-off answers.

## Source Map

- Google Search Central, "AI features and your website": https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central, helpful reliable content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central, robots meta and snippets: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Google Search Central, structured data policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google crawler docs, Google-Extended: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- OpenAI crawler docs: https://developers.openai.com/api/docs/bots
- OpenAI merchant/product discovery: https://chatgpt.com/merchants/
- Perplexity crawler docs: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- Anthropic crawler docs: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Bing AI Performance announcement: https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- Microsoft grounding post: https://blogs.bing.com/search/February-2026/Elevating-the-Role-of-Grounding-on-the-AI-Web
- GEO paper: https://arxiv.org/abs/2311.09735
- Verifiability in generative search engines: https://aclanthology.org/2023.findings-emnlp.467/
- llms.txt proposal: https://llmstxt.org/
- Ahrefs AI brand visibility correlations: https://ahrefs.com/blog/ai-brand-visibility-correlations/
- Ahrefs AI Overview citation overlap study: https://ahrefs.com/blog/search-rankings-ai-citations/
- Semrush AI Overviews study: https://www.semrush.com/blog/semrush-ai-overviews-study/
