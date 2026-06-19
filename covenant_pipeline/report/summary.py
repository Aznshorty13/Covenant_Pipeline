"""Pipeline summary aggregation shared by viewer API and HTML report."""

from __future__ import annotations

import json
from pathlib import Path


def build_pipeline_summary(
    payload: dict,
    *,
    dispatch_path: Path | None = None,
    audited_json_path: str | None = None,
    pdf_path: str | None = None,
) -> dict:
    """Aggregate covenant counts, validation stats, and extraction cost from audited payload."""
    metadata = payload.get("Document_Metadata", {})
    covenants = payload.get("Phase1_Extracted_Covenants", [])

    covenant_rows = []
    total_extraction_cost = 0.0
    validation_pass = 0
    validation_fail = 0

    for cov in covenants:
        audit = cov.get("Validation_Audit") or {}
        cost = (cov.get("Cost_Metrics") or {}).get("total_cost_usd", 0.0) or 0.0
        total_extraction_cost += cost

        is_verified = audit.get("is_verified", True)
        if is_verified:
            validation_pass += 1
        else:
            validation_fail += 1

        covenant_rows.append(
            {
                "agent": cov.get("Agent"),
                "is_verified": is_verified,
                "confidence_score": audit.get("confidence_score"),
                "extraction_cost_usd": cost,
                "flagged_discrepancies": audit.get("flagged_discrepancies"),
            }
        )

    dispatch_count = None
    if dispatch_path and dispatch_path.exists():
        with open(dispatch_path, "r", encoding="utf-8") as file:
            dispatch_count = len(json.load(file))

    result = {
        "document_metadata": metadata,
        "covenant_count": len(covenants),
        "dispatch_envelope_count": dispatch_count,
        "total_extraction_cost_usd": total_extraction_cost,
        "validation_pass": validation_pass,
        "validation_fail": validation_fail,
        "covenants": covenant_rows,
    }

    if audited_json_path is not None:
        result["audited_json_path"] = audited_json_path
    if pdf_path is not None:
        result["pdf_path"] = pdf_path

    return result
