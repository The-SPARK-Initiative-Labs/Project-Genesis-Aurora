# aura_engine/process_emotions.py (v2.0 - Upgraded Model)
#
# This module has been upgraded to use a sophisticated, multi-label emotion
# classification model, providing a much richer emotional analysis.

from transformers import pipeline
from typing import List, Dict

# --- Global variable to hold the loaded model ---
# This ensures the model is loaded into memory only once.
emotion_classifier = None

def initialize_emotion_classifier():
    """
    Initializes the emotion classification pipeline if it hasn't been already.
    """
    global emotion_classifier
    if emotion_classifier is None:
        print("Initializing multi-label emotion classification model...")
        # On the first run, this will download the model from the Hugging Face Hub.
        # Subsequent runs will use the cached version for offline operation.
        emotion_classifier = pipeline(
            task="text-classification",
            model="SamLowe/roberta-base-go_emotions",
            top_k=None  # Ensures all 28 emotion scores are returned
        )
        print("✅ Emotion classifier initialized successfully.")

def get_emotional_overlay(text_chunk: str, threshold: float = 0.3) -> List[Dict]:
    """
    Analyzes a chunk of text and returns a list of detected emotions
    that exceed a given confidence threshold.

    Args:
        text_chunk (str): A string of text to be analyzed.
        threshold (float): The confidence score threshold for including an emotion.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains
                    an emotion 'label' and its 'score'. Returns an empty
                    list if the input is invalid or no emotions meet the threshold.
    """
    # Ensure the model pipeline is initialized before proceeding.
    initialize_emotion_classifier()

    if not isinstance(text_chunk, str) or not text_chunk.strip():
        return []

    try:
        # The model returns a list containing one list of results
        model_output = emotion_classifier(text_chunk)
        
        # Filter the results to only include emotions above the threshold
        detected_emotions = [
            emotion for emotion in model_output[0]
            if emotion['score'] > threshold
        ]
        
        # Sort by score in descending order
        detected_emotions.sort(key=lambda x: x['score'], reverse=True)
        
        return detected_emotions
        
    except Exception as e:
        print(f"❌ Error during emotion analysis: {e}")
        return [{'label': 'error', 'score': 1.0}]


# --- Example Usage (for testing purposes) ---
if __name__ == "__main__":
    print("--- Testing Upgraded Emotion Overlay Engine ---")

    sample_text = "I am so happy you're here, this is a wonderful surprise and I feel so much love!"
    
    print(f"\nAnalyzing: '{sample_text}'")
    emotions = get_emotional_overlay(sample_text)
    
    print("\nDetected Emotions (threshold > 0.3):")
    import pprint
    pprint.pprint(emotions)
    
    # Verify that the expected emotions are present
    labels = {e['label'] for e in emotions}
    assert 'joy' in labels
    assert 'love' in labels
    assert 'surprise' in labels
    
    print("\n✅ Test successful.")
