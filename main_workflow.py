# -*- coding: utf-8 -*-
"""
Merged Workflow: 
1. Targeted Scraper (Groups Multiple IDs into single row)
2. Defense RAG Processor (Processes single row for consolidated output)
"""

import pandas as pd
import numpy as np
import time
import re
import os
import sys
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# RAG / Custom Module Imports
try:
    from src.vector_engine import DefenseVectorDB
    from src.processors import classify_full_record_rag
    from src.validators import run_all_validations 
except ImportError as e:
    print(f"WARNING: Could not import 'src' modules ({e}). RAG step will fail if attempted.")

# ================= GLOBAL CONFIGURATION =================
INPUT_SOURCE_EXCEL = 'data/source_file.xlsx'
INTERMEDIATE_CSV   = 'scraped_raw_data.csv'
FINAL_OUTPUT_FILE  = 'final_defense_contracts.xlsx'
DRIVER_PATH        = "driver/msedgedriver.exe"
DB_PERSIST_DIR     = "./db_storage"

TARGET_COLUMNS = [
    "Customer Region", "Customer Country", "Customer Operator",
    "Supplier Region", "Supplier Country", "Domestic Content",
    "Market Segment", "System Type (General)", "System Type (Specific)",
    "System Name (General)", "System Name (Specific)", "System Piloting",
    "Supplier Name", "Program Type", "Expected MRO Contract Duration (Months)",
    "Quantity", "Value Certainty", "Value (Million)", "Currency",
    "Value (USD$ Million)", "G2G/B2G", "Signing Month", "Signing Year",
    "Description of Contract", "Additional Notes (Internal Only)",
    "Source Link(s)", "Contract Date", "Reported Date (By SGA)",
    "Matched_ID", "Header"
]

# ================= HELPER FUNCTIONS =================

def detect_header(paragraph_index, all_paragraphs):
    """
    Move upward in the <p> list to find the nearest <p><strong>HEADER</strong></p>
    """
    for i in range(paragraph_index, -1, -1):
        p = all_paragraphs[i]
        strong_tag = p.find("strong")
        if strong_tag:
            header_text = strong_tag.get_text(strip=True).upper()
            if header_text:
                return header_text
    return "UNKNOWN"

# ================= MAIN WORKFLOW FUNCTIONS =================

def run_scraper():
    print("\n--- [STEP 1/2] STARTING TARGETED SCRAPER ---")
    
    if not os.path.exists(INPUT_SOURCE_EXCEL):
        print(f"Error: Input file '{INPUT_SOURCE_EXCEL}' not found.")
        return False

    # ---------------------------------------------------------
    # 1. LOAD DATA & EXTRACT IDS
    # ---------------------------------------------------------
    print("Loading data and extracting IDs...")
    try:
        df = pd.read_excel(INPUT_SOURCE_EXCEL)
        # Ensure dates are parsed correctly
        df['Contract Date'] = pd.to_datetime(df["Contract Date"], dayfirst=True, errors="coerce")
    except Exception as e:
        print(f"Error reading source Excel: {e}")
        return False
    
    # Map URLs to dates for easy lookup later
    url_date_map = df.set_index('Source URL')['Contract Date'].to_dict()

    # Regex pattern for Contract IDs (e.g., N00019-21-C-0001)
    id_pattern = r"\b[A-Z0-9]{5,}-\d{2}-[A-Z]-\d{4}\b"
    extracted_ids = []
    
    for text in df['Contract Description'].astype(str):
        match_ids = re.findall(id_pattern, text)
        extracted_ids.append(match_ids)

    # Flatten and remove duplicates
    flat_ids = [cid for sub in extracted_ids for cid in sub]
    unique_ids = list(set(flat_ids))
    print(f"Extracted {len(unique_ids)} Unique Contract IDs.")

    # ---------------------------------------------------------
    # 2. SELENIUM SETUP & SCRAPING
    # ---------------------------------------------------------
    service = Service(DRIVER_PATH)
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Uncomment if you want it to run invisibly
    driver = webdriver.Edge(service=service, options=options)

    urls = df['Source URL'].dropna().unique().tolist()
    scraped_data = []
    
    print(f"\nStarting extraction for {len(urls)} URLs...\n")

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] Processing URL: {url}")
        current_date = url_date_map.get(url)

        try:
            driver.get(url)
            time.sleep(3) # Wait for page load

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Locate main content body
            body_div = soup.select_one("div.content.content-wrap div.inside.ntext div.body")
            if not body_div:
                print("  > Warning: Main body div not found.")
                continue

            paragraphs = body_div.find_all("p")

            # Iterate through paragraphs to find matches
            for p_index, p in enumerate(paragraphs):
                text = p.get_text(" ", strip=True)
                
                # Check if ANY of our unique IDs exist in this paragraph
                matched_ids_in_p = [cid for cid in unique_ids if cid in text]

                if matched_ids_in_p:
                    # Detect the section header (e.g. ARMY, NAVY)
                    header = detect_header(p_index, paragraphs)
                    
                    scraped_data.append({
                        "URL": url,
                        "Contract_Date": current_date,
                        "Header": header,
                        "Matched_IDs": matched_ids_in_p, # List of all IDs found in this specific paragraph
                        "Paragraph_Text": text
                    })

        except Exception as e:
            print(f"Error processing {url}: {e}")

    driver.quit()

    # ---------------------------------------------------------
    # 3. ROW EXPANSION & GROUPING LOGIC
    # ---------------------------------------------------------
    processed_rows = []

    for row in scraped_data:
        # Check how many IDs were found in this single paragraph
        ids_found = row["Matched_IDs"]
        num_ids = len(ids_found)
        
        if num_ids > 1:
            # === MULTIPLE IDs FOUND: GROUP THEM ===
            # Create ONE record with "Multiple" as supplier
            combined_id_str = ", ".join(ids_found)
            
            processed_rows.append({
                "Source Link(s)": row["URL"],
                "Contract Date": row["Contract_Date"],
                "Header": row["Header"],
                "Matched_ID": combined_id_str,      # All IDs stored in one cell
                "Description of Contract": row["Paragraph_Text"],
                "Supplier Name": "Multiple"         # EXPLICIT FLAG
            })
            print(f"  > Grouped {num_ids} IDs into single 'Multiple' record.")

        else:
            # === SINGLE ID FOUND: STANDARD PROCESSING ===
            # Create one record, leave Supplier Name empty for RAG to find
            processed_rows.append({
                "Source Link(s)": row["URL"],
                "Contract Date": row["Contract_Date"],
                "Header": row["Header"],
                "Matched_ID": ids_found[0],
                "Description of Contract": row["Paragraph_Text"],
                "Supplier Name": np.nan             # Left empty for RAG
            })

    # Save to Intermediate CSV
    scraped_df = pd.DataFrame(processed_rows)
    if not scraped_df.empty:
        # Remove time component from date
        scraped_df['Contract Date'] = pd.to_datetime(scraped_df['Contract Date']).dt.date

    scraped_df.to_csv(INTERMEDIATE_CSV, index=False, encoding='utf-8')
    print(f"\nSUCCESS: Saved {len(scraped_df)} records to '{INTERMEDIATE_CSV}'")
    return True

