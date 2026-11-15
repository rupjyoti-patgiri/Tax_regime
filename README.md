# Hybrid Tax Regime Engine

A Python proof of concept for comparing Indian income tax under the old and new regimes. It uses an LLM only to extract financial details from natural-language questions and explain results; the tax calculations themselves run in deterministic Python rules.

## Features

- Extracts salary, HRA, rent, and selected deductions from English or Hinglish prompts.
- Detects missing information needed for HRA calculations.
- Calculates taxable income, HRA exemption, deductions, 87A rebate, surcharge, marginal relief, and 4% cess.
- Compares the old and new regimes for FY 2024-25 and FY 2025-26.
- Includes an evaluation harness for comparing deterministic rules with LLM-generated calculations.

## Requirements

- Python 3.10 or later
- A Gemini API key

## Setup

```powershell
git clone https://github.com/rupjyoti-patgiri/Tax_regime.git
cd Tax_regime

py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The `.env` file is ignored by Git and must not be committed.

## Run the demo

```powershell
python run_pipeline.py
```

The demo runs an incomplete profile that prompts for clarification, followed by a complete profile that is extracted, calculated, and explained.

## Other commands

```powershell
# Regenerate structured and natural-language fixtures
python tests\generate_tests.py

# Compare the rules engine with LLM responses.
# This makes Gemini API requests and consumes quota.
python evaluation_harness.py

# Check Python syntax
python -m compileall .
```

## Project structure

```text
config.py                         Tax rules and deduction limits
implementations/method_1_rules.py Deterministic tax calculator
implementations/method_2_llm.py   Prompt for LLM-only calculation evaluation
implementations/method_3_compiled.py Prompt for LLM-generated implementation
production_pipeline/              Extraction, calculation, and explanation layers
run_pipeline.py                   CLI demonstration
evaluation_harness.py             Rules-versus-LLM evaluation script
tests/                            Generated input fixtures
```

## Important limitations

This is a demonstration project, not tax advice or production tax-filing software. It currently focuses on salary income, HRA, and a limited set of deductions. Validate outputs and applicable law with a qualified tax professional before relying on them.
