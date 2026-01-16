 # src/validators.py

import re
from data.taxonomy import VALID_DEPENDENCIES

CREWED_PLATFORMS = [
    "Fighter", "Bomber", "Transport Aircraft",
    "Main Battle Tank", "Submarine", "Surface Combatant",
    "Rotary Wing"
]

UNCREWED_KEYWORDS = [
    "UAV", "Unmanned", "Drone", "Satellite"
]

SERVICE_KEYWORDS = [
    "support", "engineering", "maintenance",
    "services", "consultation", "training"
]

def validate_market_system(result: dict) -> dict:
    ms = result.get("Market Segment", "Unknown")
    stg = result.get("System Type (General)", "Not Applicable")
    sts = result.get("System Type (Specific)", "Not Applicable")

    if ms not in VALID_DEPENDENCIES:
        return {
            "Market Segment": "Unknown",
            "System Type (General)": "Not Applicable",
            "System Type (Specific)": "Not Applicable"
        }

    if stg not in VALID_DEPENDENCIES[ms]:
        return {
            "Market Segment": ms,
            "System Type (General)": "Not Applicable",
            "System Type (Specific)": "Not Applicable"
        }

    return result


def validate_system_names(result: dict) -> dict:
    gen = result.get("System Name (General)", "Not Applicable")
    spec = result.get("System Name (Specific)", "Not Applicable")

    # Analyst rule: If no platform → General == Specific
    if gen in ["Unknown", "Not Applicable"]:
        result["System Name (General)"] = spec
        result["System Name (Specific)"] = spec

    return result


def validate_piloting(result: dict, description: str) -> dict:
    desc = description.lower()

    if any(k.lower() in desc for k in UNCREWED_KEYWORDS):
        result["System Piloting"] = "Uncrewed"
        return result

    if any(k.lower() in desc for k in SERVICE_KEYWORDS):
        result["System Piloting"] = "Not Applicable"
        return result

    if result.get("Market Segment") in ["C4ISR Systems", "Unknown"]:
        result["System Piloting"] = "Not Applicable"
        return result

    result["System Piloting"] = "Crewed"
    return result


def validate_program_quantity(result: dict) -> dict:
    prog = result.get("Program Type", "Other Service")

    if prog != "Procurement":
        result["Quantity"] = "Not Applicable"

    return result


def validate_mro(result: dict) -> dict:
    if result.get("Program Type") != "MRO/Support":
        result["Expected MRO Contract Duration (Months)"] = "Not Applicable"

    return result


def run_all_validations(result: dict, description: str) -> dict:
    result = validate_market_system(result)
    result = validate_system_names(result)
    result = validate_piloting(result, description)
    result = validate_program_quantity(result)
    result = validate_mro(result)

    return result