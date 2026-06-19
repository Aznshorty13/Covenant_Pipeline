"""Phase 3b: Node L validation pipeline."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from google import genai

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.llm.client import get_client
from covenant_pipeline.llm.cost import calculate_api_cost
from covenant_pipeline.llm.prompts import AUDITOR_SYSTEM_PROMPT
from covenant_pipeline.schemas.validation import ValidationAudit
from covenant_pipeline.utils.io import require_file


def load_pipeline_data(
    csv_path: str | Path, json_path: str | Path
) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
    try:
        df_raw = pd.read_csv(csv_path)
        with open(json_path, "r", encoding="utf-8") as file:
            compiled_data = json.load(file)
        covenants_list = compiled_data.get("Phase1_Extracted_Covenants", [])
        print(f"Successfully loaded CSV and {len(covenants_list)} compiled covenants.\n")
        return df_raw, compiled_data, covenants_list
    except FileNotFoundError as e:
        print(f"Error loading files: {e}. Please ensure files are in the working directory.")
        return pd.DataFrame(), {}, []


def build_rehydration_db(df_raw: pd.DataFrame) -> Dict[str, str]:
    if df_raw.empty:
        return {}

    def build_receipt_string(row):
        return (
            f"PDF Pages {row['Absolute_Start_Page']}-{row['Absolute_End_Page']} "
            f"(Printed Pages {row['Printed_Start_Page']}-{row['Printed_End_Page']}) | "
            f"{row['Article']}: {row['Article_Title']} | "
            f"{row['Section']}: {row['Section_Title']}"
        )

    df_raw = df_raw.copy()
    df_raw["Reconstructed_Receipt"] = df_raw.apply(build_receipt_string, axis=1)
    df_raw["Reconstructed_Receipt"] = (
        df_raw["Reconstructed_Receipt"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    )

    return dict(zip(df_raw["Reconstructed_Receipt"], df_raw["Raw_Text"]))


def apply_chaos_injection(agent_name: str, data_to_audit: Dict[str, Any]) -> None:
    if agent_name == "TotalLeverageRatio" and data_to_audit.get("step_downs"):
        try:
            original = data_to_audit["step_downs"][0]["ratio_limit"]
            data_to_audit["step_downs"][0]["ratio_limit"] = 9.99
            print(f"    -> [!] CHAOS (MATH): Corrupted {original} -> 9.99")
        except (IndexError, KeyError):
            pass

    elif agent_name == "RestrictedPayments" and "general_basket_limit" in data_to_audit:
        try:
            original = str(data_to_audit["general_basket_limit"])
            data_to_audit["general_basket_limit"] = f"PROHIBITED {original}"
            print("    -> [!] CHAOS (SEMANTIC): Injected dangerous legal negation.")
        except KeyError:
            pass

    elif agent_name == "InvestmentsAndAcquisitions":
        try:
            if "specific_carve_outs" in data_to_audit and len(data_to_audit["specific_carve_outs"]) > 0:
                carve_out = data_to_audit["specific_carve_outs"][0]
                if "category_name" in carve_out:
                    original = carve_out["category_name"]
                    carve_out["category_name"] = original + " AND FAKE TERM"
                    print(f"    -> [!] CHAOS (GRAPH): Sabotaged term name -> '{carve_out['category_name']}'")
        except (IndexError, KeyError):
            pass


def execute_llm_audit(
    client: genai.Client, raw_text: str, data_to_audit: Dict[str, Any], model: str
) -> Tuple[Dict[str, Any], float]:
    formatted_prompt = AUDITOR_SYSTEM_PROMPT.format(
        raw_text=str(raw_text).replace("\n", " ").replace("\xa0", " "),
        json_payload=json.dumps(data_to_audit, indent=2),
    )

    response = client.models.generate_content(
        model=model,
        contents=formatted_prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ValidationAudit,
            "temperature": 0.0,
        },
    )

    audit_result = response.parsed.model_dump()
    cost_metrics = calculate_api_cost(response.usage_metadata)

    return audit_result, cost_metrics["total_cost_usd"]


def run_validation_pipeline(
    csv_path: str | Path,
    json_path: str | Path,
    output_path: str | Path,
    *,
    model: str,
    rate_limit_seconds: float = 2.0,
    enable_adversarial_test: bool = False,
) -> None:
    client = get_client()
    df_raw, compiled_data, covenants_list = load_pipeline_data(csv_path, json_path)

    if not covenants_list:
        return

    text_lookup_db = build_rehydration_db(df_raw)
    total_audit_cost = 0.0

    for index, covenant_node in enumerate(covenants_list):
        receipt_key = str(covenant_node.get("Receipt", "")).strip()
        receipt_key = " ".join(receipt_key.split())

        agent_name = covenant_node.get("Agent")
        extracted_data = covenant_node.get("Extracted_Data", {})
        print(f"[{index}] Auditing Node: {agent_name}")

        raw_text = text_lookup_db.get(receipt_key)
        if not raw_text:
            print(f"    -> WARNING: Could not rehydrate text for Receipt: {receipt_key}")
            covenant_node["Validation_Audit"] = {
                "is_verified": False,
                "confidence_score": 0.0,
                "requires_human_context": True,
                "flagged_discrepancies": ["PIPELINE ERROR: Failed to join JSON Receipt to CSV Raw_Text."],
            }
            continue

        data_to_audit = {
            k: v
            for k, v in extracted_data.items()
            if k not in ["is_applicable", "is_false_flag", "false_flag_reason"]
        }

        if not any(data_to_audit.values()):
            print("    -> Status: Skipped (No quantitative data to audit).")
            covenant_node["Validation_Audit"] = {
                "is_verified": True,
                "confidence_score": 1.0,
                "requires_human_context": False,
                "flagged_discrepancies": None,
            }
            continue

        if enable_adversarial_test:
            apply_chaos_injection(agent_name, data_to_audit)

        try:
            audit_result, call_cost = execute_llm_audit(client, raw_text, data_to_audit, model)
            total_audit_cost += call_cost
            covenant_node["Validation_Audit"] = audit_result

            print("    -> Status: Audit Complete")
            print(f"    -> Verified: {audit_result['is_verified']} | Confidence: {audit_result['confidence_score']}")
            if not audit_result["is_verified"] and audit_result["flagged_discrepancies"]:
                print(f"    -> FLAGS: {audit_result['flagged_discrepancies']}")

        except Exception as e:
            print(f"    -> Status: FAILED API CALL. Error: {e}")
            covenant_node["Validation_Audit"] = {
                "is_verified": False,
                "confidence_score": 0.0,
                "requires_human_context": True,
                "flagged_discrepancies": [f"API ERROR: {str(e)}"],
            }

        time.sleep(rate_limit_seconds)

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(compiled_data, outfile, indent=4)

    print(f"\nAudit complete. Data successfully saved to {output_path}.")
    print(f"Total Exception Layer API Cost: ${total_audit_cost:.6f}")


def run_validation(paths: PipelinePaths) -> Path:
    """Run Node L validation and write audited payload."""
    require_file(paths.phase1_payload, "Phase 1 payload CSV")
    require_file(paths.compiled, "Compiled payload JSON")

    run_validation_pipeline(
        csv_path=paths.phase1_payload,
        json_path=paths.compiled,
        output_path=paths.audited,
        model=paths.extraction_model,
        rate_limit_seconds=paths.rate_limit_seconds,
        enable_adversarial_test=paths.enable_adversarial_test,
    )
    return paths.audited
