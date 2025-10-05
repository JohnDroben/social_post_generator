"""Wrapper around OpenAI API for generating a short social post.

The module expects ProxyAPI and ProxyURL in environment. It uses the Chat Completions API
via the openai python package. If the package is not available, instruct user to
install requirements from requirements.txt.
"""
from __future__ import annotations

import os
import time

import openai
from dotenv import load_dotenv

def _truncate_text(text: str, max_tokens: int = 2000) -> str:
    """Naive truncation to avoid sending huge inputs. Keep characters.

    max_tokens approximated as characters here to keep it simple.
    """
    if len(text) <= max_tokens:
        return text
    return text[: max_tokens - 100] + "\n..."


# Explicitly load .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Load ProxyAPI and ProxyURL from environment variables
proxy_api_key = os.environ.get("ProxyAPI")
proxy_url = "https://openai.api.proxyapi.ru/v1"

if not proxy_api_key:
    raise RuntimeError("ProxyAPI key must be set in the environment variables")

# Set OpenAI API key and base URL for proxy
openai.api_key = proxy_api_key
openai.api_base = proxy_url

async def mock_generate_post(page_text: str, style: str = "ироничный") -> str:
    """Mock function to simulate API response for testing purposes."""
    return f"[Тестовый пост в стиле {style}] {page_text[:50]}..."

async def generate_post(page_text: str, style: str = "ироничный") -> str:
    """Generate a short social post (<=800 chars) about page_text in given style.

    Returns the generated string. Raises RuntimeError on API or input errors.
    """
    page_text = _truncate_text(page_text, max_tokens=3000)

    user_prompt = (
        f"Напиши короткий пост (до 800 символов) по этой теме в стиле: {style}.\n"
        "Учитывай содержание: \n" + page_text
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract the generated text
        text = response["choices"][0]["message"]["content"].strip()

        # Enforce length limit
        if len(text) > 800:
            text = text[:797].rstrip() + "..."

        return text

    except Exception as e:
        raise RuntimeError(f"Error generating post: {e}")
