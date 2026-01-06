import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import os
import sys
from bs4 import BeautifulSoup
import warnings

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Defense Contract Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BEAUTIFICATION ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004e98; 
        color: white;
    }
    .stButton>button:hover {
        background-color: #003366;
        color: white;
    }
    .status-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #eef2f5;
        border-left: 5px solid #004e98;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- IMPORT HANDLING (Graceful Fail) ---
try:
    from src.vector_engine import DefenseVectorDB
    from src.processors import classify_full_record_rag
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
except ImportError as e:
    IMPORTS_LOADED = False
    IMPORT_ERROR_MSG = str(e)

# --- GLOBAL CONFIG & SESSION STATE ---
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
    "Matched_ID", "Header" # Added these to match script logic
]

if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None
if 'final_df' not in st.session_state:
    st.session_state.final_df = None

# --- HELPER FUNCTIONS (From Your Script) ---
def detect_header(paragraph_index, all_paragraphs):
    for i in range(paragraph_index, -1, -1):
        p = all_paragraphs[i]
        strong_tag = p.find("strong")
        if strong_tag:
            header_text = strong_tag.get_text(strip=True).upper()
            if header_text:
                return header_text
    return "UNKNOWN"

# --- SIDEBAR: SETUP ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312214.png", width=80)
    st.title("Settings")
    
    st.markdown("### 1. API Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API Key Loaded!")
    
    st.markdown("### 2. Driver Config")
    driver_path = st.text_input("Edge Driver Path", value="driver/msedgedriver.exe")
    
    st.divider()
    st.info("System Status:")
    if IMPORTS_LOADED:
        st.write("✅ RAG Modules Active")
    else:
        st.error("❌ RAG Modules Missing")
        st.caption(f"Error: {IMPORT_ERROR_MSG}")

# --- MAIN APP UI ---
st.title("🛡️ Defense Contract Intelligence Hub")
st.markdown("Merged Workflow: **Targeted Scraper** + **Defense RAG Processor**")

# ==========================================================
# PHASE 1: DATA UPLOAD & ID EXTRACTION
# ==========================================================
st.header("1. Data Ingestion")
uploaded_file = st.file_uploader("Upload Source Excel File", type=['xlsx'])

