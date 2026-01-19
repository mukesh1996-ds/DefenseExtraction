# ==============================================================================
# 1. MARKET STRUCTURE PROMPT (Strict Hierarchy)
# ==============================================================================
TAXONOMY_EXTRACTION_PROMPT = """
You are an expert Defense Market Analyst. Your task is to classify defense contracts into a strict three-level taxonomy based on the text description provided.

## Input
Description: {text}

## Taxonomy Logic (CRITICAL)
You must select categories in a specific order. You cannot select a child category if the parent does not match.

1. **Step 1: Market Segment**
   - Identify the broad domain (e.g., "Air Platforms", "Weapon Systems", "Naval Platforms").

2. **Step 2: System Type (General)**
   - Select the General type that belongs *strictly* to the chosen Market Segment.
   - *Constraint:* If Segment is "Air Platforms", "Fighter" is INVALID here; "Fixed Wing" is VALID.

3. **Step 3: System Type (Specific)**
   - Select the Specific type that belongs *strictly* to the chosen General type.
   - *Constraint:* If General is "Fixed Wing", "Fighter" is VALID.

## Hierarchy Rules from Taxonomy
- **Air Platforms**: 
   - "Fighter", "Bomber", "Transport" -> General: "Fixed Wing"
   - "Helicopters", "Apache", "Chinook" -> General: "Rotary Wing"
- **Land Platforms**:
   - "Tanks" -> General: "Armoured Fighting Vehicles" -> Specific: "Main Battle Tank"
   - "Trucks" -> General: "Logistics & Support"
- **Naval Platforms**:
   - "Destroyers", "Frigates" -> General: "Surface Combatants"
   - "Submarines" -> General: "Sub-Surface"
- **Weapons**:
   - "Missiles" (powered/guided) -> General: "Missile"
   - "Bombs/Rockets" (smart) -> General: "Precision Guided Weapons"
   - "Guns/Ammo" -> General: "Small Arms & Ammunition"

## Output Format (JSON)
Return valid JSON only. Use "Not Applicable" if a level is not specified in the text.
{{
  "market_segment": "Selected Segment",
  "system_type_general": "Selected General Type",
  "system_type_specific": "Selected Specific Type",
  "reasoning": "Brief explanation of the classification path."
}}
"""

# ==============================================================================
# 2. FINANCIAL & PROGRAM PROMPT (Gold Standard)
# ==============================================================================

