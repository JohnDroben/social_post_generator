"""CLI agent: download page, extract text, generate short social post via OpenAI.

Usage:
    python agent.py <url> [--style STYLE].

Environment:
    OPENAI_API_KEY must be set in environment (or placed in a .env file if desired).
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
import textwrap
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from openai_module import generate_post as real_generate_post, mock_generate_post

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

print(f"DEBUG: Attempting to load .env from {os.path.join(os.getcwd(), '.env')}")
print(f"DEBUG: Loaded OPENAI_API_KEY={os.environ.get('OPENAI_API_KEY')}")


def extract_text_from_html(html: str) -> str:
    """Extract visible text from HTML using BeautifulSoup.

    Keep it simple: join text from <p>, <h1>-<h6>, and <li>.
    """
    soup = BeautifulSoup(html, "html.parser")
    parts = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def download_page(url: str, timeout: int = 10) -> str:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a short social post from a web page")
    parser.add_argument("url", help="Page URL to summarize")
    parser.add_argument("--style", default="ироничный", help="Style of the post (default: ирoничный)")
    args = parser.parse_args(argv)

    # Skip API key check during testing
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[Тестовый режим] Переменная OPENAI_API_KEY не требуется.")

    print(f"DEBUG: OPENAI_API_KEY={api_key}")  # Temporary debug output

    try:
        html = download_page(args.url)
    except Exception as e:
        print(f"Error downloading page: {e}", file=sys.stderr)
        return 3

    page_text = extract_text_from_html(html)
    if not page_text.strip():
        print("No textual content found on the page.", file=sys.stderr)
        return 4

    # Ensure mock_generate_post is used in test mode
    generate_post_function = mock_generate_post if api_key is None else real_generate_post

    # Replace synchronous call with asynchronous call
    try:
        post = asyncio.run(generate_post_function(page_text, style=args.style))
    except Exception as e:
        print(f"Error generating post: {e}", file=sys.stderr)
        return 5

    # Ensure within 800 characters
    if len(post) > 800:
        post = post[:797].rstrip() + "..."

    print(post)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
