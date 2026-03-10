import os
import json
import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set

from .base import BaseCollector


class ArXivCollector(BaseCollector):
    """Collector for arXiv research papers related to LLMs"""

    def __init__(self, cache_dir: Optional[str] = None):
        self.base_url = "http://export.arxiv.org/api/query"
        self.namespace = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "arxiv")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.domain_queries = {
            "transformers": 'abs:"transformer architecture" AND (abs:"large language model" OR abs:LLM)',
            "reasoning": 'abs:reasoning AND (abs:"large language model" OR abs:LLM)',
            "multimodal": '(abs:"multimodal" OR abs:"multi-modal") AND (abs:"large language model" OR abs:LLM)',
            "fine-tuning": '(abs:"fine-tuning" OR abs:"finetuning") AND (abs:"large language model" OR abs:LLM)',
            "agents": 'abs:agent AND (abs:"large language model" OR abs:LLM) AND NOT abs:"software agent"',
            "reinforcement_learning": '(abs:"reinforcement learning" OR abs:RLHF) AND (abs:"large language model" OR abs:LLM)',
            "efficiency": '(abs:"efficient" OR abs:"quantization" OR abs:"pruning") AND (abs:"large language model" OR abs:LLM)',
            "evaluation": '(abs:"evaluation" OR abs:"benchmark") AND (abs:"large language model" OR abs:LLM)',
            "science": '(abs:"scientific" OR abs:"discovery") AND (abs:"large language model" OR abs:LLM)',
        }
        self.general_queries = [
            '(abs:"large language model" OR abs:LLM)',
            'abs:"foundation model"',
        ]

    def collect_data(self, days_back=7, max_results_per_query=15, use_cache=True, force_refresh=False, **kwargs):
        search_days_back = days_back * 2
        cache_file = os.path.join(self.cache_dir, f"papers_{days_back}d_{max_results_per_query}r.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 24:
                    print(f"Using cached arXiv data")
                    return cached_data
            except Exception:
                pass

        all_papers = []
        seen_ids: Set[str] = set()
        domain_counts = {}

        for query in self.general_queries:
            papers = self._execute_query(query, search_days_back, max_results_per_query, seen_ids)
            for p in papers:
                p["query_type"] = "general"
            all_papers.extend(papers)
            for p in papers:
                seen_ids.add(p["arxiv_id"])
            time.sleep(3)

        for domain, query in self.domain_queries.items():
            papers = self._execute_query(query, search_days_back, max_results_per_query, seen_ids)
            for p in papers:
                p["domain"] = domain
                p["query_type"] = "domain"
            domain_counts[domain] = len(papers)
            all_papers.extend(papers)
            for p in papers:
                seen_ids.add(p["arxiv_id"])
            time.sleep(3)

        print(f"Total unique papers collected: {len(all_papers)}")

        papers_by_domain: Dict[str, list] = {}
        for paper in all_papers:
            d = paper.get("domain", "general")
            papers_by_domain.setdefault(d, []).append(paper)

        category_counts: Dict[str, int] = {}
        for paper in all_papers:
            for cat in paper.get("categories", []):
                category_counts[cat] = category_counts.get(cat, 0) + 1

        now = datetime.now()
        last_week = sum(1 for p in all_papers if self._days_ago(p) <= 7)
        last_month = sum(1 for p in all_papers if 7 < self._days_ago(p) <= 30)

        result = {
            "papers": all_papers,
            "papers_by_domain": papers_by_domain,
            "domain_counts": domain_counts,
            "category_counts": category_counts,
            "total_papers": len(all_papers),
            "last_week_count": last_week,
            "last_month_count": last_month,
            "collection_time": datetime.now().isoformat(),
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(result, f, indent=2)
        except Exception:
            pass
        return result

    def _days_ago(self, paper):
        try:
            pub_date = datetime.strptime(paper["published"], "%Y-%m-%d")
            return (datetime.now() - pub_date).days
        except Exception:
            return 999

    def _execute_query(self, query, days_back, max_results, seen_ids):
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results * 2,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        headers = {"User-Agent": "LLMDaily/1.0 (AI Newsletter Skill)"}
        try:
            response = requests.get(self.base_url, params=params, headers=headers)
            if response.status_code != 200:
                return []
            return self._parse_response(response.text, seen_ids, days_back, max_results)
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def _parse_response(self, xml_response, seen_ids, days_back, max_results):
        papers = []
        try:
            root = ET.fromstring(xml_response)
            entries = root.findall(".//atom:entry", self.namespace)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            for entry in entries:
                arxiv_url = entry.find("atom:id", self.namespace).text
                arxiv_id = arxiv_url.split("/")[-1]
                if arxiv_id in seen_ids:
                    continue
                paper = self._parse_entry(entry)
                try:
                    pub = datetime.strptime(paper["published"], "%Y-%m-%d")
                    if pub < start_date:
                        continue
                except Exception:
                    pass
                papers.append(paper)
                if len(papers) >= max_results:
                    break
        except Exception as e:
            print(f"Error parsing XML: {e}")
        return papers

    def _parse_entry(self, entry):
        title = entry.find("atom:title", self.namespace).text.strip()
        summary = entry.find("atom:summary", self.namespace).text.strip()
        published = entry.find("atom:published", self.namespace).text
        updated = entry.find("atom:updated", self.namespace).text
        published_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        authors = [a.find("atom:name", self.namespace).text for a in entry.findall("atom:author", self.namespace)]
        arxiv_url = entry.find("atom:id", self.namespace).text
        arxiv_id = arxiv_url.split("/")[-1]
        pdf_url = None
        for link in entry.findall("atom:link", self.namespace):
            if link.get("title") == "pdf":
                pdf_url = link.get("href")
                break
        categories = [c.get("term") for c in entry.findall("arxiv:category", self.namespace)]
        primary_cat = entry.find("arxiv:primary_category", self.namespace)

        return {
            "title": title,
            "authors": authors,
            "summary": summary,
            "published": published_date,
            "updated": datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d"),
            "arxiv_id": arxiv_id,
            "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": pdf_url,
            "categories": categories,
            "primary_category": primary_cat.get("term") if primary_cat is not None else None,
        }

    def format_for_llm(self, data):
        papers = data.get("papers", [])
        papers_by_domain = data.get("papers_by_domain", {})
        output = "# ARXIV RESEARCH DATA\n\n"
        if not papers:
            return output + "No relevant papers found.\n\n"

        output += f"## Overview\nTotal papers: {len(papers)}\n"
        output += f"Papers published in the last week: {data.get('last_week_count', 0)}\n\n"

        for domain, domain_papers in papers_by_domain.items():
            if not domain_papers:
                continue
            domain_title = "General LLM Research" if domain == "general" else domain.replace("_", " ").title()
            output += f"## {domain_title} ({len(domain_papers)} papers)\n\n"
            sorted_papers = sorted(domain_papers, key=lambda x: x.get("published", ""), reverse=True)
            for i, paper in enumerate(sorted_papers[:10], 1):
                output += f"### Paper {i}: {paper['title']}\n"
                output += f"Authors: {', '.join(paper['authors'])}\n"
                output += f"Published: {paper['published']}\n"
                output += f"arXiv: [{paper['arxiv_id']}]({paper['arxiv_url']})\n\n"
                summary = paper["summary"][:500] + "... [truncated]" if len(paper["summary"]) > 500 else paper["summary"]
                output += f"Abstract:\n{summary}\n\n---\n\n"
        return output

    def get_statistics(self, data):
        papers = data.get("papers", [])
        return {
            "total_papers": len(papers),
            "last_week_count": data.get("last_week_count", 0),
            "last_month_count": data.get("last_month_count", 0),
        }
