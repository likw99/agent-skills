#!/usr/bin/env python3
import datetime
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import feedparser
import requests
import yaml

def get_last_week_date():
    return (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

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
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}, timeout=30)
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

def parse_xml_api(url, config, max_items=10):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}, timeout=30)
        response.raise_for_status()
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
        print(f"Error parsing XML API from {url}: {e}")
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
        print(f"  -> {name} ({src_type})")
        
        items = []
        if src_type == "rss":
            items = parse_rss(url)
        elif src_type == "json_api":
            items = parse_json_api(url, source.get("parser_config", {}))
        elif src_type == "xml_api":
            items = parse_xml_api(url, source.get("parser_config", {}))
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
