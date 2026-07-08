---
name: domain-research
description: Research, brainstorm, verify, and rank domain names for a business idea using live domain availability, Cloudflare Registrar/MCP pricing when available, search-engine signal/noise checks, traffic-intent analysis, and founder-speed brand diligence. Use when the user asks to find a domain name, name a startup/product, check domain availability or prices, compare TLDs, assess SEO/search traffic potential of candidate domains, or produce a ranked shortlist of buyable domains.
---

# Domain Research

## Overview

Find domains that are actually worth buying: available, affordable, memorable, low-noise in search, and aligned with real internet demand. Treat this as founder-speed naming diligence, not a pure creativity exercise.

## Workflow

### 1. Frame the Idea

Extract the business idea, audience, job-to-be-done, category, differentiator, geography, budget, and launch urgency. If context is thin, proceed with reasonable MVP assumptions and state them briefly.

Set TLD defaults:
- Prioritize `.com` when a serious brand or broad consumer market matters.
- Include `.ai`, `.app`, `.dev`, `.io`, and `.co` when the product/category makes them credible.
- Consider country TLDs only when the market is geographically focused.
- Treat novelty TLDs as optional unless they make the name meaningfully better.

### 2. Generate a Candidate Universe

Generate 40-100 candidate domains before filtering. Mix these lanes:
- Literal/category: direct keyword combinations users already search.
- Outcome-led: the result the user wants.
- Verb-led: an action the product helps people take.
- Audience-led: names that signal who it is for.
- Brandable compounds: two clear words with a strong mental image.
- Short coined names: easy spelling, no awkward pronunciation.
- Prefix/suffix MVP patterns: `get`, `try`, `use`, `join`, `hq`, `labs`, `studio`, only when the base name is strong.

Cull early for obvious failures: hard spelling, hyphens, numbers, trademark bait, confusing homophones, accidental adult/gambling/crypto meanings, and names that require a long explanation.

### 3. Verify Availability and Price

Use Cloudflare MCP/Registrar when available. Read [cloudflare-mcp.md](references/cloudflare-mcp.md) before performing live checks.

Record for every checked domain: availability status, registration price, renewal price when exposed, transfer price when exposed, currency, premium flag, TLD support, source, and timestamp.

Never purchase, register, transfer, or change DNS without explicit user confirmation.

If live Cloudflare availability is unavailable, label results as "unverified" and do only soft filtering with DNS/RDAP/search evidence. Do not present soft checks as final availability.

### 4. Check Search Signal/Noise

Read [search-signal-playbook.md](references/search-signal-playbook.md) for the query matrix. For each serious candidate, run live searches for:
- Exact brand phrase.
- Exact domain.
- Brand plus category.
- Category intent terms.
- Negative/risk terms.
- Trademark/company collisions.

Judge traffic potential from the market/category queries and adjacent demand, not from a nonexistent domain's current traffic. Use Cloudflare Radar or similar traffic tools to inspect existing exact-match domains, competitors, category leaders, and TLD-level context when available.

### 5. Score and Shortlist

Read [scoring-rubric.md](references/scoring-rubric.md). Score domains on a 100-point scale:
- Business fit: 20
- Traffic intent: 20
- Search signal/noise: 20
- Brand quality: 15
- Availability/economics: 15
- Risk/defensibility: 10

For consistent scoring, optionally run:

```bash
python3 <skill_dir>/scripts/score_domains.py candidates.json --markdown
```

The script expects gathered evidence, not raw ideas. It does not check availability or search.

### 6. Deliver the Decision

Use [report-template.md](references/report-template.md) for larger requests. For quick requests, still include:
- Top 5-10 domains ranked.
- Availability and price evidence.
- Why each name fits.
- Search signal and noise summary.
- Risks: trademark, ambiguity, spam, premium renewal, TLD weakness.
- Clear recommendation: buy now, watch, or avoid.
- Exact checks performed and timestamp.

## Rules

- Prefer real evidence over clever naming. A beautiful unavailable or high-noise name loses.
- Do not fabricate availability, prices, search volume, rankings, or trademark status.
- State when results are approximate or unavailable because a tool is missing.
- Keep founder context in mind: surface fast, practical buys before exhaustive naming theory.
- Do not provide legal advice. Flag trademark risk and recommend counsel for high-stakes launches.

## Resources

- `references/cloudflare-mcp.md` - Cloudflare MCP and Registrar availability/pricing workflow.
- `references/search-signal-playbook.md` - live SERP and traffic-intent research method.
- `references/scoring-rubric.md` - 100-point scoring model and rejection rules.
- `references/report-template.md` - final deliverable template.
- `scripts/score_domains.py` - deterministic scorer for already-researched candidates.
