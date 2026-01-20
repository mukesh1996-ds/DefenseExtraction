import re
from data.taxonomy import VALID_DEPENDENCIES


def _init_validation(result: dict):
    """
    Ensures validation dict exists.
    """
    if "__validation__" not in result or not isinstance(result["__validation__"], dict):
        result["__validation__"] = {}
    return result


def _add_check(result: dict, column: str, passed: bool, reason_if_fail: str = ""):
    """
    Adds a validation check record for a single column.
    """
    result = _init_validation(result)
    result["__validation__"][column] = {
        "passed": bool(passed),
        "reason": "OK" if passed else reason_if_fail
    }
    return result


def _compute_validation_score(result: dict):
    """
    Computes validation score from __validation__ results.
    """
    v = result.get("__validation__", {})
    if not isinstance(v, dict) or len(v) == 0:
        result["Validation Score"] = 0.0
        return result

    total = len(v)
    passed = sum(1 for k in v if v[k].get("passed") is True)
    result["Validation Score"] = round((passed / total) * 100, 2)
    return result


# ==========================================================
# VALIDATORS
# ==========================================================
def validate_market_system(result: dict) -> dict:
    """
    Ensures the classification (Market Segment -> System General)
    exists in the defined Taxonomy.
    Also records validation results.
    """
    ms = result.get("Market Segment", "Unknown")
    stg = result.get("System Type (General)", "Not Applicable")
    sts = result.get("System Type (Specific)", "Not Applicable")

    # 1. Validate Market Segment exists
    if ms not in VALID_DEPENDENCIES:
        # mark fail
        result = _add_check(
            result,
            "Market Segment",
            False,
            f"Invalid Market Segment '{ms}'. Not in taxonomy."
        )

        # auto-fix output (your existing behavior)
        result["Market Segment"] = "Unknown"
        result["System Type (General)"] = "Not Applicable"
        result["System Type (Specific)"] = "Not Applicable"

        # record system checks as fail
        result = _add_check(
            result,
            "System Type (General)",
            False,
            "Market Segment invalid, so System Type (General) forced to Not Applicable."
        )
        result = _add_check(
            result,
            "System Type (Specific)",
            False,
            "Market Segment invalid, so System Type (Specific) forced to Not Applicable."
        )
        return result

    # If MS valid
    result = _add_check(result, "Market Segment", True)

    # 2. Validate System General under Market Segment
    if stg not in VALID_DEPENDENCIES[ms]:
        # fail check
        result = _add_check(
            result,
            "System Type (General)",
            False,
            f"'{stg}' is not valid under Market Segment '{ms}'."
        )
        result = _add_check(
            result,
            "System Type (Specific)",
            False,
            "System Type (General) invalid => forcing System Type (Specific) to Not Applicable."
        )

        # auto-fix (your existing behavior)
        result["System Type (General)"] = "Not Applicable"
        result["System Type (Specific)"] = "Not Applicable"
        return result

    # STG valid
    result = _add_check(result, "System Type (General)", True)

    # STS (Specific) is not strictly validated in your taxonomy dict right now
    # We'll mark it pass if it is not empty/unknown
    if sts in ["", None, "Unknown"]:
        result = _add_check(
            result,
            "System Type (Specific)",
            False,
            "System Type (Specific) missing/Unknown."
        )
    else:
        result = _add_check(result, "System Type (Specific)", True)

    return result


def validate_system_names(result: dict) -> dict:
    """
    Ensures System Name fields are consistent.
    Also records validation results.
    """
    gen = result.get("System Name (General)", "Not Applicable")
    spec = result.get("System Name (Specific)", "Not Applicable")

    # If General missing, fill with Specific
    if gen in ["Unknown", "Not Applicable", None, ""]:
        if spec not in ["Unknown", "Not Applicable", None, ""]:
            result["System Name (General)"] = spec
            result = _add_check(
                result,
                "System Name (General)",
                True,
            )
        else:
            result["System Name (General)"] = "Not Applicable"
            result = _add_check(
                result,
                "System Name (General)",
                False,
                "Both System Name (General) and (Specific) are missing/unknown."
            )
    else:
        result = _add_check(result, "System Name (General)", True)

    # If Specific missing, fill with General
    spec = result.get("System Name (Specific)", "Not Applicable")
    gen = result.get("System Name (General)", "Not Applicable")

    if spec in ["Unknown", "Not Applicable", None, ""]:
        if gen not in ["Unknown", "Not Applicable", None, ""]:
            result["System Name (Specific)"] = gen
            result = _add_check(result, "System Name (Specific)", True)
        else:
            result["System Name (Specific)"] = "Not Applicable"
            result = _add_check(
                result,
                "System Name (Specific)",
                False,
                "Both System Name (General) and (Specific) are missing/unknown."
            )
    else:
        result = _add_check(result, "System Name (Specific)", True)

    return result


def validate_program_quantity(result: dict) -> dict:
    """
    Ensures Quantity is 'Not Applicable' if Program isn't Procurement.
    Also records validation results.
    """
    prog = result.get("Program Type", "Other Service")
    qty = result.get("Quantity", "Not Applicable")

    if prog != "Procurement":
        # auto-fix
        result["Quantity"] = "Not Applicable"

        # validation check
        result = _add_check(
            result,
            "Quantity",
            True,
        )
    else:
        # For procurement, quantity should ideally be numeric or at least not N/A
        if str(qty).strip() in ["Not Applicable", "", "Unknown", "None"]:
            result = _add_check(
                result,
                "Quantity",
                False,
                "Program Type is Procurement but Quantity is missing/Not Applicable."
            )
        else:
            result = _add_check(result, "Quantity", True)

    return result


def validate_mro(result: dict) -> dict:
    """
    Ensures MRO Duration is 'Not Applicable' if Program isn't MRO.
    Also records validation results.
    """
    prog = result.get("Program Type", "Other Service")
    duration = result.get("Expected MRO Contract Duration (Months)", "Not Applicable")

    if prog != "MRO/Support":
        result["Expected MRO Contract Duration (Months)"] = "Not Applicable"
        result = _add_check(result, "Expected MRO Contract Duration (Months)", True)
    else:
        # Must not be N/A for MRO contracts
        if str(duration).strip() in ["Not Applicable", "", "Unknown", "None"]:
            result = _add_check(
                result,
                "Expected MRO Contract Duration (Months)",
                False,
                "Program Type is MRO/Support but duration is missing/Not Applicable."
            )
        else:
            result = _add_check(result, "Expected MRO Contract Duration (Months)", True)

    return result


# ==========================================================
# MASTER VALIDATION PIPELINE
# ==========================================================
def run_all_validations(result: dict, description: str) -> dict:
    """
    Master validation pipeline.
    Fixes output values + stores PASS/FAIL reasons per column.
    """
    # Ensure validation dict exists
    result = _init_validation(result)

    # 1. Validate Hierarchy
    result = validate_market_system(result)

    # 2. Validate Names
    result = validate_system_names(result)

    # 3. Validate Logical Dependencies (Quantity & MRO)
    result = validate_program_quantity(result)
    result = validate_mro(result)

    # ✅ You can add more validations here later, ex:
    # - Customer Country not Unknown
    # - Supplier Name not Unknown
    # - Value numeric
    # - Currency present, etc.

    # Score
    result = _compute_validation_score(result)

    return result