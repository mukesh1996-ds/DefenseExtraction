import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import os
import sys
import shutil
import datetime
import traceback
from bs4 import BeautifulSoup
from io import BytesIO

import plotly.express as px

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Defense Intel Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CONSTANTS
# ==========================================================
MEMORY_PATH = "Market Segment.xlsx"

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

# ==========================================================
# SAFE SECRET LOADING (CLOUD) + RUNTIME INPUT (LOCAL)
# ==========================================================
def safe_get_secret(key:str,default=None):
    try:
        return st.secrets.get(key,default)
    except Exception:
        return default

PROJECT_ID = safe_get_secret("PROJECT_ID", "my-test-project")
SECRET_API_KEY = safe_get_secret("OPENAI_API_KEY", None)


# ==========================================================
# IMPORT HANDLING
# ==========================================================
try:
    from src.processors import classify_record_with_memory
    from src.validators import run_all_validations
    IMPORTS_LOADED = True
    IMPORT_ERROR_MSG = None
except Exception:
    IMPORTS_LOADED = False
    IMPORT_ERROR_MSG = traceback.format_exc()


# ==========================================================
# SESSION STATE INIT
# ==========================================================
def init_state():
    if "scraped_df" not in st.session_state:
        st.session_state.scraped_df = None
    if "final_df" not in st.session_state:
        st.session_state.final_df = None
    if "logs" not in st.session_state:
        st.session_state.logs = []

init_state()


# ==========================================================
# LOGGING
# ==========================================================
def log_event(msg: str, level: str = "INFO"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append({"time": ts, "level": level, "message": msg})


# ==========================================================
# HELPERS
# ==========================================================
def save_memory():
    uploaded = st.session_state.mem_uploader
    if uploaded:
        try:
            with open(MEMORY_PATH, "wb") as f:
                f.write(uploaded.getbuffer())
            log_event("✅ Memory file uploaded successfully.", "SUCCESS")
            st.toast("✅ Memory loaded successfully!", icon="💾")
        except Exception as e:
            log_event(f"❌ Memory upload failed: {e}", "ERROR")
            st.error(f"Memory upload failed: {e}")


def normalize_id(text: str):
    return str(text).replace("-", "").replace(" ", "").strip().upper()


def detect_header(paragraph_index, all_paragraphs):
    for i in range(paragraph_index, -1, -1):
        p = all_paragraphs[i]
        strong_tag = p.find("strong")
        if strong_tag:
            header_text = strong_tag.get_text(strip=True).upper()
            if header_text:
                return header_text
    return "UNKNOWN"


def get_driver():
    """Cloud-safe Selenium driver"""
    if sys.platform == "linux":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        chromium_path = shutil.which("chromium") or "/usr/bin/chromium"
        driver_path = shutil.which("chromedriver") or "/usr/bin/chromedriver"

        options.binary_location = chromium_path
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)

    # Local fallback (Windows Edge)
    driver_path = "driver/msedgedriver.exe"
    if os.path.exists(driver_path):
        service = EdgeService(driver_path)
    else:
        service = EdgeService()

    options = EdgeOptions()
    return webdriver.Edge(service=service, options=options)


def clean_numeric_series(series: pd.Series):
    cleaned = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce").fillna(0)


def build_export_file(df: pd.DataFrame, filename="Defense_Intel.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Defense_Contracts")
    return output.getvalue(), filename


def build_validation_table(df: pd.DataFrame):
    """
    Converts __validation__ dict into a table (Row | Column | PASS/FAIL | Reason).
    """
    rows = []
    for i, r in df.iterrows():
        v = r.get("__validation__", {})
        if isinstance(v, dict):
            for col_name, meta in v.items():
                rows.append({
                    "Row": i + 1,
                    "Column": col_name,
                    "Status": "✅ PASS" if meta.get("passed") else "❌ FAIL",
                    "Reason": meta.get("reason", "")
                })
    return pd.DataFrame(rows)


