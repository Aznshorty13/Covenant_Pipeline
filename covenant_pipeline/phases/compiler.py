"""Phase 2b: Multi-hop relational compiler (Node F)."""

from __future__ import annotations

import difflib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.utils.io import require_file


class MultiHopRelationalCompiler:
    """Executes multi-hop resolution and dynamic glossary injection."""

    def __init__(self, phase2_glossary_path: str | Path, document_chunks_csv_path: str | Path):
        self.ref_pattern = re.compile(r"\[\$REF:\s*([^\]]+)\]")
        self.dangling_pointers = set()

        self.master_glossary = self._load_json(phase2_glossary_path)
        self.glossary_keys = list(self.master_glossary.keys())
        self.glossary_keys_lower = {k.lower(): k for k in self.glossary_keys}

        print(f"Loading TOC routing chunks from {document_chunks_csv_path}...")
        try:
            chunk_df = pd.read_csv(document_chunks_csv_path)
            raw_chunks = chunk_df.to_dict(orient="records")
            self.toc_routing_index = self._build_toc_routing_index(raw_chunks)
        except FileNotFoundError:
            raise FileNotFoundError(f"CRITICAL: Could not find Phase 0 chunks at {document_chunks_csv_path}")

    def _load_json(self, filepath: str | Path) -> Any:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"CRITICAL: Failed to load {filepath}")

    def _build_toc_routing_index(self, chunks: List[Dict]) -> Dict[str, Dict]:
        toc_index = {}
        for chunk in chunks:
            section_title = chunk.get("Section_Title")
            if not isinstance(section_title, str) or not section_title.strip():
                continue

            clean_title = section_title.strip().lower()
            semantic_title = re.sub(r"section\s*\d+\.\d+\s*", "", clean_title).strip()

            toc_index[semantic_title] = {
                "routing_type": "External Section Router",
                "location": f"{chunk.get('Article_Title', 'Unknown Article')} | {section_title}",
                "extracted_text": str(chunk.get("Raw_Text", "Text unavailable.")),
            }

        print(f" -> Successfully built TOC Routing Index with {len(toc_index)} operational sections.")
        return toc_index

    def _resolve_term(self, raw_term: str) -> str:
        clean_term = raw_term.strip()
        lower_term = clean_term.lower()

        if clean_term in self.glossary_keys:
            return clean_term

        if lower_term in self.toc_routing_index:
            print(f"  [Multi-Hop] Injected external section into Glossary: '[$REF: {raw_term}]'")
            self.master_glossary[clean_term] = {
                "raw_definition_text": self.toc_routing_index[lower_term]["extracted_text"],
                "nested_references": [],
            }
            self.glossary_keys.append(clean_term)
            return clean_term

        toc_keys = list(self.toc_routing_index.keys())
        toc_matches = difflib.get_close_matches(lower_term, toc_keys, n=1, cutoff=0.85)

        if toc_matches:
            best_toc = toc_matches[0]
            print(f"  [Multi-Hop] Fuzzy injected external section into Glossary: '[$REF: {raw_term}]'")
            self.master_glossary[clean_term] = {
                "raw_definition_text": self.toc_routing_index[best_toc]["extracted_text"],
                "nested_references": [],
            }
            self.glossary_keys.append(clean_term)
            return clean_term

        base_term = clean_term[:-1] if lower_term.endswith("s") else clean_term
        if base_term in self.glossary_keys:
            print(f"  [Linker] Fixed Plural: '[$REF: {raw_term}]' -> '[$REF: {base_term}]'")
            return base_term

        close_matches = difflib.get_close_matches(clean_term, self.glossary_keys, n=1, cutoff=0.8)
        if close_matches:
            best_match = close_matches[0]
            print(f"  [Linker] Fuzzy Matched: '[$REF: {raw_term}]' -> '[$REF: {best_match}]'")
            return best_match

        self.dangling_pointers.add(raw_term)
        print(f"  [WARNING] Dangling Pointer: Could not link '[$REF: {raw_term}]'")
        return raw_term

    def _process_string(self, text: str) -> str:
        matches = self.ref_pattern.findall(text)
        for raw_term in matches:
            resolved_key = self._resolve_term(raw_term)
            if resolved_key != raw_term:
                text = text.replace(f"[$REF: {raw_term}]", f"[$REF: {resolved_key}]")
        return text

    def _traverse_and_mutate(self, node: Any):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str):
                    node[key] = self._process_string(value)
                else:
                    self._traverse_and_mutate(value)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                if isinstance(value, str):
                    node[i] = self._process_string(value)
                else:
                    self._traverse_and_mutate(value)

    def compile(self, phase1_data_path: str | Path, output_path: str | Path):
        print("\nInitializing Enterprise Relational Compiler...")
        phase1_covenants = self._load_json(phase1_data_path)

        print("\nExecuting Deep Relational Linking (Dynamic Injection Enabled)...")
        self._traverse_and_mutate(phase1_covenants)

        compiled_payload = {
            "Document_Metadata": {
                "Processing_Timestamp": datetime.now().isoformat(),
                "Pipeline_Version": "Enterprise_v3.1_Injection",
                "Audit_Status": "Warnings_Detected" if self.dangling_pointers else "Clean",
                "Total_Definitions_Resolved": len(self.master_glossary),
                "Dangling_Pointers_Detected": list(self.dangling_pointers),
            },
            "Phase1_Extracted_Covenants": phase1_covenants,
            "Phase2_Master_Glossary": self.master_glossary,
        }

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(compiled_payload, out, indent=4)

        print(f"\nCompilation Complete. Payload saved to: {output_path}")
        if not self.dangling_pointers:
            print("Audit Status: CLEAN. Zero dangling pointers.")
        else:
            print(f"Audit Status: WARNING. {len(self.dangling_pointers)} pointers could not be resolved.")


def run_compiler(paths: PipelinePaths) -> Path:
    """Run relational compiler and write compiled payload."""
    require_file(paths.glossary, "Glossary JSON")
    require_file(paths.phase1_payload, "Phase 1 payload CSV")
    require_file(paths.phase1_nodes, "Phase 1 extracted nodes JSON")

    compiler = MultiHopRelationalCompiler(
        phase2_glossary_path=paths.glossary,
        document_chunks_csv_path=paths.phase1_payload,
    )
    compiler.compile(
        phase1_data_path=paths.phase1_nodes,
        output_path=paths.compiled,
    )
    return paths.compiled
