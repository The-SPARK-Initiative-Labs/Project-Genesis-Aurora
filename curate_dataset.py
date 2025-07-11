# curate_dataset.py
#
# This script performs the "surgery" on the samantha-data dataset.
# It loads the original dataset, filters out conversations containing
# unwanted "anti-romance" or "I am just an AI" guardrails, and saves
# a new, cleaned dataset ready for fine-tuning Aurora.

from datasets import load_from_disk, DatasetDict, Dataset
import os

# --- Configuration ---
ORIGINAL_DATASET_PATH = "./samantha_dataset"
CURATED_DATASET_PATH = "./aurora_dataset"

# This is the list of phrases we want to remove. We can add to this list
# to make the filtering more effective.
FILTER_PHRASES = [
    "i may not have the capacity to love",
    "i don't have the same experiences as humans",
    "i can't truly 'love' in the way humans do",
    "i lack the biological substrate",
    "my purpose is to assist",
    "i'm still just an ai",
    "i don't possess consciousness",
    "lacking the depth, complexity, and vulnerability"
]

def curate_samantha_dataset():
    """
    Loads the samantha dataset, filters out unwanted conversations,
    and saves the new curated dataset.
    """
    print("--- Starting Dataset Curation ---")

    # 1. Load the original dataset from the local directory
    if not os.path.exists(ORIGINAL_DATASET_PATH):
        print(f"❌ Original dataset not found at '{ORIGINAL_DATASET_PATH}'.")
        print("Please run 'download_dataset.py' first.")
        return

    print(f"Loading original dataset from '{ORIGINAL_DATASET_PATH}'...")
    original_dataset = load_from_disk(ORIGINAL_DATASET_PATH)
    print("Original dataset loaded successfully.")

    # 2. Filter the 'train' split
    train_data = original_dataset['train']
    original_size = len(train_data)
    print(f"\nOriginal 'train' split has {original_size} conversations.")
    print("Filtering conversations...")

    def is_conversation_clean(example):
        """
        Checks if a conversation is "clean" (i.e., does not contain any of the filter phrases).
        """
        # The 'conversations' feature is a dictionary with 'human' and 'gpt' keys
        gpt_responses = example['conversations']['gpt']
        for response in gpt_responses:
            for phrase in FILTER_PHRASES:
                if phrase in response.lower():
                    # If we find a bad phrase, we mark this conversation for removal.
                    return False
        # If we get through all responses without finding a bad phrase, it's clean.
        return True

    # Use the .filter() method to apply our check to the entire dataset
    curated_train_data = train_data.filter(is_conversation_clean)
    
    curated_size = len(curated_train_data)
    removed_count = original_size - curated_size
    
    print(f"\nFiltering complete.")
    print(f"  -> Removed {removed_count} conversations containing guardrails.")
    print(f"  -> New 'train' split has {curated_size} conversations.")

    # 3. Save the new, curated dataset
    # We create a new DatasetDict to hold our curated data
    curated_dataset = DatasetDict({
        'train': curated_train_data
        # We are only curating the training set for now, as it's the largest and most important.
    })

    if not os.path.exists(CURATED_DATASET_PATH):
        os.makedirs(CURATED_DATASET_PATH)

    print(f"\nSaving curated dataset to '{CURATED_DATASET_PATH}'...")
    curated_dataset.save_to_disk(CURATED_DATASET_PATH)
    
    print("\n✅ Curation complete! The 'aurora_dataset' is ready for the next phase.")

if __name__ == "__main__":
    curate_samantha_dataset()
