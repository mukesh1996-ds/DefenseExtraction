import os
import getpass

# ==========================
# CONFIGURATION
# ==========================
INPUT_FILE = r"C:\Users\mukeshkr\Desktop\GenAI\Projects\21-DefenceRAG\data\scraped_raw_data.csv"
OUTPUT_FILE = "Processed_Contracts_Output_V2_RAG.xlsx"
DB_PERSIST_DIR = "./db_storage"

# COLUMN MAPPING
COL_DESC = "Description of Contract"
COL_DATE = "Contract Date"

PROJECT_ID = "my-test-project"
MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"  

# ==========================
# API SETUP
# ==========================

# 1. Check for the Token
if not os.getenv("LLMFOUNDRY_TOKEN"):
    print("Please set your LLMFOUNDRY_TOKEN environment variable.")
    os.environ["LLMFOUNDRY_TOKEN"] = getpass.getpass("Enter LLM Foundry Token: ")

# 2. Construct the formatted API Key
# (Assuming your Foundry setup uses "TOKEN:PROJECT" as the key)
API_KEY_FORMATTED = f'{os.environ.get("LLMFOUNDRY_TOKEN")}:{PROJECT_ID}'
BASE_URL = "https://llmfoundry.straive.com/openai/v1/"

def get_api_client():
    from openai import OpenAI
    client = OpenAI(
        api_key=API_KEY_FORMATTED,
        base_url=BASE_URL,
    )
    return client