# Cloudflare Registrar, MCP and RDAP Checks

Use this reference before checking availability or price, and for Cloudflare Radar traffic context. Verified against Cloudflare's API reference and live calls on 2026-09-17; trust the live docs if they disagree.

## Contents

- [Pick a path](#pick-a-path)
- [The domain-check endpoint](#the-domain-check-endpoint)
- [Reading results](#reading-results)
- [Token and account safety](#token-and-account-safety)
- [Through the Cloudflare MCP](#through-the-cloudflare-mcp)
- [Without Cloudflare: RDAP and other soft evidence](#without-cloudflare-rdap-and-other-soft-evidence)
- [Radar traffic context](#radar-traffic-context)

## Pick a path

1. **`scripts/check_domains.py`**, when `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set. It batches, classifies every result and timestamps it, and works in any agent or terminal.
2. **A connected Cloudflare API MCP** (`https://mcp.cloudflare.com/mcp`), when there is no token. It calls the same endpoint through its `execute` tool.
3. **`scripts/check_domains.py --rdap`**, when neither is available. It is free and soft; see the RDAP section.

## The domain-check endpoint

`POST /accounts/{account_id}/registrar/domain-check` with body `{"domains": ["a.com", "b.ai"]}`:

- It is read-only. It queries the registry in real time and reserves nothing.
- It takes 1–20 fully qualified names per request; a 21st returns error `1007`. Internationalized names go in punycode.
- It may silently omit malformed names; the script reports those as `unknown`.
- Each result has `name`, `registrable`, usually `tier` (`standard` or `premium`), `reason` when not registrable, and `pricing` only when registrable: `{currency, registration_cost, renewal_cost}`. Prices are per-year strings.

Related read-only endpoints:
- `GET .../registrar/domain-search?q=...` suggests names from a keyword. The results are cached and not authoritative, so confirm them with domain-check.
- `GET .../registrar/extensions` lists the TLDs the API can register (cursor pagination, at most 50 per page); on 2026-09-17 it listed 423, including `com`, `ai`, `io`, `app`, `dev` and `co`.

## Reading results

| `registrable` / `reason` | Status | What it means |
|---|---|---|
| `true` | `available` | A registrar's yes, priced. The only status that can earn Buy now |
| `true` with `tier: premium`, or `domain_premium` | `premium` | Registry-set price; the API won't register it. Price it in the dashboard, then judge it against the budget |
| `domain_unavailable` | `taken` | Registered, reserved or otherwise blocked |
| `extension_not_supported_via_api` | `unknown` | Cloudflare sells the TLD in its dashboard only. Check availability there. **It does not mean taken** |
| `extension_not_supported` | `unsupported` | Cloudflare doesn't sell the TLD. Check another registrar |
| `extension_disallows_registration` | `frozen` | The registry accepts no new registrations anywhere |
| anything else, or no reason | `unknown` | Unresolved |

Price notes:
- **Judge by renewal.** `registration_cost` covers only the first year. In the 2026-09-17 check, `.io` cost $32 to register and $50 a year to renew, and `.org` $8.50 then $11.20.
- **`.ai` has a two-year minimum,** so the first purchase costs twice the yearly price.
- Never quote a remembered price; every recommendation carries a price checked in this session.

## Token and account safety

Registration is a separate endpoint, `POST .../registrar/registrations`, and it is **billable and non-refundable**: it charges the account's default payment method.

- Create an account-owned token under **Manage account → API tokens** with the Registrar Domains permission. In August 2026 the token screen offered only an Admin level for it ([cloudflare-docs#32939](https://github.com/cloudflare/cloudflare-docs/issues/32939)), so assume the token can also buy domains. Use a read-only level if the screen offers one.
- Give the token a short expiry. Keep it in the shell environment or an untracked `.env.local`, never in a repo, and never in CI.
- A Cloudflare MCP session carries whatever access its sign-in granted.
- Whichever path you use, call only `domain-check`, `domain-search`, `extensions` and Radar `GET`s. Never call `registrations`, and never change DNS.

## Through the Cloudflare MCP

Tool names vary by client. Search the available tools for `cloudflare`, `registrar` and `domain`. The API server exposes `search` (find endpoints in the OpenAPI spec) and `execute` (run a JavaScript call with `cloudflare.request()` and a preset `accountId`):

```js
async () => {
  const domains = ["yourbrand.com", "yourbrand.ai"] // at most 20 per call
  const res = await cloudflare.request({
    method: "POST",
    path: `/accounts/${accountId}/registrar/domain-check`,
    body: { domains },
  })
  return res.result.domains
}
```

Map each result with the table above, and record the source (`cloudflare-mcp`) and a timestamp. If no Cloudflare tool is connected and no token is set, ask the human to connect one, or continue with RDAP and label every result unverified.

## Without Cloudflare: RDAP and other soft evidence

`scripts/check_domains.py --rdap` asks each TLD's registry, found through IANA's bootstrap file (`https://data.iana.org/rdap/dns.json`), whether a registration record exists:

- A `404` means **unregistered**, not available: premium, reserved and blocked names look the same, and there is no price.
- A `200` means taken.
- A TLD with no RDAP service is **unknown**. On 2026-09-16 the bootstrap covered `com`, `net`, `org`, `ai`, `app`, `dev` and `xyz`, but not `io`, `co`, `sh`, `me` or `us`. The shortcut `rdap.org` answers `404` for those TLDs even for registered names, so never read its 404 as free.
- Registries rate-limit, so expect about one domain a second.

Other soft evidence: DNS records (A, AAAA, CNAME or NS) show that a domain is in use, not that it is free; `site:` searches show current or past use; a registrar's web page is a hint, not a verified result.

Anything not confirmed by a registrar stays `unregistered` or `unknown` in the report, and `score_domains.py` caps it at Watch.

## Radar traffic context

Radar uses the same MCP connection or token, with no extra setup:

- `GET /radar/ranking/domain/{domain}`: rank details for an existing domain, such as a competitor or an aftermarket listing.
- `GET /radar/ranking/top`: top or trending domains, filterable by category.
- `GET /radar/ranking/timeseries_groups`: rank history.
- `GET /radar/ranking/internet_services/{categories,top,timeseries_groups}`: the same, for named Internet-service categories.

Radar is coarse by design. It gives an exact rank only for the global top 100; everything else falls into buckets (top 200k, top 1M, …) based on DNS query volume, not pageviews. Use it to sanity-check a comparable domain, never to estimate traffic. An unregistered domain has no current traffic; its upside comes from category demand, memorability and search-intent fit (see `search-signal-playbook.md`).

## Source anchors

- Registrar API guide: https://developers.cloudflare.com/registrar/registrar-api/
- Registrar API reference: https://developers.cloudflare.com/api/resources/registrar/
- Cloudflare MCP servers: https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/
- Radar ranking API: https://developers.cloudflare.com/api/resources/radar/subresources/ranking/
- IANA RDAP bootstrap: https://data.iana.org/rdap/dns.json
