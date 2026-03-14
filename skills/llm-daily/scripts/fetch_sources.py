#!/usr/bin/env python3
import datetime
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit, urlunsplit

import feedparser
import requests
import yaml

DEFAULT_TIMEOUT_SECONDS = 30
ARXIV_MIN_REQUEST_INTERVAL_SECONDS = 3.0
_last_arxiv_request_at = None


def get_last_week_date():
    return (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

def get_default_headers():
    contact_email = os.environ.get("LLM_DAILY_CONTACT_EMAIL", "").strip()
    contact_part = f"; contact: {contact_email}" if contact_email else ""
    user_agent = (
        "LLM Daily/1.0"
        f" (AI newsletter research fetcher{contact_part}; source: likw99/newsx)"
    )
    return {"User-Agent": user_agent}

def split_url_and_params(url):
    parsed = urlsplit(url)
    params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    request_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", parsed.fragment))
    return request_url, params

def is_arxiv_api_request(url):
    parsed = urlsplit(url)
    return parsed.netloc.endswith("arxiv.org") and parsed.path.endswith("/api/query")

def normalize_arxiv_params(params, max_items):
    normalized = dict(params)
    sort_order = normalized.get("sortOrder")
    if sort_order:
        sort_order_aliases = {"asc": "ascending", "desc": "descending"}
        normalized["sortOrder"] = sort_order_aliases.get(sort_order.lower(), sort_order)
    normalized.setdefault("max_results", str(max_items))
    return normalized

def maybe_wait_for_arxiv_slot():
    global _last_arxiv_request_at
    now = time.monotonic()
    if _last_arxiv_request_at is not None:
        elapsed = now - _last_arxiv_request_at
        if elapsed < ARXIV_MIN_REQUEST_INTERVAL_SECONDS:
            wait_seconds = ARXIV_MIN_REQUEST_INTERVAL_SECONDS - elapsed
            print(f"Respecting ArXiv API pacing; waiting {wait_seconds:.1f}s before request...")
            time.sleep(wait_seconds)
    _last_arxiv_request_at = time.monotonic()

def extract_xml_feed_error(xml_content):
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return None

    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]

    entry = root.find(".//entry")
    if entry is None:
        return None

    title = (entry.findtext("title") or "").strip()
    summary = (entry.findtext("summary") or "").strip()
    if title.lower() == "error" and summary:
        return summary
    return None

def parse_rss(url, max_items=10):
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '')
            desc = entry.get('summary', entry.get('description', ''))
            # Clean up desc very basically (remove massive html if present)
            if len(desc) > 300:
                desc = desc[:300] + "..."
            items.append({"title": title, "link": link, "description": desc})
        return items
    except Exception as e:
        print(f"Error parsing RSS from {url}: {e}")
        return []

