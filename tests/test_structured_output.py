# test_structured_output.py (v3.0 - Definitive)
#
# This version uses the correct function signature for model.respond(), passing
# the chat history as the first POSITIONAL argument. This is the definitive
# fix based on the TypeError analysis.

import lmstudio as lms
import sys
from aura_engine.schemas import FactList
from config import LLM_MODEL_IDENTIFIER

# --- Test Data ---
TEST_CHAT_HISTORY = [
    {"role": "system", "content": "You are a JSON-only output machine. Do not add any conversational text, markdown formatting, or any characters outside of the JSON object."},
    {"role": "user", "content": f"Read the <conversation_log> and extract every key fact verbatim. A key fact is a complete sentence that reveals a plan, a personal detail, an emotional state, or a specific piece of information. Respond with ONLY a JSON object adhering to the FactList schema.\n\n<conversation_log>\nMy sister Sarah's birthday is next Tuesday. We need to buy a gift.\n</conversation_log>"}
]


def run_isolated_test():
    """
    Executes the isolated test for the `response_format` feature.
    """
    print("--- Running Isolated Test for Structured Output ---")
    
    try:
        with lms.Client() as client:
            print(f"-> Acquiring handle for model: {LLM_MODEL_IDENTIFIER}...")
            model = client.llm.model(LLM_MODEL_IDENTIFIER)
            print("   ✅ Model handle acquired.")

            print("\n-> Attempting the structured response call with the correct signature...")
            
            # DEFINITIVE FIX: Pass the chat history as the first positional argument.
            response = model.respond(
                TEST_CHAT_HISTORY,
                response_format=FactList,
                config={"temperature": 0.0}
            )

            # If we reach here, the call succeeded. Now, let's see the result.
            print("\n--- ✅ SUCCESS! The model.respond() call completed. ---")
            print(f"   -> Type of response: {type(response)}")
            
            # Check for the .parsed attribute
            if hasattr(response, 'parsed'):
                print("   -> The 'parsed' attribute exists.")
                parsed_data = response.parsed
                print(f"   -> Type of parsed_data: {type(parsed_data)}")
                print(f"   -> Parsed Data: {parsed_data}")
            else:
                print("   -> ❌ CRITICAL FAILURE: The 'parsed' attribute does NOT exist on the response object.")
                print(f"   -> Full response object attributes: {dir(response)}")


    except Exception as e:
        print(f"\n--- ❌ FAILURE: The model.respond() call failed with an exception. ---")
        print(f"   -> Error Type: {type(e)}")
        print(f"   -> Error Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_isolated_test()
