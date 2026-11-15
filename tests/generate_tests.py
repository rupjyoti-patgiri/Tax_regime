import json
import random
import os

def generate_test_cases():
    cases = []
    
    # 1. Manual Edge Cases (Highly targeted for 87A, Marginal Relief, HRA, Surcharge)
    edge_cases = [
        # FY24 & FY25 87A Boundaries
        ("exactly_7L_fy24", 30, 625000, 150000, 0, "Non-Metro", {"sec_80c": 0}), # 7.75L gross - 75k std ded = 7L
        ("marginal_relief_87A_fy24", 30, 630000, 150000, 0, "Non-Metro", {"sec_80c": 0}), 
        ("exactly_12L_fy25", 35, 1050000, 225000, 0, "Non-Metro", {"sec_80c": 0}), 
        
        # HRA Complexities
        ("hra_metro_full_exemption", 28, 500000, 250000, 300000, "Mumbai", {"sec_80c": 150000}),
        ("hra_non_metro_partial", 45, 800000, 300000, 150000, "Pune", {"sec_80c": 100000}),
        
        # Senior Citizen & 80D
        ("senior_citizen_max_deductions", 65, 1200000, 0, 0, "Non-Metro", {"sec_80c": 150000, "sec_80d": 50000, "sec_24b": 200000}),
        
        # Surcharge & High Income Marginal Relief
        ("surcharge_50L_exact", 40, 4000000, 1075000, 0, "Non-Metro", {}), # Exactly 50L after standard deduction
        ("surcharge_marginal_relief", 42, 4050000, 1075000, 0, "Non-Metro", {}), # Triggers surcharge marginal relief
        ("surcharge_new_regime_cap", 50, 20000000, 5075000, 0, "Non-Metro", {}) # Tests the 25% cap in new regime vs 37% old
    ]
    
    for ec in edge_cases:
        cases.append({
            "id": ec[0],
            "age": ec[1],
            "is_senior_citizen": ec[1] >= 60,
            "financials": {
                "basic_pay": ec[2],
                "hra_received": ec[3],
                "rent_paid": ec[4],
                "city_type": ec[5],
                "other_allowances": 0
            },
            "investments": {
                "sec_80c": ec[6].get("sec_80c", 0),
                "sec_80ccd1b": ec[6].get("sec_80ccd1b", 0),
                "sec_80d": ec[6].get("sec_80d", 0),
                "sec_24b": ec[6].get("sec_24b", 0)
            }
        })

    # 2. Programmatic Generation to reach 200 cases
    # Varying income brackets, ages, and investment profiles
    incomes = [400000, 600000, 750000, 900000, 1100000, 1300000, 1500000, 2500000, 5500000, 12000000]
    cities = ["Mumbai", "Delhi", "Pune", "Bangalore", "Tier-3"]
    
    case_id = len(cases) + 1
    while len(cases) < 200:
        base_income = random.choice(incomes) + random.randint(-50000, 50000)
        age = random.choice([25, 35, 45, 55, 62, 70])
        city = random.choice(cities)
        city_type = "Metro" if city in ["Mumbai", "Delhi", "Kolkata", "Chennai"] else "Non-Metro"
        rent = random.randint(0, int(base_income * 0.4)) if random.random() > 0.3 else 0
        
        cases.append({
            "id": f"auto_generated_{case_id}",
            "age": age,
            "is_senior_citizen": age >= 60,
            "financials": {
                "basic_pay": int(base_income * 0.5),
                "hra_received": int(base_income * 0.2),
                "rent_paid": rent,
                "city_type": city_type,
                "other_allowances": int(base_income * 0.3)
            },
            "investments": {
                "sec_80c": random.choice([0, 50000, 150000]),
                "sec_80ccd1b": random.choice([0, 50000]),
                "sec_80d": random.choice([0, 25000, 50000]),
                "sec_24b": random.choice([0, 150000, 200000]) if age > 30 else 0
            }
        })
        case_id += 1

    # 3. Generate 50 Plain-Language Inputs (Missing info, Hinglish, Contradictions)
    raw_texts = [
        {"id": "text_01", "text": "Mera basic 8 lakh hai, HRA 2 lakh milta hai aur rent 25k per month hai Pune me. 1.5L PPF. Kaunsa regime lu?"},
        {"id": "text_02", "text": "I earn 15 LPA total. I pay 30k rent but I don't know my basic pay or HRA breakdown."}, # Missing info: basic/hra split
        {"id": "text_03", "text": "Age 65, total pension 9 lakhs. Paid 60k for health insurance. Old or new?"},
        {"id": "text_04", "text": "I live in Delhi paying 40k rent. My company gives me 3L HRA and basic is 10L. Wait, actually I shifted to Gurugram last month."}, # Contradictory/Ambiguous city
        {"id": "text_05", "text": "Gross salary is 55 Lakhs. Are there any surcharges in the new regime for FY26?"}
    ]
    
    # Auto-generate remaining texts up to 50
    templates = [
        "Salary is {income}L, invested {invest}k in ELSS. Staying in {city} paying {rent}k rent.",
        "Mera total pay {income} lakhs hai. {invest}k NPS me dala. Age {age} hai.",
        "Basic {basic}L, HRA {hra}L, rent {rent}k in {city}. Medical premium {medical}k. Best regime?",
        "Earn {income}L. No investments at all. Paying rent of {rent}k but not sure if I get HRA.",
        "Age {age}, gross {income}L. Home loan interest is 2.5L but I know max is 2L. What's my tax?"
    ]
    
    text_id = len(raw_texts) + 1
    while len(raw_texts) < 50:
        t = random.choice(templates)
        filled = t.format(
            income=random.randint(6, 60),
            invest=random.choice([50, 100, 150]),
            city=random.choice(["Mumbai", "Noida", "Bangalore", "a village"]),
            rent=random.randint(10, 50),
            age=random.choice([25, 40, 65]),
            basic=random.randint(4, 15),
            hra=random.randint(1, 5),
            medical=random.choice([10, 25, 50])
        )
        raw_texts.append({"id": f"text_{text_id:02d}", "text": filled})
        text_id += 1

    # Ensure tests directory exists
    os.makedirs('tests', exist_ok=True)
    
    with open('tests/test_cases.json', 'w') as f:
        json.dump(cases, f, indent=2)
        
    with open('tests/raw_inputs.json', 'w') as f:
        json.dump(raw_texts, f, indent=2)
        
    print(f"Generated {len(cases)} structured test cases.")
    print(f"Generated {len(raw_texts)} raw text inputs.")

if __name__ == "__main__":
    generate_test_cases()