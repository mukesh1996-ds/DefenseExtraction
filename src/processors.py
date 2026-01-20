import json
import datetime
import time
import pandas as pd
import re
import difflib
import os
from dateutil import parser
from dateutil.relativedelta import relativedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

# Imports from other files
from config import MODEL_NAME, BASE_URL
from data.taxonomy import (
    TAXONOMY_STR, VALID_DEPENDENCIES, GEOGRAPHY_MAPPING,
    VALID_OPERATORS, SUPPLIER_LIST, PROGRAM_TYPES, DOMESTIC_CONTENT_OPTIONS
)
from src.prompts import (
    GEOGRAPHY_PROMPT, FINANCIAL_PROMPT, DOMESTIC_CONTENT_PROMPT
)

# ==========================================
# ✅ MEMORY FILE PATH (STREAMLIT CLOUD SAFE)
# ==========================================
MEMORY_FILE_NAME = "Market Segment.xlsx"   # <-- Must be saved in app root by Streamlit uploader

vectorizer = None
example_vectors = None
df_examples = None


def load_memory():
    """
    Loads Memory Excel and builds TF-IDF vectors.
    Works on Streamlit Cloud & local systems.
    """
    global vectorizer, example_vectors, df_examples

    vectorizer = None
    example_vectors = None
    df_examples = None

    try:
        if os.path.exists(MEMORY_FILE_NAME):
            df_examples = pd.read_excel(MEMORY_FILE_NAME)

            if "Description of Contract" not in df_examples.columns:
                print(f"⚠️ Memory load failed: 'Description of Contract' column not found in {MEMORY_FILE_NAME}")
                return

            # Build TF-IDF
            vectorizer = TfidfVectorizer(stop_words="english")
            example_vectors = vectorizer.fit_transform(df_examples["Description of Contract"].astype(str))

            print(f"✅ Memory loaded successfully from '{MEMORY_FILE_NAME}' | Rows: {len(df_examples)}")
        else:
            print(f"⚠️ Memory file not found: '{MEMORY_FILE_NAME}' (Memory disabled)")

    except Exception as e:
        print(f"❌ CRITICAL: Failed loading memory file '{MEMORY_FILE_NAME}': {e}")
        vectorizer, example_vectors, df_examples = None, None, None


# ✅ Load Memory at import time (Streamlit Cloud safe)
load_memory()


# ==========================================
# 1. HELPER FUNCTIONS
# ==========================================
SORTED_SUPPLIER_LIST = sorted(SUPPLIER_LIST, key=len, reverse=True)


def get_best_taxonomy_match(extracted_name: str) -> str:
    if not extracted_name or extracted_name.lower() in ["unknown", "not applicable", "multiple"]:
        return "Unknown"

    clean_name = extracted_name.strip()
    clean_name_lower = clean_name.lower()

    # Exact Match
    for supplier in SORTED_SUPPLIER_LIST:
        if clean_name_lower == supplier.lower():
            return supplier

    # Brand Name Filtering
    first_word = clean_name.split(" ")[0]
    candidates = [s for s in SORTED_SUPPLIER_LIST if first_word.lower() in s.lower()]

    if candidates:
        matches = difflib.get_close_matches(clean_name, candidates, n=1, cutoff=0.4)
        if matches:
            return matches[0]

    # Global Fuzzy Match
    matches = difflib.get_close_matches(clean_name, SORTED_SUPPLIER_LIST, n=1, cutoff=0.7)
    if matches:
        return matches[0]

    # Substring Safety Net
    for supplier in SORTED_SUPPLIER_LIST:
        if supplier.lower() in clean_name_lower:
            return supplier

    return clean_name


def call_llm(prompt_text: str, system_message: str = "You are a helpful assistant. Please respond in JSON format.") -> dict:
    """
    Safe LLM wrapper.
    If API fails, returns {} instead of crashing.
    """
    time.sleep(0.2)

    try:
        # Create client inside the function to ensure fresh connection
        client = OpenAI(base_url=BASE_URL)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0,
            response_format={"type": "json_object"},
            timeout=60.0  # <--- THIS IS THE FIX (Wait up to 60 seconds)
        )

        content = response.choices[0].message.content
        if not content:
            print("⚠️ LLM returned empty response content.")
            return {}

        return json.loads(content)

    except Exception as e:
        print(f"❌ LLM Call Error: {e}")
        return {}
    
    

