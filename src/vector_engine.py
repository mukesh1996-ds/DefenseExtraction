import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. FIXED: Removed OpenAI/Chroma imports as we switched to TF-IDF
# from config import BASE_URL, EMBEDDING_MODEL # Not needed for local TF-IDF

class DefenseVectorDB:
    """
    Updated Memory Engine using TF-IDF (Scikit-Learn).
    Replaces ChromaDB to align with the new 'One-Shot' classification logic.
    """
    
    def __init__(self, persist_dir=None, api_key=None):
        # Note: persist_dir is now treated as the path to the Excel Reference File
        # If None, we try to find the default path.
        
        self.reference_file = persist_dir if persist_dir else "Market Segment.xlsx"
        print(f"Initializing Memory Engine (TF-IDF) from: {self.reference_file}...")

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.df_examples = pd.DataFrame()
        self.example_vectors = None
        self.is_ready = False

        self.load_memory()

    def load_memory(self):
        """
        Loads the Excel file and fits the TF-IDF vectorizer.
        """
        try:
            if os.path.exists(self.reference_file):
                self.df_examples = pd.read_excel(self.reference_file)
                
                # Ensure text column exists
                if 'Description of Contract' in self.df_examples.columns:
                    # Fill NaNs to avoid errors
                    self.df_examples['Description of Contract'] = self.df_examples['Description of Contract'].fillna("")
                    
                    # Fit the vectorizer
                    self.example_vectors = self.vectorizer.fit_transform(self.df_examples['Description of Contract'].astype(str))
                    self.is_ready = True
                    print(f"Success: Memory loaded with {len(self.df_examples)} examples.")
                else:
                    print(f"Warning: Column 'Description of Contract' not found in {self.reference_file}")
            else:
                print(f"Warning: Reference file not found at {self.reference_file}. Memory starting empty.")
        except Exception as e:
            print(f"CRITICAL WARNING: Could not load Memory File. Error: {e}")

    def search_context(self, query, k=1):
        """
        Finds the most similar past contract using Cosine Similarity.
        Returns a list of result dictionaries (simulating the old Document object structure if needed, 
        or just the raw data).
        """
        if not self.is_ready or self.vectorizer is None:
            return []

        try:
            # Transform current query
            new_vec = self.vectorizer.transform([query])
            
            # Calculate similarity
            similarities = cosine_similarity(new_vec, self.example_vectors).flatten()
            
            # Get top k indices
            # Note: argsort sorts ascending, so we take the last k and reverse
            best_indices = similarities.argsort()[-k:][::-1]
            
            results = []
            for idx in best_indices:
                score = similarities[idx]
                if score > 0.1: # Threshold to ignore irrelevant matches
                    row = self.df_examples.iloc[idx]
                    
                    # Construct a result object similar to what processors.py expects
                    result = {
                        "text": row['Description of Contract'],
                        "score": score,
                        "classification": {
                            "Market Segment": row.get('Market Segment', "Unknown"),
                            "System Type (General)": row.get('System Type (General)', "Not Applicable"),
                            "System Type (Specific)": row.get('System Type (Specific)', "Not Applicable"),
                            "System Name (General)": row.get('System Name (General)', "Not Applicable"),
                            "System Name (Specific)": row.get('System Name (Specific)', "Not Applicable"),
                            "System Piloting": row.get('System Piloting', "Derived from logic")
                        }
                    }
                    results.append(result)
            
            return results

        except Exception as e:
            print(f"Error searching memory: {e}")
            return []

    def add_contract(self, text, metadata):
        """
        Adds a new classified contract to the runtime memory and re-fits the vectorizer.
        """
        try:
            # Create new row
            new_row = {
                "Description of Contract": text,
                **metadata
            }
            
            # Append to DataFrame
            self.df_examples = pd.concat([self.df_examples, pd.DataFrame([new_row])], ignore_index=True)
            
            # Re-fit Vectorizer (Necessary for TF-IDF as vocabulary might change)
            # In a huge production system you'd use HashingVectorizer, but for <10k rows this is fast.
            self.example_vectors = self.vectorizer.fit_transform(self.df_examples['Description of Contract'].astype(str))
            
            print("New contract added to memory.")
            
        except Exception as e:
            print(f"Error adding to memory: {e}")