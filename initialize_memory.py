# initialize_memory.py
#
# This script sets up the foundational memory architecture for the Genesis Agent.
# It creates a persistent vector database using ChromaDB that will be stored locally
# and loads the sentence-transformer model required for generating embeddings.

import chromadb
from sentence_transformers import SentenceTransformer
import os

# --- Configuration ---
# Define constants for paths and names to make the script easily configurable.
DB_PATH = "./agent_db"
COLLECTION_NAME = "genesis_memory"
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

def populate_memory_from_file(file_path: str, collection: chromadb.Collection, model: SentenceTransformer):
    """
    Placeholder function to populate the ChromaDB collection from a text file.
    
    This function will be implemented in a later task. Its purpose is to:
    1. Read the content from a source document.
    2. Split the text into logical, semantic chunks (e.g., by paragraph).
    3. Generate vector embeddings for each text chunk using the provided BGE model.
    4. Store the chunks (as documents) and their corresponding embeddings in the
       'genesis_memory' collection. Each entry will have a unique ID.
    """
    # This is a placeholder and will be fully implemented later.
    print(f"\nPlaceholder: In the future, this function would process '{file_path}'.")
    pass

# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- Initializing Agent Memory System ---")

    # 1. Initialize ChromaDB Persistent Client
    # We use PersistentClient to ensure that our database is saved to disk
    # in the directory specified by DB_PATH. This allows the agent's memory
    # to persist between sessions.
    print(f"Setting up persistent storage at: {os.path.abspath(DB_PATH)}")
    client = chromadb.PersistentClient(path=DB_PATH)

    # 2. Load the Embedding Model
    # This downloads or loads the BAAI/bge-base-en-v1.5 model from HuggingFace.
    # We explicitly set device='cpu' to ensure VRAM is conserved for the primary LLM,
    # as per the technical blueprint.
    print(f"Loading embedding model: '{EMBEDDING_MODEL_NAME}' onto CPU...")
    # This may take a few moments on the first run as the model is downloaded.
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME, device='cpu')
    print("Embedding model loaded successfully.")

    # 3. Create or Get the ChromaDB Collection
    # This command retrieves the collection if it exists or creates it if it doesn't.
    # This makes the script safe to run multiple times (idempotent).
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )
    print(f"Collection '{COLLECTION_NAME}' is ready.")

    # 4. Final Confirmation
    print("\n✅ ChromaDB memory system initialized successfully at ./agent_db")