def get_similar_example(new_text: str):
    """
    Finds the single most similar contract from the analyst memory using TF-IDF.
    Returns the text and correct classification.
    """
    if vectorizer is None or df_examples is None or example_vectors is None:
        return None

    try:
        new_vec = vectorizer.transform([str(new_text)])
        similarities = cosine_similarity(new_vec, example_vectors).flatten()
        best_idx = similarities.argmax()

        if similarities[best_idx] > 0.1:
            row = df_examples.iloc[best_idx]
            return {
                "text": row["Description of Contract"],
                "classification": {
                    "Market Segment": row.get("Market Segment", "Unknown"),
                    "System Type (General)": row.get("System Type (General)", "Unknown"),
                    "System Type (Specific)": row.get("System Type (Specific)", "Unknown"),
                    "System Name (General)": row.get("System Name (General)", "Unknown"),
                    "System Name (Specific)": row.get("System Name (Specific)", "Unknown"),
                    "System Piloting": row.get("System Piloting", "Derived from logic")
                }
            }

    except Exception as e:
        print(f"❌ Error finding similar example: {e}")

    return None


def calculate_derived_fields(financial_data: dict, geo_data: dict, description: str, contract_date_str: str) -> dict:
    try:
        start_date = pd.to_datetime(contract_date_str, dayfirst=True)
    except Exception:
        start_date = datetime.datetime.today()

    signing_month = start_date.strftime("%B")
    signing_year = str(start_date.year)

    val_llm_output = financial_data.get("Value (Million)", "0.000")
    try:
        clean_val = str(val_llm_output).replace(",", "").replace("$", "").replace("M", "").strip()
        val_float = float(clean_val)
        val_formatted = "{:.3f}".format(val_float)
    except (ValueError, TypeError):
        val_formatted = "0.000"

    cust_country = geo_data.get("Customer Country", "Unknown")
    supp_country = geo_data.get("Supplier Country", "Unknown")
    deal_type = "B2G" if (cust_country == "USA" and supp_country == "USA") else "G2G"

    program_type = financial_data.get("Program Type", "Other Service")
    mro_duration = "Not Applicable"

    if program_type == "MRO/Support":
        desc_date_str = financial_data.get("Description Date Found", "")
        if desc_date_str and desc_date_str.strip() != "":
            try:
                end_date = parser.parse(desc_date_str, fuzzy=True)
                diff = relativedelta(end_date, start_date)
                total_months = diff.years * 12 + diff.months
                mro_duration = str(max(0, int(total_months)))
            except Exception:
                try:
                    months_match = re.search(r"(\d+)\s*months?", desc_date_str, re.IGNORECASE)
                    years_match = re.search(r"(\d+)\s*years?", desc_date_str, re.IGNORECASE)
                    if months_match:
                        mro_duration = months_match.group(1)
                    elif years_match:
                        mro_duration = str(int(years_match.group(1)) * 12)
                except Exception:
                    mro_duration = "Unknown"

    qty = financial_data.get("Quantity", "Not Applicable")
    if program_type != "Procurement":
        qty = "Not Applicable"

    return {
        "Supplier Name": financial_data.get("Supplier Name", "Unknown"),
        "Program Type": program_type,
        "Expected MRO Contract Duration (Months)": mro_duration,
        "Quantity": qty,
        "Value Certainty": financial_data.get("Value Certainty", "Confirmed"),
        "Value (Million)": val_formatted,
        "Currency": "USD$",
        "Value (USD$ Million)": val_formatted,
        "G2G/B2G": deal_type,
        "Signing Month": signing_month,
        "Signing Year": signing_year
    }


