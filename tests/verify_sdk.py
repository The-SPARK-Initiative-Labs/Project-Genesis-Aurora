# verify_sdk.py
# A script to verify the installation and functionality of the lmstudio-python SDK.
# FINAL WORKING VERSION: This script is based on our successful tests and uses
# the correct methods as confirmed by the research documents.

import lmstudio as lms
import sys

# --- CONFIGURATION ---
# We specify the identifier of the model we want to test.
MODEL_TO_TEST = "backyardai/Nemo-12B-Marlin-v5-GGUF"

def run_verification():
    """
    Performs a step-by-step verification of the LM Studio connection and inference.
    """
    print("--- LM Studio Python SDK Verification ---")

    # Step 1: Attempt to create a client connection.
    try:
        client = lms.Client()
        print("✅ Successfully created a client.")
    except Exception as e:
        print(f"❌ Could not create a client. Is the LM Studio server running?")
        print(f"   Error details: {e}")
        sys.exit(1)

    with client:
        # Step 2: Explicitly get a handle to the loaded model.
        print("\n--- Getting a handle to the loaded model ---")
        try:
            # We use client.llm.model() which we have verified works.
            model = client.llm.model(MODEL_TO_TEST)
            print(f"✅ Successfully got a handle to model: {model.identifier}")
        
        except Exception as e:
            print(f"❌ An error occurred while trying to get the model.")
            print(f"   Is the model '{MODEL_TO_TEST}' loaded in LM Studio?")
            print(f"   Error details: {e}")
            sys.exit(1)

        # Step 3: Perform a test inference.
        print("\n--- Performing a test inference ---")
        try:
            print(f"Sending a test prompt to model: '{model.identifier}'...")
            prompt = "In one short sentence, what is a large language model?"
            
            response = model.respond(prompt)
            
            print("\n✅ Received a response from the model:")
            
            # --- THE CORRECTED METHOD ---
            # The error 'PredictionResult' object has no attribute 'choices'
            # proves we must access the content directly.
            if hasattr(response, 'content'):
                print(f"   Model Response: {response.content.strip()}")
            else:
                print("   The model returned a response, but the .content attribute could not be found.")
                print(f"   (Full response object: {response})")
        
        except Exception as e:
            print(f"❌ An error occurred during inference.")
            print(f"   Error details: {e}")
            sys.exit(1)

    print("\n\n--- Verification Complete ---")
    print("✅ Your lmstudio-python SDK installation appears to be working correctly.")

if __name__ == "__main__":
    run_verification()
