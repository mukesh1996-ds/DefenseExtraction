import pandas as pd
from config import INPUT_FILE, OUTPUT_FILE, COL_DESC, COL_DATE, DB_PERSIST_DIR
from src.vector_engine import DefenseVectorDB
from src.processors import classify_full_record_rag

# TARGET COLUMN STRUCTURE
TARGET_COLUMNS = [
    "Customer Region", "Customer Country", "Customer Operator",
    "Supplier Region", "Supplier Country", "Domestic Content",
    "Market Segment", "System Type (General)", "System Type (Specific)",
    "System Name (General)", "System Name (Specific)", "System Piloting",
    "Supplier Name", "Program Type", "Expected MRO Contract Duration (Months)",
    "Quantity", "Value Certainty", "Value (Million)", "Currency",
    "Value (USD$ Million)", "G2G/B2G", "Signing Month", "Signing Year",
    "Description of Contract", "Additional Notes (Internal Only)",
    "Source Link(s)", "Contract Date", "Reported Date (By SGA)"
]

def main():
    print("==========================================")
    print("   DEFENSE CONTRACTS ADVANCED RAG SYSTEM  ")
    print("==========================================")
    
    # 1. Initialize the Vector Database
    # It will look into ./db_storage. If empty, it starts fresh.
    rag_db = DefenseVectorDB(persist_dir=DB_PERSIST_DIR)

    # 2. Load Input CSV
    print(f"Reading from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE, encoding='ISO-8859-1')
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Found {len(df)} rows. Processing with RAG...")

    results = []
    
    # 3. Iterate through rows
    for idx, row in df.iterrows():
        print(f"Processing row {idx + 1}/{len(df)}...")
        
        try:
            desc = str(row.get(COL_DESC, ""))
            c_date = str(row.get(COL_DATE, ""))

            # CALL THE RAG PROCESSOR
            # This function will Search -> Classify -> Save to DB
            res = classify_full_record_rag(desc, c_date, rag_db)

            # Add original data to the result dictionary
            res["Description of Contract"] = desc
            res["Contract Date"] = c_date

            # Map existing CSV columns if they exist
            for col in ["Source Link(s)", "Reported Date (By SGA)", "Additional Notes (Internal Only)"]:
                if col in df.columns:
                    res[col] = row[col]
            results.append(res)
            
        except Exception as e:
            print(f"Error row {idx}: {e}")
            results.append({"Description of Contract": desc, "Error": str(e)})
    # 4. Create DataFrame and Order Columns
    processed_df = pd.DataFrame(results)

    # Create missing columns and fill with blank
    for col in TARGET_COLUMNS:
        if col not in processed_df.columns:
            processed_df[col] = ""

    # Select and Reorder
    final_output_df = processed_df[TARGET_COLUMNS]

    # 5. Save to Excel
    final_output_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Success! Restructured data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()