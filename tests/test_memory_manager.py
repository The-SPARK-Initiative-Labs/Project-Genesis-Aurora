# tests/test_memory_manager.py (v1.2)
#
# This version adds the necessary path correction.

import unittest
import os
import shutil
import uuid
import sys
import lmstudio as lms

# --- Path Correction ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aura_engine.memory_manager import MemoryManager
from config import DB_PATH, COLLECTION_NAME

class TestMemoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the SDK client once for all tests in this class."""
        print("--- [Setup] Initializing SDK Client for Memory Manager Test ---")
        try:
            cls.client = lms.Client()
        except Exception as e:
            raise ConnectionError(f"Could not connect to LM Studio server. Please ensure it's running. Error: {e}")

    def setUp(self):
        """Set up a clean environment before each test."""
        print("\n--- [Test] Preparing a clean database environment ---")
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)
        self.memory_manager = MemoryManager(client=self.client)

    def tearDown(self):
        """Clean up after each test."""
        print("--- [Teardown] Shutting down memory manager ---")
        self.memory_manager.shutdown()

    def test_add_and_retrieve_memory(self):
        """
        Tests the core functionality: adding a memory and retrieving it.
        """
        print("-> Testing add_memory() and retrieve_relevant_memories()...")
        
        test_id = str(uuid.uuid4())
        test_text = "Project Genesis is the first project of the S.P.A.R.K. Initiative."
        test_metadata = {"source": "test_script", "type": "fact"}
        
        print(f"   -> Adding memory: '{test_text}'")
        self.memory_manager.add_memory(
            text=test_text,
            doc_id=test_id,
            metadata=test_metadata
        )
        
        print(f"   -> Retrieving memories relevant to: '{test_text}'")
        retrieved_memories = self.memory_manager.retrieve_relevant_memories(test_text, num_results=1)
        
        print("   -> Verifying results...")
        self.assertEqual(len(retrieved_memories), 1, "Expected to retrieve exactly one memory.")
        
        retrieved_memory = retrieved_memories[0]
        self.assertEqual(retrieved_memory['text'], test_text, "Retrieved text does not match the original.")
        self.assertEqual(retrieved_memory['metadata']['source'], 'test_script', "Retrieved metadata is incorrect.")
        
        print("   ✅ Verification successful.")


if __name__ == "__main__":
    print("--- Starting Isolated Memory Manager Test ---")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMemoryManager))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)
