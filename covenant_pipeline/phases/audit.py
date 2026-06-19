"""Phase 3a: Deterministic database audit."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.utils.io import require_file


def run_database_audit(payload_path: str | Path) -> None:
    """Verify relational integrity and computational safety of the compiled payload."""
    print("==================================================")
    print("Initializing Phase 3 Validation Gate...")
    print("==================================================\n")

    start_time = time.time()
    payload_path = Path(payload_path)

    try:
        with open(payload_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            print(f"[System] Successfully loaded {payload_path}")
    except FileNotFoundError:
        print(f"[Error] Could not find {payload_path}")
        return

    covenants = payload.get("Phase1_Extracted_Covenants", [])
    glossary = payload.get("Phase2_Master_Glossary", {})

    warnings = {
        "Dangling_Pointers": [],
        "Circular_References": [],
        "Type_Violations": [],
    }

    print("\n[Audit 1/3] Sweeping for Circular References...")
    circular_loops = set()
    global_visited = set()

    def dfs(current_term, current_path):
        if current_term not in glossary:
            return

        if current_term in global_visited:
            return

        for nested_term in glossary[current_term].get("nested_references", []):
            if nested_term in current_path:
                loop_idx = current_path.index(nested_term)
                loop = current_path[loop_idx:] + [nested_term]
                circular_loops.add(" -> ".join(loop))
            else:
                dfs(nested_term, current_path + [nested_term])

        global_visited.add(current_term)

    terms_list = list(glossary.keys())
    total_terms = len(terms_list)

    for i, term in enumerate(terms_list):
        if i > 0 and i % 50 == 0:
            print(f"  ... Checked {i}/{total_terms} definitions...")
        dfs(term, [term])

    warnings["Circular_References"] = list(circular_loops)
    if circular_loops:
        print(f"  [WARNING] Found {len(circular_loops)} circular loops. Bypassed successfully.")
    else:
        print("  [PASS] No circular references detected.")

    print("\n[Audit 2/3] Auditing Phase 1 Pointers...")
    ref_pattern = re.compile(r"\[\$REF:\s*([^\]]+)\]")
    pointer_count = {"checked": 0}

    def find_pointers(node):
        if isinstance(node, dict):
            for value in node.values():
                find_pointers(value)
        elif isinstance(node, list):
            for item in node:
                find_pointers(item)
        elif isinstance(node, str):
            for match in ref_pattern.findall(node):
                pointer_count["checked"] += 1
                if match not in glossary:
                    warnings["Dangling_Pointers"].append(match)

    find_pointers(covenants)
    warnings["Dangling_Pointers"] = list(set(warnings["Dangling_Pointers"]))

    if warnings["Dangling_Pointers"]:
        print(f"  [FAIL] Found {len(warnings['Dangling_Pointers'])} dangling pointers.")
    else:
        print(f"  [PASS] All {pointer_count['checked']} pointers perfectly resolved.")

    print("\n[Audit 3/3] Auditing Quantitative Data Types...")
    type_violation_count = 0

    for cov in covenants:
        data = cov.get("Extracted_Data", {})
        for key, value in data.items():
            if "limit" in key and value is not None:
                if not isinstance(value, (int, float)):
                    warnings["Type_Violations"].append(
                        f"{cov.get('Agent')} -> {key} is a {type(value).__name__} (Expected int/float)"
                    )
                    type_violation_count += 1

    if type_violation_count > 0:
        print(f"  [FAIL] Found {type_violation_count} mathematical type violations.")
    else:
        print("  [PASS] All limits are strictly numeric (int/float).")

    total_warnings = sum(len(v) for v in warnings.values())
    payload["Document_Metadata"]["Audit_Status"] = "Clean" if total_warnings == 0 else "Warnings_Detected"
    payload["Document_Metadata"]["Warnings"] = warnings

    with open(payload_path, "w", encoding="utf-8") as out:
        json.dump(payload, out, indent=2)

    end_time = time.time()
    print("\n==================================================")
    print(f"Audit Complete in {(end_time - start_time):.3f} seconds.")
    print(f"Final Status: {payload['Document_Metadata']['Audit_Status']}")
    print("==================================================")


def run_audit(paths: PipelinePaths) -> Path:
    """Run database audit on compiled payload (in-place update)."""
    require_file(paths.compiled, "Compiled payload JSON")
    run_database_audit(paths.compiled)
    return paths.compiled
