# Test the fixed memory consolidation system
# 
# This script creates a sample conversation log and tests the memory
# consolidation pipeline with the new native structured output implementation.

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_test_log():
    """Create a sample conversation log for testing."""
    test_content = """[2025-07-16 14:30:00] User Input: Hey Aurora, I'm working on a new project about renewable energy.
[2025-07-16 14:30:00] Aurora Response: That sounds fascinating! I'd love to hear more about your renewable energy project. What specific aspect are you focusing on?

[2025-07-16 14:30:30] User Input: I'm researching solar panel efficiency improvements. The current panels in my lab are only 18% efficient.
[2025-07-16 14:30:30] Aurora Response: 18% efficiency is actually quite good for standard silicon panels. The theoretical maximum for single-junction silicon cells is around 29%, so there's definitely room for improvement. Are you looking into perovskite tandem cells or other advanced technologies?

[2025-07-16 14:31:00] User Input: Yes! We're testing perovskite-silicon tandems. Initial results show 26% efficiency, but stability is still an issue.
[2025-07-16 14:31:00] Aurora Response: That's exciting progress! 26% efficiency is impressive for perovskite tandems. The stability challenge is well-known - moisture and heat degradation are the main culprits. Have you tried encapsulation techniques or UV-stable perovskite formulations?
"""
    
    # Write to the log file
    from config import LOG_FILE_PATH
    with open(LOG_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(test_content)
    print(f"✅ Created test log file: {LOG_FILE_PATH}")

def test_consolidation():
    """Test the memory consolidation pipeline."""
    print("--- Testing Memory Consolidation with Native Structured Output ---")
    
    # Create test log
    create_test_log()
    
    # Import and run the consolidation
    try:
        from aura_engine.memory_consolidation import run_consolidation_pipeline
        from aura_engine.memory_manager import MemoryManager
        import lmstudio as lms
        from config import LLM_MODEL_IDENTIFIER, EMBEDDING_MODEL_IDENTIFIER
        
        print("\n-> Connecting to LM Studio...")
        with lms.Client() as client:
            # Check for already loaded LLM models first
            loaded_llms = client.llm.list_loaded()
            if loaded_llms:
                llm_model = loaded_llms[0]
                print(f"   ✅ Using existing LLM model: {llm_model.identifier}")
            else:
                # Only load if none exist
                print("-> Loading LLM model...")
                llm_model = client.llm.load_new_instance(
                    LLM_MODEL_IDENTIFIER, 
                    config={"gpu_offload": "max"}
                )
                print(f"   ✅ LLM model loaded: {llm_model.identifier}")
            
            # Load embedding model
            embedding_model = client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
            print(f"   ✅ Embedding model ready")
            
            print(f"   -> Total LLM models loaded: {len(client.llm.list_loaded())}")
            
            # Initialize memory manager
            memory_manager = MemoryManager(client=client)
            
            # Run consolidation with explicit model handle
            run_consolidation_pipeline(
                client=client, 
                memory_manager=memory_manager, 
                model_handle=llm_model
            )
            
            print("\n--- ✅ Test completed successfully! ---")
            
    except Exception as e:
        print(f"\n--- ❌ Test failed: {e} ---")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_consolidation()
