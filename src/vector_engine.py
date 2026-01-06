import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 1. FIXED: Removed API_KEY_FORMATTED from imports
from config import BASE_URL, EMBEDDING_MODEL 

class DefenseVectorDB:
    # 2. FIXED: Added api_key as an argument
    def __init__(self, persist_dir, api_key=None):
        print("Initializing Vector Database (ChromaDB) with OpenAI Embeddings...")
        
        self.persist_dir = persist_dir

        # 3. FIXED: Logic to use passed key OR environment variable
        final_api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if not final_api_key:
            # This prevents the app from crashing silently; it tells you exactly what's wrong.
            raise ValueError("OpenAI API Key is missing. Please provide it in the sidebar.")

        # Initialize OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=final_api_key, # Use the dynamic key
            openai_api_base=BASE_URL 
        )
        
        # Initialize Vector Store
        self.db = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings,
            collection_name="defense_contracts_memory"
        )
        print("Vector Database Ready.")

    def search_context(self, query, k=3):
        """
        Retrieves the 3 most similar past contracts to the current query.
        """
        results = self.db.similarity_search(query, k=k)
        return results

    def add_contract(self, text, metadata):
        """
        Saves a classified contract to the DB for dynamic learning.
        """
        # Ensure metadata values are strings to avoid DB errors
        clean_meta = {k: str(v) for k, v in metadata.items() if v is not None}
        
        doc = Document(page_content=text, metadata=clean_meta)
        self.db.add_documents([doc])