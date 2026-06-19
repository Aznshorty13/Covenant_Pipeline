"""Render PDF pages as base64 JPEG data URIs for the HTML report."""

from __future__ import annotations

import base64
from pathlib import Path

import fitz

from covenant_pipeline.report.formatters import parse_receipt_pages

TARGET_WIDTH_PX = 700
JPEG_QUALITY = 75


def render_page_data_uris(pdf_path: Path, page_numbers: list[int]) -> list[str]:
    """Render PDF pages to data:image/jpeg;base64,... URIs."""
    if not page_numbers:
        return []

    doc = fitz.open(pdf_path)
    try:
        uris: list[str] = []
        page_count = len(doc)
        for page_num in page_numbers:
            if page_num < 1 or page_num > page_count:
                continue
            page = doc[page_num - 1]
            rect = page.rect
            scale = TARGET_WIDTH_PX / rect.width if rect.width else 1.0
            matrix = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            jpeg_bytes = pix.tobytes("jpeg", jpg_quality=JPEG_QUALITY)
            encoded = base64.b64encode(jpeg_bytes).decode("ascii")
            uris.append(f"data:image/jpeg;base64,{encoded}")
        return uris
    finally:
        doc.close()


def render_receipt_pages(pdf_path: Path, receipt: str | None) -> list[str]:
    """Parse receipt page range and render matching PDF pages."""
    return render_page_data_uris(pdf_path, parse_receipt_pages(receipt))
