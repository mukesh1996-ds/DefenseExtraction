import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import os
import sys
import shutil
import json
import datetime  # FIXED: Added datetime import
from bs4 import BeautifulSoup
from io import BytesIO

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

# Import Project ID from config
try:
    from config import PROJECT_ID
except ImportError:
    PROJECT_ID = "my-test-project"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Defense Contract Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 5px; height: 3em;
        background-color: #004e98; color: white;
    }
    .stButton>button:hover { background-color: #003366; color: white; }
    .status-box {
        padding: 15px; border-radius: 8px; background-color: #eef2f5;
        border-left: 5px solid #004e98; margin-bottom: 10px;
    }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- IMPORT HANDLING ---
try:
    # UPDATED IMPORTS FOR NEW LOGIC
    from src.processors import classify_record_with_memory
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
    IMPORT_ERROR_MSG = ""
except ImportError as e:
    IMPORTS_LOADED = False
    IMPORT_ERROR_MSG = str(e)

# --- GLOBAL VARIABLES ---
# EXACT COLUMNS REQUESTED BY USER
TARGET_COLUMNS = [
    "Customer Region", "Customer Country", "Customer Operator",
    "Supplier Region", "Supplier Country", "Domestic Content",
    "Market Segment", "System Type (General)", "System Type (Specific)",
    "System Name (General)", "System Name (Specific)", "System Piloting",
    "Supplier Name", "Program Type", "Expected MRO Contract Duration (Months)",
    "Quantity", "Value Certainty", "Value (Million)", "Currency",
    "Value (USD$ Million)", "Value Note (If Any)", "G2G/B2G", 
    "Signing Month", "Signing Year", "Description of Contract", 
    "Additional Notes (Internal Only)", "Source Link(s)", 
    "Contract Date", "Reported Date (By SGA)"
]

if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None
if 'final_df' not in st.session_state:
    st.session_state.final_df = None

# --- HELPER FUNCTIONS ---
def detect_header(paragraph_index, all_paragraphs):
    for i in range(paragraph_index, -1, -1):
        p = all_paragraphs[i]
        strong_tag = p.find("strong")
        if strong_tag:
            header_text = strong_tag.get_text(strip=True).upper()
            if header_text:
                return header_text
    return "UNKNOWN"

def normalize_id(id_str):
    """Removes hyphens to allow for 'smart matching'."""
    return str(id_str).replace("-", "").strip().upper()

def get_driver():
    """
    Intelligent Driver Selection with Cloud Support
    """
    if sys.platform == "linux":
        # --- CLOUD CONFIGURATION ---
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        # Anti-Detection Headers
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        chromium_path = shutil.which("chromium") or "/usr/bin/chromium"
        options.binary_location = chromium_path
        
        driver_path = shutil.which("chromedriver") or "/usr/bin/chromedriver"
        service = ChromeService(driver_path)
        
        return webdriver.Chrome(service=service, options=options)
        
    else:
        # --- LOCAL CONFIGURATION ---
        driver_path = "driver/msedgedriver.exe" 
        
        if os.path.exists(driver_path):
            service = EdgeService(driver_path)
        else:
            service = EdgeService() 

        options = EdgeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Edge(service=service, options=options)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312214.png", width=80)
    st.title("Settings")
    
    st.markdown("### 1. API Configuration")
    st.caption(f"Project ID: `{PROJECT_ID}`")
    
    user_token = st.text_input("LLM Foundry Token", type="password", placeholder="Enter your token...")
    
    formatted_api_key = None
    if user_token:
        formatted_api_key = f"{user_token}:{PROJECT_ID}"
        os.environ["LLMFOUNDRY_TOKEN"] = user_token
        os.environ["OPENAI_API_KEY"] = formatted_api_key
        st.success("✅ Token Loaded!")

    st.divider()
    st.markdown("### 2. System Check")
    if IMPORTS_LOADED:
        st.write("✅ RAG Modules Active")
    else:
        st.error("❌ RAG Modules Missing")
        st.caption(f"Error: {IMPORT_ERROR_MSG}")

    # Check for Memory File
    mem_file_path = "/content/Market Segment.xlsx" # Default path in code
    local_mem_path = "Market Segment.xlsx"
    if os.path.exists(mem_file_path) or os.path.exists(local_mem_path):
        st.write("✅ Analyst Memory File Found")
    else:
        st.warning("⚠️ 'Market Segment.xlsx' not found. Memory disabled.")

# --- MAIN UI ---
st.title("🛡️ Defense Contract Intelligence Hub")

# TABS FOR WORKFLOW
tab_batch, tab_demo = st.tabs(["📁 Batch Processing (File)", "🧪 Live Demo (Test)"])

# ==========================================================
# TAB 1: BATCH PROCESSING
# ==========================================================
with tab_batch:
    st.markdown("Merged Workflow: **Targeted Scraper** + **Analyst Memory Processor**")
    
    # 1. DATA UPLOAD
    st.subheader("1. Data Ingestion")
    uploaded_file = st.file_uploader("Upload Source Excel File", type=['xlsx'])

    if uploaded_file:
        try:
            df_source = pd.read_excel(uploaded_file)
            df_source['Contract Date'] = pd.to_datetime(df_source["Contract Date"], dayfirst=True, errors="coerce")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", len(df_source))
            with col2:
                st.metric("Unique URLs", df_source['Source URL'].nunique())
                
            # ID EXTRACTION LOGIC
            dash_pattern = r"\b[A-Z0-9]{6}-\d{2}-[A-Z0-9]-\d{4}\b"
            continuous_pattern = r"\b[A-Z0-9]{6}\d{2}[A-Z0-9]\d{4}\b"
            combined_pattern = f"{dash_pattern}|{continuous_pattern}"

            extracted_ids = []
            if 'Contract Description' in df_source.columns:
                for text in df_source['Contract Description'].astype(str):
                    match_ids = re.findall(combined_pattern, text)
                    extracted_ids.append(match_ids)
            
            flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
            
            with col3:
                st.metric("Extracted Contract IDs", len(flat_ids))

            with st.expander("🔍 View Extracted IDs"):
                if len(flat_ids) > 0:
                    st.write(flat_ids)
                else:
                    st.warning("No IDs extracted. Scraper will rely only on URLs.")
                
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.stop()

        st.divider()

        # 2. SCRAPER
        st.subheader("2. Live Scraping Execution")
        
        col_a, col_b = st.columns([1, 3])
        with col_a:
            start_scrape = st.button("🚀 Launch Scraper", type="primary")

        if start_scrape:
            status_container = st.status("Initializing Browser...", expanded=True)
            progress_bar = st.progress(0)
            
            try:
                url_date_map = df_source.set_index('Source URL')['Contract Date'].to_dict()
                urls = df_source['Source URL'].dropna().unique().tolist()
                
                driver = get_driver()
                
                if driver:
                    scraped_data = []
                    normalized_id_map = {normalize_id(cid): cid for cid in flat_ids}
                    
                    for idx, url in enumerate(urls):
                        status_container.write(f"🌍 Visiting [{idx+1}/{len(urls)}]: {url}")
                        progress_bar.progress((idx + 1) / len(urls))
                        
                        current_date = url_date_map.get(url)
                        
                        try:
                            driver.get(url)
                            time.sleep(5) 
                            
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            
                            # Fallback Selector
                            body_div = soup.select_one("div.content.content-wrap div.inside.ntext div.body")
                            if not body_div: body_div = soup.select_one("div.body")
                            if not body_div: body_div = soup.find("body")

                            if body_div:
                                paragraphs = body_div.find_all("p")
                                
                                for p_index, p in enumerate(paragraphs):
                                    text = p.get_text(" ", strip=True)
                                    clean_text = normalize_id(text)
                                    
                                    found_matches = []
                                    for clean_id, original_id in normalized_id_map.items():
                                        if clean_id in clean_text:
                                            found_matches.append(original_id)
                                    
                                    if found_matches:
                                        header = detect_header(p_index, paragraphs)
                                        scraped_data.append({
                                            "URL": url,
                                            "Contract_Date": current_date,
                                            "Header": header,
                                            "Matched_IDs": found_matches, 
                                            "Paragraph_Text": text
                                        })
                            else:
                                status_container.write(f"⚠️ Warning: No content found on {url}")

                        except Exception as e:
                            status_container.write(f"⚠️ Error on {url}: {e}")
                    
                    driver.quit()
                    status_container.update(label="Scraping Complete!", state="complete", expanded=False)
                    
                    # Process Results
                    expanded_rows = []
                    for row in scraped_data:
                        num_ids = len(row["Matched_IDs"])
                        if num_ids > 1:
                            combined_ids = ", ".join(row["Matched_IDs"])
                            expanded_rows.append({
                                "Source Link(s)": row["URL"],
                                "Contract Date": row["Contract_Date"],
                                "Header": row["Header"],
                                "Matched_ID": combined_ids,
                                "Description of Contract": row["Paragraph_Text"],
                                "Supplier Name": "Multiple" 
                            })
                        else:
                            expanded_rows.append({
                                "Source Link(s)": row["URL"],
                                "Contract Date": row["Contract_Date"],
                                "Header": row["Header"],
                                "Matched_ID": row["Matched_IDs"][0],
                                "Description of Contract": row["Paragraph_Text"],
                                "Supplier Name": np.nan 
                            })
                    
                    st.session_state.scraped_df = pd.DataFrame(expanded_rows)
                    if not st.session_state.scraped_df.empty:
                        st.session_state.scraped_df['Contract Date'] = pd.to_datetime(st.session_state.scraped_df['Contract Date']).dt.date
                
            except Exception as e:
                st.error(f"Critical Scraper Error: {e}")

        if st.session_state.scraped_df is not None:
            st.success(f"Successfully scraped {len(st.session_state.scraped_df)} relevant records.")
            st.dataframe(st.session_state.scraped_df, use_container_width=True)
            st.divider()

            # 3. AI PROCESSING
            st.subheader("3. AI Intelligence Processor")
            
            if not IMPORTS_LOADED:
                st.warning("⚠️ RAG modules (src folder) not found.")
            elif not formatted_api_key:
                st.warning("⚠️ Please enter LLM Foundry Token in sidebar to start.")
            else:
                col_rag_1, col_rag_2 = st.columns([1, 3])
                with col_rag_1:
                    start_rag = st.button("🧠 Start AI Processing", type="primary")
                
                if start_rag:
                    rag_status = st.status("Initializing Analyst Memory...", expanded=True)
                    rag_progress = st.progress(0)
                    
                    try:
                        df_to_process = st.session_state.scraped_df
                        results = []
                        total_rows = len(df_to_process)
                        
                        for idx, row in df_to_process.iterrows():
                            rag_status.write(f"🤖 Analyzing Record {idx + 1}/{total_rows}")
                            rag_progress.progress((idx + 1) / total_rows)
                            
                            desc = str(row.get("Description of Contract", ""))
                            c_date = str(row.get("Contract Date", ""))
                            pre_supplier = str(row.get("Supplier Name", ""))
                            
                            try:
                                # 1. CLASSIFY WITH MEMORY
                                res = classify_record_with_memory(desc, c_date)
                                
                                # 2. VALIDATE
                                try:
                                    res = run_all_validations(res, desc)
                                except:
                                    pass
                                
                                # 3. OVERRIDES & STANDARDIZATION
                                if pre_supplier == "Multiple":
                                    res["Supplier Name"] = "Multiple"

                                if "Value (Million)" in res:
                                    res["Value (USD$ Million)"] = res["Value (Million)"]
                                
                                # 4. METADATA MAPPING
                                res["Description of Contract"] = desc
                                res["Contract Date"] = c_date
                                res["Source Link(s)"] = row.get("Source Link(s)", "")
                                res["Header"] = row.get("Header", "")
                                res["Value Note (If Any)"] = "" # Placeholder
                                res["Reported Date (By SGA)"] = datetime.datetime.now().strftime("%Y-%m-%d")
                                
                                results.append(res)
                                
                            except Exception as e:
                                rag_status.write(f"❌ Error on row {idx}: {e}")
                                results.append({"Description of Contract": desc, "Additional Notes (Internal Only)": str(e)})
                        
                        rag_status.update(label="AI Processing Complete!", state="complete", expanded=False)
                        
                        processed_df = pd.DataFrame(results)
                        
                        # Ensure all columns exist
                        for col in TARGET_COLUMNS:
                            if col not in processed_df.columns:
                                processed_df[col] = ""
                        
                        st.session_state.final_df = processed_df[TARGET_COLUMNS]
                        
                    except Exception as e:
                        st.error(f"Pipeline Error: {e}")

            # 4. EXPORT
            if st.session_state.final_df is not None:
                st.subheader("4. Final Intelligence Report")
                st.dataframe(st.session_state.final_df, use_container_width=True)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    st.session_state.final_df.to_excel(writer, index=False, sheet_name='Defense_Contracts')
                
                st.download_button(
                    label="📥 Download Final Excel Report",
                    data=output.getvalue(),
                    file_name="Final_Defense_Contracts_Analyzed.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# ==========================================================
# TAB 2: LIVE DEMO
# ==========================================================
with tab_demo:
    st.header("🧪 Live Analyst Demo")
    st.info("Test the new 'Memory' logic on a single paragraph. No scraper required.")

    if not formatted_api_key:
        st.error("🔒 Please enter your LLM Token in the Sidebar first.")
    else:
        col_input, col_meta = st.columns([3, 1])
        
        with col_input:
            demo_text = st.text_area("Paste Contract Text Here:", height=200, 
                                     placeholder="e.g., Jacobs/HDR JV... awarded $90M contract for architect-engineer services...")
        
        with col_meta:
            # FIXED: datetime import is now available
            demo_date = st.date_input("Contract Date", value=datetime.date.today())
            run_demo = st.button("⚡ Analyze Text", type="primary")

        if run_demo and demo_text:
            with st.spinner("Consulting Analyst Memory & Taxonomy..."):
                try:
                    # 1. Run Classification
                    date_str = demo_date.strftime("%Y-%m-%d")
                    demo_result = classify_record_with_memory(demo_text, date_str)
                    
                    # 2. Run Validation
                    demo_result = run_all_validations(demo_result, demo_text)
                    
                    # 3. Add Missing Columns for Display
                    demo_result["Contract Date"] = date_str
                    demo_result["Description of Contract"] = demo_text
                    
                    # Display as JSON
                    st.subheader("Raw JSON Output")
                    st.json(demo_result)
                    
                    # Display as Table (Transposed for readability)
                    st.subheader("Structured Data")
                    
                    # Create DataFrame with TARGET COLUMNS order
                    display_data = {k: demo_result.get(k, "") for k in TARGET_COLUMNS}
                    df_demo = pd.DataFrame([display_data]).transpose()
                    df_demo.columns = ["Extracted Value"]
                    st.dataframe(df_demo, height=800, use_container_width=True)

                except Exception as e:
                    st.error(f"Analysis Failed: {e}")