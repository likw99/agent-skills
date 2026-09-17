---
name: domain-research
description: Use when naming a product or startup, finding or choosing a domain name, checking whether domains are available or what they cost to register and renew, comparing TLDs (.com, .ai, .io, .app, .dev), screening candidate names for search collisions, SEO noise, trademark risk or search demand, or when a new app needs its name and domain before setup (in saas-starter, before `pnpm init-product`). Produces a ranked shortlist of buyable domains backed by live registrar and search evidence.
---

# Domain Research

Find domains worth buying: available, affordable to keep, memorable, low-noise in search, and aimed at real demand. This is founder-speed naming diligence, not a creativity exercise. A beautiful name that is taken, noisy or expensive to renew loses.

`scripts/…` and `references/…` paths are inside this skill's folder (in saas-starter: `.agents/skills/domain-research/`); every other path is in the project. The scripts need only `python3`. Keep working files such as candidate lists and JSON results in a folder that isn't committed (in saas-starter: `.cache/domain-research/`).

## Evidence sources

Check what this session has before starting, and report which source answered each question.

| Question | Best | Fallback | Last resort |
|---|---|---|---|
| Can it be registered, and what does it cost to keep? | `scripts/check_domains.py` with `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` | A connected Cloudflare API MCP, same endpoint | `scripts/check_domains.py --rdap`: free, no price, and "unregistered" is not a yes |
| Does someone already own the name in search? | A browser tool reading real Google results | `scripts/check_search_signal.py` with `SERPAPI_KEY` or `SERPER_API_KEY` | Ask the human to run the searches; mark the name unverified |
| Does anyone search for the problem? | People also ask and related searches on category queries | Google Trends, Keyword Planner | Say that demand is unmeasured |

Setup and caveats: [cloudflare-mcp.md](references/cloudflare-mcp.md), [search-signal-playbook.md](references/search-signal-playbook.md).

## Workflow

### 1. Frame the idea

Extract the business idea, audience, job-to-be-done, category, differentiator, geography, budget and launch urgency. If context is thin, proceed on stated MVP assumptions.

TLD defaults. A project's own naming policy overrides them (in saas-starter: `docs/distribution/README.md` §2).
- `.com` for any brand you might keep.
- `.ai`, `.app`, `.dev`, `.io` or `.co` only when the product and audience make it credible. Price each one live: several renew above their first-year price, and `.ai` needs a two-year minimum.
- Country TLDs only for a geographically focused market. Novelty and keyword TLDs only when they make the name clearly better; they carry no search advantage.

### 2. Generate a candidate universe

Generate 40–100 candidates before filtering. Read [naming-patterns.md](references/naming-patterns.md) and choose patterns on two separate questions:
- **Product-fit:** does this product have a natural filler for the pattern's slot?
- **Structural risk:** is the pattern's shape risky for any product (a famous convention, squatter bait, IP-adjacent vocabulary)?

Cull early: hard spelling, hyphens, digits, someone else's trademark, confusing homophones, accidental adult, gambling or crypto meanings, and names that need a long explanation.

### 3. Verify availability and price

Read [cloudflare-mcp.md](references/cloudflare-mcp.md), then batch the candidates through the best available source: `scripts/check_domains.py --file candidates.txt --json`. Each record carries status, first-year price, renewal price, currency, source and timestamp; keep all of them.

- Only `available` is a registrar's yes. `premium`, `unknown`, `unsupported` and RDAP's `unregistered` are unresolved: confirm them another way or label them unverified. `taken` and `frozen` are out.
- Judge cost by the renewal price, since that is what keeping the domain costs.
- Never buy, register, renew, transfer or change DNS. Recommend, and let the human buy.

### 4. Check search signal and noise

For each serious candidate, run the query matrix in [search-signal-playbook.md](references/search-signal-playbook.md). Start with the bare exact phrase, one candidate per query. Then search the exact domain, the brand plus its category, risk terms, and trademark or company collisions.

With a browser tool, read real results pages. Otherwise run `scripts/check_search_signal.py <name>`, and `--query '<query>'` for the rest of the matrix. The script only fetches; reading and judging the results is your job. A spelling-fix or zero-mention warning means the name has not been checked yet.

### 5. Check category demand

This asks a different question from step 4: not "does someone own this name?" but "does anyone search for this problem?" Follow the Category Demand section of [search-signal-playbook.md](references/search-signal-playbook.md), and report the answer on its own line, apart from name collisions.

### 6. Score and shortlist

Score with [scoring-rubric.md](references/scoring-rubric.md): business fit 20, traffic intent 20, search signal and noise 20, brand quality 15, availability and economics 15, risk and defensibility 10. For consistent numbers, add your judgments to the `check_domains.py --json` records and run:

```bash
python3 scripts/score_domains.py candidates.json --markdown
```

The script scores the evidence you gathered and checks nothing itself. It never labels an unverified domain Buy now, and neither should you.

### 7. Deliver the decision

Use [report-template.md](references/report-template.md) for larger requests. A quick answer still includes:
- The top 5–10 domains, ranked and labeled Buy now, Strong shortlist, Watch or Avoid.
- Status, first-year and renewal price, with source and timestamp.
- Why each name fits, its search signal and noise, and the category-demand read.
- Risks: trademark, ambiguity, spam associations, premium or rising renewal, weak TLD.
- The checks that ran, and the evidence sources that were missing.

**In a saas-starter app** (its `package.json` defines `init-product`), save the report as `docs/app/research/domain.md`. Once the human has chosen and bought the domain, run `pnpm init-product --name "<Name>" --domain <domain> --tagline "<tagline>"` (go-live step 7). That writes the name and domain into `DISTRIBUTION.md`; fill in that section's trademark-check date and research link yourself.

## Rules

- Prefer real evidence over clever naming.
- Never fabricate availability, prices, search volume, rankings or trademark status. Say what a missing tool left unchecked.
- Surface fast, practical buys before exhaustive naming theory.
- Flag trademark risk without giving legal advice, and recommend counsel for high-stakes launches.
- Never recommend an expired or dropped domain for its backlinks or leftover traffic; Google treats that as spam.

## Resources

- `references/naming-patterns.md`: pattern catalog with real brand exemplars, the four slots, product-fit versus structural risk.
- `references/cloudflare-mcp.md`: Registrar availability and pricing, result statuses, token safety, the RDAP fallback, Radar.
- `references/search-signal-playbook.md`: search tools, query rules and matrix, reading results, category demand.
- `references/scoring-rubric.md`: the 100-point model, hard rejections, recommendation labels, base rates.
- `references/report-template.md`: the full deliverable.
- `scripts/check_domains.py`: availability and price from Cloudflare Registrar, or a free soft check with `--rdap`.
- `scripts/check_search_signal.py`: Google results through SerpApi or Serper, with spelling-fix and mention warnings. Fetches only.
- `scripts/score_domains.py`: deterministic scorer for researched candidates.
