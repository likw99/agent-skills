import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from json import JSONEncoder

from .base import BaseCollector


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class HuggingFaceCollector(BaseCollector):
    """Collector for trending AI content on Hugging Face Hub"""

    def __init__(self, hf_token: Optional[str] = None, cache_dir: Optional[str] = None):
        self.token = hf_token or os.environ.get("HF_TOKEN")
        try:
            from huggingface_hub import HfApi
            self.api = HfApi(token=self.token)
            self.available = True
        except ImportError:
            print("huggingface_hub not installed. HuggingFace collector disabled.")
            self.available = False
            self.api = None

        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "huggingface")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.ai_keywords = [
            "llm", "large language model", "language model", "transformer",
            "gpt", "bert", "diffusion", "generative", "text-to-image",
            "text-generation", "chat", "instruct", "rag", "embedding",
            "fine-tuned", "mistral", "llama", "claude", "ai", "ml",
        ]

    def collect_data(self, days_back=14, model_limit=30, dataset_limit=15, space_limit=15,
                     use_cache=True, force_refresh=False, sort_option="trendingScore", **kwargs):
        if not self.available:
            return {"models": [], "datasets": [], "spaces": [], "collection_time": datetime.now().isoformat()}

        cache_file = os.path.join(self.cache_dir, f"hf_trending_{days_back}d_{sort_option}.json")

        if not force_refresh and use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cache_time = datetime.fromisoformat(cached_data.get("collection_time", "2000-01-01T00:00:00"))
                if (datetime.now() - cache_time).total_seconds() / 3600 < 24:
                    print("Using cached HuggingFace data")
                    return cached_data
            except Exception:
                pass

        cutoff_date = datetime.now() - timedelta(days=days_back)
        models = self._collect_models(cutoff_date, model_limit, sort_option)
        datasets = self._collect_datasets(cutoff_date, dataset_limit, sort_option)
        spaces = self._collect_spaces(cutoff_date, space_limit, sort_option)

        result = {
            "models": models, "datasets": datasets, "spaces": spaces,
            "sort_option": sort_option,
            "collection_time": datetime.now().isoformat(),
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(result, f, indent=2, cls=DateTimeEncoder)
        except Exception:
            pass
        return result

    def _collect_models(self, cutoff_date, limit, sort_option):
        try:
            try:
                items = list(self.api.list_models(limit=limit * 2, sort=sort_option, direction=-1, fetch_config=True))
            except ValueError:
                items = list(self.api.list_models(limit=limit * 2, sort="likes", direction=-1, fetch_config=True))

            models = []
            for m in items:
                data = {
                    "id": m.id, "name": m.id.split("/")[-1], "author": m.id.split("/")[0],
                    "likes": m.likes, "downloads": getattr(m, "downloads", None),
                    "tags": getattr(m, "tags", []),
                    "pipeline_tag": getattr(m, "pipeline_tag", None),
                    "last_modified": m.last_modified,
                    "url": f"https://huggingface.co/{m.id}",
                }
                if self._is_ai_related(data):
                    models.append(data)
                if len(models) >= limit:
                    break
            return models
        except Exception as e:
            print(f"Error collecting models: {e}")
            return []

    def _collect_datasets(self, cutoff_date, limit, sort_option):
        try:
            try:
                items = list(self.api.list_datasets(limit=limit * 2, sort=sort_option, direction=-1))
            except ValueError:
                items = list(self.api.list_datasets(limit=limit * 2, sort="likes", direction=-1))

            datasets = []
            for d in items:
                data = {
                    "id": d.id,
                    "name": d.id.split("/")[-1] if "/" in d.id else d.id,
                    "author": d.id.split("/")[0] if "/" in d.id else "unknown",
                    "likes": getattr(d, "likes", 0),
                    "tags": getattr(d, "tags", []),
                    "url": f"https://huggingface.co/datasets/{d.id}",
                }
                if self._is_ai_related(data):
                    datasets.append(data)
                if len(datasets) >= limit:
                    break
            return datasets
        except Exception as e:
            print(f"Error collecting datasets: {e}")
            return []

    def _collect_spaces(self, cutoff_date, limit, sort_option):
        try:
            try:
                items = list(self.api.list_spaces(limit=limit * 2, sort=sort_option, direction=-1))
            except ValueError:
                items = list(self.api.list_spaces(limit=limit * 2, sort="likes", direction=-1))

            spaces = []
            for s in items:
                data = {
                    "id": s.id, "name": s.id.split("/")[-1], "author": s.id.split("/")[0],
                    "likes": s.likes,
                    "tags": getattr(s, "tags", []),
                    "sdk": getattr(s, "sdk", None),
                    "last_modified": s.last_modified,
                    "url": f"https://huggingface.co/spaces/{s.id}",
                }
                if self._is_ai_related(data):
                    spaces.append(data)
                if len(spaces) >= limit:
                    break
            return spaces
        except Exception as e:
            print(f"Error collecting spaces: {e}")
            return []

    def _is_ai_related(self, item):
        text = f"{item.get('id', '')} {' '.join(str(t) for t in item.get('tags', []))}".lower()
        if item.get("pipeline_tag") in ["text-generation", "text2text-generation", "text-classification"]:
            return True
        return any(kw in text for kw in self.ai_keywords)

    def format_for_llm(self, data):
        models = data.get("models", [])
        datasets = data.get("datasets", [])
        spaces = data.get("spaces", [])
        output = "# HUGGING FACE HUB TRENDING CONTENT\n\n"

        output += "## Trending Models\n\n"
        for i, m in enumerate(models[:15], 1):
            output += f"### Model {i}: {m.get('id', '')}\n"
            output += f"**URL**: {m.get('url', '')}\n"
            output += f"**Likes**: {m.get('likes', 0)}\n"
            if m.get("downloads"):
                output += f"**Downloads**: {m['downloads']}\n"
            if m.get("tags"):
                output += f"**Tags**: {', '.join(m['tags'][:10])}\n"
            output += "\n---\n\n"

        output += "## Trending Datasets\n\n"
        for i, d in enumerate(datasets[:10], 1):
            output += f"### Dataset {i}: {d.get('id', '')}\n"
            output += f"**URL**: {d.get('url', '')}\n"
            output += f"**Likes**: {d.get('likes', 0)}\n\n---\n\n"

        output += "## Trending Spaces\n\n"
        for i, s in enumerate(spaces[:10], 1):
            output += f"### Space {i}: {s.get('id', '')}\n"
            output += f"**URL**: {s.get('url', '')}\n"
            output += f"**Likes**: {s.get('likes', 0)}\n"
            if s.get("sdk"):
                output += f"**SDK**: {s['sdk']}\n"
            output += "\n---\n\n"

        return output

    def get_statistics(self, data):
        return {
            "total_models": len(data.get("models", [])),
            "total_datasets": len(data.get("datasets", [])),
            "total_spaces": len(data.get("spaces", [])),
            "sort_option": data.get("sort_option", "trendingScore"),
        }
