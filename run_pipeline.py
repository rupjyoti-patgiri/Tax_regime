# run_pipeline.py
from production_pipeline.llm_extractor import extract_financial_data
from production_pipeline.rule_calculator import run_calculation
from production_pipeline.llm_explainer import generate_explanation

def execute_hybrid_pipeline(user_query):
    print(f"\n👤 USER QUERY: \"{user_query}\"")
    
    try:
        # Step 1: Extract
        print("⚙️  STEP 1: Extracting via LLM...")
        extracted_data = extract_financial_data(user_query)
        
        # Check for Task 3 Clarification Loop
        if not extracted_data.get("is_complete"):
            print("🛑 PIPELINE HALTED: Missing Information Detected.")
            print(f"🤖 BOT ASKS: {extracted_data.get('clarifying_question')}")
            return

        print("✅ Data is complete. Proceeding...")
        
        # Step 2: Calculate
        print("\n🧮 STEP 2: Calculating via Deterministic Rules...")
        tax_results = run_calculation(extracted_data, "FY_2025_26")
        print(f"Calculated: {tax_results}")

        # Step 3: Explain
        print("\n💬 STEP 3: Generating Friendly Explanation...")
        explanation = generate_explanation(user_query, tax_results)
        print(f"\n🤖 BOT RESPONSE:\n{explanation}\n")

    except Exception as e:
        print(f"\n❌ System Error: {str(e)}")

if __name__ == "__main__":
    print("=== SCENARIO 1: MISSING INFORMATION (Task 3 Test) ===")
    incomplete_query = "I earn 15 LPA total. I pay 30k rent but I don't know my basic pay or HRA breakdown."
    execute_hybrid_pipeline(incomplete_query)
    
    print("\n" + "="*50 + "\n")
    
    print("=== SCENARIO 2: COMPLETE INFORMATION ===")
    complete_query = "My basic pay is 6L, HRA received is 3L, and other allowances are 4L. I pay 25k rent in Mumbai. Also invested 1.5L in PPF."
    execute_hybrid_pipeline(complete_query)