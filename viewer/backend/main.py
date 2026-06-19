"""FastAPI backend for the Covenant Pipeline viewer."""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="Covenant Viewer Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _audited_json_path() -> Path:
    raw = os.environ.get("COVENANT_AUDITED_JSON")
    if not raw:
        raise HTTPException(
            status_code=500,
            detail="COVENANT_AUDITED_JSON environment variable is not set.",
        )
    return Path(raw).resolve()


def _pdf_path() -> Path:
    raw = os.environ.get("COVENANT_PDF_PATH")
    if not raw:
        raise HTTPException(
            status_code=500,
            detail="COVENANT_PDF_PATH environment variable is not set.",
        )
    return Path(raw).resolve()


def _output_dir() -> Path | None:
    raw = os.environ.get("COVENANT_OUTPUT_DIR")
    return Path(raw).resolve() if raw else None


def _dispatch_queue_path() -> Path | None:
    raw = os.environ.get("COVENANT_DISPATCH_QUEUE_JSON")
    if raw:
        return Path(raw).resolve()
    output_dir = _output_dir()
    if output_dir:
        return output_dir / "dispatch_queue_output.json"
    return None


def _load_audited_payload() -> dict:
    path = _audited_json_path()
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Audited payload not found: {path}",
        )
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/api/document-data")
def get_document_data():
    return _load_audited_payload()


@app.get("/api/pdf")
def get_source_pdf():
    file_path = _pdf_path()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found: {file_path}")
    return FileResponse(file_path, media_type="application/pdf")


@app.get("/api/pipeline-summary")
def get_pipeline_summary():
    payload = _load_audited_payload()
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
    dispatch_path = _dispatch_queue_path()
    if dispatch_path and dispatch_path.exists():
        with open(dispatch_path, "r", encoding="utf-8") as file:
            dispatch_count = len(json.load(file))

    return {
        "document_metadata": metadata,
        "covenant_count": len(covenants),
        "dispatch_envelope_count": dispatch_count,
        "total_extraction_cost_usd": total_extraction_cost,
        "validation_pass": validation_pass,
        "validation_fail": validation_fail,
        "covenants": covenant_rows,
        "audited_json_path": str(_audited_json_path()),
        "pdf_path": str(_pdf_path()),
    }
