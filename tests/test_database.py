# test_database.py
#
# A simple, isolated script to verify that the ChromaDB installation is working
# correctly. This test does not involve the LM Studio SDK or any complex logic.
# Its only purpose is to confirm we can create, write to, read from, and
# cleanly shut down the database.

import chromadb
from chromadb.config import Settings
import os
import shutil
import uuid

# --- Configuration ---
DB_PATH = "./test_db"
COLLECTION_NAME = "test_collection"

def run_db_test():
    """
    Executes a simple, self-contained test of ChromaDB functionality.
    """
    print("--- Starting Isolated ChromaDB Test ---")

    # --- 1. Setup: Ensure a clean environment ---
    if os.path.exists(DB_PATH):
        print(f"-> Found old test database at '{DB_PATH}'. Removing it.")
        shutil.rmtree(DB_PATH)

    # --- 2. Initialization Test ---
    try:
        print(f"\n-> Attempting to create a new database at '{DB_PATH}'...")
        # We initialize the client with settings that allow it to be reset/deleted.
        client = chromadb.PersistentClient(
            path=DB_PATH,
            settings=Settings(allow_reset=True)
        )
        print("   ✅ Successfully created ChromaDB client.")
        
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"   ✅ Successfully got or created collection: '{COLLECTION_NAME}'")
    except Exception as e:
        print(f"   ❌ FAILED: Could not initialize the database. Error: {e}")
        return # Stop the test if we can't even connect

    # --- 3. Write Test ---
    try:
        print("\n-> Attempting to write one record to the database...")
        test_id = str(uuid.uuid4())
        test_doc = "This is a simple test document."
        test_meta = {"source": "db_test"}
        
        # Note: ChromaDB can generate embeddings for us if we don't provide them.
        # For this simple test, we will let it do that.
        collection.add(
            documents=[test_doc],
            ids=[test_id],
            metadatas=[test_meta]
        )
        print(f"   ✅ Successfully added document with ID: {test_id}")
    except Exception as e:
        print(f"   ❌ FAILED: Could not write to the database. Error: {e}")
        return

    # --- 4. Read Test ---
    try:
        print("\n-> Attempting to read the record back from the database...")
        retrieved = collection.get(ids=[test_id])
        
        assert len(retrieved['ids']) == 1, "The number of retrieved items was not 1."
        assert retrieved['documents'][0] == test_doc, "The retrieved document content does not match."
        assert retrieved['metadatas'][0]['source'] == 'db_test', "The retrieved metadata does not match."
        
        print(f"   ✅ Successfully retrieved and verified the document.")

    except Exception as e:
        print(f"   ❌ FAILED: Could not read or verify data. Error: {e}")
        return

    # --- 5. Shutdown Test ---
    try:
        print("\n-> Attempting to shut down the database connection cleanly...")
        client.reset() # This deletes the collection and releases file locks
        print("   ✅ Successfully reset the database.")
    except Exception as e:
        print(f"   ❌ FAILED: Could not reset the database. Error: {e}")
        return

    print("\n--- ✅ Isolated ChromaDB Test PASSED ---")


if __name__ == "__main__":
    run_db_test()
