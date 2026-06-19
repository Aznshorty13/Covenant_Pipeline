"""Gemini client initialization from environment."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ENV_LOADED = False


def _ensure_env_loaded() -> None:
    """Load ``.env`` from the repo root once (existing env vars take precedence)."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    load_dotenv(_REPO_ROOT / ".env")
    _ENV_LOADED = True


def get_client() -> genai.Client:
    """Initialize GenAI client using GEMINI_API_KEY from the environment."""
    _ensure_env_loaded()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is required for LLM stages (extract, validate). "
            "Copy .env.example to .env in the project root and set your key, "
            "or export GEMINI_API_KEY in your shell."
        )
    return genai.Client(api_key=api_key)
