#!/usr/bin/env python3
"""
Check whether candidate domains can be registered, and what they cost.

Two sources, standard library only:

  Cloudflare Registrar (default, authoritative): a real-time registry answer
  with first-year and renewal price. Needs CLOUDFLARE_API_TOKEN and
  CLOUDFLARE_ACCOUNT_ID. See references/cloudflare-mcp.md for the token, and
  for why it never goes into a repo.

  --rdap (free, soft): asks each TLD's registry whether a registration record
  exists. "unregistered" is not "available": premium, reserved and blocked
  names look the same, and there is no price. A TLD with no RDAP service
  (.io, .co, .sh, ...) comes back "unknown", never "unregistered".

Usage:
  python3 check_domains.py yourbrand.com yourbrand.ai
  python3 check_domains.py --file candidates.txt            # one per line, # comments ok
  python3 check_domains.py --file candidates.txt --json     # records score_domains.py reads
  python3 check_domains.py --rdap --file candidates.txt     # free first pass

Statuses: available, premium, unregistered (RDAP only), unknown, unsupported,
frozen, taken. Only "available" is a registrar's yes.

Read-only: it calls registrar/domain-check, which reserves nothing, and RDAP.
It never registers, renews, transfers or changes DNS.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
from _http import HttpError, request_json, status_of  # noqa: E402

API_BASE = "https://api.cloudflare.com/client/v4"
BATCH_SIZE = 20  # Cloudflare's hard cap per domain-check request
IANA_RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

STATUS_BY_REASON = {
    "domain_unavailable": "taken",
    "domain_premium": "premium",
    "extension_not_supported_via_api": "unknown",
    "extension_not_supported": "unsupported",
    "extension_disallows_registration": "frozen",
}
NOTE_BY_REASON = {
    "domain_premium": "registry premium price; the API won't register it — price it in the Cloudflare dashboard",
    "extension_not_supported_via_api": "Cloudflare sells this TLD in its dashboard only — check availability there",
    "extension_not_supported": "Cloudflare doesn't sell this TLD — check another registrar",
    "extension_disallows_registration": "the registry isn't accepting new registrations",
}
GROUPS = [
    ("available", "AVAILABLE"),
    ("unregistered", "UNREGISTERED — no registration record; not a registrar's yes, no price"),
    ("premium", "PREMIUM"),
    ("unknown", "UNKNOWN — verify elsewhere"),
    ("unsupported", "NOT SOLD BY CLOUDFLARE"),
    ("frozen", "REGISTRY FROZEN"),
    ("taken", "TAKEN"),
]
MISSING_CREDENTIALS = """\
Cloudflare credentials are not set, so nothing can be confirmed available.
  - Authoritative: export CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID
    (setup: references/cloudflare-mcp.md), or use a connected Cloudflare API MCP.
  - Free first pass: rerun with --rdap. It shows whether a registration record
    exists, without a price, and its "unregistered" is not a registrar's yes."""

_LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
Record = Dict[str, Any]


