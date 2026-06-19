"""Tier 1 deterministic routing."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.utils.io import require_file, save_json


class Tier1DeterministicRouter:
    """Filters document chunks into AI extraction envelopes using boolean matrix logic."""

    def __init__(self, json_config_path: str | Path):
        try:
            with open(json_config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
                self.rules = config_data.get("routing_rules", [])

            if not self.rules:
                raise ValueError("JSON loaded, but 'routing_rules' array was empty or missing.")

        except FileNotFoundError:
            raise FileNotFoundError(f"CRITICAL ERROR: Could not find configuration file at {json_config_path}")

    def _sanitize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        for col in ["Article_Title", "Section_Title", "Raw_Text"]:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna("")
        return df_clean

    def _build_dispatch_envelope(self, target_name: str, description: str, row: pd.Series) -> Dict[str, Any]:
        detailed_receipt = (
            f"PDF Pages {row.get('Absolute_Start_Page', 'N/A')}-{row.get('Absolute_End_Page', 'N/A')} "
            f"(Printed Pages {row.get('Printed_Start_Page', 'N/A')}-{row.get('Printed_End_Page', 'N/A')}) | "
            f"{row.get('Article', 'N/A')}: {row.get('Article_Title', 'N/A')} | "
            f"{row.get('Section', 'N/A')}: {row.get('Section_Title', 'Unknown Section')}"
        )

        return {
            "Agent": target_name,
            "Schema": f"{target_name}Schema",
            "Definition_Guardrail": description,
            "Receipt": detailed_receipt,
            "Payload_Text": row.get("Raw_Text", ""),
        }

    def route_document(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        df = self._sanitize_dataframe(df)
        dispatch_queue = []

        for rule in self.rules:
            target = rule["target_name"]
            description = rule.get("description", "")

            zone_mask = df["Article_Title"].str.upper().apply(
                lambda article: any(zone.upper() in article for zone in rule["valid_zones"])
            )

            regex_pattern = "|".join(rule["section_title_triggers"])
            trigger_mask = df["Section_Title"].str.contains(
                regex_pattern, flags=re.IGNORECASE, regex=True
            )

            blacklist_pattern = "intentionally omitted|left blank|reserved"
            body_mask = ~df["Raw_Text"].str.contains(
                blacklist_pattern, flags=re.IGNORECASE, regex=True
            )

            density_mask = df["Raw_Text"].str.len() > 150

            surviving_chunks = df[zone_mask & trigger_mask & body_mask & density_mask]

            if len(surviving_chunks) == 1:
                row = surviving_chunks.iloc[0]
                envelope = self._build_dispatch_envelope(target, description, row)
                dispatch_queue.append(envelope)

            elif len(surviving_chunks) == 0:
                print(f"[{target}] Tier 1 Failed (0 chunks). Cascading to Tier 2 Vector Search...")

            else:
                print(f"[{target}] Tier 1 Ambiguity ({len(surviving_chunks)} chunks). Cascading to Tier 2 Vector Search...")

        return dispatch_queue


def run_router(paths: PipelinePaths) -> Path:
    """Run Tier 1 routing and save dispatch queue."""
    require_file(paths.phase1_payload, "Phase 1 payload CSV")
    require_file(paths.routing_config_json, "Routing config JSON")

    print(f"Loading data from {paths.phase1_payload}...")
    credit_agreement_df = pd.read_csv(paths.phase1_payload)

    print(f"Loading routing rules from {paths.routing_config_json}...")
    router = Tier1DeterministicRouter(json_config_path=paths.routing_config_json)

    print("Executing Matrix Filter...\n")
    ai_dispatch_queue = router.route_document(credit_agreement_df)

    save_json(paths.dispatch_queue, ai_dispatch_queue)

    print("=== ROUTING COMPLETE ===")
    print(f"Successfully generated {len(ai_dispatch_queue)} LLM Extraction Envelopes.")
    print(f"File saved to: {paths.dispatch_queue}")

    return paths.dispatch_queue
