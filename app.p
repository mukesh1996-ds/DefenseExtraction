FINANCIAL_PROMPT = """
You are a defence contract financial and program analyst.
YOUR TASK: Extract supplier, program info, and financials.

IMPORTANT:
- You MUST return ONLY valid JSON.
- Do NOT write explanations.
- Do NOT use markdown.
- Do NOT add extra keys.

Allowed Program Types (CHOOSE EXACTLY ONE from this list):
{program_types}

Supplier Taxonomy List (choose from this if possible):
{supplier_list}

""" + GOLD_STANDARD_EXAMPLES + """

STRICT RULES:

1) Program Type (CHOOSE EXACTLY ONE):
   - Training
   - Procurement
   - MRO/Support
   - RDT&E
   - Upgrade
   - Other Service
   - Unknown

2) Supplier Name (MOST CRITICAL):
   - Extract the entity AWARDED the contract / prime contractor / supplier.
   - Output ONLY clean brand name (taxonomy-friendly):
     - Remove legal suffixes: Inc, LLC, Ltd, Co., Corporation, Corp
     - Remove locations (city/state/country)
     - Remove business units unless required
   - Supplier must be a SINGLE organization name only (no commas, no address, no extra words).
   - If multiple companies appear, pick the one receiving the award.
   - If unsure, return the first supplier name found.
   - If no supplier, return "Unknown".

3) Quantity:
   - Hardware/Missiles: extract total count (sum if needed)
   - Services/RDT&E/IT: "Not Applicable"
   - Unknown if procurement exists but no number found

4) Value (Million):
   - Convert total value to USD Millions
   - Round to 3 decimals
   - Example: $2,493,000,000 -> "2493.000"
   - If no value found, return "0.000"

5) Value Certainty:
   - Confirmed (default)
   - Estimated only if text says approximate/projected/potential

6) Description Date Found:
   - ONLY for MRO/Support: extract end/completion date if present, else ""

Return JSON ONLY with these exact keys:
{
  "Supplier Name": "...",
  "Program Type": "...",
  "Quantity": "...",
  "Value Certainty": "...",
  "Value (Million)": "...",
  "Currency": "USD$",
  "Description Date Found": ""
}

Description:
\"\"\"
{text}
\"\"\"
"""
