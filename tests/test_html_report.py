"""Tests for HTML audit report generation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.report.formatters import (
    parse_receipt_pages,
    render_formatted_data_html,
)
from covenant_pipeline.report.html_report import generate_html_report


class TestFormatters(unittest.TestCase):
    def test_parse_receipt_pages_single(self):
        receipt = "PDF Page 42 (Printed Pages 40-40) | Article 7: Covenants"
        self.assertEqual(parse_receipt_pages(receipt), [42])

    def test_parse_receipt_pages_range(self):
        receipt = "PDF Pages 10-12 (Printed Pages 8-8) | Section 7.1"
        self.assertEqual(parse_receipt_pages(receipt), [10, 11, 12])

    def test_parse_receipt_pages_missing(self):
        self.assertEqual(parse_receipt_pages(None), [1])

    def test_render_formatted_data_escapes_html(self):
        html = render_formatted_data_html({"note": "<script>alert(1)</script>"})
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_render_formatted_data_highlights_ref(self):
        html = render_formatted_data_html("See [$REF: EBITDA] for details")
        self.assertIn("ref-tag", html)
        self.assertIn("[$REF: EBITDA]", html)


class TestHtmlReport(unittest.TestCase):
    def _write_minimal_pdf(self, path: Path) -> None:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test covenant page")
        doc.save(path)
        doc.close()

    def _minimal_payload(self) -> dict:
        return {
            "Document_Metadata": {
                "Audit_Status": "Clean",
                "Pipeline_Version": "test",
            },
            "Phase1_Extracted_Covenants": [
                {
                    "Receipt": "PDF Page 1 (Printed Pages 1-1) | Article 7: Covenants | Section 7.1: Leverage",
                    "Agent": "TotalLeverageRatio",
                    "Extracted_Data": {
                        "ratio_limit": 4.5,
                        "definition": "[$REF: EBITDA]",
                        "is_false_flag": False,
                    },
                    "Cost_Metrics": {"total_cost_usd": 0.01},
                    "Validation_Audit": {
                        "is_verified": True,
                        "confidence_score": 1.0,
                        "flagged_discrepancies": None,
                    },
                }
            ],
            "Phase2_Master_Glossary": {
                "EBITDA": {
                    "raw_definition_text": "Earnings before interest, taxes, depreciation and amortization.",
                    "nested_references": [],
                }
            },
        }

    def test_generate_html_report_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "test.pdf"
            audited_path = tmp_path / "final_compiled_payload_audited.json"
            dispatch_path = tmp_path / "dispatch_queue_output.json"

            self._write_minimal_pdf(pdf_path)
            audited_path.write_text(json.dumps(self._minimal_payload()), encoding="utf-8")
            dispatch_path.write_text("[]", encoding="utf-8")

            paths = PipelinePaths(output_dir=tmp_path, pdf_path=pdf_path)
            output = generate_html_report(paths)

            self.assertTrue(output.exists())
            content = output.read_text(encoding="utf-8")
            self.assertIn("PIPELINE RUN SUMMARY", content)
            self.assertIn("PHASE 1 QUEUE", content)
            self.assertIn("Total Leverage Ratio", content)
            self.assertIn("data:image/jpeg;base64,", content)
            self.assertIn("EBITDA", content)

    def test_generate_html_report_uses_mocked_images_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pdf_path = tmp_path / "test.pdf"
            audited_path = tmp_path / "final_compiled_payload_audited.json"

            self._write_minimal_pdf(pdf_path)
            audited_path.write_text(json.dumps(self._minimal_payload()), encoding="utf-8")

            paths = PipelinePaths(output_dir=tmp_path, pdf_path=pdf_path)

            with patch(
                "covenant_pipeline.report.html_report.render_page_data_uris",
                return_value=["data:image/jpeg;base64,ZmFrZQ=="],
            ):
                output = generate_html_report(paths)

            content = output.read_text(encoding="utf-8")
            self.assertIn("data:image/jpeg;base64,ZmFrZQ==", content)


if __name__ == "__main__":
    unittest.main()
