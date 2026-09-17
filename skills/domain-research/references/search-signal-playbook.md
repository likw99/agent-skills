# Search Signal Playbook

Use this reference after availability filtering. It covers two questions: whether a name can win attention and search visibility without fighting noise, and whether anyone searches for the problem at all.

## Contents

- [Tools](#tools)
- [Query rules](#query-rules)
- [Query matrix](#query-matrix)
- [Reading the results](#reading-the-results)
- [Trademark and entity diligence](#trademark-and-entity-diligence)
- [Evidence log](#evidence-log)
- [Category demand](#category-demand)

## Tools

Read a real Google results page. A summarizing web-search tool is not enough: in testing, one reported "no results" for a name that a rendered results page showed ten pages of, including a live App Store app.

| Tier | Method | Cost | Caveat |
|---|---|---|---|
| 1 | A browser the agent drives (Claude in Chrome, a Playwright MCP, Cursor's browser): open `https://www.google.com/search?q=%22name%22` and read the page text | Free | 10 results a page. Google has ignored `num=` since September 2025, so add `&start=10` for page 2 |
| 2 | **SerpApi** through `scripts/check_search_signal.py` (`SERPAPI_KEY`) | 250 free searches a month, then about $25 per 1,000 | Reports Google's spelling fixes. Google sued SerpApi in December 2025; the core claims were dismissed in July 2026 and a narrower complaint was pending in September 2026, with service unaffected. Switch to Serper if that changes |
| 2 | **Serper.dev** through the same script (`SERPER_API_KEY`) | 2,500 free queries once, then about $1 per 1,000, less at volume | Doesn't report spelling fixes; rely on the script's mention count |
| 3 | Your own scraper hitting `google.com` | Free | Fragile and against Google's terms at any volume; a single verbatim-search parameter triggered a bot check in testing. Only for one occasional check with a human watching |
| Avoid | Google Custom Search JSON API | — | Closed to new customers; existing customers must move off it by January 1, 2027. Its suggested replacement, Vertex AI Search, searches only configured sites |

Every page is one billed search on tiers 2 and 3. The script's `--pages N` fetches N pages.

**Zero results are promising, not proof.** Before calling a name clean:
- Confirm Google searched for the name you asked about. The script warns when SerpApi reports a spelling fix, and when none of the results mention the name.
- Re-check with a second engine or with the browser method.

## Query rules

- **One candidate per query.** Never OR-combine candidates: their results interleave, and you can't tell which name collided.
- **Start with the bare exact phrase**, `"name"`, alone. Adding a qualifier such as `app`, `company` or the category narrows the page and can hide a collision in another category, so qualified queries come second, for context.
- **Quote the name** in every query that is about the name.

## Query matrix

For a candidate `example.ai` with stem `example` and category `AI bookkeeping`, search in this order, and record the engine and date:

1. `"example"`: exact-phrase collision. This query decides noise.
2. `"example.ai"` and `site:example.ai`: exact-domain history and prior use.
3. `"example" app`, `"example" software`, `"example" startup`, `"example" AI`: entity collisions.
4. `"example" "AI bookkeeping"`: category fit.
5. `"example" trademark`, `"example" company`, `"example" lawsuit`, `"example" scam`: risk context.
6. `"example" -<dominant unrelated meaning>`: whether the noise can be filtered out.
7. `best AI bookkeeping software`, `AI bookkeeping for freelancers` and other category-intent queries: demand (see Category demand).

With the script, run query 1 as `check_search_signal.py example`, and the rest as `check_search_signal.py --query '<query>'`. Result counts are rough hints; the top results matter more.

## Reading the results

High-signal names usually have:
- A clear link to the category, outcome or audience.
- Few or no dominant exact-phrase competitors.
- Category searches with active buyers, tools, tutorials, comparisons or recurring pain.
- Suggestions and related queries that match the job-to-be-done.
- A spelling people get right after hearing it once.
- Room to become the canonical entity for the phrase.

High-noise names usually have:
- Dominant unrelated meanings on the first page.
- Companies, apps, GitHub projects, packages or creators already using the stem.
- Acronym overload.
- Adult, gambling, piracy, crypto-scam, malware or spam associations.
- A common dictionary word with overwhelming broad results.
- Trademark conflicts in the same or an adjacent category.
- Autocorrect or "did you mean" behavior that fights the intended spelling.

Traffic upside comes from the market, not the empty domain:
- **Category demand:** are people searching for the problem and its alternatives?
- **Intent quality:** are the searches commercial, repeat-use or urgent?
- **Long-tail fit:** can the brand naturally own pages like `<brand> alternatives`, `<brand> vs X` and `<job-to-be-done> guide`?
- **Linkability:** would journalists, communities and directories mention it without confusion?
- **Verbal spread:** can people say it in podcasts, videos and chats without spelling it out?

## Trademark and entity diligence

Run these fast checks before recommending a buy:
- Search the stem with `trademark`, `company`, `inc`, `app` and the category.
- For serious launches, search the official databases: USPTO (US), the WIPO Global Brand Database (international) and EUIPO (EU).
- Watch for phonetic look-alikes, plural and singular variants, and same-category products.

Flag the risk; don't give legal advice.

## Evidence log

Keep a short log for each finalist:

```text
Domain: example.ai
Checked: 2026-07-08 · Serper (script) + browser
Searches: "example"; "example.ai"; site:example.ai; "example" "AI bookkeeping"; "example" trademark
Findings: no exact-brand company; category results show buyer intent; one unrelated dictionary meaning on page 1
Noise: medium
Action: shortlist
```

## Category demand

Everything above asks whether someone else already owns the name in search. **Category demand is a separate question:** does anyone search for the problem this product solves, whatever it is called? Report the two separately, as *Brand-name collision* and *Category demand*, and never score them together.

A newly coined name has no search volume by definition, so "traffic research on the domain name" is close to a category error. What can be researched is demand for the category.

**A keyword in the domain is not a traffic signal.** Since Google's 2012 exact-match-domain update, a keyword-rich domain earns no automatic ranking advantage. It was not a blanket penalty, but content quality and site-wide signals now outweigh the domain string. Don't score "the domain contains the keyword" as traffic intent; organic traffic comes from content and from the brand becoming a distinct, citable entity.

Methods, most direct first:

1. **People also ask and related searches.** Run category queries (matrix item 7), not the brand candidate, and copy these boxes verbatim; they are the phrases real users type. `check_search_signal.py --query '<category query>'` prints both.
2. **Google Trends** (`trends.google.com`, free, no account): relative interest between category framings over time and by region. It gives no absolute volume, but shows which framing is growing, which informs the copy whatever the name.
3. **Google Keyword Planner** (free with a Google Ads account; no spend needed, though ranges are coarser without it): approximate monthly volume and competition for category keywords. It sizes the category, not the name.
4. **NameBio** (`namebio.com`, free guest search of millions of past sales): market-value comparisons for keyword-rich domains being bought on the aftermarket (already registered, for sale). A coined name has none. A comparable price justifies a purchase price, never buying an expired domain for its links.
5. **Cloudflare Radar ranking.** See the Radar section of `cloudflare-mcp.md`. It sanity-checks how much traffic a close competitor already gets, and is too coarse to estimate an unlaunched name.

## Source anchors

- Google search operators: https://support.google.com/websearch/answer/2466433
- Google SEO starter guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Custom Search JSON API status: https://developers.google.com/custom-search/v1/overview
- `num=` removal, September 2025: https://locomotive.agency/blog/google-removes-num100-parameter-what-this-means-for-your-website/
- SerpApi pricing: https://serpapi.com/pricing · spelling fields: https://serpapi.com/spell-check
- Google v. SerpApi: https://www.courtlistener.com/docket/72059948/google-llc-v-serpapi-llc/
- Serper.dev: https://serper.dev/
- USPTO trademark search: https://www.uspto.gov/trademarks/search
- Google Trends: https://trends.google.com/
- NameBio: https://namebio.com/
- EMD update background: https://www.searchenginejournal.com/google-algorithm-history/emd-update/
