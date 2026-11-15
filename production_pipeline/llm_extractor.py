# production_pipeline/1_llm_extractor.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Using flash as it is perfectly capable of JSON extraction and highly cost-effective
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    generation_config={"response_mime_type": "application/json"}
)

def extract_financial_data(user_text):
    prompt = f"""
    You are an intelligent data extractor for an Indian Income Tax engine.
    Extract the financial information from the user's query into a strict JSON format.

    CRITICAL RULES FOR TASK 3 (Missing Information):
    1. If the user mentions paying rent but does not specify their city, you cannot calculate HRA. Set "is_complete" to false and ask what city they live in.
    2. If the user gives a "total salary" or "gross salary" but mentions rent/HRA, you need their exact "Basic Pay" and "HRA Received" breakdown. Set "is_complete" to false and ask for it.
    3. If data is missing, write a friendly "clarifying_question" in the same language/tone as the user to ask for the missing data. Do NOT guess the numbers.
    4. If all required data is present, set "is_complete" to true and "clarifying_question" to null.

    Required JSON Schema:
    {{
      "age": int (default 30),
      "is_senior_citizen": bool,
      "financials": {{
        "basic_pay": int,
        "hra_received": int,
        "rent_paid": int,
        "city_type": "Metro" or "Non-Metro",
        "other_allowances": int
      }},
      "investments": {{
        "sec_80c": int,
        "sec_80ccd1b": int,
        "sec_80d": int,
        "sec_24b": int
      }},
      "is_complete": bool,
      "clarifying_question": string or null
    }}

    User Query: "{user_text}"
    """
    
    response = model.generate_content(prompt)
    return json.loads(response.text)