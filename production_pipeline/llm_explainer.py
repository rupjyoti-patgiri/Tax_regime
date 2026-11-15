# production_pipeline/3_llm_explainer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-3.5-flash-lite")

def generate_explanation(user_text, calculation_result):
    prompt = f"""
    You are a friendly Indian Tax Advisor.
    User asked: "{user_text}"
    
    Our deterministic rules engine has computed this exact tax math:
    {calculation_result}
    
    Write a short, friendly response (under 4 sentences). 
    1. Tell them which regime is better and their tax liability.
    2. Mention any HRA exemption or 87A rebate they received if applicable.
    3. Do NOT hallucinate new math. Rely strictly on the provided dictionary.
    """
    
    response = model.generate_content(prompt)
    return response.text