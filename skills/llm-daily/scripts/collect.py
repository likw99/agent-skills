#!/usr/bin/env python3
"""
LLM Daily - Data Collection Pipeline

Collects data from multiple AI/ML news sources and outputs formatted markdown
for newsletter generation. This script is self-contained and does not depend
on any external repo.

Usage:
    python collect.py [options]
    python collect.py --skip-github --skip-producthunt
    python collect.py --force-refresh --arxiv-days 3

Output:
    - collected_data.json: Raw collected data
    - collected_data.md: Formatted markdown for LLM consumption
    - Individual source data in cache/ directory
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from collectors import (
    ArXivCollector,
    GitHubCollector,
    HuggingFaceCollector,
    VentureBeatCollector,
    TechCrunchCollector,
    ProductHuntCollector,
    SequoiaCollector,
)


def parse_args():
    parser = argparse.ArgumentParser(description="LLM Daily - Data Collection Pipeline")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory (default: ./output)")
    parser.add_argument("--force-refresh", action="store_true", help="Force refresh all caches")

    # Skip flags
    parser.add_argument("--skip-arxiv", action="store_true")
    parser.add_argument("--skip-github", action="store_true")
    parser.add_argument("--skip-huggingface", action="store_true")
    parser.add_argument("--skip-venturebeat", action="store_true")
    parser.add_argument("--skip-techcrunch", action="store_true")
    parser.add_argument("--skip-producthunt", action="store_true")
    parser.add_argument("--skip-sequoia", action="store_true")

    # Collection parameters
    parser.add_argument("--arxiv-days", type=int, default=7)
    parser.add_argument("--arxiv-results", type=int, default=50)
    parser.add_argument("--news-days", type=int, default=7)
    parser.add_argument("--huggingface-limit", type=int, default=30)
    parser.add_argument("--producthunt-limit", type=int, default=50)

    return parser.parse_args()


def collect_source(name, collector_class, run_kwargs, skip=False):
    """Collect data from a single source with error handling"""
    if skip:
        print(f"  Skipping {name}")
        return None, None

    print(f"  Collecting {name}...")
    try:
        collector = collector_class()
        formatted_data, raw_data = collector.run(**run_kwargs)
        stats = collector.get_statistics(raw_data)
        print(f"  Done: {name}")
        return formatted_data, stats
    except Exception as e:
        print(f"  Error collecting {name}: {e}")
        return None, None


def main():
    args = parse_args()
    start_time = datetime.now()

    # Set up output directory
    script_dir = Path(__file__).parent
    output_dir = Path(args.output_dir) if args.output_dir else script_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("LLM DAILY - Data Collection Pipeline")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Collect from all sources
    force = args.force_refresh
    sources = {}

    # ArXiv
    data, stats = collect_source("ArXiv", ArXivCollector, {
        "days_back": args.arxiv_days, "max_results_per_query": args.arxiv_results,
        "force_refresh": force,
    }, skip=args.skip_arxiv)
    if data:
        sources["arxiv"] = {"data": data, "stats": stats}

    # GitHub
    data, stats = collect_source("GitHub Trending", GitHubCollector, {
        "days_back": 30, "per_page": 50, "force_refresh": force,
    }, skip=args.skip_github)
    if data:
        sources["github"] = {"data": data, "stats": stats}

    # HuggingFace
    data, stats = collect_source("HuggingFace", HuggingFaceCollector, {
        "days_back": 14, "model_limit": args.huggingface_limit,
        "dataset_limit": args.huggingface_limit // 2,
        "space_limit": args.huggingface_limit // 2,
        "force_refresh": force,
    }, skip=args.skip_huggingface)
    if data:
        sources["huggingface"] = {"data": data, "stats": stats}

    # VentureBeat
    data, stats = collect_source("VentureBeat", VentureBeatCollector, {
        "days_back": args.news_days, "force_refresh": force,
    }, skip=args.skip_venturebeat)
    if data:
        sources["venturebeat"] = {"data": data, "stats": stats}

    # TechCrunch
    data, stats = collect_source("TechCrunch", TechCrunchCollector, {
        "days_back": args.news_days, "force_refresh": force,
    }, skip=args.skip_techcrunch)
    if data:
        sources["techcrunch"] = {"data": data, "stats": stats}

    # Product Hunt
    data, stats = collect_source("Product Hunt", ProductHuntCollector, {
        "days_back": args.news_days, "posts_limit": args.producthunt_limit,
        "force_refresh": force,
    }, skip=args.skip_producthunt)
    if data:
        sources["producthunt"] = {"data": data, "stats": stats}

    # Sequoia
    data, stats = collect_source("Sequoia Capital", SequoiaCollector, {
        "days_back": args.news_days, "force_refresh": force,
    }, skip=args.skip_sequoia)
    if data:
        sources["sequoia"] = {"data": data, "stats": stats}

    # Assemble output
    print("\n" + "=" * 60)
    print("Assembling collected data...")

    # Create combined markdown
    combined_md = f"# LLM DAILY - Collected Data\n"
    combined_md += f"**Collection Date**: {datetime.now().strftime('%B %d, %Y')}\n\n"

    # Stats summary
    combined_md += "## Collection Statistics\n\n"
    for source_name, source_data in sources.items():
        stats = source_data.get("stats", {})
        stat_items = []
        for k, v in stats.items():
            if isinstance(v, (int, float)) and not k.endswith("timestamp"):
                stat_items.append(f"{k}: {v}")
        combined_md += f"- **{source_name}**: {', '.join(stat_items)}\n"
    combined_md += "\n---\n\n"

    # Source data sections
    section_mapping = {
        "venturebeat": "BUSINESS",
        "techcrunch": "BUSINESS",
        "sequoia": "BUSINESS",
        "producthunt": "PRODUCTS",
        "github": "TECHNOLOGY",
        "huggingface": "TECHNOLOGY",
        "arxiv": "RESEARCH",
    }

    for section in ["BUSINESS", "PRODUCTS", "TECHNOLOGY", "RESEARCH"]:
        combined_md += f"# {section} SOURCE DATA\n\n"
        for source_name, source_data in sources.items():
            if section_mapping.get(source_name) == section:
                combined_md += source_data["data"] + "\n\n"
        combined_md += "---\n\n"

    # Save outputs
    md_path = output_dir / f"collected_data_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(combined_md)

    # Save JSON with stats
    json_path = output_dir / f"collected_stats_{datetime.now().strftime('%Y-%m-%d')}.json"
    stats_data = {
        source_name: source_data.get("stats", {})
        for source_name, source_data in sources.items()
    }
    with open(json_path, "w") as f:
        json.dump(stats_data, f, indent=2, default=str)

    end_time = datetime.now()
    runtime = (end_time - start_time).total_seconds()

    print(f"\nCollection complete!")
    print(f"  Sources collected: {len(sources)}")
    print(f"  Markdown output: {md_path}")
    print(f"  Stats JSON: {json_path}")
    print(f"  Runtime: {runtime:.1f}s")
    print("=" * 60)

    # Print the output path for the agent to pick up
    print(f"\nCOLLECTED_DATA_PATH={md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
