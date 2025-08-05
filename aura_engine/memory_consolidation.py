# aura_engine/memory_consolidation.py (v4.3 - Constrained Narrative)
#
# This version uses simple prompting and constrains the Narrative Weaver to prevent
# hallucination. All agents use basic text prompts with strict fact-only instructions.

import lmstudio as lms
import os
import sys
import time
import uuid
import json
from datetime import datetime
from typing import List, Dict

# Add project root to path to allow direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import LLM_MODEL_IDENTIFIER, LOG_FILE_PATH, EMBEDDING_MODEL_IDENTIFIER
from aura_engine.schemas import FactList, ValidationResponse, NarrativeSummary
from aura_engine.memory_manager import MemoryManager

# --- Agent Functions Using Simple Prompting ---
def _extract_facts(model: 'lms.Model', text_content: str) -> List[str]:
    """Agent 1: Simple prompting approach to test if model works."""
    print("-> Running Extractor Agent...")
    try:
        # Simple prompting first to confirm model responds
        simple_prompt = f"""Extract 3 key facts from this conversation log. Format as a simple list:

{text_content}

Facts:
1."""
        
        response = model.respond(
            simple_prompt,
            config={"temperature": 0.1, "max_tokens": 300}
        )
        
        response_str = str(response).strip()
        print(f"   -> Raw response: '{response_str}'")
        
        # Basic parsing - split by numbered lines
        facts = []
        lines = response_str.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('-')):
                # Clean up the fact text
                fact_text = line[2:].strip() if line.startswith(('1.', '2.', '3.')) else line[1:].strip()
                if fact_text:
                    facts.append(fact_text)
        
        print(f"   ✅ Extractor found {len(facts)} potential facts.")
        return facts
        
    except Exception as e:
        print(f"   ❌ Extractor Agent failed: {e}")
        return []

def _validate_fact(model: 'lms.Model', source_text: str, potential_fact: str) -> bool:
    """Agent 2: Simple prompting validation approach."""
    try:
        # Simple yes/no validation prompt
        validation_prompt = f"""Is this statement a verbatim quote from the source text?

Source text:
{source_text}

Statement to check:
{potential_fact}

Answer with just YES or NO:"""
        
        response = model.respond(
            validation_prompt,
            config={"temperature": 0.0, "max_tokens": 10}
        )
        
        response_str = str(response).strip().upper()
        print(f"      -> Validation response: '{response_str}'")
        
        # Check if response contains YES
        is_valid = "YES" in response_str
        return is_valid
        
    except Exception as e:
        print(f"   ❌ Validator Agent failed for fact '{potential_fact}': {e}")
        return False

def _generate_narrative_summary(model: 'lms.Model', verified_facts: List[str]) -> str:
    """Agent 3: Constrained narrative generation using ONLY verified facts."""
    print("-> Running Narrative Weaver Agent...")
    if not verified_facts:
        print("   ⚠️ No verified facts to weave into a narrative.")
        return "No key events or facts were recorded in this session."
    
    fact_list_str = "\n".join(f"- {fact}" for fact in verified_facts)
    try:
        # Constrained narrative generation prompt
        narrative_prompt = f"""Create a brief summary using ONLY these facts. Do not add any information not mentioned in the facts:

Facts:
{fact_list_str}

Summary (using only the facts above):"""
        
        response = model.respond(
            narrative_prompt,
            config={"temperature": 0.2, "max_tokens": 100}
        )
        
        summary_text = str(response).strip()
        print(f"   ✅ Narrative Weaver generated summary: '{summary_text}'")
        return summary_text
        
    except Exception as e:
        print(f"   ❌ Narrative Weaver Agent failed: {e}")
        return "Failed to generate a narrative summary for this session."

# --- Utility Functions ---
def _archive_log_file():
    """Archives the current log file by renaming it with a timestamp."""
    if not os.path.exists(LOG_FILE_PATH):
        print(f"   ⚠️ Log file not found at '{LOG_FILE_PATH}'. Nothing to archive.")
        return
    
    archive_dir = "./archive"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(archive_dir, f"raw_log_{timestamp}.txt")
    
    try:
        os.rename(LOG_FILE_PATH, archive_path)
        print(f"   ✅ Archived log file to '{archive_path}'")
    except OSError as e:
        print(f"   ❌ Failed to archive log file: {e}")

