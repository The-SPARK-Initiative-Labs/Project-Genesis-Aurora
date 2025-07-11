# download_dataset.py
#
# This script downloads the 'cognitivecomputations/samantha-data' dataset
# from Hugging Face and saves it to a local directory for processing.

from datasets import load_dataset
import os

# --- Configuration ---
DATASET_NAME = "cognitivecomputations/samantha-data"
LOCAL_SAVE_PATH = "./samantha_dataset"

def download_and_inspect_dataset():
    """
    Downloads the specified dataset from Hugging Face, saves it locally,
    and prints some basic information about its structure.
    """
    print(f"--- Starting Download for: {DATASET_NAME} ---")
    print(f"This may take some time depending on the dataset size and your connection speed.")
    
    try:
        # Create the save directory if it doesn't exist
        if not os.path.exists(LOCAL_SAVE_PATH):
            os.makedirs(LOCAL_SAVE_PATH)
            print(f"Created directory: {LOCAL_SAVE_PATH}")

        # Load the dataset from Hugging Face.
        # CORRECTED: Added trust_remote_code=True to allow the custom code in the dataset
        # repository to run, as required.
        dataset = load_dataset(DATASET_NAME, trust_remote_code=True)
        
        # Save the dataset to our local project folder for persistent access.
        print(f"\nSaving dataset to '{LOCAL_SAVE_PATH}'...")
        dataset.save_to_disk(LOCAL_SAVE_PATH)
        
        print("\n✅ Dataset downloaded and saved successfully!")
        
        # --- Inspect the Dataset ---
        print("\n--- Dataset Inspection ---")
        print("Dataset structure:")
        print(dataset)
        
        # Print the first example from the 'train' split to see its format.
        if 'train' in dataset:
            print("\nFirst example from the 'train' split:")
            print(dataset['train'][0])
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your internet connection and the dataset name.")

if __name__ == "__main__":
    download_and_inspect_dataset()