def _cost(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _record(domain: str, status: str, source: str, **fields: Any) -> Record:
    record: Record = {
        "domain": domain,
        "status": status,
        "reason": None,
        "tier": None,
        "currency": None,
        "registration_cost": None,
        "renewal_cost": None,
        "renewal_exceeds_registration": False,
        "note": None,
        "source": source,
    }
    record.update(fields)
    return record


def classify(result: Record) -> Record:
    """One Cloudflare domain-check result as a record. Not every `registrable: false` means taken."""
    reason = result.get("reason")
    pricing = result.get("pricing") or {}
    if result.get("registrable") is True:
        status = "premium" if result.get("tier") == "premium" else "available"
    else:
        status = STATUS_BY_REASON.get(reason or "", "unknown")

    if status == "premium":
        note = NOTE_BY_REASON["domain_premium"]
    elif reason in NOTE_BY_REASON:
        note = NOTE_BY_REASON[reason]
    elif status == "unknown":
        note = f"unrecognized reason: {reason}" if reason else "Cloudflare gave no reason"
    else:
        note = None

    first, renewal = pricing.get("registration_cost"), pricing.get("renewal_cost")
    first_cost, renewal_cost = _cost(first), _cost(renewal)
    return _record(
        result.get("name", ""),
        status,
        "cloudflare-registrar",
        reason=reason,
        tier=result.get("tier"),
        currency=pricing.get("currency"),
        registration_cost=first,
        renewal_cost=renewal,
        renewal_exceeds_registration=(
            first_cost is not None and renewal_cost is not None and renewal_cost > first_cost
        ),
        note=note,
    )


def normalize_domains(entries: Sequence[str]) -> Tuple[List[str], List[str]]:
    """Lowercase, strip scheme, path and `www.`, punycode, dedupe. Returns (valid, invalid)."""
    valid: List[str] = []
    invalid: List[str] = []
    for entry in entries:
        text = entry.strip()
        if not text or text.startswith("#"):
            continue
        name = re.sub(r"^[a-z][a-z0-9+.-]*://", "", text.lower())
        name = re.split(r"[/?#]", name, maxsplit=1)[0].split(":", 1)[0].rstrip(".")
        if name.startswith("www."):
            name = name[4:]
        try:
            name = name.encode("idna").decode("ascii")
        except UnicodeError:
            invalid.append(text)
            continue
        labels = name.split(".")
        if len(labels) < 2 or not all(_LABEL.match(label) for label in labels):
            invalid.append(text)
        elif name not in valid:
            valid.append(name)
    return valid, invalid


def rdap_server(services: Sequence[Sequence[Sequence[str]]], domain: str) -> Optional[str]:
    """The registry's RDAP base URL for the domain's TLD, from IANA's bootstrap `services`."""
    tld = domain.rsplit(".", 1)[-1]
    for tlds, urls in services:
        if tld in tlds and urls:
            return next((url for url in urls if url.startswith("https://")), urls[0])
    return None


def rdap_check(
    domain: str,
    services: Sequence[Sequence[Sequence[str]]],
    fetch_status: Callable[[str], Optional[int]],
) -> Record:
    """Soft availability from the TLD registry. A TLD with no RDAP server is "unknown", not free."""
    base = rdap_server(services, domain)
    if base is None:
        tld = domain.rsplit(".", 1)[-1]
        return _record(domain, "unknown", "rdap", note=f"no RDAP service for .{tld} — check a registrar")
    code = fetch_status(f"{base.rstrip('/')}/domain/{domain}")
    if code == 404:
        note = "no registration record — premium or reserved names look the same; confirm with a registrar"
        return _record(domain, "unregistered", "rdap", note=note)
    if code is not None and 200 <= code < 300:
        return _record(domain, "taken", "rdap")
    if code == 429:
        return _record(domain, "unknown", "rdap", note="RDAP rate limit — retry later")
    note = f"RDAP answered HTTP {code}" if code else "RDAP server unreachable"
    return _record(domain, "unknown", "rdap", note=note)


def cloudflare_check(domains: List[str], token: str, account_id: str) -> List[Record]:
    records: List[Record] = []
    for start in range(0, len(domains), BATCH_SIZE):
        batch = domains[start : start + BATCH_SIZE]
        data = request_json(
            f"{API_BASE}/accounts/{account_id}/registrar/domain-check",
            method="POST",
            headers={"Authorization": f"Bearer {token}"},
            body={"domains": batch},
        )
        if not data.get("success"):
            raise HttpError(f"Cloudflare API returned failure: {data.get('errors')}")
        returned = {r.get("name"): r for r in (data.get("result") or {}).get("domains", [])}
        for name in batch:
            if name in returned:
                records.append(classify(returned[name]))
            else:
                note = "missing from Cloudflare's response (malformed name?)"
                records.append(_record(name, "unknown", "cloudflare-registrar", note=note))
    return records


def _polite_rdap_status(url: str) -> Optional[int]:
    time.sleep(0.2)  # registry RDAP servers rate-limit bursts
    return status_of(url, accept="application/rdap+json")


def print_table(records: List[Record], source: str, checked_at: str) -> None:
    print(f"{source} · {checked_at} · {len(records)} checked")
    for status, heading in GROUPS:
        group = [r for r in records if r["status"] == status]
        if not group:
            continue
        print(f"\n{heading} ({len(group)})")
        for r in group:
            parts = []
            if r["registration_cost"] is not None:
                currency = r["currency"] or ""
                price = f"{currency} {r['registration_cost']} first year · {currency} {r['renewal_cost']}/yr renewal"
                if r["renewal_exceeds_registration"]:
                    price += " (renews higher)"
                parts.append(price)
            if r["note"]:
                parts.append(r["note"])
            print(f"  {r['domain']:<32} {' · '.join(parts)}".rstrip())


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("domains", nargs="*", help="domains to check")
    parser.add_argument("--file", help="file with one domain per line")
    parser.add_argument("--rdap", action="store_true", help="free soft check via registry RDAP: no credentials, no price")
    parser.add_argument("--json", action="store_true", help="print records as JSON (score_domains.py input)")
    args = parser.parse_args(argv)

    entries = list(args.domains)
    if args.file:
        try:
            entries += Path(args.file).read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            print(f"Can't read {args.file}: {exc}", file=sys.stderr)
            return 2
    domains, invalid = normalize_domains(entries)
    for text in invalid:
        print(f"skipping {text!r}: not a domain name", file=sys.stderr)
    if not domains:
        print("No domains to check — pass them as arguments or with --file.", file=sys.stderr)
        return 2

    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not args.rdap and not (token and account_id):
        print(MISSING_CREDENTIALS, file=sys.stderr)
        return 2

    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        if args.rdap:
            services = request_json(IANA_RDAP_BOOTSTRAP)["services"]
            records = [rdap_check(d, services, _polite_rdap_status) for d in domains]
        else:
            records = cloudflare_check(domains, token or "", account_id or "")
    except HttpError as exc:
        hint = ""
        if exc.status in (401, 403):
            hint = "\nCheck that the token is account-owned, unexpired, and has the Registrar Domains permission."
        print(f"{exc}{hint}", file=sys.stderr)
        return 1

    for record in records:
        record["checked_at"] = checked_at
    if args.json:
        print(json.dumps({"domains": records}, indent=2, ensure_ascii=False))
    else:
        source = "RDAP (soft — not a registrar check)" if args.rdap else "Cloudflare Registrar"
        print_table(records, source, checked_at)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