# NOTE: Double braces {{ }} are used here so they survive the final .format() call.
GOLD_STANDARD_EXAMPLES = """
### EXAMPLES OF PERFECT EXTRACTION (DO NOT DEVIATE):

--- EXAMPLE 1: SERVICE ON A PLATFORM (E-2D CASE) ---
Input Text:
"Northrop Grumman... modification... to extend services and adds hours increasing the full-scale fatigue repair time... in support of E-2D Advanced Hawkeye aircraft development."
Correct Output:
{{
  "Supplier Name": "Northrop Grumman Aerospace",
  "Program Type": "Procurement",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "12.015"
}}

--- EXAMPLE 2: IT / AGREEMENT (DOD ESI CASE) ---
Input Text:
"Dell Marketing... awarded... under the Department of Defense Enterprise Software Initiative (DOD ESI)... This DOD Enterprise Software Agreement (ESA) will provide Microsoft 365..."
Correct Output:
{{
  "Supplier Name": "Dell Inc",
  "Program Type": "Procurement",
  "Quantity": "Not Applicable",
  "Value Certainty": "Estimated",
  "Value (Million)": "2493.000"
}}

--- EXAMPLE 3: COMPONENT PROCUREMENT (SUBMARINE) ---
Input Text:
"BAE Systems... awarded... for Virginia-class submarine propulsors."
Correct Output:
{{
  "Supplier Name": "BAE Systems",
  "Program Type": "Procurement",
  "Quantity": "Unknown",
  "Value Certainty": "Confirmed",
  "Value (Million)": "18.694"
}}

--- EXAMPLE 4: R&D / PROGRAM (GENERIC) ---
Input Text:
"Georgia Tech... contract... for the development and application of advanced technology solutions."
Correct Output:
{{
  "Supplier Name": "Georgia Tech",
  "Program Type": "RDT&E",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "92.000"
}}

--- EXAMPLE 5: NAVAL LOGISTICS (EPF CASE) ---
Input Text:
"Austal USA... contract modification... for the detail design... and demonstration of autonomous capability in Expeditionary Fast Transport (EPF) 13."
Correct Output:
{{
  "Supplier Name": "Austal Limited",
  "Program Type": "Procurement",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "44.000"
}}

--- EXAMPLE 6: SERVICES (CONSULTATION) ---
Input Text:
"Bowhead Cybersecurity... contract for senior consultation support services."
Correct Output:
{{
  "Supplier Name": "Bowhead",
  "Program Type": "Other Service",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "92.308"
}}

--- EXAMPLE 7: MISSILES (QUANTITY & VARIANTS) ---
Input Text:
"Raytheon Missile and Defense... production and delivery of... 483 AIM-9X Block II... 82 AIM-9X block II plus... 156 Block II Captive Air Training Missiles..."
Correct Output:
{{
  "Supplier Name": "Raytheon Missiles and Defense",
  "Program Type": "Procurement",
  "Quantity": "721",
  "Value Certainty": "Confirmed",
  "Value (Million)": "328.156"
}}

--- EXAMPLE 8: COMPONENT UPGRADE (TANK) ---
Input Text:
"DRS Network & Imaging Systems... contract to procure Advanced Multi-Purpose Round Gunner's Auxiliary Sight units... for M1A2 Abrams."
Correct Output:
{{
  "Supplier Name": "DRS Network and Imaging Systems",
  "Program Type": "Procurement",
  "Quantity": "Unknown",
  "Value Certainty": "Confirmed",
  "Value (Million)": "82.741"
}}

--- EXAMPLE 9: SERVICES ON A SYSTEM (RADAR ENGINEERING) ---
Input Text:
"Lockheed Martin... for engineering services in support of the AN/SPY-1 Elevated Radar Advanced Calibration Experiment."
Correct Output:
{{
  "Supplier Name": "Lockheed Martin – Rotary and Mission Systems",
  "Program Type": "RDT&E",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "8.256"
}}

--- EXAMPLE 10: HELICOPTER SUPPORT ---
Input Text:
"DigiFlight Inc... modification... for programmatic support for the Apache Attack Helicopter."
Correct Output:
{{
  "Supplier Name": "Unknown",
  "Program Type": "Other Service",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "13.803"
}}

--- EXAMPLE 11: DEVELOPMENT vs MRO (EDGE CASE) ---
Input Text:
"Northrop Grumman... modification... to extend services and adds hours increasing the full-scale fatigue repair time... in support of E-2D Advanced Hawkeye aircraft development."
Correct Output:
{{
  "Supplier Name": "Northrop Grumman",
  "Program Type": "Procurement",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "12.015"
}}
"""