if uploaded_file:
    # Read Data
    try:
        df_source = pd.read_excel(uploaded_file)
        df_source['Contract Date'] = pd.to_datetime(df_source["Contract Date"], dayfirst=True, errors="coerce")
        
        # UI Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df_source))
        with col2:
            st.metric("Unique URLs", df_source['Source URL'].nunique())
            
        # ID Extraction Logic
        id_pattern = r"\b[A-Z0-9]{5,}-\d{2}-[A-Z]-\d{4}\b"
        extracted_ids = []
        for text in df_source['Contract Description'].astype(str):
            match_ids = re.findall(id_pattern, text)
            extracted_ids.append(match_ids)
        
        flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
        
        with col3:
            st.metric("Extracted Contract IDs", len(flat_ids))

        with st.expander("🔍 View Extracted IDs"):
            st.write(flat_ids)
            
    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.stop()

    st.divider()

    # ==========================================================
    # PHASE 2: SELENIUM SCRAPER
    # ==========================================================
    st.header("2. Live Scraping Execution")
    
    col_a, col_b = st.columns([1, 3])
    
    with col_a:
        st.info("Scraper controls the browser locally. You will see the window open.")
        start_scrape = st.button("🚀 Launch Scraper", type="primary")

    if start_scrape:
        status_container = st.status("Initializing Browser...", expanded=True)
        progress_bar = st.progress(0)
        
        try:
            # Setup Map
            url_date_map = df_source.set_index('Source URL')['Contract Date'].to_dict()
            urls = df_source['Source URL'].dropna().unique().tolist()
            
            # Selenium Setup
            service = Service(driver_path)
            options = webdriver.EdgeOptions()
            options.add_argument("--start-maximized")
            # NOTE: We keep headless=False so you can SEE the browser as requested
            driver = webdriver.Edge(service=service, options=options)
            
            scraped_data = []
            
            # Execution Loop
            for idx, url in enumerate(urls):
                status_container.write(f"🌍 Visiting [{idx+1}/{len(urls)}]: {url}")
                progress_bar.progress((idx + 1) / len(urls))
                
                current_date = url_date_map.get(url)
                
                try:
                    driver.get(url)
                    time.sleep(2) # Slight delay to let page load
                    
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    
                    # Logic: Find Body
                    body_div = soup.select_one("div.content.content-wrap div.inside.ntext div.body")
                    
                    if body_div:
                        paragraphs = body_div.find_all("p")
                        for p_index, p in enumerate(paragraphs):
                            text = p.get_text(" ", strip=True)
                            
                            # Check against ALL unique extracted IDs
                            matched_ids = [cid for cid in flat_ids if cid in text]
                            
                            if matched_ids:
                                header = detect_header(p_index, paragraphs)
                                scraped_data.append({
                                    "URL": url,
                                    "Contract_Date": current_date,
                                    "Header": header,
                                    "Matched_IDs": matched_ids, # List of IDs found
                                    "Paragraph_Text": text
                                })
                except Exception as e:
                    status_container.write(f"⚠️ Error on {url}: {e}")
            
            driver.quit()
            status_container.update(label="Scraping Complete!", state="complete", expanded=False)
            
            # --- UPDATED POST-PROCESSING LOGIC (Grouping) ---
            expanded_rows = []
            
            for row in scraped_data:
                # Check how many IDs were found in this single paragraph
                num_ids = len(row["Matched_IDs"])
                
                if num_ids > 1:
                    # === GROUP LOGIC ===
                    # If multiple IDs exist, create ONE row with "Multiple" supplier
                    combined_ids = ", ".join(row["Matched_IDs"])
                    
                    expanded_rows.append({
                        "Source Link(s)": row["URL"],
                        "Contract Date": row["Contract_Date"],
                        "Header": row["Header"],
                        "Matched_ID": combined_ids,
                        "Description of Contract": row["Paragraph_Text"],
                        "Supplier Name": "Multiple" # Flag for next step
                    })
                else:
                    # === STANDARD LOGIC ===
                    # Single ID, standard row
                    expanded_rows.append({
                        "Source Link(s)": row["URL"],
                        "Contract Date": row["Contract_Date"],
                        "Header": row["Header"],
                        "Matched_ID": row["Matched_IDs"][0],
                        "Description of Contract": row["Paragraph_Text"],
                        "Supplier Name": np.nan # Let RAG decide
                    })
            
            st.session_state.scraped_df = pd.DataFrame(expanded_rows)
            
            if not st.session_state.scraped_df.empty:
                st.session_state.scraped_df['Contract Date'] = pd.to_datetime(st.session_state.scraped_df['Contract Date']).dt.date
                
        except Exception as e:
            st.error(f"Critical Scraper Error: {e}")

    # Display Scraped Results
    if st.session_state.scraped_df is not None:
        st.success(f"Successfully scraped {len(st.session_state.scraped_df)} relevant records (grouped where applicable).")
        st.dataframe(st.session_state.scraped_df, use_container_width=True)
        
        st.divider()

        # ==========================================================
        # PHASE 3: RAG / LLM PROCESSING
        # ==========================================================
        st.header("3. AI Intelligence Processor")
        
        if not IMPORTS_LOADED:
            st.warning("⚠️ RAG modules (src folder) not found. Cannot proceed to AI processing.")
        elif not api_key:
            st.warning("⚠️ Please enter OpenAI API Key in sidebar to start AI processing.")
        else:
            col_rag_1, col_rag_2 = st.columns([1, 3])
            with col_rag_1:
                start_rag = st.button("🧠 Start AI Processing", type="primary")
            
            if start_rag:
                rag_status = st.status("Loading Vector DB...", expanded=True)
                rag_progress = st.progress(0)
                
                try:
                    # Init DB
                    rag_db = DefenseVectorDB(persist_dir="./db_storage")
                    
                    df_to_process = st.session_state.scraped_df
                    results = []
                    
                    total_rows = len(df_to_process)
                    
                    for idx, row in df_to_process.iterrows():
                        rag_status.write(f"🤖 Analyzing Record {idx + 1}/{total_rows}")
                        rag_progress.progress((idx + 1) / total_rows)
                        
                        desc = str(row.get("Description of Contract", ""))
                        c_date = str(row.get("Contract Date", ""))
                        
                        # LOGIC UPDATE: Get Pre-flagged supplier
                        pre_supplier = str(row.get("Supplier Name", ""))
                        
                        try:
                            # 1. Classification
                            res = classify_full_record_rag(desc, c_date, rag_db)
                            
                            # 2. Validation
                            try:
                                res = run_all_validations(res, desc)
                            except Exception as v_error:
                                # Optional: log warning
                                pass
                            
                            # 3. Override Supplier Name if flagged
                            if pre_supplier == "Multiple":
                                res["Supplier Name"] = "Multiple"

                            # 4. Standardization
                            if "Value (Million)" in res:
                                res["Value (USD$ Million)"] = res["Value (Million)"]
                            
                            # 5. Metadata Merge
                            res["Description of Contract"] = desc
                            res["Contract Date"] = c_date
                            res["Source Link(s)"] = row.get("Source Link(s)", "")
                            res["Header"] = row.get("Header", "")
                            res["Matched_ID"] = row.get("Matched_ID", "")
                            
                            results.append(res)
                            
                        except Exception as e:
                            rag_status.write(f"❌ Error on row {idx}: {e}")
                            results.append({"Description of Contract": desc, "Error": str(e)})
                    
                    rag_status.update(label="AI Processing Complete!", state="complete", expanded=False)
                    
                    # Final Formatting
                    processed_df = pd.DataFrame(results)
                    for col in TARGET_COLUMNS:
                        if col not in processed_df.columns:
                            processed_df[col] = ""
                            
                    st.session_state.final_df = processed_df[TARGET_COLUMNS]
                    
                except Exception as e:
                    st.error(f"RAG Pipeline Error: {e}")

        # ==========================================================
        # PHASE 4: RESULTS & EXPORT
        # ==========================================================
        if st.session_state.final_df is not None:
            st.header("4. Final Intelligence Report")
            st.dataframe(st.session_state.final_df, use_container_width=True)
            
            # Export
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                st.session_state.final_df.to_excel(writer, index=False, sheet_name='Defense_Contracts')
            
            st.download_button(
                label="📥 Download Final Excel Report",
                data=output.getvalue(),
                file_name="Final_Defense_Contracts_Analyzed.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("👋 Please upload an Excel file to begin.")