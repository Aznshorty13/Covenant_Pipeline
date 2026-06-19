"""Phase 0: PDF chunking and spatial mapping."""

from __future__ import annotations

import re
from pathlib import Path

import fitz
import pandas as pd

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.utils.io import require_file
from covenant_pipeline.utils.text import clean_footer_artifacts, compress_string


def calculate_printed_end_page(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Printed_End_Page and reorder columns."""
    df = df.copy()

    df["Printed_End_Page"] = df["Printed_Start_Page"].shift(-1)

    last_idx = df.index[-1]
    abs_start = df.loc[last_idx, "Absolute_Start_Page"]
    abs_end = df.loc[last_idx, "Absolute_End_Page"]
    printed_start = df.loc[last_idx, "Printed_Start_Page"]

    page_delta = abs_end - abs_start
    df.loc[last_idx, "Printed_End_Page"] = printed_start + page_delta
    df["Printed_End_Page"] = df["Printed_End_Page"].astype(int)

    cols = list(df.columns)
    cols.remove("Printed_End_Page")
    start_idx = cols.index("Printed_Start_Page")
    cols.insert(start_idx + 1, "Printed_End_Page")

    return df[cols]


def build_simplified_skeleton(pdf_path: str | Path, max_toc_pages: int = 20) -> pd.DataFrame:
    print("Pass 1: Building TOC Skeleton...")
    doc = fitz.open(pdf_path)

    full_text_buffer = ""
    for page_num in range(min(max_toc_pages, len(doc))):
        full_text_buffer += doc[page_num].get_text("text") + "\n"

    clean_buffer = re.sub(r"\.{2,}", " ", full_text_buffer)
    clean_buffer = re.sub(r'","', " ", clean_buffer).replace('"', "")

    toc_pattern = re.compile(
        r"(?P<type>Article|Section)\s+(?P<num>\d+(?:\.\d+)?)\.?\s+(?P<title>.{1,200}?)\s+(?P<page>\d+)(?=\n|$)",
        re.IGNORECASE | re.DOTALL,
    )

    matches = toc_pattern.finditer(clean_buffer)

    skeleton_data = []
    current_article = "Preamble"
    current_article_title = "Document Front Matter"
    highest_page_seen = 0

    for match in matches:
        item_type = match.group("type").title().strip()
        num = match.group("num")
        title = match.group("title").replace("\n", " ").strip()
        page = int(match.group("page"))

        if page < (highest_page_seen - 2):
            print("   -> TOC boundary detected. Stopping scan.")
            break

        highest_page_seen = max(highest_page_seen, page)

        if item_type == "Article":
            current_article = f"Article {num}"
            current_article_title = title
        elif item_type == "Section":
            skeleton_data.append(
                {
                    "Article": current_article,
                    "Article_Title": current_article_title,
                    "Section": f"Section {num}",
                    "Section_Title": title,
                    "Printed_Start_Page": page,
                }
            )

    return pd.DataFrame(skeleton_data)


def build_page_spread_map(pdf_path: str | Path) -> dict:
    print("Pass 1.5: Building Page Spread Map...")
    doc = fitz.open(pdf_path)
    footer_pattern = re.compile(r"(?:page\s*|^\s*-?\s*)(\d+)(?:\s*-?\s*$)", re.IGNORECASE)

    spread_data = [
        {
            "Printed_Page": 1,
            "Absolute_Start_Page": 11,
            "Absolute_End_Page": 12,
        }
    ]

    last_known_end = 12

    for page_num in range(10, len(doc)):
        absolute_page = page_num + 1
        lines = doc[page_num].get_text("text").split("\n")

        for line in reversed(lines):
            line_stripped = re.sub(r"\s+", " ", line).strip()
            if not line_stripped:
                continue

            match = footer_pattern.search(line_stripped)
            if match:
                printed_page = int(match.group(1))

                if not any(d["Printed_Page"] == printed_page for d in spread_data):
                    absolute_start = last_known_end + 1

                    spread_data.append(
                        {
                            "Printed_Page": printed_page,
                            "Absolute_Start_Page": absolute_start,
                            "Absolute_End_Page": absolute_page,
                        }
                    )

                    last_known_end = absolute_page

                break

    df_map = pd.DataFrame(spread_data)
    return df_map.set_index("Printed_Page")[["Absolute_Start_Page", "Absolute_End_Page"]].to_dict("index")


def calculate_exact_boundaries(
    pdf_path: str | Path,
    df_skeleton: pd.DataFrame,
    spread_map: dict,
    output_csv: str | Path,
) -> pd.DataFrame:
    print("Pass 2: Executing Targeted Window Search...")
    doc = fitz.open(pdf_path)

    df_skeleton = df_skeleton.copy()
    df_skeleton["Absolute_Start_Page"] = None

    for idx, row in df_skeleton.iterrows():
        section_target = str(row["Section"]).strip()
        printed_page = row["Printed_Start_Page"]

        spread = spread_map.get(printed_page)

        if not spread:
            future_pages = [p for p in spread_map.keys() if p > printed_page]
            abs_start = 1
            if future_pages:
                next_known_printed_page = min(future_pages)
                abs_end = spread_map[next_known_printed_page]["Absolute_Start_Page"]
            else:
                abs_end = len(doc)
        else:
            abs_start = spread["Absolute_Start_Page"]
            abs_end = spread["Absolute_End_Page"]

        found_exact_page = False

        for page_num in range(abs_start - 1, abs_end):
            lines = doc[page_num].get_text("text").split("\n")

            for line in lines:
                target_compressed = section_target.replace(" ", "").lower()
                line_compressed = re.sub(r"\s+", "", line).lower()

                if target_compressed in line_compressed:
                    df_skeleton.at[idx, "Absolute_Start_Page"] = page_num + 1
                    found_exact_page = True
                    break

            if found_exact_page:
                break

        if not found_exact_page:
            df_skeleton.at[idx, "Absolute_Start_Page"] = abs_start

    df_skeleton["Absolute_Start_Page"] = df_skeleton["Absolute_Start_Page"].astype(int)

    df_skeleton["Absolute_End_Page"] = df_skeleton["Absolute_Start_Page"].shift(-1)
    df_skeleton["Absolute_End_Page"] = df_skeleton["Absolute_End_Page"].fillna(len(doc))
    df_skeleton["Absolute_End_Page"] = df_skeleton["Absolute_End_Page"].astype(int)

    final_columns = [
        "Article",
        "Article_Title",
        "Section",
        "Section_Title",
        "Printed_Start_Page",
        "Absolute_Start_Page",
        "Absolute_End_Page",
    ]
    df_final = df_skeleton[final_columns]

    df_final.to_csv(output_csv, index=False)
    print(f"Map Built! Spatial mapping saved to: {output_csv}")

    return df_final


def run_extraction_engine(
    pdf_path: str | Path,
    df: pd.DataFrame,
    output_path: str | Path,
    payload_path: str | Path,
) -> Path:
    """Extract section text and export silver/gold CSV layers."""
    print("Pass 3: Initializing Production Extraction Engine...")

    df = calculate_printed_end_page(df)
    doc = fitz.open(pdf_path)

    for idx, row in df.iterrows():
        start_page = int(row["Absolute_Start_Page"]) - 1
        end_page = int(row["Absolute_End_Page"]) - 1

        current_section = compress_string(row["Section"])
        next_section = compress_string(df.loc[idx + 1, "Section"]) if idx + 1 < len(df) else None

        stream_buffer = []
        is_buffering = False
        section_completed = False

        print(f"Extracting {row['Section']} (Pages {start_page + 1} to {end_page + 1})...")

        for page_num in range(start_page, end_page + 1):
            if page_num >= len(doc) or section_completed:
                break

            page = doc[page_num]
            text_lines = page.get_text("text").split("\n")

            for line in text_lines:
                line_compressed = compress_string(line)

                if not line_compressed:
                    if is_buffering:
                        stream_buffer.append(line)
                    continue

                if not is_buffering and current_section in line_compressed:
                    is_buffering = True

                if is_buffering and next_section and next_section in line_compressed:
                    is_buffering = False
                    section_completed = True
                    break

                if is_buffering:
                    stream_buffer.append(line)

        raw_string = "\n".join(stream_buffer)
        clean_string = clean_footer_artifacts(raw_string)

        df.at[idx, "Raw_Text_Unscrubbed"] = raw_string
        df.at[idx, "Raw_Text_Clean"] = clean_string

    df.to_csv(output_path, index=False)

    payload_df = df.drop(columns=["Raw_Text_Unscrubbed"])
    payload_df = payload_df.rename(columns={"Raw_Text_Clean": "Raw_Text"})

    payload_path = Path(payload_path)
    payload_df.to_csv(payload_path, index=False)

    print("\nPipeline Complete!")
    print(f" -> Master audit file saved to: '{output_path}'")
    print(f" -> AI Payload generated and saved to: '{payload_path}'")

    return Path(payload_path)


def run_chunker(paths: PipelinePaths) -> Path:
    """Run Phase 0: TOC skeleton, page spread, boundaries, and extraction."""
    require_file(paths.pdf_path, "PDF file")

    skeleton_df = build_simplified_skeleton(paths.pdf_path)
    page_spread_dictionary = build_page_spread_map(paths.pdf_path)

    final_mapping_df = calculate_exact_boundaries(
        paths.pdf_path,
        skeleton_df,
        page_spread_dictionary,
        paths.spatial_map,
    )

    return run_extraction_engine(
        paths.pdf_path,
        final_mapping_df,
        paths.covenants,
        paths.phase1_payload,
    )
