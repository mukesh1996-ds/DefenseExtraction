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
import traceback
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

# --- IMPORT HANDLING ---
try:
    try:
        from config import PROJECT_ID
    except ImportError:
        PROJECT_ID = "my-test-project"

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
    # Search backwards for the nearest Header/Strong tag
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
    """Robust Driver Configuration for Cloud Environments"""
    if sys.platform == "linux":
        options = ChromeOptions()
        # Essential Headless Flags
        options.add_argument("--headless=new") # Newer headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Anti-Detection Flags (CRITICAL FOR CLOUD)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        chromium_path = shutil.which("chromium") or "/usr/bin/chromium"
        options.binary_location = chromium_path
        
        driver_path = shutil.which("chromedriver") or "/usr/bin/chromedriver"
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)
    else:
        # Local Driver (Edge)
        driver_path = "driver/msedgedriver.exe" 
        if os.path.exists(driver_path):
            service = EdgeService(driver_path)
        else:
            service = EdgeService() 
        options = EdgeOptions()
        return webdriver.Edge(service=service, options=options)

def create_dashboard_metrics(df):
    if df is None or df.empty: return None, None
    
    if "Market Segment" in df.columns:
        seg_counts = df["Market Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig_pie = px.pie(seg_counts, values='Count', names='Segment', hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         title="Contracts by Market Segment")
    else: fig_pie = None

    if "Value (USD$ Million)" in df.columns and "Customer Country" in df.columns:
        plot_df = df.copy()
        plot_df["Value (USD$ Million)"] = pd.to_numeric(plot_df["Value (USD$ Million)"], errors='coerce').fillna(0)
        country_val = plot_df.groupby("Customer Country")["Value (USD$ Million)"].sum().reset_index().sort_values("Value (USD$ Million)", ascending=False).head(10)
        fig_bar = px.bar(country_val, x="Customer Country", y="Value (USD$ Million)",
                         color="Value (USD$ Million)", color_continuous_scale="Blues",
                         title="Top 10 Customer Countries ($M)")
    else: fig_bar = None
        
    return fig_pie, fig_bar

def save_memory():
    uploaded = st.session_state.mem_uploader
    if uploaded:
        try:
            with open("Market Segment.xlsx", "wb") as f:
                f.write(uploaded.getbuffer())
            if not os.path.exists("src"):
                os.makedirs("src")
            shutil.copy("Market Segment.xlsx", "src/Market Segment.xlsx")
            st.toast("✅ Memory Loaded!", icon="💾")
        except Exception as e:
            st.error(f"Memory Save Failed: {e}")

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
        st.markdown(f"<span style='color:green; font-weight:bold'>✅ Loaded</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:red; font-weight:bold'>❌ Missing</span>", unsafe_allow_html=True)
        st.file_uploader("Upload 'Market Segment.xlsx'", type=['xlsx'], key="mem_uploader", on_change=save_memory)

# --- MAIN UI ---
st.title("🛡️ Defense Contract Intelligence Hub")

# CHECK: Import Failures
if not IMPORTS_LOADED:
    st.error("🚨 CRITICAL ERROR: System modules failed to load.")
    with st.expander("👀 View Technical Error Details"):
        st.code(IMPORT_ERROR_MSG, language="python")

tab_batch, tab_dashboard = st.tabs(["📁 Intelligence Cycle", "📊 Dashboard & Export"])

# ==========================================================
# TAB 1: INTELLIGENCE CYCLE
# ==========================================================
with tab_batch:
    
    # 1. INPUT
    st.subheader("1. Mission Data Input")
    uploaded_file = st.file_uploader("Upload Target List", type=['xlsx'])
    
    if uploaded_file:
        df_source = pd.read_excel(uploaded_file)
        st.info(f"Target Loaded: {len(df_source)} rows | Ready to Scrape")
        
        # 2. SCRAPE
        st.subheader("2. Acquisition (Scraping)")
        if st.button("🚀 Launch Scraper", type="primary"):
            status_box = st.status("📡 Scraping in progress...", expanded=True)
            try:
                # --- SCRAPER LOGIC START ---
                
                # 1. Prepare Target IDs
                urls = df_source['Source URL'].dropna().unique().tolist()
                
                # Extract IDs from Input Excel
                dash_pattern = r"\b[A-Z0-9]{6}-\d{2}-[A-Z0-9]-\d{4}\b"
                continuous_pattern = r"\b[A-Z0-9]{6}\d{2}[A-Z0-9]\d{4}\b"
                combined_pattern = f"{dash_pattern}|{continuous_pattern}"
                
                extracted_ids = []
                if 'Contract Description' in df_source.columns:
                    for text in df_source['Contract Description'].astype(str):
                        extracted_ids.append(re.findall(combined_pattern, text))
                
                flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
                normalized_id_map = {normalize_id(cid): cid for cid in flat_ids}
                
                if not flat_ids:
                    status_box.write("⚠️ Warning: No Contract IDs found in your input Excel 'Contract Description' column.")
                    status_box.update(state="error")
                else:
                    status_box.write(f"ℹ️ Searching for {len(flat_ids)} unique Contract IDs...")

                # 2. Launch Driver
                driver = get_driver()
                scraped_data = []

                for idx, url in enumerate(urls):
                    status_box.write(f"Scanning: {url}")
                    try:
                        driver.get(url)
                        # Increased wait time for Cloud latency
                        time.sleep(5) 
                        
                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        
                        # --- ROBUST FINDER (FIXED) ---
                        # Instead of looking for specific DIVs, we look at ALL paragraphs on the page.
                        all_paragraphs = soup.find_all("p")
                        
                        found_count_on_page = 0
                        
                        # Debugging: Check if we are blocked
                        page_title = soup.title.string if soup.title else "No Title"
                        if len(all_paragraphs) == 0:
                             print(f"⚠️ [DEBUG] {url} - Empty Page or Blocked. Title: {page_title}")

                        for p_index, p in enumerate(all_paragraphs):
                            text = p.get_text(" ", strip=True)
                            if not text: continue
                                
                            clean_text = normalize_id(text)
                            
                            # Check if any target ID is in this paragraph
                            found = [orig for cln, orig in normalized_id_map.items() if cln in clean_text]
                            
                            if found:
                                found_count_on_page += 1
                                scraped_data.append({
                                    "URL": url, 
                                    "Contract_Date": df_source.loc[df_source['Source URL'] == url, 'Contract Date'].iloc[0] if 'Contract Date' in df_source.columns else None,
                                    "Header": detect_header(p_index, all_paragraphs),
                                    "Matched_IDs": found, 
                                    "Paragraph_Text": text
                                })
                        
                        if found_count_on_page > 0:
                            status_box.write(f"✅ Found {found_count_on_page} matches on {url}")
                        else:
                            # Fallback: Print debug info to console logs if needed
                            print(f"No matches on {url}. IDs searched: {len(flat_ids)}")
                            
                    except Exception as scrape_err:
                        print(f"Failed to scrape {url}: {scrape_err}")
                
                driver.quit()
                
                # 3. Process Results
                if len(scraped_data) > 0:
                    status_box.update(label=f"✅ Scraping Complete: Found {len(scraped_data)} records", state="complete", expanded=False)
                    
                    final_rows = []
                    for row in scraped_data:
                        ids = row["Matched_IDs"]
                        entry = {
                            "Source Link(s)": row["URL"], 
                            "Contract Date": row["Contract_Date"],
                            "Header": row["Header"], 
                            "Description of Contract": row["Paragraph_Text"],
                            "Supplier Name": "Multiple" if len(ids) > 1 else np.nan,
                            "Matched_ID": ", ".join(ids) if len(ids) > 1 else ids[0]
                        }
                        final_rows.append(entry)
                    
                    st.session_state.scraped_df = pd.DataFrame(final_rows)
                    st.success(f"Successfully acquired {len(st.session_state.scraped_df)} records.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.scraped_df = None # Clear old data
                    status_box.update(label="⚠️ Scraping Finished (No Data)", state="error")
                    st.error("Scraper finished but found no matching records.")
                    st.markdown("**Troubleshooting:**\n1. Check if your Input Excel has valid Contract IDs in 'Contract Description'.\n2. The website might be blocking the Cloud Scraper (Anti-Bot).")
                
                # --- SCRAPER LOGIC END ---
            except Exception as e:
                st.error(f"Scraper System Failure: {e}")
                st.code(traceback.format_exc())

    # 3. AI PROCESSING
    st.divider()
    st.subheader("3. AI Analysis")
    
    # State Check
    has_data = st.session_state.scraped_df is not None and not st.session_state.scraped_df.empty
    
    if not has_data:
        st.info("Waiting for Scraped Data...")
        proc_btn = st.button("🧠 Start AI Processor", disabled=True)
    else:
        proc_btn = st.button("🧠 Start AI Processor", type="primary")
        
        if proc_btn:
            if not IMPORTS_LOADED:
                st.error("⛔ STOP: Modules failed to import.")
            elif not formatted_api_key:
                st.error("⛔ STOP: Missing LLM Foundry Token.")
            elif not os.path.exists("Market Segment.xlsx"):
                st.error("⛔ STOP: Memory File Missing.")
            else:
                st.write("Starting Pipeline...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    df_in = st.session_state.scraped_df
                    results = []
                    
                    for idx, row in df_in.iterrows():
                        status_text.write(f"Processing Record {idx+1}/{len(df_in)}...")
                        
                        desc = str(row.get("Description of Contract", ""))
                        c_date = str(row.get("Contract Date", ""))
                        
                        try:
                            res = classify_record_with_memory(desc, c_date) 
                            res = run_all_validations(res, desc)
                            res.update(row.to_dict())
                            res["Reported Date (By SGA)"] = datetime.datetime.now().strftime("%Y-%m-%d")
                            results.append(res)
                        except Exception as row_ex:
                            traceback.print_exc()
                            results.append({
                                "Description of Contract": desc, 
                                "Additional Notes (Internal Only)": f"AI ERROR: {str(row_ex)}"
                            })
                        
                        progress_bar.progress((idx + 1) / len(df_in))

                    st.session_state.final_df = pd.DataFrame(results)
                    for col in TARGET_COLUMNS:
                        if col not in st.session_state.final_df.columns:
                            st.session_state.final_df[col] = ""
                    st.session_state.final_df = st.session_state.final_df[TARGET_COLUMNS]
                    
                    status_text.write("✅ Analysis Complete!")
                    st.success("Analysis Finished.")
                    st.subheader("Results Preview")
                    st.dataframe(st.session_state.final_df.head())
                    
                except Exception as e:
                    st.error(f"Pipeline Crashed: {e}")
                    st.code(traceback.format_exc())

# ==========================================================
# TAB 2: DASHBOARD
# ==========================================================
with tab_dashboard:
    if st.session_state.final_df is not None:
        df = st.session_state.final_df
        c1, c2 = st.columns(2)
        total_val = pd.to_numeric(df["Value (USD$ Million)"], errors='coerce').sum()
        c1.metric("Total Value", f"${total_val:,.2f} M")
        c2.metric("Records", len(df))
        
        p, b = create_dashboard_metrics(df)
        if p: st.plotly_chart(p, use_container_width=True)
        if b: st.plotly_chart(b, use_container_width=True)
        
        st.subheader("Review Data")
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=500)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited.to_excel(writer, index=False, sheet_name='Defense_Contracts')
        st.download_button("📥 Download Excel", output.getvalue(), "Defense_Intel.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("No analysis results yet.")