# ==========================================================
# SIDEBAR (ADVANCED)
# ==========================================================
with st.sidebar:
    st.markdown("## 🛡️ Defense Intel Platform")
    st.caption("Scrape → AI Extract → Validate → Export")

    st.markdown("### 🔐 Config")
    st.write("PROJECT_ID:", PROJECT_ID)

    # ✅ Runtime API Key input fallback
    st.markdown("### 🔑 API Key")
    runtime_api_key = st.text_input(
        "Enter OPENAI_API_KEY (runtime)",
        type="password",
        help="If you are running locally, paste your key here. In Streamlit Cloud, secrets can be used."
    )

    OPENAI_API_KEY = SECRET_API_KEY if SECRET_API_KEY else runtime_api_key

    if OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        st.success("✅ API Key Active")
    else:
        st.warning("⚠️ API Key Missing (AI Processor will not run)")

    st.divider()

    st.markdown("### 🧠 Analyst Memory")
    if os.path.exists(MEMORY_PATH):
        st.success("Memory Loaded ✅")
    else:
        st.warning("Memory Missing ❌ Upload below")

    st.file_uploader(
        "Upload Market Segment.xlsx",
        type=["xlsx"],
        key="mem_uploader",
        on_change=save_memory
    )

    st.divider()

    st.markdown("### ⚙️ Controls")
    DEBUG_MODE = st.toggle("🔍 Debug Mode", value=False)
    MAX_URLS = st.slider("Max URLs to scrape", 1, 200, 10)
    SCRAPE_WAIT = st.slider("Wait time per URL (sec)", 1, 15, 5)

    st.divider()

    with st.expander("📜 Runtime Logs"):
        if st.session_state.logs:
            st.dataframe(pd.DataFrame(st.session_state.logs), use_containerwidth='stretch', height=250)
        else:
            st.info("No logs yet.")

    if st.button("🧹 Reset Session"):
        st.session_state.scraped_df = None
        st.session_state.final_df = None
        st.session_state.logs = []
        st.toast("✅ Reset complete", icon="✅")


# ==========================================================
# MAIN UI
# ==========================================================
st.title("🛡️ Defense Contract Intelligence Hub")

if not IMPORTS_LOADED:
    st.error("🚨 CRITICAL ERROR: Modules failed to import.")
    st.code(IMPORT_ERROR_MSG)
    st.stop()

tab_cycle, tab_dashboard, tab_validation = st.tabs(
    ["📁 Intelligence Cycle", "📊 Dashboard & Export", "✅ Validation Center"]
)

