"""Phase 2a: Deterministic Article 1 glossary builder."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.utils.io import require_file, save_json


def build_deterministic_glossary(article_1_text: str) -> dict:
    """Extract definitions from Article 1 and map nested references."""
    print("Initializing Pure Code Glossary Engine...")

    pattern = r'[""“”]([^""“”]+)[""“”]\s*(?:of\s+a\s+Person)?\s*means'
    matches = list(re.finditer(pattern, article_1_text, re.IGNORECASE))

    raw_glossary = {}

    for i, match in enumerate(matches):
        term = match.group(1).strip()
        start_idx = match.start()
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(article_1_text)
        raw_definition_text = article_1_text[start_idx:end_idx].strip()
        raw_glossary[term] = raw_definition_text

    print(f"  -> Extracted {len(raw_glossary)} raw definitions from text.")

    final_glossary = {}
    all_terms = list(raw_glossary.keys())
    all_terms.sort(key=len, reverse=True)

    print("  -> Executing deterministic reference mapping...")
    for term, text in raw_glossary.items():
        nested_refs = set()

        for potential_target in all_terms:
            if potential_target == term:
                continue

            escape_term = re.escape(potential_target)
            if re.search(rf"\b{escape_term}\b", text):
                nested_refs.add(potential_target)

        final_glossary[term] = {
            "raw_definition_text": text,
            "nested_references": list(nested_refs),
        }

    return final_glossary


def run_glossary(paths: PipelinePaths) -> Path:
    """Build glossary from Article 1 sections in the phase 1 payload CSV."""
    require_file(paths.phase1_payload, "Phase 1 payload CSV")

    df = pd.read_csv(paths.phase1_payload)
    article_1_df = df[df["Article"].astype(str).str.contains("Article 1", case=False, na=False)]
    real_article_1_text = " ".join(article_1_df["Raw_Text"].dropna().tolist())
    print(f"Successfully loaded {len(real_article_1_text)} characters of Article 1 text.\n")

    start_time = datetime.now()
    master_glossary = build_deterministic_glossary(real_article_1_text)
    end_time = datetime.now()

    save_json(paths.glossary, master_glossary, indent=2)

    execution_time = (end_time - start_time).total_seconds()
    print("\nPhase 2 Complete!")
    print("Total API Cost: $0.00")
    print(f"Execution Time: {execution_time:.3f} seconds")
    print(f"Payload saved to: {paths.glossary}")

    return paths.glossary
