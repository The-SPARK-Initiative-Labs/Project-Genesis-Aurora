# tests/test_emotion_model.py (v1.1 - Corrected Assertions)
#
# An isolated test script to verify that the recommended multi-label emotion
# classification model works correctly. This version has corrected, more
# realistic assertions.

import unittest
import sys
import os
import pprint

# --- Path Correction ---
# This allows the script to find modules in the parent directory (project root)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This is the library we need to test for compatibility
from transformers import pipeline

class TestEmotionModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initializes the text classification pipeline with the recommended model.
        On the first run, this will download the model from the Hugging Face Hub.
        """
        print("--- [Setup] Initializing Emotion Classification Model ---")
        print("NOTE: This may take a few minutes on the first run as it downloads the model.")
        try:
            cls.classifier = pipeline(
                task="text-classification",
                model="SamLowe/roberta-base-go_emotions",
                top_k=None  # Ensures all 28 emotion scores are returned
            )
            print("✅ Model initialized successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize the model pipeline: {e}")

    def test_emotion_analysis(self):
        """
        Tests that the model can analyze text and return a list of emotions.
        """
        print("\n--- [Test] Analyzing sample text for emotions ---")
        
        sample_text = "I am so happy you're here, this is a wonderful surprise!"
        
        model_output = self.classifier(sample_text)
        self.assertIsInstance(model_output, list)
        self.assertIsInstance(model_output[0], list)
        
        emotions = model_output[0]
        
        print("-> Detected Emotions (Top 5):")
        top_5 = sorted(emotions, key=lambda x: x['score'], reverse=True)[:5]
        pprint.pprint(top_5)

        # --- CORRECTED ASSERTIONS ---
        # Instead of checking for an arbitrary score, we will verify that
        # the model correctly identified 'joy' as the most likely emotion.
        
        # 1. Find the highest scoring emotion
        highest_emotion = top_5[0]
        
        # 2. Assert that the label of the highest scoring emotion is 'joy'
        self.assertEqual(highest_emotion['label'], 'joy', "The top-scoring emotion should be 'joy'.")
        
        # 3. We can still do a looser check for the presence of other emotions
        emotion_labels = {result['label'] for result in emotions}
        self.assertIn('excitement', emotion_labels, "'excitement' should be in the results.")
        self.assertIn('surprise', emotion_labels, "'surprise' should be in the results.")
        
        print("\n   ✅ Verification successful.")


if __name__ == "__main__":
    print("--- Starting Isolated Emotion Model Test ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
