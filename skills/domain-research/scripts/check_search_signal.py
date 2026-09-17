#!/usr/bin/env python3
"""
Fetch real Google results for a domain-name candidate. It fetches; it never judges.

Works from any terminal or agent (Codex, Cursor, CI). Backend: whichever key is
set, SerpApi first, or pick one with --provider.
  SERPAPI_KEY      serpapi.com: 250 free searches a month
  SERPER_API_KEY   serper.dev: 2,500 free queries once, then about $1 per 1,000

It prints what a reader needs: the results, how many of them mention the name,
any spelling fix Google applied (SerpApi reports one; Serper doesn't), and
People also ask plus related searches for category-demand research. Whether a
result is a competitor, a trademark or harmless noise is the agent's call; see
references/search-signal-playbook.md for the query matrix and how to read it.

Usage:
  python3 check_search_signal.py yourbrand                   # searches "yourbrand" as an exact phrase
  python3 check_search_signal.py yourbrand --pages 2         # 20 results, 2 searches
  python3 check_search_signal.py --query '"yourbrand" app'   # any query; mentions use the quoted phrase
  python3 check_search_signal.py --query 'site:yourbrand.com'
  python3 check_search_signal.py --query 'best ai bookkeeping software'
  python3 check_search_signal.py yourbrand --json

Google returns 10 results a page and has ignored `num` since September 2025,
so every page is one billed search.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence

sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
from _http import HttpError, request_json  # noqa: E402

PAGE_SIZE = 10
NO_RESULTS = "hasn't returned any results"  # SerpApi reports an empty page as an `error`
Summary = Dict[str, Any]


def _squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _texts(entries: Any, key: str) -> List[str]:
    return [str(e[key]) for e in entries or [] if isinstance(e, dict) and e.get(key)]


def _unique(values: Iterable[str]) -> List[str]:
    return list(dict.fromkeys(values))


def summarize(provider: str, data: Dict[str, Any], phrase: Optional[str]) -> Summary:
    """One results page from SerpApi or Serper as a provider-neutral summary."""
    if provider == "serpapi":
        info = data.get("search_information") or {}
        organic = data.get("organic_results") or []
        people_also_ask = _texts(data.get("related_questions"), "question")
        related = _texts(data.get("related_searches"), "query")
        error = data.get("error")
    else:
        info = {}
        organic = data.get("organic") or []
        people_also_ask = _texts(data.get("peopleAlsoAsk"), "question")
        related = _texts(data.get("relatedSearches"), "query")
        error = None

    results = [
        {
            "position": r.get("position"),
            "title": r.get("title") or "",
            "link": r.get("link") or r.get("url") or "",
            "snippet": r.get("snippet") or "",
        }
        for r in organic
        if isinstance(r, dict)
    ]
    key = _squash(phrase or "")
    mentions = (
        sum(1 for r in results if key in _squash(f"{r['title']} {r['snippet']} {r['link']}"))
        if key
        else None
    )
    return {
        "provider": provider,
        "results": results,
        "mentions": mentions,
        "total_results": info.get("total_results"),
        "spelling_fix": info.get("spelling_fix"),
        "showing_results_for": info.get("showing_results_for"),
        "organic_results_state": info.get("organic_results_state"),
        "people_also_ask": people_also_ask,
        "related_searches": related,
        "error": error,
    }


def merge(pages: List[Summary]) -> Summary:
    """Several pages as one summary; spelling and totals come from the first page."""
    merged = dict(pages[0])
    results = [dict(r) for page in pages for r in page["results"]]
    for rank, result in enumerate(results, start=1):
        result["position"] = rank
    merged["results"] = results
    if merged["mentions"] is not None:
        merged["mentions"] = sum(page["mentions"] or 0 for page in pages)
    merged["people_also_ask"] = _unique(q for page in pages for q in page["people_also_ask"])
    merged["related_searches"] = _unique(q for page in pages for q in page["related_searches"])
    return merged


def fetch_page(provider: str, query: str, page: int, key: str) -> Dict[str, Any]:
    if provider == "serpapi":
        params: Dict[str, Any] = {"engine": "google", "q": query, "api_key": key}
        if page > 1:
            params["start"] = (page - 1) * PAGE_SIZE
        return request_json("https://serpapi.com/search.json?" + urllib.parse.urlencode(params), timeout=45)
    body: Dict[str, Any] = {"q": query}
    if page > 1:
        body["page"] = page
    return request_json(
        "https://google.serper.dev/search", method="POST", headers={"X-API-KEY": key}, body=body, timeout=45
    )


def print_summary(s: Summary, phrase: Optional[str]) -> None:
    print(f"{s['query']} · {s['provider']} · {s['checked_at']}")
    count = len(s["results"])
    line = f"{count} result{'' if count == 1 else 's'}"
    if isinstance(s["total_results"], int):
        line += f" (Google estimates {s['total_results']:,})"
    if phrase and s["mentions"] is not None:
        line += f" · {s['mentions']} mention \"{phrase}\""
    print(line)

    if s["spelling_fix"] or s["showing_results_for"]:
        fixed = s["showing_results_for"] or s["spelling_fix"]
        state = s["organic_results_state"] or "state not reported"
        print(f"WARNING: Google applied a spelling fix: {fixed} ({state}). Results may not be about the name.")
    if count and phrase and s["mentions"] == 0:
        extra = " Serper doesn't report spelling fixes." if s["provider"] == "serper" else ""
        print(
            f"WARNING: no result mentions \"{phrase}\", so Google may have searched for something else."
            f"{extra} Confirm in a browser before calling the name clean."
        )
    if not count:
        print("No results. Promising, not proof: confirm in a browser or with the other provider.")

    for r in s["results"]:
        print(f"\n{r['position']}. {r['title']}\n   {r['link']}")
        if r["snippet"]:
            print(f"   {r['snippet']}")
    for heading, key in (("People also ask", "people_also_ask"), ("Related searches", "related_searches")):
        if s[key]:
            print(f"\n{heading}:")
            for text in s[key]:
                print(f"  - {text}")
    if count:
        print("\nRead these; this script does not judge them.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("phrase", nargs="?", help="candidate name, searched as an exact phrase")
    parser.add_argument("--query", help="send this query unchanged (site:, qualifiers, category terms)")
    parser.add_argument("--pages", type=int, default=1, help="pages to fetch: 10 results and one search each")
    parser.add_argument("--provider", choices=["serpapi", "serper"], help="default: whichever key is set, SerpApi first")
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = parser.parse_args(argv)

    if bool(args.phrase) == bool(args.query):
        parser.error("give either a candidate phrase or --query")
    query = args.query or f'"{args.phrase}"'
    quoted = re.search(r'"([^"]+)"', query)
    phrase = args.phrase or (quoted.group(1) if quoted else None)

    keys = {"serpapi": os.environ.get("SERPAPI_KEY"), "serper": os.environ.get("SERPER_API_KEY")}
    provider = args.provider or next((name for name, key in keys.items() if key), None)
    if provider is None or not keys[provider]:
        print(
            "Set SERPAPI_KEY or SERPER_API_KEY (see the docstring). Without one, read a real results "
            "page in a browser: references/search-signal-playbook.md.",
            file=sys.stderr,
        )
        return 2

    pages: List[Summary] = []
    try:
        for page in range(1, max(1, args.pages) + 1):
            summary = summarize(provider, fetch_page(provider, query, page, keys[provider] or ""), phrase)
            if summary["error"] and NO_RESULTS not in summary["error"]:
                print(f"{provider} error: {summary['error']}", file=sys.stderr)
                return 1
            pages.append(summary)
            if not summary["results"]:
                break
    except HttpError as exc:
        print(exc, file=sys.stderr)
        return 1

    result = merge(pages)
    result["query"] = query
    result["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_summary(result, phrase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