# ==========================================
# 2. MAIN PROCESSOR
# ==========================================
def classify_record_with_memory(description: str, contract_date_str: str) -> dict:
    """
    Main entry point for processing a single row.
    Integrates:
    - TF-IDF Analyst Memory (Market Segment, Systems, Names, Piloting)
    - Geography, Domestic Content, Financials
    """

    # ✅ Reload memory each time to ensure latest upload works in Streamlit Cloud
    # (Streamlit reruns scripts often, but this ensures consistency)
    if vectorizer is None:
        load_memory()

    # --- A. MEMORY CLASSIFICATION ---
    similar_case = get_similar_example(description)

    system_instruction = f"""
    You are a Defense Contract Analyst.
    Your goal is to extract technical data points from the "Input Text".

    REFERENCE TAXONOMY:
    {TAXONOMY_STR}
    """

    user_message = f"Input Text: {description}\n\n"

    if similar_case:
        user_message += f"""
        IMPORTANT REFERENCE - Here is a similar contract classified by a human analyst.
        Use this as a guide for your logic:

        [Past Input]: {similar_case['text'][:300]}...
        [Past Correct Output]: {json.dumps(similar_case['classification'])}

        Now, apply the same logic to the current Input Text.
        """

    user_message += """
    --------------------------------------------------------
    REQUIREMENTS:
    1. Classify 'Market Segment', 'System Type (General)', 'System Type (Specific)' using the Taxonomy.
    2. Extract 'System Name (Specific)' (e.g., MC-130J) and 'System Name (General)' (e.g., C-130).
    3. Determine 'System Piloting' (Crewed, Uncrewed, or Not Applicable).
       - Software/Services/Ammo/Infra = "Not Applicable".
       - Manned Vehicles = "Crewed".
       - Drones/Satellites = "Uncrewed".

    Return JSON only with these exact keys:
    {
        "Market Segment": "...",
        "System Type (General)": "...",
        "System Type (Specific)": "...",
        "System Name (General)": "...",
        "System Name (Specific)": "...",
        "System Piloting": "..."
    }
    """

    class_result = call_llm(user_message, system_instruction)

    # --- B. GEOGRAPHY ---
    geo_json_str = json.dumps(GEOGRAPHY_MAPPING)

    geo_prompt = GEOGRAPHY_PROMPT.format(
        operators=VALID_OPERATORS,
        geo_mapping=geo_json_str,
        text=description
    )
    geo_result = call_llm(geo_prompt)

    # --- C. DOMESTIC CONTENT ---
    cust_c = geo_result.get("Customer Country", "Unknown")
    supp_c = geo_result.get("Supplier Country", "Unknown")

    dom_prompt = DOMESTIC_CONTENT_PROMPT.format(
        supplier_country=supp_c,
        customer_country=cust_c,
        options=DOMESTIC_CONTENT_OPTIONS,
        text=description
    )
    dom_result_raw = call_llm(dom_prompt)
    dom_val = dom_result_raw.get("Domestic Content", "Imported")

    if cust_c.lower() == supp_c.lower() and cust_c != "Unknown":
        dom_val = "Indigenous"

    if dom_val not in DOMESTIC_CONTENT_OPTIONS:
        dom_val = "Imported"

    dom_result = {"Domestic Content": dom_val}

    # --- D. FINANCIALS ---
    fin_prompt = FINANCIAL_PROMPT.format(
        program_types=PROGRAM_TYPES,
        supplier_list=", ".join(SUPPLIER_LIST),
        text=description
    )
    fin_result_raw = call_llm(fin_prompt)

    # Strict Supplier Match
    raw_llm_supplier = fin_result_raw.get("Supplier Name", "Unknown")
    matched_taxonomy_name = get_best_taxonomy_match(raw_llm_supplier)
    fin_result_raw["Supplier Name"] = matched_taxonomy_name

    derived_result = calculate_derived_fields(
        fin_result_raw, geo_result, description, contract_date_str
    )

    # --- FINAL MERGE ---
    final_output = {
        **class_result,
        **geo_result,
        **dom_result,
        **derived_result
    }

    return final_output