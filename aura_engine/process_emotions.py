# process_emotions.py
#
# This module contains the function for Layer 2 of the agent's memory: The Emotional Overlay.
# It uses a pre-trained transformer model to perform sentiment analysis on a chunk of text.

# The 'pipeline' is a high-level helper from the transformers library that simplifies using models.
from transformers import pipeline

# --- Global variable to hold the loaded model ---
# We define this outside the function so that the model is loaded into memory only once.
# This is a crucial optimization to prevent re-loading the large model on every function call.
sentiment_pipeline = None

def initialize_pipeline():
    """
    Initializes the sentiment analysis pipeline if it hasn't been already.
    This function will be called automatically by get_emotional_overlay on its first run.
    """
    global sentiment_pipeline
    if sentiment_pipeline is None:
        print("Initializing sentiment analysis model for the first time...")
        # Load the specified model for sentiment analysis.
        # The library handles downloading the model from the Hugging Face Hub on the first run.
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="siebert/sentiment-roberta-large-english"
        )
        print("Model initialized successfully.")

def get_emotional_overlay(text_chunk: str) -> dict:
    """
    Analyzes a chunk of text and returns its emotional sentiment.

    Args:
        text_chunk (str): A string of text to be analyzed.

    Returns:
        dict: A dictionary containing the 'label' (e.g., 'POSITIVE') and 'score' (a float).
              Returns an error dictionary if the input is invalid.
    """
    # Ensure the model pipeline is initialized before proceeding.
    initialize_pipeline()

    if not isinstance(text_chunk, str) or not text_chunk.strip():
        return {'label': 'ERROR', 'score': 0.0, 'message': 'Input must be a non-empty string.'}

    # Run the text through the sentiment analysis pipeline.
    # The result is typically a list containing one dictionary.
    try:
        result = sentiment_pipeline(text_chunk)
        # We return the first (and only) dictionary from the list.
        return result[0]
    except Exception as e:
        return {'label': 'ERROR', 'score': 0.0, 'message': str(e)}


# --- Example Usage (for testing purposes) ---
if __name__ == "__main__":
    print("--- Testing Layer 2: The Emotional Overlay Engine ---")

    # 1. Define some test sentences
    positive_text = "This is a wonderful and brilliant plan. I am so excited to start!"
    negative_text = "I am concerned this might be a terrible mistake with many problems."
    neutral_text = "The system is currently operational."

    # 2. Get the emotional overlay for each sentence
    print(f"\nAnalyzing: '{positive_text}'")
    positive_result = get_emotional_overlay(positive_text)
    print(f"Result: {positive_result}")

    print(f"\nAnalyzing: '{negative_text}'")
    negative_result = get_emotional_overlay(negative_text)
    print(f"Result: {negative_result}")

    print(f"\nAnalyzing: '{neutral_text}'")
    neutral_result = get_emotional_overlay(neutral_text)
    print(f"Result: {neutral_result}")

    # 3. Test the reusability of the pipeline (it should not re-initialize)
    print("\n--- Verifying model is not reloaded ---")
    print("Analyzing a second positive text...")
    second_positive_result = get_emotional_overlay("I feel very optimistic about our progress.")
    print(f"Result: {second_positive_result}")
    print("Notice the 'Initializing...' message did not appear a second time.")