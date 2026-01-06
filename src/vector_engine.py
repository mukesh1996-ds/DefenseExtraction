import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config import API_KEY_FORMATTED, BASE_URL, EMBEDDING_MODEL


class DefenseVectorDB:
    def __init__(self, persist_dir):
        print("Initializing Vector Database (ChromaDB) with OpenAI Embeddings...")
        
        self.persist_dir = persist_dir

        # Initialize OpenAI Embeddings
        # We pass the same API key and Base URL from config
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=API_KEY_FORMATTED,
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