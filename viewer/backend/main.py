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
    from covenant_pipeline.report.summary import build_pipeline_summary

    payload = _load_audited_payload()
    return build_pipeline_summary(
        payload,
        dispatch_path=_dispatch_queue_path(),
        audited_json_path=str(_audited_json_path()),
        pdf_path=str(_pdf_path()),
    )
