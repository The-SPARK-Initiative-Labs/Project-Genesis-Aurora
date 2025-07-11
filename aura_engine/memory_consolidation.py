# aura_engine/memory_consolidation.py (v2.4 - Restored & Corrected)
#
# This version RESTORES the use of the `response_format` parameter for all
# agent calls. This leverages the SDK's guaranteed structured output feature,
# which is more robust than manual parsing. This is the correct, architecturally
# sound implementation.

import lmstudio as lms
import os
import sys
import time
import uuid
from datetime import datetime
from typing import List

# Import our custom schemas and configuration
from config import LLM_MODEL_IDENTIFIER, LOG_FILE_PATH
from aura_engine.schemas import FactList, ValidationResponse, NarrativeSummary
from aura_engine.memory_manager import MemoryManager

# --- Prompt Templates ---
# NOTE: To save space, the long prompt strings are omitted here, but they are the same as before.
EXTRACTOR_PROMPT = """You are an information extraction robot. Your sole function is to read the provided <conversation_log> and extract every key fact verbatim. A key fact is a complete sentence that reveals a plan, a personal detail, an emotional state, or a specific piece of information. Respond with ONLY a JSON object that adheres to the following schema: { "facts": [ {"fact_text": "verbatim sentence of the first fact"}, {"fact_text": "verbatim sentence of the second fact"} ] } Do not summarize. Do not paraphrase. Extract the sentences exactly as they appear in the text. <conversation_log>{text_content}</conversation_log>"""
VALIDATOR_PROMPT = """You are a factual verification robot. Your only function is to determine if the <potential_fact> is a VERBATIM, word-for-word quote found within the <source_text>. Respond with ONLY a JSON object that adheres to the following schema: {"is_verbatim": boolean} <source_text>{source_text}</source_text> <potential_fact>{potential_fact}</potential_fact>"""
NARRATIVE_WEAVER_PROMPT = """You are a narrative weaving robot. Your sole function is to read the following list of <verified_facts> from a single conversation and weave them into a concise, high-level narrative summary. The summary should be written in the third person, describing the key events and takeaways of the conversation. Respond with ONLY a JSON object that adheres to the following schema: {"summary_text": "concise narrative summary"} <verified_facts>{fact_list}</verified_facts>"""

# --- Agent Functions ---
def extract_facts(model: 'lms.Model', text_content: str) -> List[str]:
    """Agent 1: Extracts potential facts from the text using a Pydantic schema."""
    print("-> Running Extractor Agent...")
    try:
        response = model.respond(
            EXTRACTOR_PROMPT.format(text_content=text_content),
            response_format=FactList, # RESTORED: Use the SDK's guaranteed structured output
            config={"temperature": 0.0}
        )
        fact_list_obj = response.parsed
        extracted_facts = [fact.fact_text for fact in fact_list_obj.facts]
        print(f"   ✅ Extractor found and validated {len(extracted_facts)} potential facts.")
        return extracted_facts
    except Exception as e:
        print(f"   ❌ Extractor Agent failed: {e}")
        return []

def validate_fact(model: 'lms.Model', source_text: str, potential_fact: str) -> bool:
    """Agent 2: Validates that a potential fact is a verbatim quote."""
    try:
        response = model.respond(
            VALIDATOR_PROMPT.format(source_text=source_text, potential_fact=potential_fact),
            response_format=ValidationResponse, # RESTORED
            config={"temperature": 0.0}
        )
        validation_obj = response.parsed
        return validation_obj.is_verbatim
    except Exception as e:
        print(f"   ❌ Validator Agent failed for fact '{potential_fact}': {e}")
        return False

def generate_narrative_summary(model: 'lms.Model', verified_facts: List[str]) -> str:
    """Agent 3: Weaves verified facts into a narrative summary."""
    print("-> Running Narrative Weaver Agent...")
    if not verified_facts:
        print("   ⚠️ No verified facts to weave into a narrative.")
        return "No key events or facts were recorded in this session."
    
    fact_list_str = "\n".join(f"- {fact}" for fact in verified_facts)
    try:
        response = model.respond(
            NARRATIVE_WEAVER_PROMPT.format(fact_list=fact_list_str),
            response_format=NarrativeSummary, # RESTORED
            config={"temperature": 0.5}
        )
        summary_obj = response.parsed
        print(f"   ✅ Narrative Weaver generated summary: '{summary_obj.summary_text}'")
        return summary_obj.summary_text
    except Exception as e:
        print(f"   ❌ Narrative Weaver Agent failed: {e}")
        return "Failed to generate a narrative summary for this session."

