import os

# ==========================
# CONFIGURATION
# ==========================
# Paths (Adjusted for Cloud if needed, but these are fine for now)
INPUT_FILE = "data/scraped_raw_data.csv" 
OUTPUT_FILE = "Processed_Contracts_Output_V2_RAG.xlsx"
DB_PERSIST_DIR = "./db_storage"

# COLUMN MAPPING
COL_DESC = "Description of Contract"
COL_DATE = "Contract Date"

# LLM FOUNDRY SETTINGS
PROJECT_ID = "my-test-project"
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"  
BASE_URL = "https://llmfoundry.straive.com/openai/v1/"

# NOTE: We removed getpass() and API_KEY_FORMATTED from here.
# We will construct the key in the main app instead.