#!/usr/bin/env python3
"""
LLM Daily - Newsletter Publisher (Buttondown)

Publishes a markdown newsletter to Buttondown email service.

Usage:
    python publish.py <newsletter_file> [--status draft|scheduled]

Requires BUTTONDOWN_API_KEY environment variable.
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime


def publish_to_buttondown(content: str, subject: str = None, status: str = None) -> dict:
    """Publish newsletter content to Buttondown"""
    api_key = os.environ.get("BUTTONDOWN_API_KEY")
    if not api_key:
        print("ERROR: BUTTONDOWN_API_KEY environment variable not set.")
        print("Set it in your environment or skip publishing.")
        return {"error": "BUTTONDOWN_API_KEY not set"}

    api_url = "https://api.buttondown.email/v1/emails"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }

    if not subject:
        today = datetime.now().strftime("%B %d, %Y")
        subject = f"LLM Daily: {today}"

    if not status:
        status = os.environ.get("NEWSLETTER_STATUS", "draft")

    data = {
        "subject": subject,
        "body": content,
        "status": status,
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 201:
            result = response.json()
            print(f"Newsletter published to Buttondown!")
            print(f"  ID: {result.get('id')}")
            print(f"  Status: {status}")
            print(f"  Subject: {subject}")
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {"error": response.text, "status_code": response.status_code}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Publish LLM Daily newsletter to Buttondown")
    parser.add_argument("file", help="Path to newsletter markdown file")
    parser.add_argument("--subject", type=str, default=None, help="Email subject line")
    parser.add_argument("--status", type=str, choices=["draft", "scheduled"], default=None,
                        help="Newsletter status (default: draft)")
    args = parser.parse_args()

    # Read newsletter content
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return 1

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("Error: Newsletter file is empty")
        return 1

    print(f"Publishing newsletter ({len(content)} chars)...")
    result = publish_to_buttondown(content, args.subject, args.status)

    if "error" in result:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