# --- Utility Functions ---
def archive_log_file():
    """Archives the current log file by renaming it with a timestamp."""
    if not os.path.exists(LOG_FILE_PATH):
        print(f"   ⚠️ Log file not found at '{LOG_FILE_PATH}'. Nothing to archive.")
        return
    
    archive_dir = "./archive"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(archive_dir, f"raw_log_{timestamp}.txt")
    
    os.rename(LOG_FILE_PATH, archive_path)
    print(f"   ✅ Archived log file to '{archive_path}'")

# --- Main Consolidation Function ---
def consolidate_memory_from_log(client: 'lms.Client', memory_manager: 'MemoryManager'):
    """The main function to run the entire memory consolidation pipeline."""
    print("\n--- Starting Memory Consolidation Pipeline ---")
    
    print(f"-> Reading log file from '{LOG_FILE_PATH}'...")
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            log_content = f.read()
        if not log_content.strip():
            print("   ✅ Log file is empty. No consolidation needed.")
            return
        print("   ✅ Log file read successfully.")
    except FileNotFoundError:
        print("   ❌ No log file found. No consolidation needed.")
        return

    model = client.llm.model(LLM_MODEL_IDENTIFIER)
    print(f"-> Acquired handle for model: {model.identifier}")
    
    potential_facts = extract_facts(model, log_content)
    
    verified_facts = []
    if potential_facts:
        print("\n-> Running Validation Pipeline...")
        for i, fact in enumerate(potential_facts, 1):
            print(f"   -> Validating fact {i}/{len(potential_facts)}: '{fact}'")
            time.sleep(1)
            if validate_fact(model, source_text=log_content, potential_fact=fact):
                verified_facts.append(fact)
                print(f"      ✅ Fact VERIFIED.")
            else:
                print(f"      ❌ Fact REJECTED.")
    
    narrative_summary = generate_narrative_summary(model, verified_facts)

    print("\n-> Storing memories in ChromaDB...")
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
    archive_log_file()
    
    print("\n--- ✅ Memory Consolidation Pipeline Complete ---")

# --- Test Block ---
if __name__ == "__main__":
    print("--- Running Direct Test of Memory Consolidation Module ---")
    
    print("\n[Setup] Creating dummy log file...")
    dummy_log_content = """Ben: Morning. My sister Sarah's birthday is next Tuesday. Aurora: We should remember that. Ben: For this weekend, we absolutely have to make the garden project the top priority. Aurora: I agree. Ben: I'm also feeling pretty stressed about that big presentation at work."""
    with open(LOG_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(dummy_log_content)
    print("   ✅ Dummy log file created.")

    try:
        print("\n[Setup] Connecting to LM Studio and initializing Memory Manager...")
        with lms.Client() as client:
            test_memory_manager = MemoryManager(client=client)
            print("   ✅ Client and Memory Manager initialized.")
            
            consolidate_memory_from_log(client=client, memory_manager=test_memory_manager)
            
            print("\n--- Verifying Test Results in ChromaDB ---")
            retrieved_summaries = test_memory_manager.collection.get(where={"type": "summary"})
            print(f"-> Retrieved Summaries: {retrieved_summaries['documents']}")
            assert len(retrieved_summaries['documents']) > 0, "❌ FAILURE: Narrative summary was not stored."

            retrieved_facts = test_memory_manager.collection.get(where={"type": "fact"})
            print(f"-> Retrieved Facts: {retrieved_facts['documents']}")
            assert len(retrieved_facts['documents']) >= 2, "❌ FAILURE: Not enough verified facts were stored."
            
            print("\n--- ✅ Direct test of module completed successfully. ---")

    except Exception as e:
        print(f"\n--- ❌ A critical error occurred in the main test block: {e} ---", file=sys.stderr)
