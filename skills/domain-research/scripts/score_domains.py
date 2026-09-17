#!/usr/bin/env python3
"""
Score domain candidates that have already been researched.

Input is JSON: a list of objects, or an object with a "domains" (or
"candidates") list, so `check_domains.py --json` output works as-is once the
agent's judgments are merged in. Per domain:

  judgments, 0-10 (default 5)  business_fit, traffic_intent, brand_quality,
                               search_signal (or search_noise),
                               risk_defensibility (or risk / trademark_risk)
  availability evidence        status from check_domains.py, a raw Cloudflare
                               result (registrable, reason, tier, pricing), or
                               the older availability / can_register / premium
  price, USD a year            registration_cost and renewal_cost, or price_usd.
                               The higher one counts: it is what keeping the
                               domain costs.

Only a registrar-confirmed "available" can earn Buy now or Strong shortlist;
unverified, RDAP-only, premium and unsupported domains top out at Watch. An
explicit availability_economics score overrides the inferred one, not that cap.

It checks nothing itself: no availability, search, DNS or trademark lookups.

Usage:
  python3 score_domains.py candidates.json --markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

WEIGHTS = {
    "business_fit": 20,
    "traffic_intent": 20,
    "search_signal": 20,
    "brand_quality": 15,
    "availability_economics": 15,
    "risk_defensibility": 10,
}

# Base availability score, 0-10, before the price adjustment.
AVAILABILITY_BASE = {
    "available": 9,
    "premium": 5,
    "unregistered": 4,  # RDAP: no registration record, but no registrar's yes and no price
    "unknown": 3,
    "unverified": 3,
    "unsupported": 3,
    "frozen": 0,
    "taken": 0,
}
TAKEN_WORDS = {"taken", "unavailable", "registered", "domain_unavailable"}
AVAILABLE_WORDS = {"available", "can_register", "registerable"}
STATUS_BY_REASON = {
    "domain_unavailable": "taken",
    "domain_premium": "premium",
    "extension_not_supported_via_api": "unknown",
    "extension_not_supported": "unsupported",
    "extension_disallows_registration": "frozen",
}

Item = Dict[str, Any]


def clamp(value: Any, minimum: float = 0, maximum: float = 10) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return minimum
    return max(minimum, min(maximum, number))


def _number(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_present(*values: Any) -> Any:
    return next((value for value in values if value not in (None, "")), None)


def normalize_component(value: Any, weight: int) -> float:
    return clamp(value) / 10.0 * weight


def availability_status(item: Item) -> str:
    """One status word from whichever availability evidence the item carries."""
    raw = str(item.get("status") or item.get("availability") or "").strip().lower()
    if raw in TAKEN_WORDS:
        return "taken"
    if raw in AVAILABLE_WORDS:
        return "premium" if item.get("premium") else "available"
    if raw:
        return raw
    if item.get("can_register") is False:
        return "taken"
    registrable = item.get("registrable", item.get("can_register"))
    if registrable is True:
        return "premium" if item.get("premium") or item.get("tier") == "premium" else "available"
    if registrable is False:
        return STATUS_BY_REASON.get(str(item.get("reason")), "unknown")
    return "premium" if item.get("premium") else "unknown"


def yearly_price_usd(item: Item) -> Optional[float]:
    """The higher of first-year and renewal price, in USD; None if unknown or another currency."""
    pricing = item.get("pricing") or {}
    currency = str(item.get("currency") or pricing.get("currency") or "USD").upper()
    if currency != "USD":
        return None
    candidates = [
        item.get("registration_cost"),
        item.get("renewal_cost"),
        pricing.get("registration_cost"),
        pricing.get("renewal_cost"),
        item.get("price_usd"),
        item.get("registration_price_usd"),
        item.get("renewal_price_usd"),
    ]
    prices = [price for price in map(_number, candidates) if price is not None]
    return max(prices) if prices else None


def infer_availability_score(item: Item) -> float:
    base = AVAILABILITY_BASE.get(availability_status(item), 3)
    if base == 0:
        return 0
    if item.get("tld_supported") is False:
        base = min(base, 4)

    price = yearly_price_usd(item)
    if price is not None:
        if price <= 25:
            base += 1
        elif price <= 80:
            base -= 1
        elif price <= 250:
            base -= 3
        else:
            base -= 5

    return clamp(base)


def infer_search_signal_score(item: Item) -> float:
    if "search_signal" in item:
        return clamp(item["search_signal"])
    noise = item.get("search_noise", item.get("noise"))
    if noise is None:
        return 5
    return 10 - clamp(noise)


def infer_risk_score(item: Item) -> float:
    if "risk_defensibility" in item:
        return clamp(item["risk_defensibility"])
    risk = item.get("risk", item.get("trademark_risk"))
    if risk is None:
        return 6
    return 10 - clamp(risk)


def component_scores(item: Item) -> Dict[str, float]:
    return {
        "business_fit": clamp(item.get("business_fit", 5)),
        "traffic_intent": clamp(item.get("traffic_intent", 5)),
        "search_signal": infer_search_signal_score(item),
        "brand_quality": clamp(item.get("brand_quality", 5)),
        "availability_economics": clamp(
            item.get("availability_economics", infer_availability_score(item))
        ),
        "risk_defensibility": infer_risk_score(item),
    }


def recommendation(total: float, item: Item) -> str:
    status = availability_status(item)
    if status in ("taken", "frozen"):
        return "Avoid"
    if clamp(item.get("risk", item.get("trademark_risk", 0))) >= 8:
        return "Avoid"
    if total < 55:
        return "Avoid"
    if status != "available":
        return "Watch"  # the evidence is unresolved: unverified, RDAP-only, premium or not sold here
    if total >= 80:
        return "Buy now"
    if total >= 70:
        return "Strong shortlist"
    return "Watch"


def score_item(item: Item) -> Item:
    scores = component_scores(item)
    weighted = {
        key: round(normalize_component(scores[key], weight), 2)
        for key, weight in WEIGHTS.items()
    }
    total = round(sum(weighted.values()), 2)
    result = dict(item)
    result["domain"] = item.get("domain") or item.get("name") or ""
    result["availability_status"] = availability_status(item)
    result["component_scores_0_to_10"] = scores
    result["weighted_scores"] = weighted
    result["score"] = total
    result["recommendation"] = recommendation(total, item)
    return result


def load_items(path: Path) -> List[Item]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("domains", data.get("candidates", []))
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON list or an object with domains/candidates.")
    return [item for item in data if isinstance(item, dict)]


def _price_cell(item: Item) -> str:
    pricing = item.get("pricing") or {}
    first = _first_present(
        item.get("registration_cost"),
        pricing.get("registration_cost"),
        item.get("price_usd"),
        item.get("registration_price_usd"),
    )
    renewal = _first_present(item.get("renewal_cost"), pricing.get("renewal_cost"), item.get("renewal_price_usd"))
    if first is None:
        return "" if renewal is None else f"? / {renewal}"
    if renewal is None or _number(renewal) == _number(first):
        return str(first)
    return f"{first} / {renewal}"


def markdown_table(items: List[Item]) -> str:
    lines = [
        "| Rank | Domain | Score | Recommendation | Status | Price/yr (first / renewal) | Notes |",
        "|---:|---|---:|---|---|---:|---|",
    ]
    for index, item in enumerate(items, start=1):
        notes = str(_first_present(item.get("notes"), item.get("why"), item.get("note")) or "")
        notes = notes.replace("|", "\\|")
        lines.append(
            f"| {index} | {item['domain']} | {item['score']} | {item['recommendation']} | "
            f"{item['availability_status']} | {_price_cell(item)} | {notes} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", type=Path, help="JSON file of researched candidates")
    parser.add_argument("--markdown", action="store_true", help="Emit a markdown table")
    args = parser.parse_args()

    try:
        items = load_items(args.input)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    scored = sorted((score_item(item) for item in items), key=lambda x: x["score"], reverse=True)
    if args.markdown:
        print(markdown_table(scored))
    else:
        print(json.dumps({"domains": scored}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
