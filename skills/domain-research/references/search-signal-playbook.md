# Search Signal Playbook

Use this reference after initial availability filtering. The goal is to measure whether a domain name can win attention and search visibility without fighting too much noise.

## Query Matrix

Run live searches on at least one major search engine; use more than one for important decisions. Record the engine and date.

For a candidate `example.ai` with stem `example` and category `AI bookkeeping`, search:

- `"example"` - exact phrase collision.
- `"example.ai"` and `example.ai` - exact-domain collision/history.
- `site:example.ai` - indexed pages or prior use.
- `"example" "AI bookkeeping"` - category fit.
- `example AI`, `example app`, `example software`, `example startup` - entity collisions.
- `best AI bookkeeping software`, `AI bookkeeping for freelancers`, and other category-intent queries - demand context.
- `"example" trademark`, `"example" company`, `"example" lawsuit`, `"example" scam` - risk context.
- `"example" -<dominant unrelated meaning>` - test whether noise can be filtered.

Use quoted searches for exact phrases and `site:` to inspect a specific domain. Treat search result counts as rough hints only; the actual top results matter more.

## What Good Looks Like

High-signal names usually have:

- A clear relationship to category, outcome, or audience.
- Few or no dominant exact-phrase competitors.
- Category searches with active buyers, tools, tutorials, comparisons, or recurring pain.
- Search suggestions and related queries that align with the product's job-to-be-done.
- A memorable phrase people can spell after hearing once.
- Room to become the canonical entity for the phrase.

## What Bad Looks Like

High-noise names usually have:

- Dominant unrelated meanings in the first page of results.
- Existing companies, apps, GitHub projects, packages, or creators using the same stem.
- Acronym overload.
- Adult, gambling, piracy, crypto-scam, malware, or spam associations.
- Common dictionary terms with overwhelming broad results.
- Trademark conflicts in the same or adjacent category.
- Autocorrect or "did you mean" behavior that fights the intended spelling.

## Traffic-Upside Heuristics

Estimate traffic potential from the market, not the empty domain:

- Category demand: Are people actively searching for the problem and alternatives?
- Intent quality: Are searches commercial, repeat-use, or urgent?
- Long-tail fit: Can the brand naturally own pages like `<brand> alternatives`, `<brand> vs X`, and `<job-to-be-done> guide`?
- Linkability: Would journalists, communities, or directories mention this name without confusion?
- Verbal spread: Can users say it in podcasts, videos, and chats without spelling friction?

## Trademark and Entity Diligence

Do fast checks before recommending a buy:

- Search exact stem plus `trademark`, `company`, `inc`, `app`, and the category.
- Check official trademark databases for serious launches: USPTO for the US, WIPO Global Brand Database for international marks, EUIPO for EU markets.
- Watch for phonetic similarity, plural/singular variants, and same-category products.

Flag risk; do not give legal advice.

## Evidence Log

Keep a short log for each finalist:

```text
Domain: example.ai
Checked: 2026-07-08
Searches: "example"; "example.ai"; site:example.ai; "example" "AI bookkeeping"; "example" trademark
Findings: no exact-brand company; category SERPs show active buyer intent; one unrelated dictionary meaning on page 1
Noise: medium
Action: shortlist
```

## Source Anchors

- Google search operators: https://support.google.com/websearch/answer/2466433
- Google SEO starter guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- USPTO trademark search: https://www.uspto.gov/trademarks/search
