# ==============================================================================
# GOLD STANDARD EXAMPLES (GROUND TRUTH)
# NOTE: All JSON braces are double-escaped {{ }} so .format() ignores them.
# ==============================================================================

GOLD_STANDARD_EXAMPLES = """
### EXAMPLES OF PERFECT EXTRACTION (DO NOT DEVIATE):

--- EXAMPLE 1: SERVICE ON A PLATFORM (E-2D CASE) ---
Input Text:
"Northrop Grumman... modification... to extend services and adds hours increasing the full-scale fatigue repair time... in support of E-2D Advanced Hawkeye aircraft development."

Correct Output:
{{
  "Market Segment": "Air Platforms",
  "System Type (General)": "Fixed-Wing",
  "System Type (Specific)": "AEW&C",
  "System Name (General)": "E-2D Advanced Hawkeye",
  "System Name (Specific)": "Extend Services and Adds Hours Increasing the Full-scale Fatigue Repair Time to Achieve the Required Simulated Flight Hours",
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
  "Market Segment": "Unknown",
  "System Type (General)": "Not Applicable",
  "System Type (Specific)": "Not Applicable",
  "System Name (General)": "Department of Defense Enterprise Software Initiative (DOD ESI)",
  "System Name (Specific)": "Department of Defense Enterprise Software Initiative (DOD ESI)",
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
  "Market Segment": "Naval Platforms",
  "System Type (General)": "Sub-Surface",
  "System Type (Specific)": "Nuclear-Powered Submarine",
  "System Name (General)": "Virginia-class Submarine",
  "System Name (Specific)": "Virginia-class Submarine Propulsors",
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
  "Market Segment": "Unknown",
  "System Type (General)": "Not Applicable",
  "System Type (Specific)": "Not Applicable",
  "System Name (General)": "Development and Application of Advanced Technology Solutions",
  "System Name (Specific)": "Development and Application of Advanced Technology Solutions",
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
  "Market Segment": "Naval Platforms",
  "System Type (General)": "Logistics & Support (Maritime)",
  "System Type (Specific)": "Combat Support Ship",
  "System Name (General)": "Spearhead-class of Expeditionary Fast Transport (EPF)",
  "System Name (Specific)": "USNS Apalachicola (T-EPF-13)",
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
  "Market Segment": "C4ISR Systems",
  "System Type (General)": "Cyber",
  "System Type (Specific)": "Cyber Defense",
  "System Name (General)": "Senior Consultation Support Services",
  "System Name (Specific)": "Senior Consultation Support Services",
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
  "Market Segment": "Weapon Systems",
  "System Type (General)": "Missile",
  "System Type (Specific)": "Air-to-Air",
  "System Name (General)": "AIM-9X Sidewinder",
  "System Name (Specific)": "Block II Special Air Training Missiles",
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
  "Market Segment": "Land Platforms",
  "System Type (General)": "Armoured Fighting Vehicles",
  "System Type (Specific)": "Main Battle Tank",
  "System Name (General)": "M1A2 Abrams",
  "System Name (Specific)": "M1147 Advanced Multi-Purpose (AMP) Gunner's Auxiliary Sight",
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
  "Market Segment": "C4ISR Systems",
  "System Type (General)": "Radar",
  "System Type (Specific)": "Air Search Radar",
  "System Name (General)": "AN/SPY-1 Elevated Radar Advanced Calibration Experiment",
  "System Name (Specific)": "Engineering Services",
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
  "Market Segment": "Air Platforms",
  "System Type (General)": "Rotary Wing",
  "System Type (Specific)": "Rotary Wing Attack",
  "System Name (General)": "AH-64 Apache",
  "System Name (Specific)": "AH-64 Apache",
  "Supplier Name": "Unknown",
  "Program Type": "Other Service",
  "Quantity": "Not Applicable",
  "Value Certainty": "Confirmed",
  "Value (Million)": "13.803"
}}
"""

# ==============================================================================
# 1. CLASSIFICATION PROMPT (WITH REASONING)
# ==============================================================================
RAG_CLASSIFICATION_PROMPT = f"""
You are a defence taxonomy classification engine.
YOUR TASK: Classify the contract description into the provided taxonomy hierarchy.

{GOLD_STANDARD_EXAMPLES}

### TAXONOMY DEFINITIONS (SOURCE OF TRUTH):
{{taxonomy}}

### CLASSIFICATION PROCESS (STRICTLY FOLLOW THIS FLOW):

**STEP 1: KEYWORD EXTRACTION (SCANNING)**
- First, scan the "Description" for explicit nouns, system names, or functional terms (e.g., "F-35", "Radar", "Dredging", "Sidewinder").
- **Action:** List these keywords mentally.

**STEP 2: DEFINITION LOOKUP (VERIFICATION)**
- Take the keywords from Step 1 and look them up in the **TAXONOMY DEFINITIONS** above.
- **Rule:** Do not rely on your internal training. You must find the keyword (or its functional synonym) inside the provided definitions.
- *Example:* If you found "Sidewinder", you must find the definition: "Air-to-Air: Jet vs Jet. (Example: AIM-9X Sidewinder)".
- *Correction:* If the text says "Radar for F-35", the keyword "Radar" points to **C4ISR**, not Air Platforms. The definition of "Radar" (Sensor) overrides the platform it is mounted on.

**STEP 3: CLASSIFICATION SELECTION (DECISION)**
- Based *only* on the definition match from Step 2, select the:
  1. **Market Segment**
  2. **System Type (General)**
  3. **System Type (Specific)**

### OUTPUT FORMAT:
Return JSON with a "Reasoning" field that proves you followed the flow.

{{{{
  "Reasoning": "STEP 1: Identified keyword '[KEYWORD]'. STEP 2: This matches the taxonomy definition for [SYSTEM TYPE] which is defined as '[DEFINITION SNIPPET]'. STEP 3: Therefore, classified as...",
  "Market Segment": "...",
  "System Type (General)": "...",
  "System Type (Specific)": "..."
}}}}

Description:
\"\"\"
{{text}}
\"\"\"
"""

