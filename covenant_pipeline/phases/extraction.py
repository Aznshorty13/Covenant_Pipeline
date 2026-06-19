"""Phase 1: LLM covenant extraction."""

from __future__ import annotations

import json
import time
from pathlib import Path

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.llm.client import get_client
from covenant_pipeline.llm.cost import calculate_api_cost
from covenant_pipeline.llm.prompts import MASTER_SYSTEM_PROMPT
from covenant_pipeline.schemas.covenants import SCHEMA_ROUTER
from covenant_pipeline.utils.io import load_json, require_file, save_json


def run_extraction(paths: PipelinePaths) -> Path:
    """Run Phase 1 LLM extraction over the dispatch queue."""
    require_file(paths.dispatch_queue, "Dispatch queue JSON")

    dispatch_queue = load_json(paths.dispatch_queue)
    print(f"Successfully loaded {len(dispatch_queue)} envelopes from the queue.\n")

    client = get_client()
    results_database = []
    total_pipeline_cost = 0.0

    for index, envelope in enumerate(dispatch_queue):
        agent_name = envelope.get("Agent")

        if agent_name not in SCHEMA_ROUTER:
            print(f"[{index}] Skipping {agent_name}... Schema not yet built.")
            continue

        print(f"[{index}] Processing Envelope: {agent_name}")
        print(f"    Receipt: {envelope.get('Receipt')}")

        target_schema = SCHEMA_ROUTER[agent_name]
        raw_text = envelope.get("Payload_Text", "")
        clean_text = raw_text.replace("\n", " ").replace("\xa0", " ")

        formatted_prompt = MASTER_SYSTEM_PROMPT.format(
            agent_name=agent_name,
            guardrail=envelope.get("Definition_Guardrail", ""),
            payload_text=clean_text,
        )

        try:
            response = client.models.generate_content(
                model=paths.extraction_model,
                contents=formatted_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": target_schema,
                    "temperature": 0.0,
                },
            )

            extracted_data = response.parsed
            cost_metrics = calculate_api_cost(response.usage_metadata)
            total_pipeline_cost += cost_metrics["total_cost_usd"]

            results_database.append(
                {
                    "Receipt": envelope.get("Receipt"),
                    "Agent": agent_name,
                    "Extracted_Data": extracted_data.model_dump(),
                    "Cost_Metrics": cost_metrics,
                }
            )

            print("    Status: Extraction Successful")
            print(f"    Tokens: {cost_metrics['input_tokens']} In | {cost_metrics['output_tokens']} Out")
            print(f"    Cost:   ${cost_metrics['total_cost_usd']:.6f}")
            print("    Extracted Payload:")
            print(json.dumps(extracted_data.model_dump(), indent=2))
            print("\n" + "-" * 40 + "\n")

        except Exception as e:
            print(f"    Status: FAILED. Error: {e}\n")

        time.sleep(paths.rate_limit_seconds)

    print(f"Finished processing. Successfully extracted {len(results_database)} covenants.")
    print(f"Total Pipeline API Cost: ${total_pipeline_cost:.6f}\n")

    if results_database:
        save_json(paths.phase1_nodes, results_database)
        print(f"Extraction complete. Data successfully saved to {paths.phase1_nodes}.")
    else:
        print("No covenants extracted. File not saved.")

    return paths.phase1_nodes
