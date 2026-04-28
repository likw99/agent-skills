# GEO Templates

## Table of Contents

- GEO Audit Output
- Query Matrix
- robots.txt Policy
- llms.txt
- Citation-Ready Page Brief
- JSON-LD Starting Points
- Founder MVP Plan

## GEO Audit Output

```markdown
# GEO Audit: <site/product>

## Executive Read

- Current AI visibility:
- Biggest blocker:
- Fastest win:
- Highest-leverage content opportunity:
- Risk or assumption:

## Priority Actions

| Priority | Action | Why it matters | Effort | Owner |
| --- | --- | --- | --- | --- |
| P0 |  |  | S/M/L |  |

## Access and Crawlability

- robots.txt:
- sitemap:
- noindex/snippet controls:
- WAF/CDN:
- AI user-agent findings:

## Entity Clarity

- Canonical brand:
- Canonical product/category:
- SameAs/profile gaps:
- Schema gaps:
- Inconsistent claims:

## Citation-Ready Content

- Pages to rewrite:
- Missing evidence:
- Missing comparison/decision pages:
- Thin or duplicate pages:

## Off-Site Proof

- Existing mentions:
- High-signal targets:
- Partner/integration directory gaps:

## Measurement Plan

- Query set:
- Engines:
- Metrics:
- Retest cadence:
```

## Query Matrix

```markdown
| Query | Intent | Engine | Answer includes brand? | Cited URL | Competitors cited | Missing fact | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <brand> alternatives | Commercial | ChatGPT Search | Yes/No |  |  |  |  |
| best <category> for <audience> | Commercial | Perplexity | Yes/No |  |  |  |  |
| how to <job> with <tool type> | Informational | Google AI Mode | Yes/No |  |  |  |  |
```

## robots.txt Policy

Choose deliberately. This example allows AI search visibility while blocking model training for providers that expose separate controls.

```txt
# Classic search
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# AI search / answer visibility
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

# User-directed retrieval. Only allow if this matches the site's content policy.
User-agent: ChatGPT-User
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-User
Allow: /

# Model training controls. Adjust to the user's preference.
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

Notes:
- Re-check current provider docs before shipping.
- Do not block CSS/JS needed to render public content.
- For Google AI Overviews and AI Mode, Googlebot/snippet controls matter more than `Google-Extended`.

## llms.txt

```markdown
# <Product or Site Name>

> <One-sentence description of what this site/product does and who it helps.>

## Core Resources

- [Overview](https://example.com/): Clear product summary, positioning, and primary use cases.
- [Pricing](https://example.com/pricing): Plans, limits, and buying guidance.
- [Docs](https://example.com/docs): Setup guides, API reference, and examples.
- [Security](https://example.com/security): Security, privacy, data retention, and compliance details.

## Comparisons

- [<Product> vs <Competitor>](https://example.com/compare/competitor): Honest comparison, strengths, limitations, and migration guidance.

## Optional

- [Changelog](https://example.com/changelog): Product updates and release history.
```

## Citation-Ready Page Brief

```markdown
# Page: <title>

Primary query:
Secondary queries:
Target engine(s):
Conversion goal:

## Direct Answer

Write 2-4 sentences that answer the primary query directly.

## Evidence to Add

- Statistic:
- Quote:
- Screenshot/demo:
- Customer proof:
- Primary source:
- Date-sensitive fact:

## Structure

1. Direct answer
2. Who this is for
3. How it works
4. Comparison table
5. Limitations
6. FAQ
7. CTA

## Schema

Recommended type:
Required visible fields:
```

## JSON-LD Starting Points

Organization:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example",
    "https://github.com/example"
  ]
}
</script>
```

Software application:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Example",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "url": "https://example.com",
  "description": "A concise visible-on-page description.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

FAQ:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does Example do?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Example helps ... This answer must match visible page text."
      }
    }
  ]
}
</script>
```

## Founder MVP Plan

```markdown
## Ship Today

1. Fix crawl/access blockers.
2. Add or repair Organization/Product schema.
3. Publish `/llms.txt` for the 5-10 most important pages.
4. Rewrite the homepage hero and top product page with direct answers and evidence.

## Ship This Week

1. Create one comparison page and one alternatives page.
2. Add a security/trust page if buyers ask trust questions.
3. Add a YouTube demo or transcript-backed walkthrough.
4. Seed 5 high-quality third-party profiles/directories.

## Measure

1. Run the same 20-query matrix weekly.
2. Track citations, mentions, competitors, and referral conversions.
3. Update pages that are retrieved but not cited.
```