# ==========================================================
# TAB 1: INTELLIGENCE CYCLE
# ==========================================================
with tab_cycle:
    st.subheader("1️⃣ Mission Data Input")
    uploaded_file = st.file_uploader("Upload Target List (Excel)", type=["xlsx"])

    if uploaded_file:
        df_source = pd.read_excel(uploaded_file)
        st.info(f"✅ Target Loaded: {len(df_source)} rows")
        st.dataframe(df_source.head(5), width='stretch')

        if "Source URL" not in df_source.columns:
            st.error("❌ Input Excel must contain column: 'Source URL'")
            st.stop()

        if "Contract Description" not in df_source.columns:
            st.error("❌ Input Excel must contain column: 'Contract Description'")
            st.stop()

        # ==================================================
        # SCRAPER
        # ==================================================
        st.subheader("2️⃣ Acquisition (Scraping)")
        if st.button("🚀 Launch Scraper", type="primary"):

            urls = df_source["Source URL"].dropna().unique().tolist()[:MAX_URLS]

            dash_pattern = r"\b[A-Z0-9]{6}\s*-\s*\d{2}\s*-\s*[A-Z0-9]\s*-\s*\d{4}\b"
            continuous_pattern = r"\b[A-Z0-9]{6}\d{2}[A-Z0-9]\d{4}\b"
            combined_pattern = f"{dash_pattern}|{continuous_pattern}"

            extracted_ids = []
            for text in df_source["Contract Description"].astype(str):
                extracted_ids.append(re.findall(combined_pattern, text.upper()))

            flat_ids = sorted(list(set([cid for sub in extracted_ids for cid in sub])))
            normalized_id_map = {normalize_id(cid): cid for cid in flat_ids}

            if not flat_ids:
                st.error("⚠️ No Contract IDs found in 'Contract Description'")
                st.stop()

            log_event(f"✅ Extracted {len(flat_ids)} unique contract IDs.", "SUCCESS")
            st.success(f"✅ Found {len(flat_ids)} unique Contract IDs in input Excel")

            status_box = st.status("📡 Scraping in progress...", expanded=True)
            progress = st.progress(0)

            driver = None
            scraped_data = []

            try:
                driver = get_driver()

                for i, url in enumerate(urls):
                    status_box.write(f"🔎 {i+1}/{len(urls)} Scanning: {url}")

                    try:
                        driver.get(url)

                        try:
                            WebDriverWait(driver, 12).until(
                                EC.presence_of_element_located((By.TAG_NAME, "p"))
                            )
                        except Exception:
                            pass

                        time.sleep(SCRAPE_WAIT)

                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        all_paragraphs = soup.find_all("p")

                        if DEBUG_MODE:
                            status_box.write(f"✅ Title: {soup.title.string if soup.title else 'No Title'}")
                            status_box.write(f"✅ Paragraph count: {len(all_paragraphs)}")

                        found_count = 0

                        for p_index, p in enumerate(all_paragraphs):
                            text = p.get_text(" ", strip=True)
                            if not text:
                                continue

                            clean_text = normalize_id(text)

                            found = [
                                orig for cln, orig in normalized_id_map.items()
                                if cln in clean_text
                            ]

                            if found:
                                found_count += 1
                                contract_date = None
                                if "Contract Date" in df_source.columns:
                                    try:
                                        contract_date = df_source.loc[
                                            df_source["Source URL"] == url, "Contract Date"
                                        ].iloc[0]
                                    except Exception:
                                        contract_date = None

                                scraped_data.append({
                                    "URL": url,
                                    "Contract_Date": contract_date,
                                    "Header": detect_header(p_index, all_paragraphs),
                                    "Matched_IDs": found,
                                    "Paragraph_Text": text
                                })

                        status_box.write(f"✅ Matches found: {found_count}")

                    except Exception as e:
                        status_box.error(f"❌ Failed: {e}")
                        log_event(f"❌ Scrape failed for {url}: {e}", "ERROR")

                    progress.progress((i + 1) / len(urls))

            except Exception as e:
                st.error(f"Scraper crashed: {e}")
                st.code(traceback.format_exc())
                log_event(f"❌ Scraper crashed: {e}", "ERROR")

            finally:
                if driver is not None:
                    try:
                        driver.quit()
                    except Exception:
                        pass

            if scraped_data:
                final_rows = []
                for row in scraped_data:
                    ids = row["Matched_IDs"]
                    final_rows.append({
                        "Source Link(s)": row["URL"],
                        "Contract Date": row["Contract_Date"],
                        "Header": row["Header"],
                        "Description of Contract": row["Paragraph_Text"],
                        "Supplier Name": "Multiple" if len(ids) > 1 else np.nan,
                        "Matched_ID": ", ".join(ids) if len(ids) > 1 else ids[0]
                    })

                st.session_state.scraped_df = pd.DataFrame(final_rows)
                st.success(f"✅ Scraping complete: {len(st.session_state.scraped_df)} records")
                log_event(f"✅ Scraping complete. Records: {len(st.session_state.scraped_df)}", "SUCCESS")

                st.dataframe(st.session_state.scraped_df.head(15), width='stretch')
            else:
                st.session_state.scraped_df = None
                st.warning("⚠️ Scraping finished but found 0 matched records.")
                log_event("⚠️ Scraping finished but no matched records found.", "ERROR")

        # ==================================================
        # AI PROCESSOR
        # ==================================================
        st.divider()
        st.subheader("3️⃣ AI Extraction + Validation")

        has_data = st.session_state.scraped_df is not None and not st.session_state.scraped_df.empty

        if not has_data:
            st.info("Waiting for scraped data...")
        else:
            if st.button("🧠 Start AI Processor", type="primary"):

                if not OPENAI_API_KEY:
                    st.error("⛔ OPENAI_API_KEY missing. Enter in sidebar.")
                    st.stop()

                if not os.path.exists(MEMORY_PATH):
                    st.error("⛔ Memory file missing. Upload Market Segment.xlsx")
                    st.stop()

                df_in = st.session_state.scraped_df.copy()

                status = st.status("🧠 AI Processing running...", expanded=True)
                progress_ai = st.progress(0)

                results = []

                for idx, row in df_in.iterrows():
                    desc = str(row.get("Description of Contract", ""))
                    c_date = str(row.get("Contract Date", ""))

                    status.write(f"Processing {idx+1}/{len(df_in)}")

                    try:
                        res = classify_record_with_memory(desc, c_date)
                        res = run_all_validations(res, desc)

                        row_dict = row.to_dict()
                        row_dict.pop("Supplier Name", None)
                        res.update(row_dict)

                        res["Reported Date (By SGA)"] = datetime.datetime.now().strftime("%Y-%m-%d")

                        results.append(res)

                        if DEBUG_MODE and idx == 0:
                            status.write("✅ First record output (Debug):")
                            status.json(res)

                    except Exception as e:
                        if DEBUG_MODE:
                            status.error("❌ AI failed")
                            status.code(traceback.format_exc())

                        log_event(f"❌ AI failed on row {idx+1}: {e}", "ERROR")

                        results.append({
                            "Description of Contract": desc,
                            "Additional Notes (Internal Only)": f"AI ERROR: {str(e)}",
                            "Source Link(s)": row.get("Source Link(s)", ""),
                            "Contract Date": row.get("Contract Date", ""),
                            "Reported Date (By SGA)": datetime.datetime.now().strftime("%Y-%m-%d")
                        })

                    progress_ai.progress((idx + 1) / len(df_in))

                df_out = pd.DataFrame(results)
                df_out.columns = df_out.columns.str.strip()

                # ✅ Preserve validation column + score before reorder
                validation_col = df_out["__validation__"] if "__validation__" in df_out.columns else None
                score_col = df_out["Validation Score"] if "Validation Score" in df_out.columns else None

                # Ensure required columns exist
                for col in TARGET_COLUMNS:
                    if col not in df_out.columns:
                        df_out[col] = ""

                # Reorder final output columns
                df_out = df_out[TARGET_COLUMNS]

                # Attach back internal columns (used for Validation Center)
                if validation_col is not None:
                    df_out["__validation__"] = validation_col
                if score_col is not None:
                    df_out["Validation Score"] = score_col

                st.session_state.final_df = df_out

                status.update(label="✅ AI Processing Complete", state="complete", expanded=False)
                st.success("✅ Extraction + Validation Complete!")

                st.dataframe(st.session_state.final_df.head(15), width='stretch')


