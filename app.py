import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import os
import sys
import shutil
import json
import datetime
import traceback  # <--- ADDED FOR DEBUGGING
from bs4 import BeautifulSoup
from io import BytesIO

# Visualization
import plotly.express as px
import plotly.graph_objects as go

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Defense Intel Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEBUGGING / ERROR CATCHING IMPORTS ---
# We wrap this in a try-catch that PRINTS the error to the screen
try:
    # Try importing project config
    try:
        from config import PROJECT_ID
    except ImportError:
        PROJECT_ID = "my-test-project"

    # Try importing local modules
    # NOTE: If these files initialize API clients at the top level, 
    # they will crash here if keys aren't set yet.
    from src.processors import classify_record_with_memory
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
    IMPORT_ERROR_MSG = None

except Exception as e:
    IMPORTS_LOADED = False
    IMPORT_ERROR_MSG = traceback.format_exc()

# --- GLOBAL VARIABLES ---
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
            if header_text: return header_text
    return "UNKNOWN"

def normalize_id(id_str):
    return str(id_str).replace("-", "").strip().upper()

def get_driver():
    # ... (Keep your existing driver logic here, omitted for brevity as it works) ...
    # Placeholder for brevity since scraping works:
    if sys.platform == "linux":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_path = shutil.which("chromedriver") or "/usr/bin/chromedriver"
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)
    else:
        # Local Logic
        return webdriver.Edge() 

def save_memory():
    """Saves uploaded memory file with error handling."""
    uploaded = st.session_state.mem_uploader
    if uploaded:
        try:
            # Save to root
            with open("Market Segment.xlsx", "wb") as f:
                f.write(uploaded.getbuffer())
            
            # Save to src (Create directory if missing)
            if not os.path.exists("src"):
                os.makedirs("src")
            
            shutil.copy("Market Segment.xlsx", "src/Market Segment.xlsx")
            st.toast("✅ Memory Loaded!", icon="💾")
        except Exception as e:
            st.error(f"Failed to save file: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312214.png", width=60)
    st.markdown("## **Intel Hub**")
    
    st.markdown("### 1. Credentials")
    user_token = st.text_input("LLM Foundry Token", type="password")
    
    formatted_api_key = None
    if user_token:
        formatted_api_key = f"{user_token}:{PROJECT_ID}"
        os.environ["LLMFOUNDRY_TOKEN"] = user_token
        os.environ["OPENAI_API_KEY"] = formatted_api_key
        st.success("Token Active")

    st.markdown("### 2. Analyst Memory")
    mem_exists = os.path.exists("Market Segment.xlsx")
    
    if mem_exists:
        st.markdown(f"<span style='color:green'>✅ Loaded</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:red'>❌ Missing</span>", unsafe_allow_html=True)
        st.file_uploader("Upload 'Market Segment.xlsx'", type=['xlsx'], key="mem_uploader", on_change=save_memory)

# --- MAIN UI ---
st.title("🛡️ Defense Contract Intelligence Hub")

# !!! CRITICAL ERROR DISPLAY !!!
if not IMPORTS_LOADED:
    st.error("🚨 CRITICAL ERROR: System modules failed to load.")
    st.markdown("This usually happens if `src/processors.py` tries to connect to an API before you enter the key.")
    with st.expander("👀 View Technical Error Details"):
        st.code(IMPORT_ERROR_MSG, language="python")

tab_batch, tab_dashboard = st.tabs(["📁 Intelligence Cycle", "📊 Dashboard"])

with tab_batch:
    # 1. INPUT & SCRAPE (Keeping simplified for focus)
    st.subheader("1. Mission Data")
    uploaded_file = st.file_uploader("Upload Target List", type=['xlsx'])
    
    if uploaded_file and st.button("🚀 Launch Scraper"):
        # ... (Your existing scraping logic goes here) ...
        # Mocking data for testing if scraping is skipped
        st.session_state.scraped_df = pd.DataFrame([{"Description of Contract": "Test Contract", "Contract Date": "2023-01-01"}])
        st.success("Scraping Mocked/Done")

    # 3. AI PROCESSING (THE BROKEN PART)
    st.divider()
    st.subheader("3. AI Analysis")
    
    # DEBUG PANEL
    with st.expander("🛠️ Debugging Info (Open if AI Fails)"):
        st.write(f"**Modules Loaded:** {IMPORTS_LOADED}")
        st.write(f"**API Key Set:** {'Yes' if formatted_api_key else 'No'}")
        st.write(f"**Memory File Exists:** {os.path.exists('Market Segment.xlsx')}")
        st.write(f"**Scraped Data Available:** {st.session_state.scraped_df is not None}")

    if st.button("🧠 Start AI Processor", type="primary"):
        # 1. Validate Environment
        if not IMPORTS_LOADED:
            st.error("Cannot start: Modules failed to import (see top of page).")
        elif not formatted_api_key:
            st.error("Cannot start: Missing API Token.")
        elif not os.path.exists("Market Segment.xlsx"):
            st.error("Cannot start: Missing Memory File.")
        else:
            # 2. Run with Full Error Catching
            st.write("Starting Pipeline...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                df_in = st.session_state.scraped_df
                results = []
                
                for idx, row in df_in.iterrows():
                    status_text.write(f"Processing Record {idx+1}...")
                    desc = str(row.get("Description of Contract", ""))
                    c_date = str(row.get("Contract Date", ""))
                    
                    try:
                        # --- THE DANGER ZONE ---
                        # We specifically wrap the AI call to see if it crashes inside
                        res = classify_record_with_memory(desc, c_date) 
                        res = run_all_validations(res, desc)
                        res.update(row.to_dict())
                        results.append(res)
                        # -----------------------
                        
                    except Exception as row_error:
                        st.error(f"❌ Row {idx} Failed.")
                        st.code(traceback.format_exc()) # SHOWS EXACT ERROR
                        results.append(row.to_dict()) # Save partial data
                    
                    progress_bar.progress((idx + 1) / len(df_in))

                st.session_state.final_df = pd.DataFrame(results)
                st.success("Analysis Complete")
                
            except Exception as pipeline_error:
                st.error("🔥 The Entire Pipeline Crashed")
                st.markdown("**Error Traceback:**")
                st.code(traceback.format_exc())