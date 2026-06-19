"""Text formatting and cleaning helpers."""

import re

import pandas as pd


def compress_string(text: str) -> str:
    """
    Aggressively strips all whitespace, newlines, and lowercases the string.
    Neutralizes EDGAR formatting artifacts for deterministic boundary detection.
    """
    if pd.isna(text):
        return ""
    return re.sub(r"\s+", "", str(text)).lower()


def clean_footer_artifacts(text: str) -> str:
    """Removes physical page footers from extracted PDF text."""
    if not isinstance(text, str):
        return ""

    cleaned_text = re.sub(r"(?i)CREDIT AGREEMENT\s*[-–]\s*Page\s*\d+", "", text)
    return cleaned_text.strip()
