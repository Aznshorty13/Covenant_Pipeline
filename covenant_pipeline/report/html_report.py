"""Generate standalone HTML audit report from pipeline artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import fitz

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.report.formatters import (
    available_terms,
    format_agent_name,
    get_audit_info,
    parse_receipt_pages,
    render_formatted_data_html,
    split_receipt,
    unique_covenants,
)
from covenant_pipeline.report.pdf_images import render_page_data_uris
from covenant_pipeline.report.summary import build_pipeline_summary
from covenant_pipeline.utils.io import load_json, require_file

_TEMPLATE_PATH = Path(__file__).resolve().parent / "template" / "report.html"
_PLACEHOLDER = "{{REPORT_DATA_JSON}}"


def _template_dir() -> Path:
    return _TEMPLATE_PATH.parent


def _build_covenant_records(payload: dict, pdf_path: Path) -> tuple[list[dict], int]:
    glossary = payload.get("Phase2_Master_Glossary") or {}
    covenants = unique_covenants(payload.get("Phase1_Extracted_Covenants") or [])

    doc = fitz.open(pdf_path)
    try:
        pdf_page_count = len(doc)
    finally:
        doc.close()

    records: list[dict] = []
    for index, covenant in enumerate(covenants):
        receipt = covenant.get("Receipt")
        page_numbers = parse_receipt_pages(receipt)
        page_images = render_page_data_uris(pdf_path, page_numbers)
        page_receipt, section_receipt = split_receipt(receipt)
        terms = available_terms(covenant, glossary)
        audit = get_audit_info(covenant)

        records.append(
            {
                "id": index,
                "agent": covenant.get("Agent"),
                "agent_display": format_agent_name(covenant.get("Agent")),
                "receipt": receipt,
                "page_receipt": page_receipt,
                "section_receipt": section_receipt,
                "audit": audit,
                "extracted_data_html": render_formatted_data_html(covenant.get("Extracted_Data")),
                "page_images": page_images,
                "page_numbers": page_numbers,
                "glossary_terms": terms,
            }
        )

    return records, pdf_page_count


def _build_report_data(paths: PipelinePaths, payload: dict) -> dict:
    summary = build_pipeline_summary(
        payload,
        dispatch_path=paths.dispatch_queue,
        audited_json_path=str(paths.audited.resolve()),
        pdf_path=str(paths.pdf_path.resolve()) if paths.pdf_path else None,
    )
    covenants, pdf_page_count = _build_covenant_records(payload, paths.pdf_path)
    glossary = payload.get("Phase2_Master_Glossary") or {}

    return {
        "summary": summary,
        "covenants": covenants,
        "glossary": glossary,
        "pdf_page_count": pdf_page_count,
    }


def generate_html_report(paths: PipelinePaths) -> Path:
    """Write covenant_audit_report.html to the output directory."""
    require_file(paths.audited, "Audited JSON")
    if paths.pdf_path is None:
        raise FileNotFoundError("pdf_path is required to generate HTML report")
    require_file(paths.pdf_path, "Source PDF")
    require_file(_TEMPLATE_PATH, "Report HTML template")

    payload = load_json(paths.audited)
    report_data = _build_report_data(paths, payload)

    template = _TEMPLATE_PATH.read_text(encoding="utf-8")
    if _PLACEHOLDER not in template:
        raise ValueError(f"Report template missing placeholder {_PLACEHOLDER}")

    report_json = json.dumps(report_data, ensure_ascii=False)
    html_content = template.replace(_PLACEHOLDER, report_json)

    output_path = paths.report_html
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"HTML report written: {output_path} ({size_mb:.1f} MB)")
    return output_path