# We use string concatenation to ensure the {text} placeholder remains valid
# while keeping the JSON examples double-escaped.
FINANCIAL_PROMPT = """
You are a defence contract financial and program analyst.
YOUR TASK: Extract supplier, program info, and financials.

""" + GOLD_STANDARD_EXAMPLES + """

STRICT RULES:

1. **Program Type (CHOOSE EXACTLY ONE)**:
   - **Training**: Purchase of military training *services*. Note: Purchase of training aircraft or simulators falls under "Procurement".
   - **Procurement**: Acquisition of new products, systems, or production kits. **IMPORTANT**: Includes services, repairs, or modifications performed on *test articles* or prototypes to support development/production (e.g., "fatigue repair" for design validation).
   - **MRO/Support**: Maintenance, Repair, and Operations. Select ONLY for contracts related to the sustainment/repair of *existing, fielded, operational* equipment. Do NOT select this if the "repair" is part of a development or testing phase.
   - **RDT&E**: Contracts primarily for research, prototyping, or testing where the outcome is knowledge/design validation rather than a fielded product.
   - **Upgrade**: Purchase of components/services to modernize existing equipment.
   - **Other Service**: General consulting, IT support, or services not tied to a specific weapon system's lifecycle.
   - **Unknown**: If the program type cannot be determined.

2. **Supplier Name (CRITICAL)**: 
   - **Context Understanding**: Read the entire description. Identify the specific entity that has been AWARDED the contract/is performing the work.
   - **Position Independent**: The supplier is usually at the start, but if mentioned later, prioritize the entity actually performing the scope of work.
   - **Taxonomy Alignment**: Output the **Clean Brand Name** (e.g., "The Boeing Co., St. Louis" -> "Boeing").
     - Your goal is to output a name that matches a standard defence taxonomy.
     - Remove legal suffixes ("Inc", "LLC", "Corp") and location details.
     - *Example:* "Lockheed Martin Aeronautics Co." -> "Lockheed Martin".
   - **Fallback**: If the specific supplier is unclear, extract the first company name mentioned in the text.

3. **Quantity (Crucial)**:
   - **Hardware/Missiles:** EXTRACT the total count. If text says "483 AIM-9X... 82 AIM-9X...", SUM THEM UP (483+82=565).
   - **Services/RDT&E/IT:** Use "Not Applicable".
   - **Unknown:** If hardware is bought but no number is given, use "Unknown".

4. **Value Calculation**:
   - Convert to **MILLIONS**.
   - Round to **3 decimal places**.
   - Do NOT include currency symbols or text.
   - Ex: $2,493,000,000 -> "2493.000"

5. **Value Certainty (LOGIC CHANGE)**:
   - **Confirmed**: This is the **DEFAULT**. Use "Confirmed" for all definitive contract awards, modifications, BPAs, and IDIQs where a specific value (or ceiling) is stated.
     - *CRITICAL RULE:* If the text says "estimated value", "ceiling", or "maximum value" in the context of a signed agreement (like a BPA), treat this as **Confirmed** (as it represents the confirmed contract capacity).
   - **Estimated**: Use ONLY if the text explicitly states the value is "potential", "approximate" (without a precise figure), or "projected" outside of the current award structure.

6. **Description Date Found**:
   - For MRO contracts, extract the completion date. Otherwise leave empty.

Return JSON ONLY:
{{
  "Supplier Name": "...",
  "Program Type": "...",
  "Quantity": "...",
  "Value Certainty": "...",
  "Value (Million)": "...", 
  "Currency": "...",
  "Description Date Found": "..."
}}

Description:
\"\"\"
{text}
\"\"\"
"""

# ==============================================================================
# 3. GEOGRAPHY PROMPT
# ==============================================================================
GEOGRAPHY_PROMPT = """
You are a defence contract geography analyst.
YOUR TASK: Extract Customer and Supplier locations and Customer Operator.

STRICT RULES:
1. **Supplier Country**: The country where the supplier company is BASED (not necessarily HQ).
2. **Special Circumstance - Ukraine**:
   - If a country buys equipment UNILATERALLY for Ukraine -> Customer: [Purchasing Country], Operator: "Ukraine (Assistance)".

3. **CUSTOMER OPERATOR (CRITICAL - NO HALLUCINATION):**
   - You MUST pick one value from the provided list ONLY. 
   - If the operator in the text is "Naval Information Warfare Center", map it to "Navy".
   - If "Air Force Life Cycle Management Center", map it to "Air Force".
   - **VALID LIST:** {operators}

MAPPING:
{geo_mapping}

Return JSON ONLY:
{{
  "Customer Region": "...",
  "Customer Country": "...",
  "Customer Operator": "...",
  "Supplier Region": "...",
  "Supplier Country": "..."
}}

Description:
\"\"\"
{text}
\"\"\"
"""

# ==============================================================================
# 4. DOMESTIC CONTENT PROMPT
# ==============================================================================
DOMESTIC_CONTENT_PROMPT = """
You are a defence procurement analyst.
YOUR TASK: Classify the "Domestic Content" based on the text.

STRICT DEFINITIONS:
1. Imported: Product originates from a different country and is physically imported.
2. Indigenous: Product is produced within the customer's country.
   - NOTE: This INCLUDES local production units/subsidiaries of a foreign company located in the customer's country.
3. Local Assembly: Components manufactured abroad, imported, and assembled locally (CKD/SKD).
4. License Production: Local company manufactures a foreign product under a licensing agreement.

INPUT CONTEXT:
- Supplier Country: {supplier_country}
- Customer Country: {customer_country}

OPTIONS:
{options}

Return JSON ONLY:
{{
  "Domestic Content": "..."
}}

Description:
\"\"\"
{text}
\"\"\"
"""