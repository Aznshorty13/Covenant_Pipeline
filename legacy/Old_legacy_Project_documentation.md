# **Table of Contents** {#table-of-contents}

[Table of Contents	1](#table-of-contents)

[Road Map: Credit Agreement	2](#road-map:-credit-agreement)

[Stage 1: Sketch Solution for Specific Example \- Hallador	3](#stage-1:-sketch-solution-for-specific-example---hallador)

[Overview of Pipeline	3](#overview-of-pipeline)

[Phase 0	4](#phase-0)

[Ingestion & Structural Slicing (The Python Chunker)	4](#ingestion-&-structural-slicing-\(the-python-chunker\))

[Phase 1	4](#phase-1)

[The Cascading Waterfall Router (Phase 1 Entry)	4](#the-cascading-waterfall-router-\(phase-1-entry\))

[The Parallel Extraction Agents (Node D)	5](#the-parallel-extraction-agents-\(node-d\))

[The Rater Agent (Node D)	5](#the-rater-agent-\(node-d\))

[Phase 2	5](#phase-2)

[The Deterministic Glossary Engine (Node H)	5](#the-deterministic-glossary-engine-\(node-h\))

[The Fuzzy Relational Compiler (Node I)	6](#the-fuzzy-relational-compiler-\(node-i\))

[Phase 3	6](#phase-3)

[The Automated Integrity Auditor (Node J)	6](#the-automated-integrity-auditor-\(node-j\))

[The Exception Layer: Validation Agent (Node L)	6](#the-exception-layer:-validation-agent-\(node-l\))

[The Terminal UI (Node M)	7](#the-terminal-ui-\(node-m\))

[Diagram Node Legend (V2 Architecture)	7](#diagram-node-legend-\(v2-architecture\))

[Stage 0: The Real-World Problem	9](#stage-0:-the-real-world-problem)

[The Process	9](#the-process)

[Abrigo	10](#abrigo)

[Credit Risk Functions	10](#credit-risk-functions)

[Risk Analyst	10](#risk-analyst)

[Covenants	10](#covenants)

[The MVP Covenant Target List	10](#the-mvp-covenant-target-list)

[Other Covenants	11](#other-covenants)

[Documents	12](#documents)

[Credit Agreements	12](#credit-agreements)

[Stage 2: Technichal Implementation	12](#stage-2:-technichal-implementation)

[PDF Chunker Guide	12](#pdf-chunker-guide)

[Deterministic Bounding Box Pipeline: EDGAR PDF Extraction	12](#deterministic-bounding-box-pipeline:-edgar-pdf-extraction)

[Deterministic Bounding Box Pipeline: Automated Verification Engine	15](#deterministic-bounding-box-pipeline:-automated-verification-engine)

[Extraction\_PDF\_Chunker	16](#extraction_pdf_chunker)

[Result and Architectural Overview	16](#result-and-architectural-overview)

[Step-by-Step Documentation & Reasoning	16](#step-by-step-documentation-&-reasoning)

[Auditing	17](#auditing)

[Result and Architectural Overview	17](#result-and-architectural-overview-1)

[Step-by-Step Documentation & Reasoning	17](#step-by-step-documentation-&-reasoning-1)

[Result and Architectural Overview	19](#result-and-architectural-overview-2)

[Step-by-Step Documentation & Reasoning	19](#step-by-step-documentation-&-reasoning-2)

[Multi-Tier Deterministic Routing Pipeline	20](#multi-tier-deterministic-routing-pipeline)

[System Overview	20](#system-overview)

[Part 1: Tier 1 (Deterministic Matrix Router)	20](#part-1:-tier-1-\(deterministic-matrix-router\))

[Part 2: Advanced Pipeline Logic & Edge Cases	21](#part-2:-advanced-pipeline-logic-&-edge-cases)

[Additional Notes	22](#additional-notes)

[Agent Covenant Extraction Architecture Documentation	22](#agent-covenant-extraction-architecture-documentation)

[Pipeline Phase 2: Deterministic Glossary Engine	24](#pipeline-phase-2:-deterministic-glossary-engine)

[Pipeline Node I: Fuzzy Relational Compiler	25](#pipeline-node-i:-fuzzy-relational-compiler)

[Pipeline Phase 3: Automated Integrity Auditor	26](#pipeline-phase-3:-automated-integrity-auditor)

[Node L Validation Agent	28](#node-l-validation-agent)

[Module 1: Configuration & Schemas	28](#module-1:-configuration-&-schemas)

[Module 2: Utilities & Authentication	28](#module-2:-utilities-&-authentication)

[Module 3: Data Ingestion & Rehydration	28](#module-3:-data-ingestion-&-rehydration)

[Module 4: The Audit Engine	29](#module-4:-the-audit-engine)

[Module 5: Orchestration (The Pipeline)	29](#module-5:-orchestration-\(the-pipeline\))

[Execution Block	29](#execution-block)

[Frontend UI	30](#frontend-ui)

[Appendix	32](#appendix)

[The Actor-Critic Validation Paradigm	32](#the-actor-critic-validation-paradigm)

[Application to the Credit Agreement Pipeline	33](#application-to-the-credit-agreement-pipeline)

[Personal Work Flow	35](#heading=h.le9j3va3za77)

[ETC	35](#old)

# 

# 

# **Road Map: Credit Agreement** {#road-map:-credit-agreement}

**Stage 0: Learning the Real Word Environment and Problem**

* Gets better if given real information  
  * How does Texas Capital input information

**Stage 1: Sketch Solution for Specific Example \- Hallador**

* Keep Generalization In Mind

**Stage 2: Implementation of Solution/ PoC**

**Stage 3: Sketch Scaling of Solution to outside Hallador**  
**Stage 4: Implementation of Scaling Solution/ PoC**

**Stage 5: Enterprise Integration**

# 

# **Stage 1: Sketch Solution for Specific Example \- Hallador** {#stage-1:-sketch-solution-for-specific-example---hallador}

## **Overview of Pipeline** {#overview-of-pipeline}

## **Phase 0** {#phase-0}

### **Ingestion & Structural Slicing (The Python Chunker)** {#ingestion-&-structural-slicing-(the-python-chunker)}

* **The Problem:** Feeding an entire 150-page PDF to an LLM causes token saturation, high API latency, and output truncation. Furthermore, unstructured text cannot be audited.  
* **The Execution:** A Python Document Chunker deterministically slices the PDF using structural boundaries, physically isolating Article 1 (Definitions) from Article X (Covenants). The chunker attaches an immutable metadata payload (Article Name, Section Number, Page Number, and the raw source text) to every single chunk.  
* **The Result:** Agents ingest strictly bounded, highly relevant text blocks that are permanently tethered to their physical location in the original document, which propagates as a high-resolution `Receipt` through the entire pipeline.

## **Phase 1** {#phase-1}

### **The Cascading Waterfall Router (Phase 1 Entry)** {#the-cascading-waterfall-router-(phase-1-entry)}

* **The Problem:** Relying on generative LLMs to classify raw legal text is cost-prohibitive and slow, while standard string searches trigger false positives (cross-references) and fail when multiple distinct covenants are compressed into single paragraphs.  
* **The Execution:** Document chunks cascade through a non-destructive, three-tiered routing engine governed by confidence thresholds.  
  * **Tier 1 (Deterministic Matrix):** Utilizes zero-cost Python Pandas logic (broad-net Article Zones AND strict Section Titles) to filter text into independent target pools, allowing one chunk to trigger multiple agents safely.  
  * **Tier 2 (Metadata-Constrained Hybrid Retrieval):** Triggered strictly as a fallback when Tier 1 deterministic routing encounters an ambiguity or missing section. It first applies broad metadata constraints (e.g., isolating specific legal Articles) to radically reduce the searchable corpus. It then executes a Hybrid Search algorithm—fusing Dense Semantic Vectors with Sparse Lexical scoring (e.g., BM25/TF-IDF)—to ground the semantic intent with exact legal terminology. This eliminates the hallucination risk of pure vector search and successfully isolates a highly accurate Top-K candidate subset.   
  * **Tier 3 (LLM Re-Ranker & Classifier):** Handles Tier 2 outputs dynamically. For high-confidence subsets, it acts strictly as a tie-breaker to select the correct chunk. For low-confidence states, it executes fallback logic by either registering a True Negative (omitted covenant) or processing the entire valid zone as a broad-context classifier.  
  * Note: It might be better to do Tier 3 if Tier 1 fails. But use Regex on the entire document to see what chunks pop up so we can focus the attention.  
* **The Result:** Deterministically reduces 150-page documents to highly isolated extraction envelopes. This architecture eliminates context-based hallucination, prevents false-positive data drops, and minimizes API expenditure by restricting generative AI to pure extraction, precise tie-breaking, or controlled broad-context evaluation.  
* **Note:** One should think of the Extraction Agents (Covenant List) goes to the router so that the router chooses the correct chunks.  
  * This is in contrast to the Chunks all going through the router, and the router has to assign chunks to the extraction agent.  
  * Namely to each agent we assign a chunk rather than for each chunk we assign an extraction agent.

.

### **The Parallel Extraction Agents (Node D)** {#the-parallel-extraction-agents-(node-d)}

* **The Problem:** Generative extraction is prone to dropped clauses, hallucinated pointers, and the loss of data provenance (the "black box" problem).  
* **The Execution:** Three parallel Extraction Agents are spawned for complex chunks, using slightly varied temperatures. They are strictly prompted to extract the mathematical root nodes and insert `[$REF: Term]` tags for missing variables. They are additionally forced to append the chunk's metadata (Page, Section) and the exact source text they read into the final JSON output.  
* **The Result:** Produces three competing JSONs that contain both the mathematical framework and the hardcoded, auditable "receipts."

### **The Rater Agent (Node D)** {#the-rater-agent-(node-d)}

* **The Problem:** The pipeline cannot blindly trust the output of any single extraction agent, especially on high-ambiguity chunks.  
* **The Execution:** A separate, isolated LLM evaluates the original source text against the three JSON outputs generated by the Extraction Agents. It evaluates strictly on fidelity: *“Which JSON captures all root nodes accurately, passes through the metadata perfectly, and hallucinates zero reference tags?”*  
* **The Result:** Only the highest-scored, fully vetted JSON is passed down the pipeline.

  ## **Phase 2** {#phase-2}

  ### **The Deterministic Glossary Engine (Node H)** {#the-deterministic-glossary-engine-(node-h)}

* **The Problem:** Extracting a 300+ term glossary using an LLM on-demand is computationally expensive, slow, and prone to hallucinated text or missed dependencies.  
* **The Execution:** A pure Python script executes a single sweep of the isolated Article 1 text. It uses Regex targeting standard legal definition formatting (`"Term" means...`) to extract the exact text blocks for every defined term. It then utilizes a dynamic plural-aware Regex boundary search to map the exact dictionary keys to their respective textual occurrences within the definitions.  
* **The Result:** Deterministically generates a perfect, flat relational dictionary (`resolved_definitions.json`) containing the raw text and explicitly nested references for every term in the document in fractions of a second, with zero API cost.

  ### **The Fuzzy Relational Compiler (Node I)** {#the-fuzzy-relational-compiler-(node-i)}

* **The Problem:** LLM extraction agents in Phase 1 output probabilistic placeholder tags (e.g., `[$REF: Permitted Acquisitions]`). Because LLMs hallucinate plurals and standard formatting, strict string matching fails when linking to the deterministic Phase 2 dictionary.  
* **The Execution:** A recursive Python script traverses the Phase 1 JSON tree. Upon locating a `[$REF: Term]` tag, it applies a three-tier fallback sequence against the Phase 2 dictionary keys: 1\) Exact Match, 2\) Base Word Strip (removing trailing 's'), and 3\) Fuzzy String Matching (`difflib` with a cutoff threshold).  
* **The Result:** Successfully maps AI-generated placeholders to strict database keys, mutating the Phase 1 JSON in memory to correct typographical errors before merging the Phase 1 Math and Phase 2 Dictionary into a single, flat relational schema (`final_compiled_payload.json`).

  ## **Phase 3** {#phase-3}

  ### **The Automated Integrity Auditor (Node J)** {#the-automated-integrity-auditor-(node-j)}

* **The Problem:** Compiling a flat relational database from highly interconnected legal text introduces vulnerabilities such as Circular References (infinite loops) and Dangling Pointers (unresolved links) which cause downstream failures in UIs or risk calculators.  
* **The Execution:** An independent Python script executes three sequential tests:  
  1. **Circular Reference Audit:** Executes a Depth-First Search (DFS) with a memory cache (`global_visited`) across the entire dictionary. If a traversal path loops, it logs the path and gracefully breaks the loop to prevent stack overflows.  
  2. **Pointer Audit:** Sweeps the final compiled payload to verify that no `[$REF]` tag exists without a corresponding key in the Master Glossary.  
  3. **Type Validation:** Verifies that all targeted quantitative fields (e.g., limits, ratios) are strict numerical classes (int/float) rather than strings.  
* **The Result:** Appends a strict diagnostic log to the JSON header metadata. The payload allows downstream systems to process valid math while identifying specific logical flaws in the source document without crashing the application.

### **The Exception Layer: Validation Agent (Node L)** {#the-exception-layer:-validation-agent-(node-l)}

* **The Problem:** "Silent" hallucinations can pass strict Pydantic data typing (e.g., extracting 1.25 instead of 1.50) but remain factually wrong.  
* **The Execution:** An independent LLM-as-a-Judge compares the final compiled JSON against the raw text stored in the metadata receipts. It does not overwrite data; it appends a "Confidence Score" (High/Low) and flags discrepancies.  
* **The Result:** Establishes strict data provenance and acts as the final AI safety net before human review.

### **The Terminal UI (Node M)** {#the-terminal-ui-(node-m)}

* **The Problem:** Human risk analysts cannot trust black-box AI outputs without verifying the source, but manually searching a 150-page PDF defeats the purpose of automation.  
* **The Execution:** The end-user dashboard displays the extracted JSON math and confidence flags alongside the raw source text and page numbers that the Extraction Agents passed down from the Python Chunker.  
* **The Result:** Human underwriters can verify the AI's logic, check the exact source clause, and approve complex covenant math in seconds rather than hours.

  ### **Diagram Node Legend (V2 Architecture)** {#diagram-node-legend-(v2-architecture)}

* **Node A:** Raw PDF Ingestion (Credit Agreement)  
* **Node B:** Python Document Chunker (Structural Slicing & Metadata Tagging)  
* **Node C1 & C2:** Sliced Text Payloads (Article 1 Definitions vs. Unassigned Chunks)  
* **Node R1, R2, R3:** The Waterfall Routing Gates (RegEx, Vector Similarity, LLM Classifier)  
* **Node D:** Parallel Extraction Agents (Phase 1 Covenant & Math Pass)  
* **Node E:** Phase 1 JSON Output (Root Nodes \+ `[$REF]` Tags)  
* **Node H:** Deterministic Glossary Engine (Phase 2 Pure Python Dictionary Builder)  
* **Node G:** Master Glossary JSON (Resolved Dictionary)  
* **Node F:** Fuzzy Relational Compiler (Phase 2 Linker & Schema Assembler)  
* **Node I:** Compiled JSON Database (Merged Flat Relational Schema)  
* **Node J:** Automated Integrity Auditor (Phase 3 Circular Loop & Type Validation)  
* **Node L:** Validation Agent / LLM-as-a-Judge (Confidence Scoring)  
* **Node M:** Terminal UI / Human Dashboard (Metadata Receipts & `[$REF]` Hyperlinks)

# **Stage 0: The Real-World Problem** {#stage-0:-the-real-world-problem}

## **The Process** {#the-process}

![][image1]

## **Abrigo** {#abrigo}

## **Credit Risk Functions** {#credit-risk-functions}

## 

## **Risk Analyst** {#risk-analyst}

## 

## **Covenants** {#covenants}

### **The MVP Covenant Target List** {#the-mvp-covenant-target-list}

**1\. Maximum Consolidated Total Leverage Ratio**

* **What it is:** The ratio of the company's total debt to its cash flow.  
* **Why it tests the pipeline:** This is the ultimate stress test for your Phase 2 Definition Linker. It forces the system to extract a float (e.g., `3.00`) and then successfully track down the deeply nested, highly complex legal definitions for `[$REF: Consolidated Total Debt]` and `[$REF: Consolidated EBITDA]`.

**2\. Minimum Fixed Charge Coverage Ratio (FCCR)**

* **What it is:** A measure of the company's ability to pay its fixed expenses (interest, lease payments) from its operating profit.  
* **Why it tests your pipeline:** It proves your Pydantic schema can handle dynamic logic. The AI must recognize that this limit is a **Minimum** (e.g., `1.25`), whereas the Leverage Ratio is a **Maximum**. It also tests a different set of nested variables, like `[$REF: Fixed Charges]`.

**3\. Maximum Capital Expenditures (CapEx) Limit**

* **What it is:** A hard cap on how much the company can spend on physical assets in a given fiscal year.  
* **Why it tests your pipeline:** It proves your pipeline can extract absolute dollar limits instead of just ratios. It forces your validation gate to handle large integers (e.g., `$15,000,000`) and resolves terms like `[$REF: Permitted Capital Expenditures]`.

### **Other Covenants** {#other-covenants}

**1\. Conditional Logic: Restricted Payments (Section 7.4)**

* **What it is:** The rules dictating when Hallador is allowed to pay cash dividends to its shareholders.  
* **The Hallador Text:** Section 7.4(b) states Hallador can make Restricted Payments *only if* the Total Leverage Ratio is $\\le$ 2.00 to 1.00 **and** Liquidity is $\\ge$ **$50,000,000**.  
* **Why it tests your architecture:** This is not a static limit; it is a boolean logic gate. It proves your Pydantic schema can extract nested, cross-referenced conditions. Your JSON wouldn't just extract a limit; it would extract a condition\_dependency array that points back to the Total Leverage and Liquidity root nodes.

**2\. Hard-Cap Dollar Limits: Investments & Acquisitions (Section 7.5)**

* **What it is:** Caps on how much money the company can spend buying other companies, creating joint ventures, or funding specific projects.  
* **The Hallador Text:** \* Section 7.5(n): Investments in "ERAS SPVs" cannot exceed **$200,000,000**.  
  * Section 7.5(p): "Other investments" cannot exceed **$50,000,000**.  
  * Definition of "Permitted Acquisition": Aggregate Acquisition Consideration cannot exceed **$50,000,000**.  
* **Why it tests your architecture:** It proves your validation gate handles large integer boundaries (200000000) just as smoothly as it handles float ratios (1.25). It also tests the pipeline's ability to extract specific categorical carve-outs (e.g., knowing the difference between an ERAS SPV investment and a general investment).

**3\. Nested Sub-Limits: Debt Incurrence (Section 7.1)**

* **What it is:** The maximum amount of additional debt the company can take on outside of this specific Texas Capital Bank loan.  
* **The Hallador Text:** \* Section 7.1(c): Capitalized Lease Obligations cannot exceed **$25,000,000**.  
  * Section 7.1(m): Subordinated Debt cannot exceed **$150,000,000**.  
* **Why it tests your architecture:** Standard LLMs often read Article 7, see the first dollar amount, and stop extracting. By targeting Section 7.1, you prove that your parallel Extraction Agents are thorough enough to extract an array of multiple, distinct sub-limits within a single section.

**4\. Operational Deadlines: Reporting Requirements (Section 6.1)**

* **What it is:** The Affirmative Covenants dictating exactly how many days the borrower has to submit their financials to the bank before triggering a technical default.  
* **The Hallador Text:**  
  * Section 6.1(a): Annual Financial Statements are due within **90 days** after the fiscal year-end.  
  * Section 6.1(b): Quarterly Financial Statements are due within **45 days** after the fiscal quarter-end.  
* **Why it tests your architecture:** This shifts the pipeline from pure math extraction to operational timeline extraction. It shows the product team that your architecture could easily feed into an automated calendar or tickler system for the underwriting team.

## 

## **Documents** {#documents}

### **Credit Agreements** {#credit-agreements}

# **Stage 2: Technichal Implementation** {#stage-2:-technichal-implementation}

## **PDF Chunker Guide** {#pdf-chunker-guide}

### **Deterministic Bounding Box Pipeline: EDGAR PDF Extraction** {#deterministic-bounding-box-pipeline:-edgar-pdf-extraction}

#### **Architecture Overview**

The pipeline decouples logical index extraction (TOC) from physical spatial mapping (Page Footers) to construct a deterministic bounding box for every legal section. This approach bypasses the inherent formatting anomalies, page-bleeding, and missing punctuation caused by HTML-to-PDF EDGAR conversions.

#### **Glossary of Core Concepts**

This pipeline exists to resolve the discrepancy between logical document flow and physical PDF structure caused by EDGAR HTML-to-PDF conversions. Understanding these three terms is required to understand the pipeline logic.

* **Printed Page:** The logical page number written in the text of the document's footer (e.g., `"CREDIT AGREEMENT - Page 52"`). This dictates the flow of the original document but has no direct correlation to the physical PDF structure.  
* **Absolute Page:** The physical, 1-indexed page number of the PDF file itself as read by a PDF engine (e.g., the 114th physical page in a 300-page file).  
* **Page Spread:** The realization that EDGAR conversions treat text as a continuous ribbon. Therefore, a single *Printed Page* physically spans across multiple *Absolute Pages* (e.g., Printed Page 52 exists from Absolute Page 113 to Absolute Page 114).

#### **Module 1: Pass 1 \- The TOC Skeleton (`build_simplified_skeleton`)**

**Action:** Scans the first 20 absolute pages of the PDF to extract the logical hierarchy (Article, Article Title, Section, Section Title, Printed Start Page).

**Core Logic & Mechanisms:**

* **Sequential Regex:** Captures the structural string and anchors to the printed page number at the end of the line.  
* **The Monotonic Page Drop (Kill Switch):** Tracks the highest printed page number seen. If the parsed page number drops by more than 2 (e.g., from Page 163 back to Page 5), the loop instantly breaks.

**Reasoning:**

* Attempting to parse headers directly from the main body is brittle due to cross-references and broken punctuation. Building a ground-truth "skeleton" first limits extraction to known entities.  
* The Monotonic Page Drop is necessary because hardcoded stop words (e.g., "ARTICLE 1") are unreliable in legal documents. Mathematical page drops guarantee the scanner has exited the TOC and hit body text, preventing false positives like capturing "Article 55" from a cross-reference.

#### **Module 2: Pass 1.5 \- The Continuous Ribbon Page Map (`build_page_spread_map`)**

**Action:** Scans the document to create a spatial dictionary mapping every Printed Page to a specific `[Absolute_Start_Page, Absolute_End_Page]` window.

**Core Logic & Mechanisms:**

* **The Offset Scan:** The `range(10, len(doc))` offsets the initial scan to start at Absolute Page 11, entirely skipping the TOC.  
* **Bottom-Up Parsing:** Reads the lines of each page in reverse (`reversed(lines)`) to instantly catch the footer regex.  
* **Continuous Ribbon Formula:** `Absolute_Start_Page = last_known_end + 1`. The start of a new printed page is mathematically bound to the absolute end of the previous one.  
* **Manual Edge Case Injection:** Seeds the dictionary state with Printed Page 1 \= `[Abs 11, Abs 12]` to account for the non-standard `LEGAL_US_W` preamble footer.

**Reasoning:**

* In EDGAR HTML-to-PDF conversions, printed pages do not map 1:1 with absolute pages. Text acts as a continuous ribbon, meaning a single printed page often spans across 2 or 3 absolute PDF pages.  
* The TOC offset prevents the "TOC Bleed" bug, where orphaned page numbers inside the TOC (e.g., "169") are falsely identified as page footers, which would corrupt the sequential chain.  
* The Continuous Ribbon Formula ensures zero absolute pages are dropped from the search space, even if a page break completely mangles the layout.

#### **Module 3: Pass 2 \- The Targeted Window Search (`calculate_exact_boundaries`)**

**Action:** Iterates through the Pass 1 Skeleton, looks up the bounding window in the Pass 1.5 Spread Map, and searches the raw PDF text to establish exact `Absolute_Start_Page` integers. Calculates the `Absolute_End_Page` mathematically.

**Core Logic & Mechanisms:**

* **Targeted Window Search:** Instead of scanning the whole document, the script only loads the 1-3 absolute pages defined by the Spread Map for that specific section.  
* **Spatial Interpolation (Null Fallback):** If a printed page is missing from the Spread Map, it calculates a fallback window ending at the start of the next known printed page.  
* **Bulletproof String Compression:** Strips all whitespace and lowercases both the PDF line and the target string before comparison (e.g., `section11.18` in `section11.18waiverofjurytrial`).  
* **The Pandas Shift:** Derives the `Absolute_End_Page` by shifting the `Absolute_Start_Page` column up by one row (`df.shift(-1)`).

**Reasoning:**

* Window Search solves the "Shared Page" problem. Pure page math (Option 1\) fails when Sections 1.4, 1.5, and 1.6 all exist on the same absolute page. Restricting the search window forces the regex to physically collide with the exact line boundary.  
* String Compression bypasses EDGAR spacing bugs where the PDF converter randomly injects spaces into numbers (e.g., converting "Section 11.18" into "Section 1 1.18") or smashes footers and headers into the same line.  
* The Pandas Shift works flawlessly for End Pages *only because* Pass 2 guarantees the Start Pages are strictly accurate to the physical line. Section A mathematically must end where Section B begins.

### **Deterministic Bounding Box Pipeline: Automated Verification Engine** {#deterministic-bounding-box-pipeline:-automated-verification-engine}

#### **Architecture Overview**

The Verification Engine acts as an independent auditing layer. It does not generate data; it blindly consumes the output artifact (`final_spatial_map.csv`) and cross-references it against the raw physical reality of the PDF. This ensures the extraction pipeline is 100% deterministic and free of spatial drift.

#### **Module 4: The Verification Engine (`verify_spatial_map`)**

**Action:** Iterates through every row of the generated spatial map, opens the PDF to the exact specified absolute page, and proves that the target section actually begins on that physical page.

**Step 1: Artifact Ingestion**

* **What it does:** Loads the final CSV into a Pandas DataFrame and opens the raw PDF using PyMuPDF.  
* **Reason:** By using the final CSV as the sole source of truth, it tests the actual output data, not the internal logic of the generation script.

**Step 2: String Compression & Normalization**

* **What it does:** Takes the target section string (e.g., `Section 11.18`) and the raw PDF text lines, converts both to lowercase, and removes all whitespace (resulting in `section11.18`).  
* **Reason:** EDGAR HTML-to-PDF conversions inject random spaces into numbers and smash headers into footers. Compressing the strings ensures the test evaluates the *content* rather than the *formatting*, preventing false negatives.

**Step 3: Strict Page-Bound Collision Testing**

* **What it does:** Extracts text *only* from the specific `Absolute_Start_Page` defined in the CSV. It evaluates the text line-by-line to find a compressed string match.  
* **Reason:** Validates the spatial coordinate system. If the script finds the string on the exact page specified, it mathematically proves the bounding box is physically accurate.

**Step 4: Audit Reporting**

* **What it does:** Tracks any section that fails the collision test and prints a summary report detailing the total success rate and the exact locations of the misses.  
* **Reason:** Provides immediate, actionable diagnostic data. If a row fails, you know exactly which section and page to investigate to patch the pipeline.

## **Extraction\_PDF\_Chunker** {#extraction_pdf_chunker}

### **Result and Architectural Overview** {#result-and-architectural-overview}

**Result:** This is the finalized, production-ready Pass 3 pipeline. It ingests the spatial map, calculates the exact logical page boundaries, cleanly extracts the target text using a State Machine, sanitizes the payload of physical PDF artifacts, and bifurcates the output into a Master Audit file (Silver Layer) and an AI Agent Payload (Gold Layer).

**Architectural Overview:** The code has been strictly refactored into four decoupled modules: Text Utilities, Metadata Operations, the Extraction Engine, and the Pipeline Orchestrator. This modularity allows you to unit-test the string compression or regex scrubbing independently of the heavy PyMuPDF document loading. It implements the Medallion Data Architecture paradigm, ensuring data provenance is never destroyed while simultaneously protecting downstream LLMs from context-window pollution.

### **Step-by-Step Documentation & Reasoning** {#step-by-step-documentation-&-reasoning}

#### **Module 1: Text Utilities**

* **`compress_string`**: Handles the zero-trust string matching requirement. Legal PDFs contain hidden spaces and zero-width characters. By aggressively lowercasing and stripping all whitespace, we ensure deterministic boundary matching regardless of physical document kerning.  
* **`clean_footer_artifacts`**: Implements the destructive cleanup. By utilizing Regex (`(?i)` for case insensitivity and `\s*` for variable whitespace), it systematically hunts down specific header/footer patterns and removes them. This guarantees the AI agents receive a pristine text string free of disruptive pagination metadata.

#### **Module 2: Metadata Operations**

* **`calculate_metadata_boundaries`**: Centralizes the structural logic. Applying `.shift(-1)` mathematically establishes the `Printed_End_Page` based on contiguous section flow. By handling this *before* extraction, we define the strict rules the extraction engine must follow.  
* **Column Reordering (`cols.insert`)**: Explicitly manipulating the pandas column list ensures the CSV schema remains highly readable for human data engineers. Placing `Printed_End_Page` directly next to `Printed_Start_Page` prevents cognitive overhead during visual EDA.

#### **Module 3: The Extraction Engine**

* **`extract_section_text`**: This is the isolated State Machine. By decoupling it from the pandas dataframe loop, it can be tested independently. It requires the physical `fitz.Document` object, precise page boundaries, and the logic strings.  
* **The Boolean Triggers**: `is_buffering` acts as the switch. It prevents the engine from accumulating text until the exact section header is crossed, and `section_completed` ensures the loop hard-breaks the moment the subsequent section is detected. This prevents multi-page sections from accidentally ingesting data past their assigned end-point.

#### **Module 4: Pipeline Orchestrator**

* **`run_pipeline`**: The central nervous system of Pass 3\. It orchestrates the loading of data, executes the extraction loop, and manages the Medallion output.  
* **The Silver/Gold Export**: By writing to `MASTER_CSV` first, we preserve the immutable "Bronze" data (`Raw_Text_Unscrubbed`) alongside the "Silver" text for human auditing. The script then actively drops the unscrubbed column to generate the `PAYLOAD_CSV`. This explicit separation of concerns protects downstream LLM prompt windows from context saturation while retaining full data provenance for human reviewers.

### **Auditing** {#auditing}

#### **End Page and Text vs Block**

### **Result and Architectural Overview** {#result-and-architectural-overview-1}

**Result:** The audit definitively proves two things about the Phase 3 extraction engine. First, the `.shift(-1)` logic is structurally sound; the extraction engine correctly halts *before* ingesting the final physical page footer on multi-page spans, resulting in a clean, surgical text cut. Second, the `Raw_Text_Stream` method is vastly superior to the `Raw_Text_Blocks` method for EDGAR PDFs, as the block method is highly vulnerable to catastrophic data loss from invisible overlapping bounding boxes (failing spectacularly on sections like 2.10).

**Architectural Overview:** This script functions as the automated Quality Assurance (QA) gate for Phase 3\. Instead of manually reading hundreds of pages, this auditing layer programmatically cross-references the pipeline's mathematical assumptions (the spatial map) against the physical reality of the extracted text. It establishes immediate data provenance and catches systemic parser failures before the payload is ever routed to the expensive, upstream generative AI agents in Phase 1\.

### **Step-by-Step Documentation & Reasoning** {#step-by-step-documentation-&-reasoning-1}

#### **1\. Establish Logical Ground Truth**

* **The Code:** `df['Printed_Start_Page'].shift(-1)` followed by the absolute delta calculation for the final index.  
* **The Reasoning:** Before you can audit an output, you must define the expected truth. Because the legal document is strictly sequential, the end of one section defines the boundary of the next. We calculate this in memory during the audit to ensure the original CSV metadata wasn't corrupted or altered during extraction.

#### **2\. The Regex Anchor Audit (Proving the Boundary)**

* **The Code:** `re.findall(r'Page\s+(\d+)', text, flags=re.IGNORECASE)` applied to the raw stream, extracting the final footer integer, then comparing it to the logical truth.  
* **The Reasoning:** We need to prove the State Machine halted correctly. If Section 1.1 mathematically ends on Page 49, the text payload should *not* contain the "Page 49" footer, because the buffer should have terminated midway down the page the exact millisecond it detected "Section 1.2". Filtering for mismatches (`footer_int != logic_int`) surfaces these exact occurrences, mathematically proving that the buffer is performing surgical cuts mid-page.

#### **3\. Text vs. Block Variance Audit (Catching Spatial Failures)**

* **The Code:** `abs(Stream_Len - Block_Len) / max_lens` applied across the dataframe.  
* **The Reasoning:** Relying on human intuition to evaluate two different text parsing libraries across 150 pages is impossible. By calculating the absolute string length of both columns and extracting the variance as a percentage, we can instantly sort the dataframe to surface catastrophic data loss. A variance of \>80% immediately flags that one of the extraction methods hit a fatal error (such as `PyMuPDF` blocks aborting due to a hidden HTML anchor).

#### **4\. Visual Diff Generator**

* **The Code:** `difflib.unified_diff()` passing in the `Stream` and `Block` payloads of the worst-performing row.  
* **The Reasoning:** Once the variance math flags a failure, a data engineer must see exactly what the algorithm dropped. `difflib` replicates standard Git behavior (highlighting additions and deletions), allowing you to visually verify whether a method dropped a single stray character or an entire critical covenant paragraph, without needing to open the raw CSV or PDF.

#### **Scrubbing Footers from Text**

### **Result and Architectural Overview** {#result-and-architectural-overview-2}

**Result:** This standalone script isolates and audits the `clean_footer_artifacts` regex transformation. It mathematically calculates the exact number of characters removed from each section and flags any rows where the deletion exceeds a safe heuristic limit, ensuring no vital covenant text was accidentally consumed.

**Architectural Overview:** In data engineering, this is known as a **Bronze-to-Silver Validation Check**. The `Raw_Text_Unscrubbed` column represents your immutable "Bronze" layer (the exact physical stream), while `Raw_Text_Clean` is your "Silver" layer (sanitized for the LLM). Because regex is inherently destructive, this script acts as a circuit breaker. It uses a Page-Span Heuristic to determine the maximum expected size of a footer, compares it to the actual characters dropped, and visually prints a diff of any anomalies. This ensures the generative AI agents in Phase 1 only receive mathematically proven data.

### **Step-by-Step Documentation & Reasoning** {#step-by-step-documentation-&-reasoning-2}

#### **1\. Exact Character Drop Calculation**

* **The Code:** `df['Unscrubbed_Len'] - df['Clean_Len']`  
* **The Reasoning:** The foundation of the audit. You cannot manage what you do not measure. By subtracting the length of the clean text from the raw text, we get an absolute integer representing the exact destructive footprint of our regex function.

#### **2\. The Page-Span Heuristic**

* **The Code:** `(df['Page_Span'] + 1) * 45`  
* **The Reasoning:** A blind character threshold (e.g., "flag anything over 100 characters") will trigger false positives. A section that spans 10 pages *should* have roughly 300 characters of footers removed. A section that stays on 1 page should have 0 or 30 characters removed. By multiplying the section's actual page span by a safe buffer of 45 characters, we dynamically create a custom, mathematically sound threshold for every single row.

#### **3\. Isolation of Over-Scrubbing**

* **The Code:** `df[df['Chars_Removed'] > df['Expected_Max_Removal']]`  
* **The Reasoning:** This acts as the circuit breaker. If the regex accidentally matched a vital clause that said `"Page 52 of the Annex"`, the `Chars_Removed` metric will spike above the expected limit, instantly isolating the row for human review.

#### **4\. The Visual Diff (The Terminal UI)**

* **The Code:** `difflib.unified_diff(unscrubbed_lines, clean_lines)`  
* **The Reasoning:** If an anomaly is flagged, knowing *that* it broke is useless without knowing *how* it broke. Pushing the two strings through `difflib` replicates a Git pull request view directly in your terminal. It highlights the exact string the regex deleted with a `-` sign, allowing you to instantly diagnose if the regex needs to be tightened without manually hunting through a massive CSV.

## **Multi-Tier Deterministic Routing Pipeline** {#multi-tier-deterministic-routing-pipeline}

### **System Overview** {#system-overview}

This document defines a retrieval-augmented routing pipeline designed to extract financial covenants from legal documents (e.g., LSTA Credit Agreements). The architecture utilizes a cascading waterfall methodology to isolate precise text chunks prior to generative LLM extraction, reducing API token expenditure and eliminating context-based hallucination.

### **Part 1: Tier 1 (Deterministic Matrix Router)** {#part-1:-tier-1-(deterministic-matrix-router)}

#### **Layer 1: Configuration (The Rulebook)**

**Action:** Business logic is maintained in an external JSON file (`covenant_config.json`).

* Defines `target_name` (maps to downstream Pydantic schemas).  
* Defines `valid_zones` (acceptable `Article_Title` boundaries).  
* Defines `section_title_triggers` (exact text or RegEx constraints).

**Reasoning:** Externalizing rules decouples business logic from execution code, permitting non-engineers to update extraction parameters without altering Python scripts. Constraining triggers to `Section_Title` rather than `Raw_Text` prevents false positive routing caused by document cross-references.

#### **Layer 2: Matrix Engine (The Tagger)**

**Action:** Evaluates the Layer 1 Rulebook against the ingested CSV utilizing vectorized Pandas operations.

* **Zone Gate (OR Logic):** Filters dataset by checking if `Article_Title` matches any defined `valid_zones`.  
* **Section Gate (OR Logic):** Checks if `Section_Title` matches the specified triggers.  
* **Filter (AND Logic):** The chunk must pass both the Zone Gate and the Section Gate to yield a positive match.

**Reasoning:** Vectorized matrix evaluation provides low-latency filtering. This step eliminates irrelevant document noise prior to API execution.

#### **Layer 3: Dispatcher (The Handoff)**

**Action:** Formats surviving dataframe rows into JSON Extraction Envelopes.

* Embeds the `Payload_Text`.  
* Assigns the target extraction instruction (e.g., `TotalLeverageRatioSchema`).  
* Appends document metadata (Page Number, Section Title) for auditability.

**Reasoning:** Generative LLMs require isolated, structured prompts. The Dispatcher translates tabular data into discrete API payloads for parallel agent execution.

### **Part 2: Advanced Pipeline Logic & Edge Cases** {#part-2:-advanced-pipeline-logic-&-edge-cases}

#### **Independent Target Pools (Multi-Covenant Sections)**

**Problem:** Unstructured legal boilerplate frequently combines multiple distinct covenants into a single paragraph. 

**Mechanism:** The Tier 1 Python loop evaluates every rule independently against the entire dataframe. A single text chunk containing terms for multiple targets receives independent tags and generates separate extraction envelopes. Data is non-destructive; chunks are not locked or consumed by a single global classification.

#### **Cascade Routing (Tier 1 Failures)**

**Problem:** Missing section metadata or OCR failures cause Tier 1 strict matching to return zero chunks. 

**Mechanism:** The pipeline utilizes a Cascade architecture rather than a Funnel. If Tier 1 returns zero matches for a target, it does not forward a filtered subset of "closest" guesses. It defaults to the Unassigned Pool (the entire remaining text bucket for that target's valid zones). Tier 2 initiates its search across this complete Unassigned Pool.

#### **Tier 2: Semantic Retrieval (Vector Search)**

**Action:** Functions as the primary fallback when exact-string matching (Tier 1\) fails. **Mechanism:** Converts the Unassigned Pool into mathematical vectors. Executes cosine similarity searches based on covenant concepts rather than explicit titles. This bypasses missing metadata by evaluating the semantic meaning of the raw text.

#### **Tier 3: LLM Re-Ranking (Top-K Tie-Breaker)**

**Action:** Resolves semantic ambiguity among high-probability Tier 2 results. **Mechanism:** If Tier 2 returns multiple candidates with tightly clustered confidence scores (e.g., Top-K retrieval), the subset is routed to a classifier LLM. The LLM evaluates only the top candidates and identifies the singular correct chunk. This resolves ties dynamically while minimizing the context window size and API costs compared to full-document LLM evaluation.

### **Additional Notes** {#additional-notes}

#### **1\. The Myth: "1 Section \= 1 Covenant"**

**The Problem:** In messy legal boilerplate, multiple covenants (e.g., Debt and Restricted Payments) are often smashed into a single paragraph under a generic heading like "General Provisions." 

**The Solution: Independent Target Pools.**

* The Tier 1 Python loop evaluates the document independently for every rule. It is **non-destructive**.  
* If a single paragraph contains both Debt and Dividends, the matrix tags it `True` for both. The router generates two separate dispatch envelopes for the exact same text, sending it to two different extraction agents. No data is lost or overwritten by a single global classification.

#### **2\. Architecture: Cascade vs. Funnel**

**The Problem:** If Tier 1 fails to find an exact match, how should the document be passed to Tier 2? 

**The Solution: The Cascade.**

* *Why Funnels Fail:* A funnel forces Tier 1 to pick the 10 "closest" chunks and pass them to Tier 2\. If Tier 1 failed because the formatting was weird, it is "blind" and will likely drop the correct chunk entirely. Tier 2 is left searching the wrong text.  
* *Why Cascades Win:* In a Cascade, if Tier 1 fails to find a specific covenant (e.g., CapEx), Tier 1 steps out of the way entirely. It hands Tier 2 the **Unassigned Pool** (the entire remaining text bucket for that Article) and tells Tier 2 to start its semantic search from scratch.

## **Agent Covenant Extraction Architecture Documentation** {#agent-covenant-extraction-architecture-documentation}

#### **Module 1: Environment & Configuration**

**Purpose:** Establishes the connection to the LLM and sets global execution parameters.

* **Model Selection:** `gemini-3.1-flash-lite` is hardcoded as the `EXTRACTION_MODEL`.  
  * *Reasoning:* Flash-tier models are optimized for high-volume, low-latency strict structured output (JSON mode) at a lower compute cost compared to Pro models.  
* **Pricing Constants:** Hardcodes `INPUT_PRICE_PER_MILLION` ($0.25) and `OUTPUT_PRICE_PER_MILLION` ($1.50) to allow for localized cost tracking without external API calls.

#### **Module 2: Pydantic Schemas (The Data Blueprints)**

**Purpose:** Forces the LLM to map unstructured legal text into highly rigid, predictable JSON structures.

* **Base Fields:** Every schema includes `is_false_flag`, `false_flag_reason`, and `is_applicable`.  
  * *Reasoning:* Provides a deterministic escape hatch. If the LLM is fed a cross-reference or boilerplate text, it flags it rather than hallucinating limits.  
* **Financial Covenants (e.g., Total Leverage, Fixed Charge):**  
  * Uses `Union[float, str]` for numerical limits.  
  * *Reasoning:* Allows the pipeline to extract a hard number (e.g., `2.5`) or safely catch a capitalized defined term as a string (e.g., `[$REF: Maximum Leverage]`) without throwing a type error.  
* **Negative Covenants (e.g., Liens, Mergers):**  
  * Implements the `UnifiedExceptions` nested schema containing `defined_term_refs` (List) and `inline_list_summaries` (List).  
  * *Reasoning:* Legal drafting varies. The document may point to an external definition ("except for Permitted Acquisitions") or list exceptions inline ("except (a) tax liens, (b) easements"). This pattern pushes the structural routing decision down to the LLM, preventing the need for complex pre-processing rules.

#### **Module 3: System Prompt Engineering**

**Purpose:** Contextualizes the LLM and sets strict operational rules for the extraction.

* **Dynamic Injection:** Uses `.format()` to inject the specific `agent_name`, the contextual `guardrail` definition from the CSV, and the clean `payload_text`.  
* **The Missing Variable Protocol:** Explicitly instructs the LLM to format unknown capitalized terms as `[$REF: Exact Term Name]`.  
  * *Reasoning:* Prevents the LLM from attempting to guess missing values and standardizes the output string so the downstream Node F (Pointer Aggregator) can easily parse and locate the missing terms using regex or string matching.

#### **Module 4: Cost Tracking Engine**

**Purpose:** Generates a verifiable audit trail for API usage.

* **Function:** `calculate_api_cost(usage_metadata)` intercepts the token counts directly from the Gemini API response object.  
* *Reasoning:* Enterprise data pipelines require granular unit economics. By appending this data directly to the extracted JSON payload, the system creates a permanent receipt of the exact computational cost to process a single covenant.

#### **Module 5: Execution Pipeline (The Dispatcher)**

**Purpose:** Routes the payloads to the LLM and manages file I/O.

* **The Input:** Ingests `dispatch_queue_output.json`.  
* **The Router:** Uses a `schema_router` dictionary to map the string-based `Agent` name from the queue to the corresponding Python Pydantic class.  
* **Sequential Loop:** Uses a standard `for` loop with a `time.sleep(2)` delay rather than concurrent threads.  
  * *Reasoning:* This is an intentional constraint for the Proof of Concept to adhere to the 15 Requests Per Minute (RPM) limit of the Gemini free tier, preventing `429 Too Many Requests` API crashes. In a production environment with paid limits, this module would be upgraded to `concurrent.futures.ThreadPoolExecutor` for parallel processing.  
* **The Output:** Dumps a final array containing the original receipt, the extracted data, and the cost metrics to `phase1_extracted_nodes.json`, which serves as the payload for Phase 2\.

## **Pipeline Phase 2: Deterministic Glossary Engine** {#pipeline-phase-2:-deterministic-glossary-engine}

**Module Goal:** To systematically extract every legally defined term from Article 1 of a credit agreement and mathematically link all nested references within those definitions without using an LLM.

**Architecture:** Pure Python, Regex-based extraction.

**Code Breakdown & Reasoning:**

* **`get_plural_regex(term: str) -> str`**  
  * **Function:** Dynamically generates a Regex pattern to match both the exact base word and its standard plural form.  
  * **Reasoning:** Prevents false-negative matching. If the dictionary defines "Subsidiary," but a text block uses the word "subsidiaries," a strict exact-match regex would miss the connection. This dynamically catches standard `s` plurals and words ending in `y` that change to `ies` (excluding vowel-y endings like "day").  
* **`build_deterministic_glossary(article_1_text: str) -> dict`**  
  * **Function 1 (The Sweep):** Uses the regex pattern `r'["“”]([^"“”]+)["“”]\s*(?:of\s+a\s+Person)?\s*means'` to locate the starting index of every single defined term in the raw text block.  
  * **Reasoning:** Credit agreements predictably format definitions as `"Term" means...`. This regex captures the term inside the quotes and accounts for standard legal formatting quirks (like "of a Person").  
  * **Function 2 (The Chipper):** Slices the text between the starting index of Term A and the starting index of Term B.  
  * **Reasoning:** This guarantees that the entire multi-paragraph definition is captured precisely without needing to arbitrarily guess the length of the definition.  
  * **Function 3 (The Deterministic Linker):** Sorts all extracted terms by length (descending). It then iterates through every definition's text and applies the `get_plural_regex` pattern to search for the presence of other master keys.  
  * **Reasoning (Sorting):** Sorting by length prevents a shorter term (like "Net Income") from being falsely flagged inside a longer composite term (like "Consolidated Net Income").  
  * **Reasoning (Regex over Fuzzy):** Because we are searching for an exact known master key within a massive block of text, `difflib` (fuzzy matching) is too computationally expensive. We rely on the smart plural regex to find deterministic matches instantly.  
* **Execution Block:**  
  * **Function:** Loads the Phase 0 extracted CSV, isolates rows marked as 'Article 1', concatenates them into a single string, and executes the engine.  
  * **Reasoning:** Ensures the dictionary is only built using the legal definitions section, avoiding false positives from the rest of the document.

## **Pipeline Node I: Multihop Relational Compiler**

**Module Goal:** To ingest the probabilistic math output from the Phase 1 AI agent, correct any hallucinated or pluralized `[$REF: ...]` tags, and relationally link them to the deterministic dictionary generated in Phase 2 (including dynamic injection of external sections).

**Architecture:** Python, Recursive Sweep, Fuzzy String Matching (`difflib`), Multi-Hop Dynamic Injector.

**Code Breakdown & Reasoning:**

* **`MultiHopRelationalCompiler` Initialization**  
  * **Function:** Loads `resolved_definitions.json` (Master Glossary) and the raw document chunks CSV. Builds a `toc_routing_index` by stripping numerical identifiers (e.g., "Section 1.1") from chunk titles to create a semantic lookup table.  
  * **Reasoning:** Establishes two distinct search spaces: the static definitions from Article 1 and the dynamic section text available for "Multi-Hop" injection if a reference points to an external clause (like Events of Default).  
* **`_resolve_term(raw_term: str)`**  
  * **Hop 1 (Exact Match):** Checks if the term exists in the Master Glossary.  
  * **Hop 2 (Multi-Hop Injection):** If the term matches a section title in the `toc_routing_index`, it dynamically injects the raw section text into the `master_glossary` as a new definition. Nested references are disabled for injected sections to prevent circular loops.  
  * **Hop 3 (Plural/Base Match):** Strips trailing 's' characters and checks the glossary for the base singular term.  
  * **Hop 4 (Fuzzy Semantic Match):** Uses `difflib.get_close_matches(..., cutoff=0.8)` to find the closest master key.  
  * **Hop 5 (Dangling Pointer Log):** If all hops fail, the term is added to a `dangling_pointers` set.  
  * **Reasoning:** This cascading strategy ensures the pipeline is robust against OOV (Out of Vocabulary) terms. Dynamic injection turns the glossary into a living data structure that expands to cover any cited section of the agreement, effectively solving "missing definition" hallucinations.  
* **`_process_string(text: str)` & `_traverse_and_mutate(node: Any)`**  
  * **Function:** A recursive visitor pattern that navigates through all nested dictionaries and lists in the Phase 1 JSON. It identifies all `[$REF: ...]` tags, resolves them via the 5-Hop engine, and overwrites the strings.  
  * **Reasoning:** The Phase 1 Pydantic schema generates highly nested structures (e.g., arrays of `step_downs` inside covenants). Recursion ensures 100% coverage of the payload hierarchy, ensuring every reference is standardized before reaching the UI.  
* **`compile(phase1_data_path: str, output_path: str)`**  
  * **Function:** Assembles the final production artifact. It triggers the recursive mutation, generates the final JSON containing `Document_Metadata` (with `Audit_Status` flag), `Phase1_Extracted_Covenants`, and the expanded `Phase2_Master_Glossary`.  
  * **Reasoning:** By separating the quantitative extraction from the textual reference resolution, we maintain a clean separation of concerns. This "Assembler" pattern ensures the downstream React frontend receives a single, unified, and audit-ready payload (`final_compiled_payload.json`) that is immediately ready for database ingestion.  
* Note: No need to overwrite strings, in future build just have the tagged data separate.

## **Pipeline Phase 3: Automated Integrity Auditor** {#pipeline-phase-3:-automated-integrity-auditor}

**Module Goal:** To independently verify the relational integrity, mathematical type-safety, and computational stability of the compiled JSON payload before it is passed to a downstream database or frontend UI.

**Architecture:** Python, Graph Traversal (DFS with Memoization), Data Type Validation.

**Code Breakdown & Reasoning:**

* **`dfs(current_term, current_path)` & Circular Reference Detection**  
  * **What it does:** Executes a Depth-First Search (DFS) algorithm to trace the `nested_references` of every term in the glossary. It tracks the active traversal chain in `current_path`. If it encounters a term already in `current_path`, it records the loop and stops traversing that branch (Graceful Degradation/Fail-Soft).  
  * **Reasoning:** Legal documents contain naturally occurring circular definitions (e.g., "Person" references "Governmental Authority", which references "Person"). If a downstream UI tries to recursively open these links, it will cause a Stack Overflow and crash the browser. This algorithm safely identifies these loops so the UI knows where to stop expanding.  
  * **Memoization (`global_visited` set):** Once a term's entire tree is verified as safe, it is added to `global_visited`. If the DFS encounters this term again through a different path, it skips it.  
  * **Reasoning:** In a highly interconnected glossary of 300+ terms, there are millions of overlapping paths. Without memoization, verifying all paths takes minutes. With memoization, it takes milliseconds.  
* **`find_pointers(node)` & Pointer Audit**  
  * **What it does:** Recursively sweeps the Phase 1 quantitative JSON object looking for the regex pattern `r'\[\$REF:\s*([^\]]+)\]'`. For every match found, it checks if the extracted term exists as an exact key in the Phase 2 Master Glossary. If not, it is logged as a "Dangling Pointer."  
  * **Reasoning:** Acts as a direct QA test on the Node I Relational Compiler. If the Phase 1 AI hallucinated a term so badly that even the Fuzzy Matcher couldn't salvage it, this function catches the broken link. It guarantees that no dead hyperlinks will be presented to the end user.  
* **Quantitative Data Type Validation**  
  * **What it does:** Iterates through the Phase 1 extracted math fields. Specifically targets keys containing the substring "limit". It runs an `isinstance(value, (int, float))` check on the payload values.  
  * **Reasoning:** Downstream financial software (like risk calculators or loan origination systems) require strict numeric types to execute math. If the LLM hallucinated a string (e.g., `"50,000,000"` instead of `50000000.0`), it will crash the downstream software. This audit guarantees strict schema type-adherence.  
* **Diagnostic Metadata Injection**  
  * **What it does:** Aggregates all circular loops, dangling pointers, and type violations. If any are found, it mutates the JSON header to `"Audit_Status": "Warnings_Detected"` and appends the exact error logs into a `"Warnings"` dictionary.  
  * **Reasoning:** Creates an immutable, machine-readable audit trail. It allows a database administrator or frontend developer to instantly assess the health of the data payload by reading the first 10 lines of the JSON, without having to manually parse the entire file.

  ## **Node L Validation Agent** {#node-l-validation-agent}

  ### **Module 1: Configuration & Schemas** {#module-1:-configuration-&-schemas}

* **What it does:** Defines global static constants (model selection, token pricing), the `AUDITOR_SYSTEM_PROMPT`, and the strict Pydantic model (`ValidationAudit`) which mandates the required fields: `is_verified`, `confidence_score`, `requires_human_context`, and `flagged_discrepancies`.  
* **Reasoning:** \* **Separation of Concerns:** Isolating static definitions from active logic loops prevents hardcoding "magic numbers" in the execution flow.  
  * **Schema Enforcement:** Wrapping the LLM output in a strict Pydantic model forces the probabilistic model to conform to a predictable relational database schema, ensuring downstream parsing does not fail.  
  * **Prompt Boundary:** The zero-shot prompt explicitly restricts the LLM to proofreading, forbidding it from acting as a financial analyst or recalculating math based on market standards.

  ### **Module 2: Utilities & Authentication** {#module-2:-utilities-&-authentication}

* **What it does:** Contains `initialize_client` to securely fetch the API key from the environment and initialize the Google GenAI client. Contains `calculate_api_cost` to track prompt and candidate token usage.  
* **Reasoning:** \* **Security:** Decoupling authentication prevents the accidental hardcoding of API keys in the execution logic, maintaining security for sensitive financial data.  
  * **Portability:** If the pipeline needs to migrate to a different LLM provider or SDK, only this specific module requires rewriting.  
  * **Cost Tracking:** Abstracting cost calculation into a dedicated function ensures deterministic tracking of the pipeline's computational overhead per execution.

  ### **Module 3: Data Ingestion & Rehydration** {#module-3:-data-ingestion-&-rehydration}

* **What it does:** `load_pipeline_data` ingests the raw CSV and the compiled JSON. `build_rehydration_db` uses Pandas to dynamically reconstruct the composite `Receipt` string from individual CSV columns (`Article`, `Section`, `Printed_Start_Page`, etc.). It applies a strict regex string normalization to both datasets and creates a lookup dictionary mapping the `Receipt` key to the `Raw_Text`.  
* **Reasoning:** \* **Database Normalization:** Storing heavy raw text inside the JSON payload bloats the database. Rehydrating the text just-in-time ensures a lightweight relational structure and guarantees the LLM only reads the necessary paragraphs.  
  * **Drift Prevention:** The regex string normalization (`.str.strip().str.replace(r'\s+', ' ', regex=True)`) is critical to prevent the Pandas join from silently failing due to invisible encoding artifacts or line breaks introduced during the initial PDF parsing.  
  * **Testability:** Separating ingestion and dictionary building makes it possible to unit-test the Pandas join logic independently of the LLM execution.

  ### **Module 4: The Audit Engine** {#module-4:-the-audit-engine}

* **What it does:** Contains `apply_chaos_injection` for adversarial testing and `execute_llm_audit` which handles formatting the prompt, executing the API call at `0.0` temperature, and parsing the response.  
* **Reasoning:** \* **Adversarial Provenance Testing:** "LLM-as-a-Judge" architectures are prone to rubber-stamping. The Chaos Injector temporarily mutates a known, correct numerical value in the JSON payload (e.g., changing `2.50` to `9.99`). This mathematically proves the system's integrity by forcing a discrepancy; if the LLM catches the injected error, it verifies the agent is actively cross-referencing the rehydrated `Raw_Text`.  
  * **Determinism:** Setting the temperature to `0.0` inside an isolated function ensures consistent, repeatable API behavior.

  ### **Module 5: Orchestration (The Pipeline)** {#module-5:-orchestration-(the-pipeline)}

* **What it does:** The `run_validation_pipeline` function acts as the controller. It dictates the execution sequence: loading data, building the rehydration database, iterating through the JSON nodes, stripping operational pipeline flags (`is_applicable`, `is_false_flag`), conditionally applying the adversarial test, calling the audit engine, catching API failures, and non-destructively appending the `Validation_Audit` object back to the JSON tree.  
* **Reasoning:** \* **Token Optimization:** Stripping internal pipeline routing flags before generating the prompt prevents LLM confusion and saves API tokens, forcing the model to focus entirely on auditing the mathematical values and `[$REF]` tags.  
  * **Resilience:** The `try/except` failsafe ensures pipeline stability; an API timeout will log a `requires_human_context: True` flag on that specific node rather than crashing the entire batch process.  
  * **Non-Destructive Appending:** Injecting the audit dictionary directly alongside the core data as a sibling node preserves the exact JSON schema integrity and relational links required for downstream UI ingestion.

  ### **Execution Block** {#execution-block}

* **What it does:** The `if __name__ == "__main__":` guard block triggers the pipeline with the required file paths and adversarial testing toggles.  
* **Reasoning:** Ensures that if this file is imported as a module into a larger master pipeline runner in the future, the code will not automatically execute upon import.

## **Frontend UI** {#frontend-ui}

**Module 1: Dependencies and Environment Setup**

* **What it does:** Imports React core hooks (`useState`, `useEffect`, `useMemo`) and `react-pdf` components. Assigns a local worker file URL to `pdfjs.GlobalWorkerOptions.workerSrc`.  
* **Why it's there:** Establishes the necessary libraries for state management and UI generation. The worker configuration is strictly required by Vite to process heavy PDF files on a background thread, preventing the browser from freezing during render.

**Module 2: Application State (`useState`)**

* **What it does:** Initializes memory blocks for the API payload, loading/error flags, the currently selected covenant, the active glossary term, and the total PDF page count.  
* **Why it's there:** Drives the React render cycle. When these variables update (e.g., user clicks a button, API data arrives), the UI automatically redraws to reflect the new data state.

**Module 3: Backend Initialization (`useEffect`)**

* **What it does:** Executes a `fetch` request to `http://127.0.0.1:8000/api/document-data` exactly once when the application mounts. Populates the `payload` state.  
* **Why it's there:** Bridges the decoupled architecture. Pulls the deterministic pipeline JSON from the local FastAPI server into the frontend's memory.

**Module 4: Data Transformation Engine (`useMemo`)**

* **`uniqueCovenants`**  
  * **What it does:** Scans `Phase1_Extracted_Covenants` and returns a filtered array containing only the first instance of each `Agent` name.  
  * **Why it's there:** Acts as a frontend deduplication filter to keep the UI queue clean while a permanent deduplication fix is implemented in the Python extraction pipeline.  
* **`pagesToRender`**  
  * **What it does:** Uses a Regular Expression (`/PDF Pages? (\d+)(?:-(\d+))?/`) to parse the `Receipt` string of the selected covenant and generates an array of integers (e.g., `[261, 262, 263]`).  
  * **Why it's there:** Converts a human-readable text reference into precise programmatic rendering instructions for the PDF viewer.  
* **`availableTerms`**  
  * **What it does:** Converts the extracted JSON to a string, runs a Regex search for `[$REF: ...]`, and cross-references the findings against `Phase2_Master_Glossary` (including nested references).  
  * **Why it's there:** Dynamically populates the glossary dropdown list based *only* on terms present in the currently selected covenant, preventing UI clutter.

**Module 5: Presentation Helpers**

* **`formatAgentName`**  
  * **What it does:** Utilizes Regex to insert a space before capital letters in a continuous string (e.g., "TotalLeverageRatio" \-\> "Total Leverage Ratio").  
  * **Why it's there:** Improves human readability of raw backend variables in the UI.  
* **`renderFormattedData`**  
  * **What it does:** A recursive function that maps over JSON objects and arrays to create HTML elements. Filters out specific metadata keys (`is_false_flag`, `confidence_score`, etc.) and highlights `[$REF: ]` tags in blue.  
  * **Why it's there:** Translates raw, nested JSON into a clean, human-readable hierarchy while acting as a filter to hide internal pipeline metadata from the end user.

**Module 6: UI Layout (3-Column Architecture)**

* **Column 1: Phase 1 Queue**  
  * **What it does:** Maps over `uniqueCovenants` to generate clickable navigation buttons. Splits the `Receipt` string at the pipe (`|`) to render the page target and article section on separate lines.  
  * **Why it's there:** Serves as the master navigation index for the analyst.  
* **Column 2: Document Provenance**  
  * **What it does:** Implements `<Document>` and `<Page>` from `react-pdf`. Fetches the raw PDF byte stream from the backend `/api/pdf` endpoint and maps over the `pagesToRender` array to draw stacked canvases.  
  * **Why it's there:** Provides visual proof of the extraction pipeline by displaying the source document scrolled to the exact target location.  
* **Column 3: Audit & Glossary**  
  * **What it does:** Calculates and displays a "Confidence Score" badge with conditional flag reasoning. Invokes `renderFormattedData` for the mathematical logic. Renders a `<select>` dropdown powered by `availableTerms` to display raw definition text.  
  * **Why it's there:** Distills mathematical logic and legal definitions into an actionable format for human review, separating data presentation from data processing.


### 

# **Appendix** {#appendix}

## **The Actor-Critic Validation Paradigm** {#the-actor-critic-validation-paradigm}

**Reference:** [Advancing Mathematics Research with AI-Driven Formal Proof Search](https://arxiv.org/html/2605.22763v1), May 2026, Google Deepmind

#### **1\. Deterministic Validation (The "Compiler")**

* **Concept:** Binary, hard-coded validation. The system either passes or fails based on strict rules.  
* **Mechanism:** Type-checking, schema enforcement (e.g., Pydantic), mathematical bounds, or syntax execution.  
* **Reasoning:** LLMs are probabilistic text engines; they do not "know" math or strict logic. To prevent hallucinations from cascading through a multi-step pipeline, the LLM must be sandboxed. Deterministic validation shifts the burden of absolute truth away from the LLM and onto traditional code.  
* **Limitation:** It is a binary gate. It cannot evaluate nuance, strategy, or the *quality* of an output, only its formatting and logic constraints.

#### **2\. Heuristic / Score-Based Validation (The "Rater Agent")**

* **Concept:** Decoupling generation from evaluation to score intermediate or "fuzzy" outputs.  
* **Mechanism:** Running parallel generation tasks and using a separate LLM (often a faster, cheaper model) to evaluate the outputs against a strict rubric, selecting the best one via a tournament or Elo style ranking.  
* **Reasoning:** LLMs struggle with generation (predicting a sequence of correct tokens from scratch) but excel at evaluation (analyzing an existing block of text against a set of rules). It is computationally cheaper and far more reliable to have an LLM spot a hallucination in a generated text than to prompt an LLM to never hallucinate in the first place.

### **Application to the Credit Agreement Pipeline** {#application-to-the-credit-agreement-pipeline}

By mapping the DeepMind research onto the ingestion and extraction DAG, the pipeline transforms from a single-shot script into a resilient, self-correcting system.

#### **Phase 1: The Extraction Tournament (Node D)**

* **The Problem:** High-ambiguity document chunks (falling to Tier 3\) are prone to dropped clauses or hallucinated `$REF` tags.  
* **The Execution:** Instead of a single extraction pass, spawn three parallel Extraction Agents for complex chunks, using slightly varied temperatures or focus prompts.  
* **The Rater Agent:** Takes the original source text and the three JSON outputs. Evaluates strictly on fidelity: *“Which JSON captures all root nodes accurately without hallucinating reference tags?”*  
* **The Result:** Only the highest-scored, vetted JSON is passed to the Linker phase.

#### **Phase 2: The Definition Linker Tournament (Node H)**

* **The Problem:** Legal definitions are heavily nested. Missing a recursive variable (e.g., a sub-definition of "Consolidated Net Income") breaks the entire pointer sequence.  
* **The Execution:** Spawn parallel Definition Agents to compile the Missing Variables List against the Article 1 text.  
* **The Rater Agent:** Evaluates the compiled outputs to determine which resolved all nested dependencies without leaving any dangling pointers or logical gaps.  
* **The Result:** Guarantees structural integrity before the data is assembled.

#### **Phase 3: The Deterministic Terminal Gate (Node J)**

* **The Problem:** You cannot push hallucinated or malformed data into a production database.  
* **The Execution:** The Pydantic Strict Gate acts as the absolute arbiter at the end of the pipeline.  
* **The Result:** Because the upstream Rater Agents (Nodes D and H) continuously filtered out poor extractions and broken links, the Pydantic gate receives high-quality, pre-vetted JSON. This drastically reduces fatal pipeline exceptions and the need for Tier 1 Auto-Heal (Node K) or human intervention (Node M).

Chat Link: [https://gemini.google.com/share/bbd58a7be3c8](https://gemini.google.com/share/bbd58a7be3c8)

Youtube video at later date:

[DeepMind’s New AI Found A Strange New Way To Think](https://www.youtube.com/watch?v=Dkqzqw8rxXI)

# **OLD** {#old}

## **Pipeline Node I: Fuzzy Relational Compiler** {#pipeline-node-i:-fuzzy-relational-compiler}

**Module Goal:** To ingest the probabilistic math output from the Phase 1 AI agent, correct any hallucinated or pluralized `[$REF: ...]` tags, and relationally link them to the deterministic dictionary generated in Phase 2\.

**Architecture:** Python, Recursive Sweep, Fuzzy String Matching (`difflib`).

**Code Breakdown & Reasoning:**

* **`fuzzy_link_references(phase1_data: list, glossary_keys: list)`**  
  * **Function 1 (The Traverse):** Recursively navigates through all nested dictionaries and lists in the Phase 1 JSON payload.  
  * **Reasoning:** The Phase 1 Pydantic schema produces deeply nested data (e.g., arrays of `step_downs` inside `Extracted_Data`). A recursive function ensures every single string is checked for a `[$REF]` tag regardless of where it lives in the JSON hierarchy.  
  * **Function 2 (The Processor \- Exact & Base Match):** Extracts the text inside the `[$REF: ...]` tag. It first checks if the exact string exists in `glossary_keys`. If it fails, it strips any trailing 's' and checks again.  
  * **Reasoning:** This is the first line of defense against the AI hallucinating plurals (e.g., `[$REF: Permitted Acquisitions]`). It is computationally cheaper than fuzzy matching and solves the majority of AI extraction errors.  
  * **Function 3 (The Processor \- Fuzzy Match):** If the exact and base word checks fail, it uses `difflib.get_close_matches(..., cutoff=0.8)` to find the closest master key. If a match is found, it uses `.replace()` to permanently overwrite the bad AI tag with the correct master key.  
  * **Reasoning:** This is the final safety net for complex typos, misspellings, or weird plurals (e.g., "Subsidiaries") generated by the AI. Mutating the data in memory ensures the final JSON output contains perfect relational links for downstream database ingestion.  
  * **Function 4 (Dangling Pointer Log):** If all three matching steps fail, the term is added to a `dangling_pointers` set.  
  * **Reasoning:** Acts as an audit trail. If a term truly cannot be linked, it prevents the compiler from failing silently and flags the term for manual review.  
* **`compile_final_payload(phase1_path: str, phase2_path: str, output_path: str)`**  
  * **Function:** Loads the Phase 1 (Math) JSON and Phase 2 (Dictionary) JSON. Extracts the keys from Phase 2 to use as the truth index. Runs the `fuzzy_link_references` function. Packages both datasets into a final flat relational schema.  
  * **Reasoning:** Modern data engineering dictates separating the quantitative math from the textual definitions to prevent JSON bloat. This script acts as the final assembler, linking the two distinct files into a single, clean database-ready artifact (`final_compiled_payload.json`). It also sets the `Audit_Status` flag in the metadata based on the presence of dangling pointers.

[image1]: <data:image/png;base64,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>