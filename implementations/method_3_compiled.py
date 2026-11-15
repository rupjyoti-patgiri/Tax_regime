# implementations/method_3_compiled.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_compiler_prompt(fy="FY_2025_26"):
    prompt = f"""
    You are an AI Software Architect. Write a standalone, deterministic Python 3.10+ function named `calculate_tax(input_data)` that calculates Indian Income Tax for {fy}.
    
    FINANCE ACT 2025 SUMMARY (New Regime):
    - Standard deduction: ₹75,000. 
    - Slabs: 0-4L: Nil, 4-8L: 5%, 8-12L: 10%, 12-16L: 15%, 16-20L: 20%, 20-24L: 25%, >24L: 30%.
    - Section 87A rebate: Up to ₹12,00,000 (Max rebate ₹60,000). Apply marginal relief.
    - Surcharge: 10% (>50L), 15% (>1Cr), 25% (>2Cr). Note: Surcharge capped at 25%. Apply marginal relief.
    
    FINANCE ACT 2024/25 SUMMARY (Old Regime):
    - Standard deduction: ₹50,000. 
    - Slabs: 0-2.5L: Nil, 2.5-5L: 5%, 5-10L: 20%, >10L: 30%.
    - Section 87A rebate: Up to ₹5,00,000 (Max rebate ₹12,500).
    - Deductions: 80C up to 1.5L, 80CCD(1B) up to 50k, 80D up to 25k (50k for senior citizens), 24b up to 2L.
    - HRA Exemption: Min of (Actual HRA, Rent - 10% of Basic, 50% Basic if Metro else 40%).
    - Surcharge: 10% (>50L), 15% (>1Cr), 25% (>2Cr), 37% (>5Cr). Apply marginal relief.
    
    - Add 4% cess on all final tax amounts.

    Return ONLY raw, valid Python code. Do not include markdown formatting or explanations.
    """
    return prompt