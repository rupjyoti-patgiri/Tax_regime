# Final Design: Hybrid Income-Tax Engine (The "LLM-Sandwich")

## 1. Executive Summary
To serve 100,000 users reliably, this system adopts a **Hybrid Architecture ("LLM-Sandwich")**. It strictly separates unstructured natural language processing from deterministic mathematics. There is no prize for using AI where it is objectively worse; therefore, LLMs are used exclusively for semantic extraction and communication, while mathematical execution and legal compliance are strictly delegated to a deterministic Python rule engine.

## 2. Architecture & Component Breakdown

### A. The Input Extractor (Component: LLM)
*   **Role:** Parses unstructured, multilingual (e.g., Hinglish) user input into a strict JSON schema.
*   **Task 3 Implementation:** Acts as a gatekeeper. If required data (like Basic Pay vs. HRA split, or City Type) is missing, it sets `is_complete: false` and generates a contextual clarifying question rather than hallucinating assumptions.
*   **Justification:** Deterministic regex/NLP rules fail entirely at parsing conversational Hinglish, contradictory statements, or implied financial constraints. An LLM is the only viable tool here.

### B. The Tax Calculator (Component: Rule)
*   **Role:** A pure Python function that takes validated JSON and computes deductions, HRA exemptions, tax slabs, rebates, and marginal relief. 
*   **Justification (Based on Task 4 Metrics):**
    *   **Accuracy & Determinism:** Method 1 (Rules) scored 100% Rupee-exact accuracy and was 100% deterministic across 10 loops. Method 2 (LLM query-time) failed on edge cases (specifically Surcharge Marginal Relief and the 25% surcharge cap in the New Regime) and produced varying numbers across 10 runs.
    *   **Latency:** Rules run in `< 1 ms`. The LLM runtime math took `~2-4 seconds` per query. At 100,000 users, LLM compute time becomes a massive UX bottleneck.
    *   **Cost:** Rules cost `$0.00` in API fees. Query-time LLMs cost `~$0.30 - $0.50` per 1,000 requests. 
    *   **Traceability:** Legal compliance requires traceability. If a user questions their tax liability, Method 1 traces every rupee back to a specific rule in `config.py`. Method 2 (LLM) is a black box (0% traceable).

### C. The Output Explainer (Component: LLM)
*   **Role:** Takes the deterministic JSON output and writes a friendly, conversational explanation (e.g., "Aapka tax 0 hai New Regime me!").
*   **Justification:** Providing a cold JSON payload is poor UX. Prompting a cheap, fast LLM (like Gemini 1.5 Flash) with *pre-computed numbers* allows for a human-like response with zero risk of mathematical hallucination.

## 3. Evaluation of Discarded Architectures

*   **Why not Method 2 (LLM at Query-Time)?** 
    LLMs are statistical engines, not calculators. While they understand tax concepts, they fail at multi-step arithmetic constraints (e.g., calculating HRA exemption using minimums of three different formulas, then cascading that into marginal relief). A silent failure here means illegal tax advice.
*   **Why not Method 3 (LLM-Compiled Rules)?** 
    Using an LLM to write the Python code one-time is excellent for rapid prototyping. However, we cannot blindly deploy LLM-compiled code. It requires intense human code-review. Furthermore, if the code breaks, the developer must debug machine-generated logic rather than a cleanly authored, human-readable configuration file. 

## 4. Surviving The Budget (Task 5: The Law Change)

During Task 5, we simulated the shift from the FY 2024-25 rules to the FY 2025-26 rules (which introduced a ₹75,000 standard deduction, altered slabs, and expanded the 87A rebate to ₹12 Lakhs).

**How the architectures coped:**
*   **Method 2 (LLM):** Struggled immediately. LLMs suffer from pre-training bias. Even when provided the exact FY26 rules in the prompt, the LLM occasionally defaulted to its pre-trained FY24 knowledge, causing **silent failures** (confident, but mathematically wrong answers). 
*   **Method 1 (Our Hybrid Engine):** Survived flawlessly. Updating the engine required changing exactly one file (`config.py`). Because the business logic (slabs, limits, percentages) is entirely decoupled from the extraction and explanation layers, the update took 2 minutes, required no prompt re-engineering, and guaranteed 100% accuracy immediately upon deployment.

**Future-Proofing Protocol:**
To keep the system correct through the next Budget, we simply create an `FY_2026_27` dictionary in `config.py`. The LLMs (Extractor and Explainer) require zero updates, as their job is purely semantic, isolating all legal risk to a single, auditable configuration file.