# ==========================================================
# TAB 2: DASHBOARD & EXPORT
# ==========================================================
with tab_dashboard:
    if st.session_state.final_df is None or st.session_state.final_df.empty:
        st.info("No final results yet.")
    else:
        df = st.session_state.final_df.copy()
        df.columns = df.columns.str.strip()

        st.subheader("📊 Dashboard")

        if "Value (USD$ Million)" in df.columns:
            df["Value (USD$ Million)"] = clean_numeric_series(df["Value (USD$ Million)"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Records", len(df))
        c2.metric("Total Value (USD$ M)", f"{df['Value (USD$ Million)'].sum():,.2f}")
        c3.metric("Avg Validation Score", f"{df.get('Validation Score', pd.Series([0])).mean():.2f}%")

        st.divider()
        st.subheader("📈 Quick Charts")

        ch1, ch2 = st.columns(2)

        with ch1:
            if "Market Segment" in df.columns:
                seg_counts = df["Market Segment"].fillna("Unknown").value_counts().reset_index()
                seg_counts.columns = ["Market Segment", "Count"]
                fig = px.pie(seg_counts, values="Count", names="Market Segment", hole=0.4,
                             title="Contracts by Market Segment")
                st.plotly_chart(fig, width='stretch')

        with ch2:
            if "Customer Country" in df.columns:
                top_country = (
                    df.groupby("Customer Country")["Value (USD$ Million)"]
                    .sum()
                    .reset_index()
                    .sort_values("Value (USD$ Million)", ascending=False)
                    .head(10)
                )
                fig2 = px.bar(top_country, x="Customer Country", y="Value (USD$ Million)",
                              title="Top 10 Countries by Contract Value")
                st.plotly_chart(fig2, uwidth='stretch')

        st.divider()
        st.subheader("🧾 Review & Edit Extracted Data")

        edited = st.data_editor(
            df.drop(columns=["__validation__"], errors="ignore"),
            num_rows="dynamic",
            width='stretch',
            height=520
        )

        st.divider()
        st.subheader("📥 Export")

        colE1, colE2 = st.columns(2)

        with colE1:
            excel_bytes, excel_name = build_export_file(edited[TARGET_COLUMNS], "Defense_Intel.xlsx")
            st.download_button(
                "⬇️ Download Excel",
                excel_bytes,
                excel_name,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch'
            )

        with colE2:
            csv_data = edited[TARGET_COLUMNS].to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download CSV",
                csv_data,
                "Defense_Intel.csv",
                "text/csv",
                uswidth='stretch'
            )


# ==========================================================
# TAB 3: VALIDATION CENTER
# ==========================================================
with tab_validation:
    st.subheader("✅ Validation Center (Per Column / Per Row)")

    if st.session_state.final_df is None or st.session_state.final_df.empty:
        st.info("No validation data yet.")
        st.stop()

    df = st.session_state.final_df.copy()
    val_df = build_validation_table(df)

    if val_df.empty:
        st.warning("No validation report found. Please confirm you deployed updated validators.py")
        st.stop()

    total_checks = len(val_df)
    failed_checks = (val_df["Status"] == "❌ FAIL").sum()
    passed_checks = (val_df["Status"] == "✅ PASS").sum()

    a1, a2, a3 = st.columns(3)
    a1.metric("Total Checks", total_checks)
    a2.metric("✅ Passed", passed_checks)
    a3.metric("❌ Failed", failed_checks)

    show_failed_only = st.toggle("Show only failed validations", value=True)

    if show_failed_only:
        st.dataframe(val_df[val_df["Status"] == "❌ FAIL"], width='stretch', height=420)
    else:
        st.dataframe(val_df, width='stretch', height=420)

    st.divider()
    st.subheader("🧾 Row-wise Validation (Expand)")

    max_rows = min(25, len(df))
    for idx in range(max_rows):
        row_data = df.iloc[idx]
        v = row_data.get("__validation__", {})

        failed_cols = []
        if isinstance(v, dict):
            failed_cols = [k for k, meta in v.items() if not meta.get("passed")]

        score = row_data.get("Validation Score", 0)
        title = f"Record #{idx+1} | Score: {score}% | Failed: {len(failed_cols)}"

        with st.expander(title):
            st.write("**Source Link(s):**", row_data.get("Source Link(s)", ""))
            st.write("**Contract Date:**", row_data.get("Contract Date", ""))
            st.write("**Description Snippet:**")
            st.code(str(row_data.get("Description of Contract", ""))[:600])

            if not isinstance(v, dict) or len(v) == 0:
                st.info("No validation report found for this record.")
            else:
                row_val = []
                for col_name, meta in v.items():
                    row_val.append({
                        "Column": col_name,
                        "Status": "✅ PASS" if meta.get("passed") else "❌ FAIL",
                        "Reason": meta.get("reason", "")
                    })
                st.dataframe(pd.DataFrame(row_val), width='stretch')