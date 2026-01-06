import json
import datetime
import time
import pandas as pd
import re
import difflib
import os 
from dateutil import parser
from dateutil.relativedelta import relativedelta
from sentence_transformers import CrossEncoder

# Imports from other files
from config import get_api_client, MODEL_NAME
from data.taxonomy import (
    TAXONOMY_STR, VALID_DEPENDENCIES, GEOGRAPHY_MAPPING, 
    VALID_OPERATORS, SUPPLIER_LIST, PROGRAM_TYPES, DOMESTIC_CONTENT_OPTIONS
)
from src.prompts import (
    RAG_CLASSIFICATION_PROMPT, SYSTEM_NAME_PROMPT, SYSTEM_PILOTING_PROMPT,
    GEOGRAPHY_PROMPT, FINANCIAL_PROMPT, DOMESTIC_CONTENT_PROMPT
)

client = get_api_client()

# ==========================================
# 0. INITIALIZE RE-RANKER (GLOBAL)
# ==========================================
# LOGIC UPDATE: Try Online -> Fail -> Try Local Folder

# NOTE: We point to the FOLDER, not the specific file.
LOCAL_MODEL_PATH = r"C:\Users\mukeshkr\Desktop\DefenseExtraction\model"

print("Loading Cross-Encoder Re-Ranker model...")
try:
    # 1. Try downloading/loading from Hugging Face Hub
    print("Attempting to download model from Hugging Face...")
    RERANKER_MODEL = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    print("Success: Re-Ranker loaded from Hugging Face Hub.")
except Exception as e_hub:
    print(f" > Could not download from Hub ({e_hub}).")
    print(f" > Switching to local path: {LOCAL_MODEL_PATH}")
    
    try:
        # 2. Try loading from your local folder
        if os.path.exists(LOCAL_MODEL_PATH):
            # We pass the FOLDER path. It automatically finds model.safetensors & config.json
            RERANKER_MODEL = CrossEncoder(LOCAL_MODEL_PATH)
            print(f"Success: Re-Ranker loaded from local path.")
        else:
            print(f"Error: Local model folder not found at: {LOCAL_MODEL_PATH}")
            RERANKER_MODEL = None
            
    except Exception as e_local:
        print(f"CRITICAL WARNING: Could not load Re-Ranker from Local path. Error: {e_local}")
        RERANKER_MODEL = None

# ==========================================
# 1. HYBRID TAXONOMY MATCHING LOGIC
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
    first_word = clean_name.split(' ')[0]
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

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def call_llm(prompt_text: str) -> dict:
    time.sleep(2) 
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please respond in JSON format."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM Call Error: {e}")
        return {}
    

def validate_and_fix(result: dict) -> dict:
    ms = result.get("Market Segment", "Unknown")
    stg = result.get("System Type (General)", "Not Applicable")
    sts = result.get("System Type (Specific)", "Not Applicable")

    if ms not in VALID_DEPENDENCIES:
        return {"Market Segment": "Unknown", "System Type (General)": "Not Applicable", "System Type (Specific)": "Not Applicable"}

    if stg not in VALID_DEPENDENCIES[ms]:
        if ms == "C4ISR Systems":
            return {"Market Segment": ms, "System Type (General)": "Integrated C4ISR System", "System Type (Specific)": "Integrated C4ISR System"}
        else:
            return {"Market Segment": ms, "System Type (General)": "Not Applicable", "System Type (Specific)": "Not Applicable"}

    return {"Market Segment": ms, "System Type (General)": stg, "System Type (Specific)": sts}

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
                    months_match = re.search(r'(\d+)\s*months?', desc_date_str, re.IGNORECASE)
                    years_match = re.search(r'(\d+)\s*years?', desc_date_str, re.IGNORECASE)
                    if months_match:
                        mro_duration = months_match.group(1)
                    elif years_match:
                        mro_duration = str(int(years_match.group(1)) * 12)
                except:
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
# 3. MAIN RAG PIPELINE
# ==========================================

def classify_full_record_rag(description: str, contract_date_str: str, vector_db) -> dict:
    
    # 1. RETRIEVE CONTEXT
    raw_similar_docs = vector_db.search_context(description, k=10)
    
    # --- RE-RANKING LOGIC ---
    if raw_similar_docs and RERANKER_MODEL:
        try:
            pairs = [[description, doc.page_content] for doc in raw_similar_docs]
            scores = RERANKER_MODEL.predict(pairs)
            
            scored_docs = []
            for doc, score in zip(raw_similar_docs, scores):
                doc.metadata["rerank_score"] = float(score)
                scored_docs.append((doc, score))
            
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            top_docs = [item[0] for item in scored_docs[:3]]
            
        except Exception as e:
            print(f"Re-ranking failed: {e}. Falling back to vector order.")
            top_docs = raw_similar_docs[:3]
    else:
        top_docs = raw_similar_docs[:3]
    # ------------------------

    # Construct Context String
    context_str = ""
    if top_docs:
        context_str = "Below are examples of how similar contracts were classified previously (Ranked by Relevance):\n"
        for i, doc in enumerate(top_docs):
            past_segment = doc.metadata.get("Market Segment", "Unknown")
            past_general = doc.metadata.get("System Type (General)", "Unknown")
            snippet = doc.page_content[:200].replace("\n", " ") 
            context_str += f"{i+1}. TEXT: \"{snippet}...\" -> CLASSIFICATION: {past_segment} / {past_general}\n"
    else:
        context_str = "No similar past contracts found (Cold Start)."

    # 2. CLASSIFY SYSTEM (RAG)
    classify_prompt = RAG_CLASSIFICATION_PROMPT.format(
        context=context_str,
        taxonomy=TAXONOMY_STR,
        text=description
    )
    raw_class_result = call_llm(classify_prompt)
    base_result = validate_and_fix(raw_class_result)

    # 3. GEOGRAPHY
    geo_json_str = json.dumps(GEOGRAPHY_MAPPING)
    geo_prompt = GEOGRAPHY_PROMPT.format(
        operators=VALID_OPERATORS, 
        geo_mapping=geo_json_str, 
        text=description
    )
    geo_result = call_llm(geo_prompt)

    # 4. DOMESTIC CONTENT
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

    # 5. OTHER EXTRACTIONS
    name_result = call_llm(SYSTEM_NAME_PROMPT.format(text=description))
    piloting_result = call_llm(SYSTEM_PILOTING_PROMPT.format(text=description))
    
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

    # 6. DERIVED FIELDS
    derived_result = calculate_derived_fields(fin_result_raw, geo_result, description, contract_date_str)

    # 7. COMBINE ALL
    final_output = {
        **base_result, 
        **name_result, 
        **piloting_result, 
        **geo_result, 
        **dom_result,
        **derived_result
    }

    # 8. SAVE TO MEMORY
    metadata_to_save = {
        "Market Segment": final_output.get("Market Segment"),
        "System Type (General)": final_output.get("System Type (General)")
    }
    vector_db.add_contract(description, metadata_to_save)

    return final_output