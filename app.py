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

# Import Project ID from config
try:
    from config import PROJECT_ID
except ImportError:
    PROJECT_ID = "my-test-project"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Defense Intel Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (DEFENSE THEME) ---
st.markdown("""
    <style>
    /* Main Layout */
    .main { background-color: #f0f2f6; }
    h1, h2, h3 { color: #0f172a; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    
    /* Metrics & Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #004e98;
    }
    .css-card { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    
    /* Buttons */
    .stButton>button {
        width: 100%; border-radius: 6px; height: 3em; font-weight: 600;
        transition: all 0.3s ease;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #004e98 0%, #003366 100%);
        border: none;
        color: white;
    }
    button[kind="primary"]:hover { box-shadow: 0 4px 12px rgba(0,78,152,0.4); }
    button[kind="secondary"] { border: 1px solid #004e98; color: #004e98; background-color: white; }
    
    /* Status Indicators */
    .status-good { color: #15803d; font-weight: bold; }
    .status-bad { color: #b91c1c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- IMPORT HANDLING ---
try:
    from src.processors import classify_record_with_memory
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
except ImportError as e:
    IMPORTS_LOADED = False

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
    if sys.platform == "linux":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        chromium_path = shutil.which("chromium") or "/usr/bin/chromium"
        options.binary_location = chromium_path
        driver_path = shutil.which("chromedriver") or "/usr/bin/chromedriver"
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)
    else:
        # Local Edge Driver
        driver_path = "driver/msedgedriver.exe" 
        if os.path.exists(driver_path):
            service = EdgeService(driver_path)
        else:
            service = EdgeService() 
        options = EdgeOptions()
        options.add_argument("--start-maximized")
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

# --- MEMORY MANAGEMENT ---
def clear_memory():
    """Strictly deletes the memory file to enforce 'missing' state."""
    if os.path.exists("Market Segment.xlsx"):
        os.remove("Market Segment.xlsx")
    if os.path.exists("src/Market Segment.xlsx"):
        os.remove("src/Market Segment.xlsx")
    st.toast("🧹 Memory Cleared! AI will now fail if run.", icon="🗑️")

def save_memory():
    """Saves uploaded memory file."""
    uploaded = st.session_state.mem_uploader
    if uploaded:
        with open("Market Segment.xlsx", "wb") as f:
            f.write(uploaded.getbuffer())
        # Ensure it exists in src for the module
        os.makedirs("src", exist_ok=True)
        shutil.copy("Market Segment.xlsx", "src/Market Segment.xlsx")
        st.toast("✅ Memory Loaded!", icon="💾")

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

    st.markdown("---")
    st.markdown("### 2. Analyst Memory")
    
    # Check for file existence strictly
    mem_exists = os.path.exists("Market Segment.xlsx")
    
    if mem_exists:
        try:
            df_mem = pd.read_excel("Market Segment.xlsx")
            st.markdown(f"<span class='status-good'>✅ Loaded ({len(df_mem)} rules)</span>", unsafe_allow_html=True)
            if st.button("🗑️ Clear / Reset Memory"):
                clear_memory()
                time.sleep(1)
                st.rerun()
        except:
            st.error("File Corrupted")
    else:
        st.markdown("<span class='status-bad'>❌ Missing (AI Blocked)</span>", unsafe_allow_html=True)
        st.file_uploader("Upload 'Market Segment.xlsx'", type=['xlsx'], key="mem_uploader", on_change=save_memory)

# --- MAIN UI ---
st.title("🛡️ Defense Contract Intelligence Hub")

tab_batch, tab_dashboard, tab_demo = st.tabs(["📁 Intelligence Cycle", "📊 Dashboard & Export", "🧪 Analyst Sandbox"])

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
        
        # 2. SCRAPE (Independent Step)
        st.subheader("2. Acquisition (Scraping)")
        if st.button("🚀 Launch Scraper", type="primary"):
            status_box = st.status("📡 Scraping in progress...", expanded=True)
            try:
                # --- SCRAPER LOGIC START ---
                url_date_map = df_source.set_index('Source URL')['Contract Date'].to_dict()
                urls = df_source['Source URL'].dropna().unique().tolist()
                driver = get_driver()
                
                scraped_data = []
                # ID Extraction
                dash_pattern = r"\b[A-Z0-9]{6}-\d{2}-[A-Z0-9]-\d{4}\b"
                continuous_pattern = r"\b[A-Z0-9]{6}\d{2}[A-Z0-9]\d{4}\b"
                combined_pattern = f"{dash_pattern}|{continuous_pattern}"
                extracted_ids = []
                if 'Contract Description' in df_source.columns:
                    for text in df_source['Contract Description'].astype(str):
                        extracted_ids.append(re.findall(combined_pattern, text))
                flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
                normalized_id_map = {normalize_id(cid): cid for cid in flat_ids}

                for idx, url in enumerate(urls):
                    status_box.write(f"Scanning: {url}")
                    try:
                        driver.get(url)
                        time.sleep(2)
                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        body_div = soup.select_one("div.content.content-wrap div.inside.ntext div.body") or soup.select_one("div.body") or soup.find("body")
                        
                        if body_div:
                            for p_index, p in enumerate(body_div.find_all("p")):
                                text = p.get_text(" ", strip=True)
                                clean_text = normalize_id(text)
                                found = [orig for cln, orig in normalized_id_map.items() if cln in clean_text]
                                if found:
                                    scraped_data.append({
                                        "URL": url, "Contract_Date": url_date_map.get(url),
                                        "Header": detect_header(p_index, body_div.find_all("p")),
                                        "Matched_IDs": found, "Paragraph_Text": text
                                    })
                    except: pass
                
                driver.quit()
                status_box.update(label="✅ Scraping Complete", state="complete", expanded=False)
                
                # Expand Rows
                final_rows = []
                for row in scraped_data:
                    ids = row["Matched_IDs"]
                    entry = {
                        "Source Link(s)": row["URL"], "Contract Date": row["Contract_Date"],
                        "Header": row["Header"], "Description of Contract": row["Paragraph_Text"],
                        "Supplier Name": "Multiple" if len(ids) > 1 else np.nan,
                        "Matched_ID": ", ".join(ids) if len(ids) > 1 else ids[0]
                    }
                    final_rows.append(entry)
                
                st.session_state.scraped_df = pd.DataFrame(final_rows)
                if not st.session_state.scraped_df.empty:
                    st.success(f"Acquired {len(st.session_state.scraped_df)} records.")
                    time.sleep(1)
                    st.rerun() # Refresh to update UI
                # --- SCRAPER LOGIC END ---
            except Exception as e:
                st.error(f"Scraper Failed: {e}")

    # 3. AI PROCESSING (Gated Step)
    st.divider()
    st.subheader("3. AI Analysis")
    
    # State Check
    has_data = st.session_state.scraped_df is not None
    has_token = formatted_api_key is not None
    has_memory = os.path.exists("Market Segment.xlsx")
    
    if not has_data:
        st.info("Waiting for Scraped Data...")
        proc_btn = st.button("🧠 Start AI Processor", disabled=True)
    else:
        # The button is enabled, but the LOGIC inside checks strict requirements
        proc_btn = st.button("🧠 Start AI Processor", type="primary")
        
        if proc_btn:
            if not has_token:
                st.error("⛔ STOP: Missing LLM Foundry Token (See Sidebar)")
            elif not has_memory:
                st.error("⛔ STOP: Analyst Memory File Missing! Cannot classify data.")
                st.error("Please upload 'Market Segment.xlsx' in the Sidebar to proceed.")
            elif not IMPORTS_LOADED:
                st.error("⛔ STOP: System Modules (src/) not found.")
            else:
                # ALL CHECKS PASSED - RUN AI
                with st.status("🧠 Processing...", expanded=True) as status:
                    try:
                        df_in = st.session_state.scraped_df
                        results = []
                        for idx, row in df_in.iterrows():
                            status.write(f"Analyzing Record {idx+1}/{len(df_in)}")
                            
                            # Core AI Logic
                            desc = str(row.get("Description of Contract", ""))
                            c_date = str(row.get("Contract Date", ""))
                            try:
                                res = classify_record_with_memory(desc, c_date) # Uses memory file
                                res = run_all_validations(res, desc)
                                res.update(row.to_dict()) # Merge Scraped Data
                                res["Reported Date (By SGA)"] = datetime.datetime.now().strftime("%Y-%m-%d")
                                results.append(res)
                            except Exception as ex:
                                results.append({"Description of Contract": desc, "Additional Notes (Internal Only)": str(ex)})
                        
                        # Finalize
                        st.session_state.final_df = pd.DataFrame(results)
                        # Ensure columns
                        for col in TARGET_COLUMNS:
                            if col not in st.session_state.final_df.columns:
                                st.session_state.final_df[col] = ""
                        
                        st.session_state.final_df = st.session_state.final_df[TARGET_COLUMNS]
                        status.update(label="✅ Analysis Complete!", state="complete")
                        st.toast("Job Done! Check Dashboard Tab.")
                        
                    except Exception as e:
                        st.error(f"AI Pipeline Failed: {e}")

# ==========================================================
# TAB 2: DASHBOARD
# ==========================================================
with tab_dashboard:
    if st.session_state.final_df is not None:
        df = st.session_state.final_df
        
        # Metrics
        c1, c2 = st.columns(2)
        total_val = pd.to_numeric(df["Value (USD$ Million)"], errors='coerce').sum()
        c1.metric("Total Value", f"${total_val:,.2f} M")
        c2.metric("Records", len(df))
        
        # Charts
        p, b = create_dashboard_metrics(df)
        if p: st.plotly_chart(p, use_container_width=True)
        
        # Data Editor (Scrollable)
        st.subheader("Review Data")
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=False, height=500)
        
        # Export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited.to_excel(writer, index=False, sheet_name='Defense_Contracts')
        st.download_button("📥 Download Excel", output.getvalue(), "Defense_Intel.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("No analysis results yet.")

# ==========================================================
# TAB 3: ANALYST SANDBOX (RESTORED)
# ==========================================================
with tab_demo:
    st.markdown("### 🧪 Laboratory Environment")
    st.caption("Test specific contract text against the AI model without running a full batch.")
    
    col_input, col_view = st.columns([1, 1])
    
    with col_input:
        demo_text = st.text_area("Input Contract Text:", height=300, 
            placeholder="Example: Raytheon Missiles & Defense was awarded a $250M modification for Tomahawk cruise missile production...")
        
        demo_date = st.date_input("Contract Date", value=datetime.date.today())
        
        # Same STRICT checks here too
        if st.button("⚡ Analyze Fragment", type="primary"):
            mem_exists = os.path.exists("Market Segment.xlsx")
            
            if not formatted_api_key:
                st.error("Please enter API Token in Sidebar.")
            elif not mem_exists:
                st.error("Missing Analyst Memory File (Market Segment.xlsx). Upload in Sidebar.")
            else:
                with st.spinner("Classifying..."):
                    try:
                        d_res = classify_record_with_memory(demo_text, str(demo_date))
                        d_res = run_all_validations(d_res, demo_text)
                        st.session_state['demo_result'] = d_res
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col_view:
        if 'demo_result' in st.session_state:
            res = st.session_state['demo_result']
            
            # Visualizing the Result as a Card
            st.markdown(f"""
            <div class="css-card">
                <h4 style="color:#004e98;">{res.get('Supplier Name', 'Unknown Supplier')}</h4>
                <p><strong>System:</strong> {res.get('System Name (Specific)', 'N/A')}</p>
                <p><strong>Value:</strong> ${res.get('Value (USD$ Million)', '0')} M</p>
                <hr>
                <small>{res.get('Customer Country', 'Unknown')} | {res.get('Market Segment', 'Unknown')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.json(res, expanded=False)