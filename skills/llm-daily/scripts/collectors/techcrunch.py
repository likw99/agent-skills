import os
import json
import feedparser
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base import BaseCollector


class TechCrunchCollector(BaseCollector):
    """Collector for AI news from TechCrunch RSS feed"""

    def __init__(self, cache_dir: Optional[str] = None):
        self.rss_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "techcrunch")
        os.makedirs(self.cache_dir, exist_ok=True)

    def collect_data(self, days_back=7, max_articles=25, use_cache=True, force_refresh=False, **kwargs):
        cache_file = os.path.join(self.cache_dir, f"techcrunch_{days_back}d.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 12:
                    print("Using cached TechCrunch data")
                    return cached_data
            except Exception:
                pass

        articles = self._fetch_rss(days_back)[:max_articles]
        result = {
            "articles": articles,
            "source": "TechCrunch",
            "article_count": len(articles),
            "collection_time": datetime.now().isoformat(),
        }

        with open(cache_file, "w") as f:
            json.dump(result, f, indent=2)
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
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": self._clean_html(entry.get("summary", "")),
                    "published": pub_date.isoformat() if pub_date else "",
                    "authors": self._extract_authors(entry),
                    "categories": [t.get("term", "") for t in entry.get("tags", [])],
                })
            return sorted(articles, key=lambda x: x.get("published", ""), reverse=True)
        except Exception as e:
            print(f"Error fetching TechCrunch RSS: {e}")
            return []

    def _parse_date(self, entry):
        for attr in ("published_parsed", "updated_parsed"):
            if hasattr(entry, attr) and getattr(entry, attr):
                return datetime.fromtimestamp(time.mktime(getattr(entry, attr)))
        return datetime.now()

    def _extract_authors(self, entry):
        if hasattr(entry, "authors"):
            return [a.get("name", "") for a in entry.authors]
        if hasattr(entry, "author"):
            return [entry.author]
        return []

    def _clean_html(self, text):
        return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", text)).strip()

    def format_for_llm(self, data):
        articles = data.get("articles", [])
        output = "# TECHCRUNCH AI NEWS\n\n"
        if not articles:
            return output + "No recent articles found.\n\n"
        for article in articles:
            output += f"### {article.get('title', '')}\n"
            if article.get("authors"):
                output += f"By: {', '.join(article['authors'])}\n"
            output += f"Link: {article.get('link', '')}\n"
            output += f"Published: {article.get('published', '').split('T')[0]}\n\n"
            if article.get("summary"):
                output += f"{article['summary'][:500]}\n\n"
            output += "---\n\n"
        return output

    def get_statistics(self, data):
        return {"total_articles": len(data.get("articles", []))}
