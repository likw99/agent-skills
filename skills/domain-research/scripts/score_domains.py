#!/usr/bin/env python3
"""
Score already-researched domain candidates.

Input is JSON: a list of objects or an object with a "domains" list.
Each domain may include either explicit component scores:
  business_fit, traffic_intent, search_signal, brand_quality,
  availability_economics, risk_defensibility

or shorthand evidence fields:
  availability, price_usd, premium, tld_supported, search_noise, risk

This script does not check availability, prices, search engines, DNS, or trademarks.
It only applies a deterministic rubric to evidence gathered by the agent.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WEIGHTS = {
    "business_fit": 20,
    "traffic_intent": 20,
    "search_signal": 20,
    "brand_quality": 15,
    "availability_economics": 15,
    "risk_defensibility": 10,
}


def clamp(value: Any, minimum: float = 0, maximum: float = 10) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return minimum
    return max(minimum, min(maximum, number))


def normalize_component(value: Any, weight: int) -> float:
    return clamp(value) / 10.0 * weight


def infer_availability_score(item: dict[str, Any]) -> float:
    raw = str(item.get("availability", "")).lower()
    can_register = item.get("can_register")
    premium = bool(item.get("premium", False))
    supported = item.get("tld_supported", True)
    price = item.get("price_usd", item.get("registration_price_usd"))

    if raw in {"unavailable", "taken", "registered"} or can_register is False:
        return 0
    if raw in {"unknown", "unverified", ""}:
        base = 3
    elif raw in {"premium"} or premium:
        base = 5
    elif raw in {"available", "can_register", "registerable"} or can_register is True:
        base = 9
    else:
        base = 5

    if supported is False:
        base = min(base, 4)

    try:
        price_float = float(price)
    except (TypeError, ValueError):
        price_float = None

    if price_float is not None:
        if price_float <= 25:
            base += 1
        elif price_float <= 80:
            base -= 1
        elif price_float <= 250:
            base -= 3
        else:
            base -= 5

    return clamp(base)


def infer_search_signal_score(item: dict[str, Any]) -> float:
    if "search_signal" in item:
        return clamp(item["search_signal"])
    noise = item.get("search_noise", item.get("noise"))
    if noise is None:
        return 5
    return 10 - clamp(noise)


def infer_risk_score(item: dict[str, Any]) -> float:
    if "risk_defensibility" in item:
        return clamp(item["risk_defensibility"])
    risk = item.get("risk", item.get("trademark_risk"))
    if risk is None:
        return 6
    return 10 - clamp(risk)


def component_scores(item: dict[str, Any]) -> dict[str, float]:
    scores = {
        "business_fit": clamp(item.get("business_fit", 5)),
        "traffic_intent": clamp(item.get("traffic_intent", 5)),
        "search_signal": infer_search_signal_score(item),
        "brand_quality": clamp(item.get("brand_quality", 5)),
        "availability_economics": clamp(
            item.get("availability_economics", infer_availability_score(item))
        ),
        "risk_defensibility": infer_risk_score(item),
    }
    return scores


def recommendation(total: float, item: dict[str, Any]) -> str:
    raw = str(item.get("availability", "")).lower()
    if raw in {"unavailable", "taken", "registered"} or item.get("can_register") is False:
        return "Avoid"
    if clamp(item.get("risk", item.get("trademark_risk", 0))) >= 8:
        return "Avoid"
    if total >= 80:
        return "Buy now"
    if total >= 70:
        return "Strong shortlist"
    if total >= 55:
        return "Watch"
    return "Avoid"


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    scores = component_scores(item)
    weighted = {
        key: round(normalize_component(scores[key], weight), 2)
        for key, weight in WEIGHTS.items()
    }
    total = round(sum(weighted.values()), 2)
    result = dict(item)
    result["component_scores_0_to_10"] = scores
    result["weighted_scores"] = weighted
    result["score"] = total
    result["recommendation"] = recommendation(total, item)
    return result


def load_items(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("domains", data.get("candidates", []))
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON list or an object with domains/candidates.")
    return [item for item in data if isinstance(item, dict)]


def markdown_table(items: list[dict[str, Any]]) -> str:
    lines = [
        "| Rank | Domain | Score | Recommendation | Availability | Price | Notes |",
        "|---:|---|---:|---|---|---:|---|",
    ]
    for index, item in enumerate(items, start=1):
        domain = item.get("domain", "")
        price = item.get("price_usd", item.get("registration_price_usd", ""))
        notes = str(item.get("notes", item.get("why", ""))).replace("|", "\\|")
        lines.append(
            f"| {index} | {domain} | {item['score']} | {item['recommendation']} | "
            f"{item.get('availability', '')} | {price} | {notes} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score researched domain candidates.")
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
