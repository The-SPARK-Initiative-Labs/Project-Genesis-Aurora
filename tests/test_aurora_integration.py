# tests/test_aurora_integration.py (v1.2)
#
# This version adds the necessary path correction to allow the test
# to run from within the `tests/` subdirectory.

import unittest
import os
import shutil
from unittest.mock import patch
import sys

# --- Path Correction ---
# This allows the script to find modules in the parent directory (project root)
# where 'aura_engine' and 'config' are located.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aura_engine.aurora import Aurora
from config import DB_PATH, LOG_FILE_PATH

class TestAuroraIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a clean environment before the test."""
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

    def test_aurora_lifecycle(self):
        """Tests the full lifecycle of the Aurora agent."""
        simulated_inputs = [
            "Hello, Aurora. This is the final integration test.",
            "quit"
        ]

        aurora_agent = None
        try:
            with patch('builtins.input', side_effect=simulated_inputs):
                print("\n--- [TEST] Initializing and running Aurora instance... ---")
                
                aurora_agent = Aurora()
                aurora_agent.run_chat_loop()

            print("--- [TEST] Aurora instance has completed its chat loop. ---")

            # Verify the results *before* shutdown
            print("\n--- [VERIFY] Checking test assertions... ---")

            # Assertion 1: Verify the raw log file
            print(f"   -> Verifying log file: '{LOG_FILE_PATH}'")
            self.assertTrue(os.path.exists(LOG_FILE_PATH))
            with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
                log_content = f.read()
            self.assertIn("User: Hello, Aurora. This is the final integration test.", log_content)
            print("      ✅ Log file contains the correct interaction.")

            # Assertion 2: Verify the database contents
            print("   -> Verifying ChromaDB contents via MemoryManager...")
            memories_in_db = aurora_agent.memory.collection.get()
            self.assertEqual(len(memories_in_db['ids']), 1, "Memory was not stored in the database.")
            print("      ✅ ChromaDB contains one memory.")

        finally:
            # Ensure a clean shutdown
            if aurora_agent:
                aurora_agent.shutdown()


if __name__ == "__main__":
    print("--- Starting Final Integration Test for Aurora Class ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
