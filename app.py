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
    
    /* Headers */
    h1, h2, h3 { color: #0f172a; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    
    /* Cards */
    .css-1r6slb0 { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #004e98;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem; color: #64748b; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #0f172a; font-weight: bold; }
    
    /* Buttons */
    .stButton>button {
        width: 100%; border-radius: 6px; height: 3em; font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Primary Action Button */
    button[kind="primary"] {
        background: linear-gradient(90deg, #004e98 0%, #003366 100%);
        border: none;
        color: white;
    }
    button[kind="primary"]:hover { box-shadow: 0 4px 12px rgba(0,78,152,0.4); }

    /* Secondary Action Button */
    button[kind="secondary"] { border: 1px solid #004e98; color: #004e98; background-color: white; }
    
    /* Status Box */
    .status-box { padding: 15px; border-radius: 8px; background-color: #eef2f5; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- IMPORT HANDLING ---
try:
    from src.processors import classify_record_with_memory
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
    IMPORT_ERROR_MSG = ""
except ImportError as e:
    IMPORTS_LOADED = False
    IMPORT_ERROR_MSG = str(e)

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
    """Generates charts for the dashboard."""
    if df is None or df.empty:
        return None, None
    
    # 1. Market Segment Pie Chart
    if "Market Segment" in df.columns:
        seg_counts = df["Market Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig_pie = px.pie(seg_counts, values='Count', names='Segment', hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         title="Contracts by Market Segment")
        fig_pie.update_layout(height=350, margin=dict(t=30, b=0, l=0, r=0))
    else:
        fig_pie = None

    # 2. Value by Customer Country (Bar Chart)
    if "Value (USD$ Million)" in df.columns and "Customer Country" in df.columns:
        # Clean data for plotting
        plot_df = df.copy()
        plot_df["Value (USD$ Million)"] = pd.to_numeric(plot_df["Value (USD$ Million)"], errors='coerce').fillna(0)
        country_val = plot_df.groupby("Customer Country")["Value (USD$ Million)"].sum().reset_index().sort_values("Value (USD$ Million)", ascending=False).head(10)
        
        fig_bar = px.bar(country_val, x="Customer Country", y="Value (USD$ Million)",
                         color="Value (USD$ Million)", 
                         color_continuous_scale="Blues",
                         title="Top 10 Customer Countries by Detected Value ($M)")
        fig_bar.update_layout(height=350, margin=dict(t=30, b=0, l=0, r=0))
    else:
        fig_bar = None
        
    return fig_pie, fig_bar

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312214.png", width=60)
    st.markdown("## **Intel Hub**")
    
    st.markdown("### ⚙️ Configuration")
    st.caption(f"Project ID: `{PROJECT_ID}`")
    
    user_token = st.text_input("🔑 LLM Foundry Token", type="password", placeholder="Paste token here...")
    
    formatted_api_key = None
    if user_token:
        formatted_api_key = f"{user_token}:{PROJECT_ID}"
        os.environ["LLMFOUNDRY_TOKEN"] = user_token
        os.environ["OPENAI_API_KEY"] = formatted_api_key
        st.success("Connected Securely")

    st.markdown("---")
    st.markdown("### 📡 System Status")
    
    # Module Check
    if IMPORTS_LOADED:
        st.markdown("✅ **RAG Core:** `Online`")
    else:
        st.markdown("❌ **RAG Core:** `Offline`")
        st.error("Missing `src` folder")

    # Memory Check
    mem_path = "Market Segment.xlsx"
    if os.path.exists(mem_path) or os.path.exists("/content/" + mem_path):
        st.markdown("✅ **Analyst Memory:** `Loaded`")
    else:
        st.markdown("⚠️ **Analyst Memory:** `Not Found`")

# --- MAIN UI ---
st.title("🛡️ Defense Contract Intelligence Hub")
st.markdown("**Automated Open-Source Intelligence (OSINT) Collection & Analysis**")

# TABS FOR WORKFLOW
tab_batch, tab_dashboard, tab_demo = st.tabs(["📁 Data Processing", "📊 Intel Dashboard", "🧪 Analyst Sandbox"])

# ==========================================================
# TAB 1: BATCH PROCESSING
# ==========================================================
with tab_batch:
    
    # 1. DATA INGESTION SECTION
    with st.container():
        st.subheader("1. Mission Data Import")
        uploaded_file = st.file_uploader("Upload Target List (Excel)", type=['xlsx'], help="Must contain 'Source URL' column")

        if uploaded_file:
            try:
                df_source = pd.read_excel(uploaded_file)
                df_source['Contract Date'] = pd.to_datetime(df_source["Contract Date"], dayfirst=True, errors="coerce")
                
                # Metrics Row
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Rows Loaded", len(df_source))
                col2.metric("Unique URLs", df_source['Source URL'].nunique())
                
                # Extract IDs
                dash_pattern = r"\b[A-Z0-9]{6}-\d{2}-[A-Z0-9]-\d{4}\b"
                continuous_pattern = r"\b[A-Z0-9]{6}\d{2}[A-Z0-9]\d{4}\b"
                combined_pattern = f"{dash_pattern}|{continuous_pattern}"

                extracted_ids = []
                if 'Contract Description' in df_source.columns:
                    for text in df_source['Contract Description'].astype(str):
                        match_ids = re.findall(combined_pattern, text)
                        extracted_ids.append(match_ids)
                
                flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
                
                col3.metric("Contract IDs", len(flat_ids))
                col4.metric("Est. Processing Time", f"~{len(df_source)*10/60:.1f} min")

                with st.expander("📝 View Raw Import Data"):
                    st.dataframe(df_source.head())
                    
            except Exception as e:
                st.error(f"File Error: {e}")
                st.stop()
        else:
            st.info("👋 Upload an Excel file to begin the intelligence cycle.")

    st.divider()

    # 2. OPERATION EXECUTION SECTION
    if uploaded_file:
        st.subheader("2. Intelligence Operations")
        
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            st.markdown("##### Phase 1: Acquisition")
            start_scrape = st.button("🚀 Launch Scraper", type="primary", use_container_width=True)
            
        with col_act2:
            st.markdown("##### Phase 2: Analysis")
            # Logic: Button is disabled if no scraped data exists
            start_rag = st.button("🧠 Start AI Processor", type="secondary", use_container_width=True, disabled=st.session_state.scraped_df is None)

        # --- SCRAPER LOGIC ---
        if start_scrape:
            status_container = st.status("📡 Establishing Secure Connection...", expanded=True)
            progress_bar = st.progress(0)
            log_area = st.empty()
            
            try:
                url_date_map = df_source.set_index('Source URL')['Contract Date'].to_dict()
                urls = df_source['Source URL'].dropna().unique().tolist()
                
                driver = get_driver()
                
                if driver:
                    scraped_data = []
                    normalized_id_map = {normalize_id(cid): cid for cid in flat_ids}
                    
                    for idx, url in enumerate(urls):
                        status_container.update(label=f"Scanning Target {idx+1}/{len(urls)}: {url[:40]}...", state="running")
                        progress_bar.progress((idx + 1) / len(urls))
                        
                        current_date = url_date_map.get(url)
                        try:
                            driver.get(url)
                            time.sleep(3) # Respectful delay
                            
                            html = driver.page_source
                            soup = BeautifulSoup(html, "html.parser")
                            
                            # Smart Selector Logic
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
                                            "URL": url, "Contract_Date": current_date,
                                            "Header": header, "Matched_IDs": found_matches, 
                                            "Paragraph_Text": text
                                        })
                        except Exception as e:
                            log_area.text(f"⚠️ Error: {e}")
                    
                    driver.quit()
                    status_container.update(label="✅ Acquisition Complete", state="complete", expanded=False)
                    
                    # Post-Processing
                    expanded_rows = []
                    for row in scraped_data:
                        num_ids = len(row["Matched_IDs"])
                        if num_ids > 1:
                            combined_ids = ", ".join(row["Matched_IDs"])
                            expanded_rows.append({
                                "Source Link(s)": row["URL"], "Contract Date": row["Contract_Date"],
                                "Header": row["Header"], "Matched_ID": combined_ids,
                                "Description of Contract": row["Paragraph_Text"], "Supplier Name": "Multiple"
                            })
                        else:
                            expanded_rows.append({
                                "Source Link(s)": row["URL"], "Contract Date": row["Contract_Date"],
                                "Header": row["Header"], "Matched_ID": row["Matched_IDs"][0],
                                "Description of Contract": row["Paragraph_Text"], "Supplier Name": np.nan 
                            })
                    
                    st.session_state.scraped_df = pd.DataFrame(expanded_rows)
                    if not st.session_state.scraped_df.empty:
                        st.session_state.scraped_df['Contract Date'] = pd.to_datetime(st.session_state.scraped_df['Contract Date']).dt.date
                        st.success(f"Captured {len(st.session_state.scraped_df)} intelligence records.")
                        
                        # --- CRITICAL FIX 1: AUTO-REFRESH ---
                        # This forces the page to reload so the "Start AI" button sees the new data and enables itself.
                        time.sleep(1)
                        st.rerun()
            
            except Exception as e:
                st.error(f"Critical System Failure: {e}")

        # --- RAG AI LOGIC ---
        if start_rag:
            if not IMPORTS_LOADED:
                st.error("Missing RAG Modules.")
            elif not formatted_api_key:
                st.warning("⚠️ Token Required in Sidebar.")
            else:
                rag_status = st.status("🧠 Analyzing Intelligence Data...", expanded=True)
                rag_progress = st.progress(0)
                
                try:
                    df_to_process = st.session_state.scraped_df
                    results = []
                    total_rows = len(df_to_process)
                    
                    for idx, row in df_to_process.iterrows():
                        rag_status.write(f"Processing Record {idx + 1}/{total_rows}")
                        rag_progress.progress((idx + 1) / total_rows)
                        
                        desc = str(row.get("Description of Contract", ""))
                        c_date = str(row.get("Contract Date", ""))
                        pre_supplier = str(row.get("Supplier Name", ""))
                        
                        try:
                            # 1. Classify
                            res = classify_record_with_memory(desc, c_date)
                            # 2. Validate
                            try: res = run_all_validations(res, desc)
                            except: pass
                            
                            # 3. Standardize
                            if pre_supplier == "Multiple": res["Supplier Name"] = "Multiple"
                            if "Value (Million)" in res: res["Value (USD$ Million)"] = res["Value (Million)"]
                            
                            # 4. Map Metadata
                            res.update({
                                "Description of Contract": desc, "Contract Date": c_date,
                                "Source Link(s)": row.get("Source Link(s)", ""), "Header": row.get("Header", ""),
                                "Reported Date (By SGA)": datetime.datetime.now().strftime("%Y-%m-%d")
                            })
                            results.append(res)
                        except Exception as e:
                            results.append({"Description of Contract": desc, "Additional Notes (Internal Only)": f"Error: {e}"})
                    
                    rag_status.update(label="✅ Analysis Complete", state="complete", expanded=False)
                    
                    processed_df = pd.DataFrame(results)
                    for col in TARGET_COLUMNS:
                        if col not in processed_df.columns: processed_df[col] = ""
                    
                    st.session_state.final_df = processed_df[TARGET_COLUMNS]
                    st.toast("Analysis Complete! Switch to 'Intel Dashboard' tab.", icon="🎉")
                    
                except Exception as e:
                    st.error(f"Pipeline Error: {e}")

# ==========================================================
# TAB 2: DASHBOARD & EXPORT
# ==========================================================
with tab_dashboard:
    st.header("📊 Intelligence Report")
    
    if st.session_state.final_df is not None:
        df_viz = st.session_state.final_df
        
        # 1. TOP LEVEL METRICS
        m1, m2, m3 = st.columns(3)
        total_val = pd.to_numeric(df_viz["Value (USD$ Million)"], errors='coerce').sum()
        m1.metric("Total Detected Value", f"${total_val:,.1f} M")
        m2.metric("Contracts Analyzed", len(df_viz))
        m3.metric("Suppliers Identified", df_viz["Supplier Name"].nunique())
        
        st.markdown("---")
        
        # 2. CHARTS
        chart1, chart2 = st.columns(2)
        fig_pie, fig_bar = create_dashboard_metrics(df_viz)
        
        with chart1:
            if fig_pie: st.plotly_chart(fig_pie, use_container_width=True)
        with chart2:
            if fig_bar: st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("---")
        
        # 3. EDITABLE DATAFRAME
        st.subheader("📝 Review & Edit Intelligence")
        st.info("Double-click any cell to edit data before export.")
        
        # --- CRITICAL FIX 2: COLUMN VISIBILITY IN CLOUD ---
        # Setting use_container_width=False forces horizontal scrolling,
        # preventing the cloud deployment from squashing 30 columns into zero width.
        edited_df = st.data_editor(
            df_viz, 
            num_rows="dynamic",
            use_container_width=False,  # <--- THIS IS THE KEY FIX
            height=600,
            column_config={
                "Value (USD$ Million)": st.column_config.NumberColumn(format="$%.2f"),
                "Source Link(s)": st.column_config.LinkColumn("Source"),
            }
        )
        
        # 4. EXPORT
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='Defense_Contracts')
            
            # Auto-adjust columns width
            worksheet = writer.sheets['Defense_Contracts']
            for i, col in enumerate(edited_df.columns):
                width = max(edited_df[col].astype(str).map(len).max(), len(col))
                worksheet.set_column(i, i, width)
        
        st.download_button(
            label="📥 Download Validated Report (Excel)",
            data=output.getvalue(),
            file_name=f"Defense_Intel_Report_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
        
    else:
        st.info("⚠️ No intelligence data available yet. Please run the Batch Processing workflow first.")

# ==========================================================
# TAB 3: ANALYST SANDBOX
# ==========================================================
with tab_demo:
    st.markdown("### 🧪 Laboratory Environment")
    st.caption("Test specific contract text against the AI model without running a full batch.")
    
    col_input, col_view = st.columns([1, 1])
    
    with col_input:
        demo_text = st.text_area("Input Contract Text:", height=300, 
            placeholder="Example: Raytheon Missiles & Defense was awarded a $250M modification for Tomahawk cruise missile production...")
        
        demo_date = st.date_input("Contract Date", value=datetime.date.today())
        
        if st.button("⚡ Analyze Fragment", type="primary"):
            if not formatted_api_key:
                st.error("Please enter API Token in Sidebar.")
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
            <div class="css-1r6slb0">
                <h4 style="color:#004e98;">{res.get('Supplier Name', 'Unknown Supplier')}</h4>
                <p><strong>System:</strong> {res.get('System Name (Specific)', 'N/A')}</p>
                <p><strong>Value:</strong> ${res.get('Value (USD$ Million)', '0')} M</p>
                <hr>
                <small>{res.get('Customer Country', 'Unknown')} | {res.get('Market Segment', 'Unknown')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.json(res, expanded=False)