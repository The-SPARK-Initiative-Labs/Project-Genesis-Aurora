# aura_engine/memory_manager.py (v4.0 - Verified Fixes)
#
# This version applies the verified fixes based on our successful isolated
# database test and the previous integration test failures.
# 1. Initializes ChromaDB with settings to allow reset, fixing the shutdown error.
# 2. Correctly handles the data structure from the SDK's .embed() method.

import chromadb
from chromadb.config import Settings
import lmstudio as lms
from config import DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_IDENTIFIER
from typing import Dict, Any, List

class MemoryManager:
    """
    Manages all interactions with the ChromaDB vector memory, using the
    lmstudio SDK for embedding generation.
    """
    def __init__(self, client: lms.Client):
        """Initializes the MemoryManager."""
        print("Initializing Memory Manager...")
        self.client = client
        # VERIFIED FIX 1: Initialize the client with settings that allow reset.
        # This is required for the shutdown() method to work during testing.
        self.db_client = chromadb.PersistentClient(
            path=DB_PATH,
            settings=Settings(allow_reset=True)
        )
        
        print(f"Loading embedding model: {EMBEDDING_MODEL_IDENTIFIER}...")
        self.embedding_model = self.client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
        print("✅ Embedding model loaded.")

        self.collection = self.db_client.get_or_create_collection(name=COLLECTION_NAME)
        print("✅ Memory Manager initialized successfully.")

    def add_memory(self, text: str, doc_id: str, metadata: Dict[str, Any]):
        """
        Adds a new piece of text to the vector memory with its metadata.
        """
        try:
            # VERIFIED FIX 2: The SDK's .embed() method returns a list of embedding objects.
            # We access the first item in that list to get the embedding object for our text.
            embedding_response = self.embedding_model.embed(texts=[text])
            embedding_object = embedding_response[0]
            embedding_vector = embedding_object.embedding
            
            self.collection.add(
                documents=[text],
                ids=[doc_id],
                embeddings=[embedding_vector],
                metadatas=[metadata]
            )
            print(f"   -> Memory added to DB: {doc_id} (Type: {metadata.get('type', 'N/A')})")
        except Exception as e:
            print(f"   ❌ Error adding memory: {e}")

    def retrieve_relevant_memories(self, query_text: str, num_results: int = 3) -> list:
        """
        Retrieves the most relevant memories and their metadata.
        """
        try:
            # Apply the same fix for the query embedding
            query_embedding_response = self.embedding_model.embed(texts=[query_text])
            query_embedding_object = query_embedding_response[0]
            query_embedding_vector = query_embedding_object.embedding

            results = self.collection.query(
                query_embeddings=[query_embedding_vector],
                n_results=num_results,
                include=['documents', 'metadatas']
            )
            
            retrieved = []
            if results.get('ids') and results['ids'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    retrieved.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i]
                    })
            return retrieved
        except Exception as e:
            print(f"   ❌ Error retrieving memories: {e}")
            return []

    def shutdown(self):
        """
        Shuts down the ChromaDB client connection cleanly by resetting it.
        """
        print("Shutting down Memory Manager and ChromaDB connection...")
        self.db_client.reset()
        print("✅ Memory Manager shut down.")
# aura_engine/memory_manager.py (v4.1 - Final)
#
# This version applies the definitive fix for the embed method's signature,
# removing the unexpected keyword argument.

import chromadb
from chromadb.config import Settings
import lmstudio as lms
from config import DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_IDENTIFIER
from typing import Dict, Any, List

class MemoryManager:
    """
    Manages all interactions with the ChromaDB vector memory, using the
    lmstudio SDK for embedding generation.
    """
    def __init__(self, client: lms.Client):
        """Initializes the MemoryManager."""
        print("Initializing Memory Manager...")
        self.client = client
        self.db_client = chromadb.PersistentClient(
            path=DB_PATH,
            settings=Settings(allow_reset=True)
        )
        
        print(f"Loading embedding model: {EMBEDDING_MODEL_IDENTIFIER}...")
        self.embedding_model = self.client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
        print("✅ Embedding model loaded.")

        self.collection = self.db_client.get_or_create_collection(name=COLLECTION_NAME)
        print("✅ Memory Manager initialized successfully.")

    def add_memory(self, text: str, doc_id: str, metadata: Dict[str, Any]):
        """
        Adds a new piece of text to the vector memory with its metadata.
        """
        try:
            # DEFINITIVE FIX: The .embed() method expects a positional argument, not a keyword argument.
            embedding_response = self.embedding_model.embed([text])
            embedding_vector = embedding_response[0]
            
            self.collection.add(
                documents=[text],
                ids=[doc_id],
                embeddings=[embedding_vector],
                metadatas=[metadata]
            )
            print(f"   -> Memory added to DB: {doc_id} (Type: {metadata.get('type', 'N/A')})")
        except Exception as e:
            print(f"   ❌ Error adding memory: {e}")

    def retrieve_relevant_memories(self, query_text: str, num_results: int = 3) -> list:
        """
        Retrieves the most relevant memories and their metadata.
        """
        try:
            # Apply the same fix for the query embedding
            query_embedding_response = self.embedding_model.embed([query_text])
            query_embedding_vector = query_embedding_response[0]

            results = self.collection.query(
                query_embeddings=[query_embedding_vector],
                n_results=num_results,
                include=['documents', 'metadatas']
            )
            
            retrieved = []
            if results.get('ids') and results['ids'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    retrieved.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i]
                    })
            return retrieved
        except Exception as e:
            print(f"   ❌ Error retrieving memories: {e}")
            return []

    def shutdown(self):
        """
        Shuts down the ChromaDB client connection cleanly by resetting it.
        """
        print("Shutting down Memory Manager and ChromaDB connection...")
        self.db_client.reset()
        print("✅ Memory Manager shut down.")