def parse_json_api(url, config, max_items=10):
    try:
        response = requests.get(url, headers=get_default_headers(), timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        
        list_path = config.get("list_path", "")
        if list_path:
            for key in list_path.split("."):
                if key and data is not None:
                    data = data.get(key)
        
        if not isinstance(data, list):
            print(f"JSON API {url} did not return a list at path '{list_path}'.")
            return []
            
        items = []
        for item in data[:max_items]:
            title = str(item.get(config.get("title_key", "title"), "No Title"))
            
            link_key = config.get("link_key")
            link = str(item.get(link_key, "")) if link_key else ""
            if config.get("link_prefix"):
                link = config.get("link_prefix") + link
                
            desc_key = config.get("description_key")
            desc = str(item.get(desc_key, "")) if desc_key else ""
            
            if len(desc) > 300:
                desc = desc[:300] + "..."
                
            items.append({"title": title, "link": link, "description": desc})
        return items
    except Exception as e:
        print(f"Error parsing JSON API from {url}: {e}")
        return []

def parse_xml_api(url, config, max_items=10, source_name="XML API"):
    try:
        request_url, params = split_url_and_params(url)
        parser_params = config.get("request_params", {})
        if parser_params:
            params.update({key: str(value) for key, value in parser_params.items()})

        is_arxiv = is_arxiv_api_request(request_url)
        if is_arxiv:
            params = normalize_arxiv_params(params, max_items)

        headers = get_default_headers()
        max_retries = 3 if is_arxiv else 1
        response = None
        for attempt in range(max_retries):
            if is_arxiv:
                maybe_wait_for_arxiv_slot()

            response = requests.get(
                request_url,
                params=params or None,
                headers=headers,
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

            feed_error = extract_xml_feed_error(response.content) if is_arxiv else None
            if response.status_code == 429 and is_arxiv:
                wait = int(response.headers.get("Retry-After", 2 ** (attempt + 2)))
                print(f"ArXiv rate limited (429). Waiting {wait}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait)
                continue
            if response.status_code >= 400:
                if feed_error:
                    raise ValueError(f"ArXiv API rejected the request: {feed_error}")
                response.raise_for_status()
            if feed_error:
                raise ValueError(f"ArXiv API returned an error feed: {feed_error}")
            response.raise_for_status()
            break
        else:
            print(f"Giving up on {request_url} after {max_retries} retries (429).")
            return []

        root = ET.fromstring(response.content)
        
        items = []
        # Strip namespaces for easier querying
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
                
        for entry in root.findall(f".//{config.get('item_tag', 'item')}")[:max_items]:
            title_elem = entry.find(config.get("title_tag", "title"))
            title = title_elem.text.strip().replace('\\n', ' ') if title_elem is not None else "No Title"
            
            link_elem = entry.find(config.get("link_tag", "link"))
            link = link_elem.text.strip() if link_elem is not None else ""
            # ArXiv sometimes uses <id> as link or multiple <link> tags
            if not link and config.get("link_tag") == "id":
                id_elem = entry.find("id")
                if id_elem is not None:
                    link = id_elem.text.strip()
                    
            desc_elem = entry.find(config.get("description_tag", "description"))
            desc = desc_elem.text.strip().replace('\\n', ' ') if desc_elem is not None else ""
            if len(desc) > 300:
                desc = desc[:300] + "..."
                
            items.append({"title": title, "link": link, "description": desc})
        return items
    except Exception as e:
        print(f"Error parsing XML API from {source_name} ({request_url if 'request_url' in locals() else url}): {e}")
        return []

def main():
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    yaml_path = project_dir / "references" / "sources.yaml"
    output_dir = script_dir / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "context.md"

    if not yaml_path.exists():
        print(f"Configuration not found at {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    if not sources:
        print("No sources found in sources.yaml")
        sys.exit(0)

    last_week_date = get_last_week_date()
    
    results = {}

    print("Fetching data from sources...")
    for source in sources:
        name = source.get("name")
        category = source.get("category", "OTHER")
        url = source.get("url", "").replace("{last_week_date}", last_week_date)
        src_type = source.get("type", "rss")
        max_items = source.get("max_items", 10)
        print(f"  -> {name} ({src_type})")
        
        items = []
        if src_type == "rss":
            items = parse_rss(url, max_items=max_items)
        elif src_type == "json_api":
            items = parse_json_api(url, source.get("parser_config", {}), max_items=max_items)
        elif src_type == "xml_api":
            items = parse_xml_api(url, source.get("parser_config", {}), max_items=max_items, source_name=name)
        else:
            print(f"Unknown source type: {src_type} for {name}")
            
        if category not in results:
            results[category] = []
        results[category].append({"source_name": name, "items": items})

    print("Generating context.md...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# LLM Daily Context Data\\n\\n")
        f.write(f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        
        for category, sources_data in results.items():
            f.write(f"## {category}\\n\\n")
            for src in sources_data:
                f.write(f"### Source: {src['source_name']}\\n")
                if not src['items']:
                    f.write("*No items found or failed to fetch.*\\n\\n")
                    continue
                for item in src['items']:
                    title = item['title'].replace('\\n', ' ')
                    desc = item['description'].replace('\\n', ' ')
                    f.write(f"- **{title}**\\n")
                    f.write(f"  Link: {item['link']}\\n")
                    f.write(f"  Description: {desc}\\n")
                f.write("\\n")
            f.write("---\\n\\n")

    print(f"Successfully wrote {output_file}")
    print(f"COLLECTED_DATA_PATH={output_file}")

if __name__ == "__main__":
    main()