def run_rag_processor():
    print("\n--- [STEP 2/2] STARTING RAG PROCESSOR ---")
    
    # Initialize Vector Engine
    rag_db = DefenseVectorDB(persist_dir=DB_PERSIST_DIR)

    if not os.path.exists(INTERMEDIATE_CSV):
        print(f"Error: {INTERMEDIATE_CSV} missing.")
        return

    df = pd.read_csv(INTERMEDIATE_CSV, encoding='utf-8')
    results = []

    for idx, row in df.iterrows():
        print(f"Processing row {idx + 1}/{len(df)}...")
        
        desc = str(row.get("Description of Contract", ""))
        c_date = str(row.get("Contract Date", ""))
        
        # Check if Scraper flagged this as Multiple
        pre_supplier = str(row.get("Supplier Name", ""))
        
        try:
            # 1. Run RAG Classification
            res = classify_full_record_rag(desc, c_date, rag_db)
            
            # 2. Run Validation Logic
            try:
                res = run_all_validations(res, desc)
            except Exception as v_error:
                print(f"  ! Validation Warning: {v_error}")

            # 3. Override Supplier Name if needed
            # If the scraper saw multiple IDs, we force "Multiple" regardless of what RAG thinks
            if pre_supplier == "Multiple":
                res["Supplier Name"] = "Multiple"

            # 4. Standardize Currency/Value
            if "Value (Million)" in res:
                res["Value (USD$ Million)"] = res["Value (Million)"]

            # 5. Merge Metadata from Scraper
            res["Description of Contract"] = desc
            res["Contract Date"] = c_date
            res["Source Link(s)"] = row.get("Source Link(s)", "")
            res["Header"] = row.get("Header", "")
            res["Matched_ID"] = row.get("Matched_ID", "")
            
            results.append(res)

        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            # Return partial data with error
            results.append({
                "Description of Contract": desc, 
                "Error": str(e),
                "Source Link(s)": row.get("Source Link(s)", "")
            })

    # ---------------------------------------------------------
    # FINAL OUTPUT FORMATTING
    # ---------------------------------------------------------
    processed_df = pd.DataFrame(results)
    
    # Ensure all target columns exist (fill missing with empty string)
    for col in TARGET_COLUMNS:
        if col not in processed_df.columns:
            processed_df[col] = ""
            
    # Reorder columns
    final_output_df = processed_df[TARGET_COLUMNS]
    
    final_output_df.to_excel(FINAL_OUTPUT_FILE, index=False)
    print(f"\nCOMPLETE. Final dataset saved to: {FINAL_OUTPUT_FILE}")

if __name__ == "__main__":
    # Execute full pipeline
    if run_scraper():
        time.sleep(2) # Brief pause to ensure file release
        run_rag_processor()