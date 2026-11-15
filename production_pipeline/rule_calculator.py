# production_pipeline/2_rule_calculator.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from implementations.method_1_rules import calculate_tax

def run_calculation(extracted_data, fy="FY_2025_26"):
    if not extracted_data.get("is_complete"):
        raise ValueError("Cannot calculate. Incomplete data.")
        
    return calculate_tax(extracted_data, fy)