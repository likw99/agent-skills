import os
import json
import feedparser
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base import BaseCollector


class SequoiaCollector(BaseCollector):
    """Collector for Sequoia Capital insights via RSS feed"""

    def __init__(self, cache_dir: Optional[str] = None):
        self.rss_url = "https://www.sequoiacap.com/rss"
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "sequoia")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.relevance_keywords = [
            "ai", "artificial intelligence", "machine learning", "deep learning",
            "llm", "generative ai", "foundation model", "gpt", "transformer",
            "fintech", "saas", "software", "platform", "cloud",
            "startup", "funding", "investment", "venture capital",
            "technology", "innovation", "developer", "open source",
        ]

    def collect_data(self, days_back=7, max_articles=15, use_cache=True, force_refresh=False, **kwargs):
        cache_file = os.path.join(self.cache_dir, f"sequoia_{days_back}d.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 12:
                    print("Using cached Sequoia data")
                    return cached_data
            except Exception:
                pass

        articles = self._fetch_rss(days_back)
        relevant = [a for a in articles if self._relevance_score(a) >= 3]
        relevant = sorted(relevant, key=lambda x: x.get("published", ""), reverse=True)[:max_articles]

        result = {
            "articles": relevant,
            "source": "Sequoia Capital",
            "article_count": len(relevant),
            "collection_time": datetime.now().isoformat(),
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return result

    def _fetch_rss(self, days_back):
        cutoff = datetime.now() - timedelta(days=days_back)
        try:
            feed = feedparser.parse(self.rss_url)
            articles = []
            for entry in feed.entries:
                pub_date = self._parse_date(entry)
                if pub_date and pub_date < cutoff:
                    continue
                summary = self._clean_html(entry.get("summary", ""))
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": summary,
                    "published": pub_date.isoformat() if pub_date else "",
                    "author": "Sequoia Capital",
                    "categories": [t.get("term", "") for t in entry.get("tags", [])],
                })
            return articles
        except Exception as e:
            print(f"Error fetching Sequoia RSS: {e}")
            return []

    def _parse_date(self, entry):
        for attr in ("published_parsed", "updated_parsed"):
            if hasattr(entry, attr) and getattr(entry, attr):
                return datetime.fromtimestamp(time.mktime(getattr(entry, attr)))
        return datetime.now()

    def _clean_html(self, text):
        if not text:
            return ""
        try:
            from bs4 import BeautifulSoup
            return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)
        except ImportError:
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()

    def _relevance_score(self, article):
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        matches = sum(1 for kw in self.relevance_keywords if kw in text)
        if matches >= 5:
            return 8
        if matches >= 3:
            return 6
        if matches >= 2:
            return 4
        if matches >= 1:
            return 3
        return 1

    def format_for_llm(self, data):
        articles = data.get("articles", [])
        output = "# SEQUOIA CAPITAL INSIGHTS\n\n"
        if not articles:
            return output + "No recent insights found.\n\n"
        for article in articles:
            output += f"### {article.get('title', '')}\n"
            output += f"Link: {article.get('link', '')}\n"
            output += f"Published: {article.get('published', '').split('T')[0]}\n\n"
            if article.get("summary"):
                output += f"{article['summary'][:500]}\n\n"
            output += "---\n\n"
        return output

    def get_statistics(self, data):
        return {"total_articles": len(data.get("articles", []))}
