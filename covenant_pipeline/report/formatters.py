"""HTML formatting helpers mirroring viewer/frontend/src/App.jsx logic."""

from __future__ import annotations

import html
import json
import re
from typing import Any

RECEIPT_PAGE_PATTERN = re.compile(r"PDF Pages? (\d+)(?:-(\d+))?")
REF_PATTERN = re.compile(r"\[\$REF:\s*(.*?)\]")

SKIP_KEYS = frozenset({"is_false_flag", "false_flag_reason", "is_applicable", "confidence_score"})


def format_agent_name(name: str | None) -> str:
    if not name:
        return "Unknown Agent"
    return re.sub(r"([A-Z])", r" \1", name).strip()


def get_audit_info(covenant: dict) -> dict:
    audit = covenant.get("Validation_Audit") or {}
    extracted = covenant.get("Extracted_Data") or {}
    return {
        "confidence": audit.get("confidence_score", 1),
        "is_verified": audit.get("is_verified", True),
        "discrepancies": audit.get("flagged_discrepancies"),
        "false_flag": extracted.get("is_false_flag") is True,
        "false_flag_reason": extracted.get("false_flag_reason"),
    }


def unique_covenants(covenants: list[dict]) -> list[dict]:
    seen: set[str] = set()
    result: list[dict] = []
    for cov in covenants:
        agent = cov.get("Agent")
        if not agent or agent in seen:
            continue
        seen.add(agent)
        result.append(cov)
    return result


def parse_receipt_pages(receipt: str | None) -> list[int]:
    if not receipt:
        return [1]
    match = RECEIPT_PAGE_PATTERN.search(receipt)
    if not match:
        return [1]
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else start
    return list(range(start, end + 1))


def available_terms(covenant: dict, glossary: dict) -> list[str]:
    extracted = covenant.get("Extracted_Data")
    if not glossary or extracted is None:
        return []

    json_string = json.dumps(extracted)
    found_terms: set[str] = set()
    for match in REF_PATTERN.finditer(json_string):
        found_terms.add(match.group(1))

    expanded: set[str] = set(found_terms)
    for term in found_terms:
        definition = glossary.get(term) or {}
        for nested in definition.get("nested_references") or []:
            expanded.add(nested)

    return sorted(expanded)


def _format_scalar_html(data: Any) -> str:
    text = str(data)
    escaped = html.escape(text)
    if isinstance(data, str) and "[$REF:" in data:
        return f'<span class="ref-tag">{escaped}</span>'
    return f'<span class="value-scalar">{escaped}</span>'


def render_formatted_data_html(data: Any) -> str:
    if not isinstance(data, (dict, list)):
        return _format_scalar_html(data)

    if isinstance(data, list):
        items = "".join(f"<li>{render_formatted_data_html(item)}</li>" for item in data)
        return f'<ul class="value-list">{items}</ul>'

    parts: list[str] = []
    for key, value in data.items():
        if key.lower() in SKIP_KEYS:
            continue
        label = html.escape(key.replace("_", " "))
        parts.append(
            f'<div class="value-block">'
            f'<div class="value-key">{label}</div>'
            f'<div class="value-body">{render_formatted_data_html(value)}</div>'
            f"</div>"
        )
    return f'<div class="value-object">{"".join(parts)}</div>'


def split_receipt(receipt: str | None) -> tuple[str, str]:
    if not receipt:
        return "", ""
    parts = receipt.split("|")
    page_receipt = parts[0].strip() if parts else ""
    section_receipt = " | ".join(p.strip() for p in parts[1:]).strip() if len(parts) > 1 else ""
    return page_receipt, section_receipt
