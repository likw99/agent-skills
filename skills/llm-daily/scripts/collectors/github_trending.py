import os
import json
import requests
import time
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

from .base import BaseCollector


class GitHubCollector(BaseCollector):
    """Collector for trending AI repositories on GitHub"""

    def __init__(self, github_token: Optional[str] = None, cache_dir: Optional[str] = None):
        self.token = github_token or os.environ.get("GITHUB_TOKEN")
        self.headers = {"User-Agent": "LLMDaily/1.0"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "github")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.target_languages = ["jupyter-notebook", "python", "typescript"]
        self.high_relevance_keywords = [
            "llm", "large language model", "gpt", "llama", "mistral", "claude", "gemini",
            "diffusion", "stable diffusion", "text-to-image",
            "transformer", "attention mechanism", "fine-tuning",
            "rag", "retrieval augmented", "vector database", "embeddings",
            "prompt engineering", "agent", "multimodal",
        ]
        self.medium_relevance_keywords = [
            "machine learning", "deep learning", "neural network",
            "artificial intelligence", "tensorflow", "pytorch",
            "hugging face", "langchain", "llamaindex",
            "embedding", "tokenizer", "inference", "openai", "anthropic",
            "chatbot", "text generation", "image generation",
        ]

    def collect_data(self, days_back=7, per_page=25, use_cache=True, force_refresh=False, **kwargs):
        cache_file = os.path.join(self.cache_dir, "ai_repos_trending.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 24:
                    print("Using cached GitHub data")
                    return cached_data
            except Exception:
                pass

        all_repos = []
        seen_ids: set = set()

        for language in self.target_languages:
            print(f"Scraping trending {language} repositories...")
            repos = self._scrape_trending_page(language)
            for repo in repos:
                name = repo.get("full_name")
                if name and name not in seen_ids:
                    seen_ids.add(name)
                    all_repos.append(repo)
            time.sleep(2)

        ai_repos = [r for r in all_repos if self._calculate_ai_relevance(r) >= 5]
        print(f"Filtered {len(ai_repos)} AI-related repos from {len(all_repos)} total")

        sorted_repos = sorted(ai_repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:per_page]

        # Enrich top repos
        max_enrich = min(15, len(sorted_repos))
        for repo in sorted_repos[:max_enrich]:
            owner, name = repo.get("owner", ""), repo.get("name", "")
            if owner and name:
                readme = self._get_readme(owner, name)
                if readme:
                    repo["readme_excerpt"] = readme[:1000]
                commits = self._get_recent_commits(owner, name)
                if commits:
                    repo["recent_commits"] = commits
                time.sleep(1)

        result = {
            "repositories": sorted_repos,
            "total_repos": len(all_repos),
            "collection_time": datetime.now().isoformat(),
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(result, f, indent=2)
        except Exception:
            pass
        return result

    def _scrape_trending_page(self, language):
        url = f"https://github.com/trending/{language}?since=daily"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return []
            soup = BeautifulSoup(response.content, "html.parser")
            repos = []
            for article in soup.select("article.Box-row"):
                try:
                    title_elem = article.select_one("h2 a")
                    if not title_elem:
                        continue
                    repo_path = title_elem["href"].strip().lstrip("/")
                    owner, name = repo_path.split("/")
                    desc_elem = article.select_one("p")
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    lang_elem = article.select_one("[itemprop='programmingLanguage']")
                    repo_language = lang_elem.get_text(strip=True) if lang_elem else None
                    stat_elems = article.select("a.Link--muted")
                    stars = int(stat_elems[0].get_text(strip=True).replace(",", "")) if len(stat_elems) > 0 and stat_elems[0].get_text(strip=True).replace(",", "").isdigit() else 0
                    forks = int(stat_elems[1].get_text(strip=True).replace(",", "")) if len(stat_elems) > 1 and stat_elems[1].get_text(strip=True).replace(",", "").isdigit() else 0

                    repos.append({
                        "owner": owner, "name": name, "full_name": f"{owner}/{name}",
                        "html_url": f"https://github.com/{owner}/{name}",
                        "description": description, "language": repo_language,
                        "stargazers_count": stars, "forks_count": forks,
                        "source": "trending_page",
                    })
                except Exception:
                    continue
            return repos
        except Exception as e:
            print(f"Error scraping trending page: {e}")
            return []

    def _calculate_ai_relevance(self, repo):
        score = 0
        name = repo.get("name", "").lower()
        desc = repo.get("description", "").lower()
        for kw in self.high_relevance_keywords:
            if kw in name:
                score += 10
            elif kw in desc:
                score += 5
        for kw in self.medium_relevance_keywords:
            if kw in name:
                score += 5
            elif kw in desc:
                score += 3
        return score

    def _get_readme(self, owner, repo_name):
        url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return base64.b64decode(resp.json().get("content", "")).decode("utf-8")
        except Exception:
            pass
        return None

    def _get_recent_commits(self, owner, repo_name, limit=3):
        url = f"https://api.github.com/repos/{owner}/{repo_name}/commits?per_page={limit}"
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return [
                    {
                        "sha": c.get("sha", "")[:7],
                        "message": c.get("commit", {}).get("message", "").split("\n")[0],
                        "date": c.get("commit", {}).get("author", {}).get("date", ""),
                    }
                    for c in resp.json()
                ]
        except Exception:
            pass
        return []

    def format_for_llm(self, data):
        repos = data.get("repositories", [])
        output = "# GITHUB TRENDING AI PROJECTS\n\n"
        if not repos:
            return output + "No trending AI repositories found.\n\n"

        for i, repo in enumerate(sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True), 1):
            output += f"## Project {i}: {repo.get('full_name', '')}\n\n"
            output += f"**URL**: {repo.get('html_url', '')}\n"
            if repo.get("description"):
                output += f"**Description**: {repo['description']}\n\n"
            output += f"**Language**: {repo.get('language') or 'N/A'}\n"
            output += f"**Stars**: {repo.get('stargazers_count', 0)}\n"
            output += f"**Forks**: {repo.get('forks_count', 0)}\n\n"
            if repo.get("readme_excerpt"):
                excerpt = repo["readme_excerpt"][:500]
                output += f"**README Excerpt**:\n{excerpt}\n\n"
            if repo.get("recent_commits"):
                output += "**Recent Commits**:\n"
                for c in repo["recent_commits"]:
                    output += f"- {c.get('date', '').split('T')[0]}: {c.get('message', '')}\n"
                output += "\n"
            output += "---\n\n"
        return output

    def get_statistics(self, data):
        repos = data.get("repositories", [])
        return {"total_repos": len(repos)}
