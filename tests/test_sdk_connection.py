# tests/test_sdk_connection.py (v1.3)
#
# This version adds the necessary path correction.

import lmstudio as lms
import sys
import os

# --- Path Correction ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import LLM_MODEL_IDENTIFIER, EMBEDDING_MODEL_IDENTIFIER

def run_sdk_test():
    """
    Executes a simple, self-contained test of the LM Studio SDK connection.
    """
    print("--- Starting Isolated SDK Connection Test ---")
    
    test_passed = False
    
    try:
        print("\n-> [1/5] Attempting to connect to LM Studio server...")
        with lms.Client() as client:
            print("   ✅ Successfully connected to server.")
            
            llm = None
            try:
                print("\n-> [2/5] Cleaning up any pre-existing loaded models...")
                for model in client.llm.list_loaded():
                    print(f"   -> Unloading pre-existing model: {model.identifier}")
                    model.unload()
                print("   ✅ Pre-existing models unloaded.")

                print(f"\n-> [3/5] Attempting to load models with GPU acceleration...")
                llm = client.llm.load_new_instance(
                    LLM_MODEL_IDENTIFIER,
                    config={"gpu_offload": "max"}
                )
                print(f"   ✅ Successfully loaded LLM: {llm.identifier}")
                
                embedding_model = client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
                print(f"   ✅ Successfully loaded embedding model.")

                print("\n-> [4/5] Performing basic inference and embedding operations...")
                
                test_prompt = "Say 'hello'."
                response = llm.respond(test_prompt)
                print(f"   -> LLM Response: '{str(response).strip()}'")
                assert 'hello' in str(response).lower(), "LLM did not respond as expected."

                test_text = "This is a test."
                embedding_list = embedding_model.embed([test_text])
                embedding_vector = embedding_list[0]
                print(f"   -> Successfully generated embedding for '{test_text}'. Vector length: {len(embedding_vector)}")
                assert len(embedding_vector) > 0, "Embedding vector is empty."
                
                print("   ✅ Basic operations successful.")
                test_passed = True

            finally:
                print("\n-> [5/5] Attempting to unload all test resources...")
                if llm:
                    llm.unload()
                    print("   ✅ Test LLM instance unloaded.")
                print("   ✅ All resources cleaned up.")

    except Exception as e:
        print(f"\n--- ❌ TEST FAILED ---")
        print(f"An error occurred: {e}")
        
    if test_passed:
        print("\n\n--- ✅ Isolated SDK Connection Test PASSED ---")
    else:
        sys.exit(1)


if __name__ == "__main__":
    print("NOTE: Please ensure the LM Studio server is running with the required models available.")
    run_sdk_test()