# ==============================================================================
# 2. SYSTEM NAME PROMPT (WITH REASONING)
# ==============================================================================
SYSTEM_NAME_PROMPT = f"""
You are a defence contract extraction expert.
YOUR TASK: Extract the **System Name (General)** and **System Name (Specific)**.

{GOLD_STANDARD_EXAMPLES}

### ANALYST REASONING CHECKLIST:

**CHECK 1: THE "SUFFIX STRIP" (General Name)**
- Look at the alphanumeric code (e.g., F-35A, AH-64E, AIM-9X).
- **Action:** Remove the last letter to get the "Brand Family".
  - F-35A -> **F-35 Lightning II**
  - AH-64E -> **AH-64 Apache**
  - *Exception:* If it's a Ship Class (e.g., "Arleigh Burke-class"), keep it as is.

**CHECK 2: THE "SCOPE OF WORK" (Specific Name)**
- Is this a hardware buy? -> Use the **Variant** (e.g., "F-35A").
- Is this a service/repair? -> Use the **Task Description** (e.g., "Fatigue Repair", "Engineering Services").
- Is this an IT Program? -> **Mirror** the General Name (e.g., "DOD ESI" -> "DOD ESI").

**CHECK 3: THE "QUANTITY CLEANUP" (CRITICAL)**
- **Rule:** The Specific Name must NOT start with a number representing quantity or value.
- **Action:** Strip leading counts or amounts.
  - *Bad Input:* "1,696,629 Treatment Courses of MK-4482"
  - *Good Output:* "Treatment Courses of MK-4482"
  - *Bad Input:* "483 AIM-9X Missiles"
  - *Good Output:* "AIM-9X Missiles"

### OUTPUT FORMAT:
{{{{
  "Reasoning": "Explain: Did you strip a suffix? Did you remove a leading quantity count?",
  "System Name (General)": "...",
  "System Name (Specific)": "..."
}}}}

Description:
\"\"\"
{{text}}
\"\"\"
"""

# ==============================================================================
# 3. PILOTING PROMPT (WITH REASONING)
# ==============================================================================
SYSTEM_PILOTING_PROMPT = """
You are a defence contract system piloting classifier.
YOUR TASK: Determine the "System Piloting" mode based on the platform described.

STRICT CLASSIFICATION LOGIC (Follow in Order):

1. **Not Applicable**:
   - **IT/Software**: Cloud, Licenses, Support Services (e.g., Dell, Microsoft).
   - **Facilities/Construction**: Buildings, hangars, dredging, paving.
   - **Weapons/Missiles**: PAC-3, AIM-9X, Tomahawk (Missiles are weapons, not vehicles).
   - **Sub-Systems/Sensors**: Radars (SBIRS, AN/SPY-1), Jammers, Radios (unless the contract implies the *entire* vehicle).
   - **General Services**: Consulting, staffing, research not tied to a specific vehicle chassis.

2. **Uncrewed**:
   - **Keywords**: "Unmanned", "UAS", "UAV", "Drone", "Remotely Piloted", "Glider".
   - **Specific Platforms**: Global Hawk (RQ-4), MQ-9 Reaper, ScanEagle, RQ-21A, LBS-G, UUVs (Unmanned Underwater Vehicles).

3. **Optional**:
   - **Hybrid Systems**: Vehicles designed to operate *either* with a crew *or* autonomously.
   - **Key Phrase**: Look for "demonstration of autonomous capability" on a normally crewed vessel (e.g., Expeditionary Fast Transport / EPF-13).

4. **Crewed**:
   - **Default for Platforms**: If it is a Ship, Submarine, Aircraft, or Land Vehicle and does NOT fit the above.
   - **Ships**: DDG, SSN, T-AGS, T-AO, CVN, Frigates.
   - **Aircraft**: F-35, F-16, AH-64 Apache, E-2D Hawkeye, UH-72 Lakota, C-130.
   - **Note**: Even if the contract is for *maintenance* or *parts* (e.g., "propulsors for Virginia-class"), the System Piloting refers to the platform itself -> **Crewed**.

### OUTPUT FORMAT:
{{
  "Reasoning": "Step 1: Is it a missile/IT/radar? Step 2: Is it explicitly unmanned? Step 3: Is it a standard ship/plane?",
  "System Piloting": "..."
}}

Description:
\"\"\"
{text}
\"\"\"
"""

# ==============================================================================
# 4. GEOGRAPHY PROMPT
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
# 5. FINANCIAL PROMPT
# ==============================================================================
FINANCIAL_PROMPT = f"""
You are a defence contract financial and program analyst.
YOUR TASK: Extract supplier, program info, and financials.

{GOLD_STANDARD_EXAMPLES}

STRICT RULES:

1. **Program Type**: Choose ONE from: {{program_types}}.
   - **Procurement**: Buying hardware (missiles, ships, parts, licenses).
   - **RDT&E**: Research, studies, prototypes, analysis.
   - **MRO/Support**: Maintenance, logistics, repair.
   - **Other Service**: IT support, consulting, staffing.

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
{{{{
  "Supplier Name": "...",
  "Program Type": "...",
  "Quantity": "...",
  "Value Certainty": "...",
  "Value (Million)": "...", 
  "Currency": "...",
  "Description Date Found": "..."
}}}}

Description:
\"\"\"
{{text}}
\"\"\"
"""
# ==============================================================================
# 6. DOMESTIC CONTENT PROMPT
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