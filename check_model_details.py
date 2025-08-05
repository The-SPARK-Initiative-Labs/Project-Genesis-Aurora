#!/usr/bin/env python3
# Quick script to check model quantization details

import lmstudio as lms
from config import LLM_MODEL_IDENTIFIER

def check_model_details():
    """Check detailed model information including quantization."""
    print("--- Checking Model Details ---")
    
    try:
        with lms.Client() as client:
            print(f"Looking up model: {LLM_MODEL_IDENTIFIER}")
            
            # Get or load the model
            model = client.llm.model(LLM_MODEL_IDENTIFIER)
            print(f"Model handle identifier: {model.identifier}")
            
            # Get detailed model info
            print("\n--- Model Information ---")
            model_info = model.get_info()
            print(f"Architecture: {model_info.architecture if hasattr(model_info, 'architecture') else 'Not available'}")
            print(f"Model Info: {model_info}")
            
            # Get load configuration
            print("\n--- Load Configuration ---")
            load_config = model.get_load_config()
            print(f"Load Config: {load_config}")
            
            # List all downloaded models to see more details
            print("\n--- All Downloaded Models ---")
            downloaded_models = client.system.list_downloaded_models(model_type="llm")
            for downloaded_model in downloaded_models:
                if LLM_MODEL_IDENTIFIER in downloaded_model.path or "nemo" in downloaded_model.path.lower():
                    print(f"Path: {downloaded_model.path}")
                    print(f"Model details: {downloaded_model}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_model_details()
