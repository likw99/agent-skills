# Cloudflare MCP and Registrar Checks

Use this reference when verifying availability, prices, ownership status, Cloudflare Radar traffic context, or Cloudflare API details.

## Tool Discovery

Cloudflare's API MCP server exposes Cloudflare API access through a `search` tool for endpoint discovery and an `execute` tool for API calls. Tool names vary by client, so discover them instead of hard-coding names:

1. Search available tools for `Cloudflare`, `cloudflare-api`, `MCP`, `registrar`, `domain`, and `radar`.
2. If a Cloudflare API MCP tool is present, search within it for `registrar domain search`, `domain check`, `domain availability`, `registrar domains`, and `radar ranking`.
3. If no Cloudflare MCP tool is connected, ask the user to connect it or proceed with a clearly labeled unverified fallback.

Cloudflare's current MCP docs list a remote Cloudflare API server at `https://mcp.cloudflare.com/mcp`, plus product-specific servers such as Radar for Internet traffic insights and URL scans. Prefer the API/Radar MCP surfaces when available; use web docs only to confirm endpoint names and payloads.

## Registrar Endpoints to Prefer

Use current Cloudflare API docs through MCP search before executing. The likely endpoint families are:

- `GET /accounts/{account_id}/registrar/domain-search` - search for registerable domain suggestions from a query/seed.
- `POST /accounts/{account_id}/registrar/domain-check` - check whether specific domains can be registered.
- `GET /accounts/{account_id}/registrar/domains` - list domains already managed by the account.
- `GET /accounts/{account_id}/registrar/domains/{domain_name}` - inspect a domain already in the account.

If endpoint names or payloads differ in live docs, trust the live docs.

## Data to Capture

For each checked domain, capture:

- `domain`
- `availability`: `available`, `unavailable`, `premium`, `unsupported`, `unknown`, or the exact API status.
- `can_register` or equivalent boolean when exposed.
- Registration price, renewal price, transfer price, currency, and term.
- Premium-domain flag and premium price, if exposed.
- TLD support status.
- Source endpoint/tool name.
- Timestamp and account context.

Do not assume a price if the API omits it. Some APIs expose availability separately from price, and premium domains can behave differently from ordinary registrations.

## Fallback When MCP Is Missing

Use fallback checks only as soft evidence:

- DNS lookup: existing A/AAAA/CNAME/NS records imply use, not ownership availability.
- RDAP/WHOIS: can show registration status but may be rate-limited or privacy-protected.
- Search engine `site:domain.tld` and exact-domain queries: can show historical/current use.
- Browser registrar pages: useful for manual hints, but avoid presenting them as Cloudflare-verified.

Mark fallback candidates as `availability: unknown` unless a reliable registrar/API confirms registerability.

## Radar and Traffic Context

Use Cloudflare Radar MCP/API for:

- Existing exact-match domains and competitors that already receive meaningful traffic.
- Trending domains in the category.
- Adjacent category leaders that indicate demand patterns.
- TLD/context checks when deciding whether a TLD looks credible for the target audience.

Do not infer that an unregistered domain has current traffic. Its traffic upside comes from category demand, brand memorability, backlinks/PR potential, and search intent fit.

## Safety Boundary

Never register, renew, transfer, buy, bid on, or change DNS for a domain without explicit user confirmation in the current conversation.

## Source Anchors

- Cloudflare MCP servers: https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/
- Cloudflare Registrar API: https://developers.cloudflare.com/api/resources/registrar/
- Cloudflare Radar ranking API: https://developers.cloudflare.com/api/resources/radar/subresources/ranking/
