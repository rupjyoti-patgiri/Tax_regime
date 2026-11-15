# config.py

TAX_RULES = {
    "FY_2024_25": {
        "old_regime": {
            "standard_deduction": 50000,
            "cess_rate": 0.04,
            "rebate_87A": {"income_limit": 500000, "max_rebate": 12500},
            "slabs": [
                {"limit": 250000, "rate": 0.00},
                {"limit": 500000, "rate": 0.05},
                {"limit": 1000000, "rate": 0.20},
                {"limit": float('inf'), "rate": 0.30}
            ],
            "surcharge": [
                {"threshold": 5000000, "rate": 0.10},
                {"threshold": 10000000, "rate": 0.15},
                {"threshold": 20000000, "rate": 0.25},
                {"threshold": 50000000, "rate": 0.37}
            ]
        },
        "new_regime": {
            "standard_deduction": 75000,
            "cess_rate": 0.04,
            "rebate_87A": {"income_limit": 700000, "max_rebate": 25000},
            "slabs": [
                {"limit": 300000, "rate": 0.00},
                {"limit": 700000, "rate": 0.05},
                {"limit": 1000000, "rate": 0.10},
                {"limit": 1200000, "rate": 0.15},
                {"limit": 1500000, "rate": 0.20},
                {"limit": float('inf'), "rate": 0.30}
            ],
            "surcharge": [
                {"threshold": 5000000, "rate": 0.10},
                {"threshold": 10000000, "rate": 0.15},
                {"threshold": 20000000, "rate": 0.25} # Capped at 25% in new regime
            ]
        }
    },
    "FY_2025_26": {
        "old_regime": {
            # Old regime remains strictly the same in FY 25-26
            "standard_deduction": 50000,
            "cess_rate": 0.04,
            "rebate_87A": {"income_limit": 500000, "max_rebate": 12500},
            "slabs": [
                {"limit": 250000, "rate": 0.00},
                {"limit": 500000, "rate": 0.05},
                {"limit": 1000000, "rate": 0.20},
                {"limit": float('inf'), "rate": 0.30}
            ],
            "surcharge": [
                {"threshold": 5000000, "rate": 0.10},
                {"threshold": 10000000, "rate": 0.15},
                {"threshold": 20000000, "rate": 0.25},
                {"threshold": 50000000, "rate": 0.37}
            ]
        },
        "new_regime": {
            "standard_deduction": 75000,
            "cess_rate": 0.04,
            "rebate_87A": {"income_limit": 1200000, "max_rebate": 60000}, # New 12L threshold
            "slabs": [
                {"limit": 400000, "rate": 0.00},
                {"limit": 800000, "rate": 0.05},
                {"limit": 1200000, "rate": 0.10},
                {"limit": 1600000, "rate": 0.15},
                {"limit": 2000000, "rate": 0.20},
                {"limit": 2400000, "rate": 0.25},
                {"limit": float('inf'), "rate": 0.30}
            ],
            "surcharge": [
                {"threshold": 5000000, "rate": 0.10},
                {"threshold": 10000000, "rate": 0.15},
                {"threshold": 20000000, "rate": 0.25}
            ]
        }
    },
    "DEDUCTION_LIMITS": {
        "SEC_80C": 150000,
        "SEC_80CCD_1B": 50000,
        "SEC_24B": 200000,
        "SEC_80D_NORMAL": 25000,
        "SEC_80D_SENIOR": 50000
    },
    "HRA_RULES": {
        "metro_cities": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "metro_percentage": 0.50,
        "non_metro_percentage": 0.40,
        "rent_minus_basic_percentage": 0.10
    }
}