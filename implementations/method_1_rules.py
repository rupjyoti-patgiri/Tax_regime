# implementations/method_1_rules.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TAX_RULES

def calculate_tax(input_data, fy="FY_2025_26"):
    rules = TAX_RULES[fy]
    limits = TAX_RULES["DEDUCTION_LIMITS"]
    hra_rules = TAX_RULES["HRA_RULES"]
    
    fin = input_data.get("financials", {})
    inv = input_data.get("investments", {})
    
    basic = fin.get("basic_pay", 0)
    hra_received = fin.get("hra_received", 0)
    rent = fin.get("rent_paid", 0)
    other = fin.get("other_allowances", 0)
    
    gross_salary = basic + hra_received + other
    
    # 1. HRA Exemption Calculation (Old Regime Only)
    hra_exemption = 0
    if rent > 0 and hra_received > 0:
        rent_minus_10_basic = max(0, rent - (0.10 * basic))
        metro_multiplier = hra_rules["metro_percentage"] if fin.get("city_type", "").lower() == "metro" else hra_rules["non_metro_percentage"]
        limit_basic = metro_multiplier * basic
        hra_exemption = min(hra_received, rent_minus_10_basic, limit_basic)
        
    # 2. Old Regime Deductions
    sec_80c = min(inv.get("sec_80c", 0), limits["SEC_80C"])
    sec_80ccd1b = min(inv.get("sec_80ccd1b", 0), limits["SEC_80CCD_1B"])
    max_80d = limits["SEC_80D_SENIOR"] if input_data.get("is_senior_citizen") else limits["SEC_80D_NORMAL"]
    sec_80d = min(inv.get("sec_80d", 0), max_80d)
    sec_24b = min(inv.get("sec_24b", 0), limits["SEC_24B"])
    
    total_old_deductions = sec_80c + sec_80ccd1b + sec_80d + sec_24b + rules["old_regime"]["standard_deduction"] + hra_exemption
    taxable_income_old = max(0, gross_salary - total_old_deductions)
    
    # 3. New Regime Deductions (Only Standard Deduction)
    taxable_income_new = max(0, gross_salary - rules["new_regime"]["standard_deduction"])
    
    # --- HELPER FUNCTIONS ---
    def apply_slabs(income, slabs):
        tax = 0
        prev_limit = 0
        for slab in slabs:
            if income > prev_limit:
                taxable_at_slab = min(income, slab["limit"]) - prev_limit
                tax += taxable_at_slab * slab["rate"]
                prev_limit = slab["limit"]
            else:
                break
        return tax

    def apply_rebate_87A(income, tax, regime_rules):
        limit = regime_rules["rebate_87A"]["income_limit"]
        if income <= limit:
            return 0, 0 # Full rebate, tax becomes 0
        
        # Marginal Relief for 87A (Income slightly above threshold)
        income_above = income - limit
        marginal_relief = 0
        if tax > income_above:
            marginal_relief = tax - income_above
            tax = income_above
        return tax, marginal_relief

    def apply_surcharge(income, tax, surcharge_slabs, slab_rules):
        if income <= 5000000:
            return tax, 0
            
        rate = 0
        threshold = 5000000
        # Find applicable surcharge bracket
        for slab in sorted(surcharge_slabs, key=lambda x: x["threshold"], reverse=True):
            if income > slab["threshold"]:
                rate = slab["rate"]
                threshold = slab["threshold"]
                break
                
        tax_with_surcharge = tax * (1 + rate)
        
        # Surcharge Marginal Relief calculation
        # Tax + Surcharge cannot exceed (Tax on threshold + Surcharge on threshold) + (Income - threshold)
        tax_at_threshold = apply_slabs(threshold, slab_rules)
        rate_at_threshold = 0
        for slab in sorted(surcharge_slabs, key=lambda x: x["threshold"], reverse=True):
            if threshold > slab["threshold"]:
                rate_at_threshold = slab["rate"]
                break
                
        tax_with_surcharge_at_threshold = tax_at_threshold * (1 + rate_at_threshold)
        max_allowed_tax = tax_with_surcharge_at_threshold + (income - threshold)
        
        marginal_relief = max(0, tax_with_surcharge - max_allowed_tax)
        final_tax = tax_with_surcharge - marginal_relief
        
        return final_tax, marginal_relief

    # --- FINAL CALCULATIONS ---
    # Old Regime
    tax_old = apply_slabs(taxable_income_old, rules["old_regime"]["slabs"])
    tax_old, relief_87a_old = apply_rebate_87A(taxable_income_old, tax_old, rules["old_regime"])
    tax_old, relief_surcharge_old = apply_surcharge(taxable_income_old, tax_old, rules["old_regime"]["surcharge"], rules["old_regime"]["slabs"])
    final_tax_old = round(tax_old * (1 + rules["old_regime"]["cess_rate"]))

    # New Regime
    tax_new = apply_slabs(taxable_income_new, rules["new_regime"]["slabs"])
    tax_new, relief_87a_new = apply_rebate_87A(taxable_income_new, tax_new, rules["new_regime"])
    tax_new, relief_surcharge_new = apply_surcharge(taxable_income_new, tax_new, rules["new_regime"]["surcharge"], rules["new_regime"]["slabs"])
    final_tax_new = round(tax_new * (1 + rules["new_regime"]["cess_rate"]))

    return {
        "taxable_income_old": taxable_income_old,
        "taxable_income_new": taxable_income_new,
        "hra_exemption": hra_exemption,
        "old_regime_tax": final_tax_old,
        "new_regime_tax": final_tax_new,
        "better_regime": "NEW" if final_tax_new <= final_tax_old else "OLD"
    }