# --- Main Consolidation Function ---
def run_consolidation_pipeline(client: 'lms.Client', memory_manager: 'MemoryManager', model_handle=None):
    """The main function to run the entire memory consolidation pipeline."""
    print("\n--- Starting Memory Consolidation Pipeline (Sleep Cycle) ---")
    
    print(f"-> Reading log file from '{LOG_FILE_PATH}'...")
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            log_content = f.read()
        if not log_content.strip():
            print("   ✅ Log file is empty. No consolidation needed.")
            return
        print("   ✅ Log file read successfully.")
    except FileNotFoundError:
        print("   ✅ No log file found. No consolidation needed.")
        return

    # Use provided model handle or get first loaded model
    if model_handle:
        model = model_handle
        print(f"-> Using provided model handle: {model.identifier}")
    else:
        loaded_models = client.llm.list_loaded()
        if not loaded_models:
            print("   ❌ No LLM models are loaded. Cannot run consolidation.")
            return
        
        model = loaded_models[0]  # Use the first loaded model
        print(f"-> Using first loaded model: {model.identifier}")
    
    potential_facts = _extract_facts(model, log_content)
    
    verified_facts = []
    if potential_facts:
        print("\n-> Running Validation Pipeline...")
        for i, fact in enumerate(potential_facts, 1):
            print(f"   -> Validating fact {i}/{len(potential_facts)}: '{fact}'")
            time.sleep(0.5)
            if _validate_fact(model, source_text=log_content, potential_fact=fact):
                verified_facts.append(fact)
                print(f"      ✅ Fact VERIFIED.")
            else:
                print(f"      ❌ Fact REJECTED.")
    
    narrative_summary = _generate_narrative_summary(model, verified_facts)

    print("\n-> Storing consolidated memories in ChromaDB...")
    timestamp = datetime.now().isoformat()
    if verified_facts:
        for fact_text in verified_facts:
            memory_manager.add_memory(
                text=fact_text,
                doc_id=str(uuid.uuid4()),
                metadata={"type": "fact", "source": "consolidation", "timestamp": timestamp}
            )
    
    memory_manager.add_memory(
        text=narrative_summary,
        doc_id=str(uuid.uuid4()),
        metadata={"type": "summary", "source": "consolidation", "timestamp": timestamp}
    )
    
    print("\n-> Archiving processed log file...")
    _archive_log_file()
    
    print("\n--- ✅ Memory Consolidation Pipeline Complete ---")

# --- Main Execution Block for Standalone Script ---
if __name__ == "__main__":
    print("--- Running Standalone Memory Consolidation Script ---")
    
    client = None
    try:
        # This script now manages its own connection and resources.
        print("\n[Setup] Connecting to LM Studio...")
        client = lms.Client()
        
        print("-> Loading necessary models...")
        # Load and verify LLM model
        llm_model = client.llm.model(LLM_MODEL_IDENTIFIER)
        print(f"   -> LLM model '{llm_model.identifier}' loaded.")
        
        # Verify LLM is actually loaded
        loaded_llms = client.llm.list_loaded()
        if not loaded_llms:
            print("   -> LLM model not detected as loaded, forcing reload...")
            llm_model = client.llm.load_new_instance(LLM_MODEL_IDENTIFIER, config={"gpu_offload": "max"})
            print(f"   -> LLM model '{llm_model.identifier}' force-loaded.")
        
        # Load embedding model
        embedding_model = client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
        print(f"   -> Embedding model '{EMBEDDING_MODEL_IDENTIFIER}' loaded.")
        print("   ✅ Models loaded.")

        # Store the actual loaded model handle for later use
        stored_llm_model = llm_model
        
        # Keep reference to loaded models to prevent unloading
        memory_manager = MemoryManager(client=client)
        
        # Verify models are still loaded after MemoryManager init
        loaded_llms = client.llm.list_loaded()
        print(f"   -> LLM models loaded after MemoryManager init: {len(loaded_llms)}")
        
        if not loaded_llms:
            print("   -> Re-loading LLM model after MemoryManager init...")
            llm_model = client.llm.load_new_instance(LLM_MODEL_IDENTIFIER, config={"gpu_offload": "max"})
            print(f"   -> LLM model '{llm_model.identifier}' re-loaded.")
        
        print("   ✅ Memory Manager initialized.")
        
        run_consolidation_pipeline(client=client, memory_manager=memory_manager, model_handle=stored_llm_model)

    except Exception as e:
        print(f"\n--- ❌ A critical error occurred: {e} ---", file=sys.stderr)
    finally:
        # Ensure all resources are cleaned up cleanly.
        if client:
            print("\n[Cleanup] Unloading all models...")
            for model in client.llm.list_loaded():
                model.unload()
            for model in client.embedding.list_loaded():
                model.unload()
            print("   ✅ All models unloaded.")
        print("\n--- Standalone Script Finished ---")
