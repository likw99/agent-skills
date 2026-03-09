import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base import BaseCollector


class ProductHuntCollector(BaseCollector):
    """Collector for AI products on Product Hunt"""

    def __init__(self, api_token: Optional[str] = None, cache_dir: Optional[str] = None):
        self.token = api_token or os.environ.get("PRODUCTHUNT_API_TOKEN")
        self.api_url = "https://api.producthunt.com/v2/api/graphql"
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "producthunt")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.ai_keywords = [
            "ai", "artificial intelligence", "machine learning", "deep learning",
            "llm", "language model", "generative", "gpt", "chatgpt",
            "diffusion", "openai", "claude", "anthropic", "gemini", "mistral",
            "rag", "text to image", "text to video", "image generation",
        ]

    def collect_data(self, days_back=7, posts_limit=50, use_cache=True, force_refresh=False, **kwargs):
        cache_file = os.path.join(self.cache_dir, f"ph_posts_{days_back}d.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 24:
                    print("Using cached Product Hunt data")
                    return cached_data
            except Exception:
                pass

        posts = self._fetch_posts(days_back, posts_limit)
        ai_products = self._filter_ai(posts)

        result = {
            "products": ai_products,
            "total_posts": len(posts),
            "ai_products_count": len(ai_products),
            "collection_time": datetime.now().isoformat(),
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(result, f, indent=2)
        except Exception:
            pass
        return result

    def _fetch_posts(self, days_back, limit):
        if not self.token:
            print("No Product Hunt API token. Skipping.")
            return []
        try:
            import subprocess, tempfile
            query = '{"query": "query { posts(first: ' + str(limit) + ') { edges { node { id name tagline description url votesCount commentsCount website topics { edges { node { name } } } featuredAt createdAt } } } }"}'
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
                tmp_path = tmp.name
            subprocess.run([
                "curl", "-s", "-X", "POST",
                "-H", f"Authorization: Bearer {self.token}",
                "-H", "Content-Type: application/json",
                "-H", "Accept: application/json",
                "-d", query, self.api_url, "-o", tmp_path,
            ], check=True)
            with open(tmp_path, "r") as f:
                data = json.load(f)
            os.unlink(tmp_path)

            posts = []
            for edge in data.get("data", {}).get("posts", {}).get("edges", []):
                node = edge.get("node", {})
                topics = []
                try:
                    for te in node.get("topics", {}).get("edges", []):
                        topics.append(te.get("node", {}).get("name", ""))
                except Exception:
                    pass
                posts.append({
                    "name": node.get("name", ""),
                    "tagline": node.get("tagline", ""),
                    "description": node.get("description", ""),
                    "url": node.get("url", ""),
                    "votes_count": node.get("votesCount", 0),
                    "website": node.get("website", ""),
                    "topics": topics,
                    "featured_at": node.get("featuredAt", ""),
                })
            return posts
        except Exception as e:
            print(f"Error fetching Product Hunt: {e}")
            return []

    def _filter_ai(self, posts):
        result = []
        for post in posts:
            text = f"{post.get('name', '')} {post.get('tagline', '')} {post.get('description', '')} {' '.join(post.get('topics', []))}".lower()
            if any(kw in text for kw in self.ai_keywords):
                result.append(post)
        return result

    def format_for_llm(self, data):
        products = data.get("products", [])
        output = "# PRODUCT HUNT AI PRODUCTS\n\n"
        if not products:
            return output + "No AI products found.\n\n"
        for i, p in enumerate(sorted(products, key=lambda x: x.get("votes_count", 0), reverse=True), 1):
            output += f"## Product {i}: {p.get('name', '')}\n\n"
            if p.get("tagline"):
                output += f"**Tagline**: {p['tagline']}\n"
            output += f"**URL**: {p.get('url', '')}\n"
            output += f"**Votes**: {p.get('votes_count', 0)}\n"
            if p.get("topics"):
                output += f"**Topics**: {', '.join(p['topics'])}\n"
            if p.get("description"):
                output += f"\n{p['description'][:500]}\n"
            output += "\n---\n\n"
        return output

    def get_statistics(self, data):
        return {"total_products": len(data.get("products", []))}
