# implementations/method_2_llm.py
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TAX_RULES
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_llm_query_prompt(input_json, fy="FY_2025_26"):
    rules = TAX_RULES[fy]
    
    prompt = f"""
    You are an expert Indian Income Tax Calculator.
    Calculate the final income tax for both the old and new regimes based on the following rules.
    
    RULES FOR {fy}:
    {json.dumps(rules, indent=2)}
    
    DEDUCTION LIMITS:
    {json.dumps(TAX_RULES["DEDUCTION_LIMITS"], indent=2)}
    
    HRA RULES:
    {json.dumps(TAX_RULES["HRA_RULES"], indent=2)}
    
    USER PROFILE:
    {json.dumps(input_json, indent=2)}

    CRITICAL INSTRUCTIONS:
    1. Calculate Gross Salary (Basic + HRA + Other).
    2. Calculate HRA exemption accurately for the Old Regime based on Metro/Non-Metro rules.
    3. Apply Marginal Relief on 87A if taxable income just exceeds the rebate limit.
    4. Apply High-Income Surcharge and its Marginal Relief if income > 50 Lakhs. Note new regime surcharge caps at 25%.
    5. Add 4% health and education cess to the final tax.
    
    Return ONLY a valid JSON object with the following exact keys:
    {{
      "old_regime_tax": <number>,
      "new_regime_tax": <number>,
      "better_regime": <"NEW" or "OLD">
    }}
    """
    return prompt

# We will execute model.generate_content() inside the Evaluation Harness.