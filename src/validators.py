# src/validators.py

import re
from data.taxonomy import VALID_DEPENDENCIES

def validate_market_system(result: dict) -> dict:
    """
    Ensures the classification (Market Segment -> System General) 
    exists in the defined Taxonomy.
    """
    ms = result.get("Market Segment", "Unknown")
    stg = result.get("System Type (General)", "Not Applicable")
    
    # 1. Check if Market Segment exists
    if ms not in VALID_DEPENDENCIES:
        return {
            "Market Segment": "Unknown",
            "System Type (General)": "Not Applicable",
            "System Type (Specific)": "Not Applicable"
        }

    # 2. Check if System General is valid for that Market Segment
    # Note: We allow "Not Applicable" as a fallback if the specific type is wrong
    if stg not in VALID_DEPENDENCIES[ms]:
        # Try to save it: if MS is correct but STG is wrong, default STG to Not Applicable
        # unless it's C4ISR, where we might default to "Other C4ISR" or similar logic.
        # For safety, we set systems to N/A but keep the Market Segment.
        result["System Type (General)"] = "Not Applicable"
        result["System Type (Specific)"] = "Not Applicable"
        
    return result


def validate_system_names(result: dict) -> dict:
    """
    Ensures System Name fields are consistent.
    """
    gen = result.get("System Name (General)", "Not Applicable")
    spec = result.get("System Name (Specific)", "Not Applicable")

    # Rule: If General Name is missing/unknown, fill it with Specific Name
    if gen in ["Unknown", "Not Applicable", None, ""]:
        result["System Name (General)"] = spec if spec else "Not Applicable"
        
    # Rule: If Specific Name is missing, fill it with General Name
    if spec in ["Unknown", "Not Applicable", None, ""]:
        result["System Name (Specific)"] = result["System Name (General)"]

    return result


def validate_program_quantity(result: dict) -> dict:
    """
    Ensures Quantity is 'Not Applicable' if the Program isn't Procurement.
    """
    prog = result.get("Program Type", "Other Service")

    if prog != "Procurement":
        result["Quantity"] = "Not Applicable"

    return result


def validate_mro(result: dict) -> dict:
    """
    Ensures MRO Duration is 'Not Applicable' if Program isn't MRO.
    """
    if result.get("Program Type") != "MRO/Support":
        result["Expected MRO Contract Duration (Months)"] = "Not Applicable"

    return result


def run_all_validations(result: dict, description: str) -> dict:
    """
    Master validation pipeline.
    """
    # 1. Validate Hierarchy
    result = validate_market_system(result)
    
    # 2. Validate Names
    result = validate_system_names(result)
    
    # 3. Validate Logical Dependencies (Quantity & MRO)
    result = validate_program_quantity(result)
    result = validate_mro(result)

    # Note: 'validate_piloting' was removed to allow the LLM's 
    # superior reasoning (defined in processors.py) to prevail.

    return result