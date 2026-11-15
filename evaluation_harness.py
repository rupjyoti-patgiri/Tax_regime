# evaluation_harness.py
import json
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv
from implementations.method_1_rules import calculate_tax
from implementations.method_2_llm import generate_llm_query_prompt

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Using flash to avoid instantaneous rate-limiting during 10x loop testing
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    generation_config={"response_mime_type": "application/json"}
)

# Cost Estimates for gemini-3.5-flash-lite (per 1M tokens)
COST_INPUT_1M = 0.075
COST_OUTPUT_1M = 0.30

def evaluate_implementations(max_cases=5):
    print("🚀 Starting Evaluation Harness: Task 4 Metrics...")
    
    with open('tests/test_cases.json', 'r') as f:
        test_cases = json.load(f)[:max_cases] # Limiting to prevent free-tier quota ban
        
    total_tests = len(test_cases)
    exact_matches = 0
    non_deterministic_count = 0
    
    total_rule_latency = 0
    total_llm_latency = 0
    
    total_input_tokens = 0
    total_output_tokens = 0

    traceability_log = {
        "method_1_rules": "100% Traceable. Every rupee maps directly to specific code logic and legal clauses (e.g., config.py -> HRA_RULES).",
        "method_2_llm": "0% Traceable. Black-box generation. Cannot mathematically prove how the LLM arrived at the final integer."
    }

    for idx, test in enumerate(test_cases):
        print(f"\n[{idx+1}/{total_tests}] Evaluating Case: {test['id']} (Income: ₹{test['financials']['basic_pay'] * 2})")

        # --- 1. BASELINE: DETERMINISTIC RULES ---
        start_rule = time.perf_counter()
        rule_result = calculate_tax(test, "FY_2025_26")
        total_rule_latency += (time.perf_counter() - start_rule)
        
        # --- 2. CHALLENGER: LLM QUERY-TIME (10x Loop for Determinism) ---
        prompt = generate_llm_query_prompt(test, "FY_2025_26")
        
        input_tokens = model.count_tokens(prompt).total_tokens
        total_input_tokens += (input_tokens * 10) # Billed for every run

        llm_runs = []
        start_llm = time.perf_counter()
        
        for i in range(10):
            try:
                response = model.generate_content(prompt)
                res_json = json.loads(response.text)
                llm_runs.append(res_json)
                total_output_tokens += model.count_tokens(response.text).total_tokens
            except Exception as e:
                print(f"  Run {i+1} Failed: JSON Parsing or API Error")
                llm_runs.append({"new_regime_tax": -1, "old_regime_tax": -1})
                
        total_llm_latency += ((time.perf_counter() - start_llm) / 10)

        # --- 3. METRICS GATHERING ---
        primary_llm_run = llm_runs[0]
        
        # Accuracy
        is_accurate = (
            primary_llm_run.get("new_regime_tax") == rule_result["new_regime_tax"] and
            primary_llm_run.get("old_regime_tax") == rule_result["old_regime_tax"]
        )
        if is_accurate:
            exact_matches += 1

        # Determinism (Did all 10 runs yield the exact same tax array?)
        is_deterministic = all(
            r.get("new_regime_tax") == primary_llm_run.get("new_regime_tax") and
            r.get("old_regime_tax") == primary_llm_run.get("old_regime_tax")
            for r in llm_runs
        )
        if not is_deterministic:
            non_deterministic_count += 1

        print(f"  Rule Output : New = ₹{rule_result['new_regime_tax']} | Old = ₹{rule_result['old_regime_tax']}")
        print(f"  LLM Output  : New = ₹{primary_llm_run.get('new_regime_tax')} | Old = ₹{primary_llm_run.get('old_regime_tax')}")
        print(f"  Accurate: {'✅' if is_accurate else '❌'} | Deterministic (10 runs): {'✅' if is_deterministic else '❌'}")

    # --- 4. FINAL REPORT (Task 4 Outputs) ---
    print("\n==================================================")
    print("📊 TASK 4: EVALUATION METRICS REPORT")
    print("==================================================")
    print(f"Accuracy (Rupee-Exact) : {(exact_matches / total_tests) * 100:.2f}%")
    print(f"Determinism (10x runs) : {((total_tests - non_deterministic_count) / total_tests) * 100:.2f}% stable")
    print(f"Latency per request (Method 1: Rules) : {(total_rule_latency / total_tests) * 1000:.3f} ms")
    print(f"Latency per request (Method 2: LLM)   : {(total_llm_latency / total_tests) * 1000:.3f} ms")
    
    # Calculate Cost per 1000 requests
    avg_input_per_req = total_input_tokens / (total_tests * 10)
    avg_output_per_req = total_output_tokens / (total_tests * 10)
    
    cost_per_1000 = ((avg_input_per_req * 1000) / 1000000 * COST_INPUT_1M) + \
                    ((avg_output_per_req * 1000) / 1000000 * COST_OUTPUT_1M)
                    
    print(f"Cost per 1,000 requests (Method 1)    : $0.0000 (Local Compute)")
    print(f"Cost per 1,000 requests (Method 2)    : ${cost_per_1000:.6f} USD")
    print("\nTRACEABILITY AUDIT:")
    for method, status in traceability_log.items():
        print(f"- {method}: {status}")
    print("==================================================\n")

if __name__ == "__main__":
    evaluate_implementations(max_cases=5) # Kept at 5 to avoid 429 quota bans. Change to 200 for full run.