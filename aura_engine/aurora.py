# aura_engine/aurora.py (v1.8 - Final Fixes)
#
# This is the final, complete version of the Aurora class. It integrates
# the voice engine and includes the missing `import json` statement.

import lmstudio as lms
import uuid
import json # DEFINITIVE FIX: Added missing import for JSON serialization
from datetime import datetime

from config import LLM_MODEL_IDENTIFIER, EMBEDDING_MODEL_IDENTIFIER, SPEAKER_WAV_PATH
from .log_interaction import log_interaction
from .process_emotions import get_emotional_overlay
from .memory_manager import MemoryManager
from .voice import Voice # Import the voice class

class Aurora:
    """
    The main class for the Aurora agent, managing her state and subsystems.
    """
    def __init__(self):
        """Initializes the Aurora agent and all her subsystems."""
        print("--- Aurora System Boot ---")
        self.client = None
        self.model = None
        self.memory = None
        self.chat_history = None
        self.voice = None # Add the voice attribute
        self._initialize_systems()

    def _initialize_systems(self):
        """Connects to the SDK and intelligently initializes all subsystems."""
        try:
            # Initialize Voice Engine first
            self.voice = Voice(speaker_wav_path=SPEAKER_WAV_PATH)

            self.client = lms.Client()
            print("✅ Successfully connected to LM Studio server.")

            print("-> Checking loaded LLM status...")
            loaded_llms = self.client.llm.list_loaded()
            model_is_loaded = any(LLM_MODEL_IDENTIFIER in m.identifier for m in loaded_llms)

            if model_is_loaded:
                print(f"   ✅ Target LLM '{LLM_MODEL_IDENTIFIER}' is already loaded.")
                self.model = self.client.llm.model(LLM_MODEL_IDENTIFIER)
            else:
                print("   -> Target LLM not found. Unloading any existing models...")
                for model in loaded_llms:
                    model.unload()
                
                print(f"   -> Loading new instance of '{LLM_MODEL_IDENTIFIER}' with GPU acceleration...")
                self.model = self.client.llm.load_new_instance(
                    LLM_MODEL_IDENTIFIER,
                    config={"gpu_offload": "max"}
                )
            print(f"✅ LLM instance '{self.model.identifier}' is ready.")

            print(f"-> Getting or loading embedding model: {EMBEDDING_MODEL_IDENTIFIER}...")
            self.client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
            print("✅ Embedding model is ready.")
            
            self.memory = MemoryManager(client=self.client)
            system_prompt = "You are an AI assistant named Aurora. You are a truthful, loving, and helpful life partner for Ben. Be concise and factual in your responses."
            self.chat_history = lms.Chat(system_prompt)
            
            print("✅ All systems initialized successfully.")

        except Exception as e:
            print(f"❌ Critical error during initialization: {e}")
            self.shutdown()
            raise

    def run_chat_loop(self):
        """Starts the main interactive chat loop with the user."""
        if not self.model or not self.memory or not self.chat_history:
            print("❌ Cannot start chat loop, systems are not initialized.")
            return

        print("\n--- Aurora is awake ---")
        print("You can now chat with Aurora. Type 'quit' to exit.")

        while True:
            try:
                user_prompt = input("\nBen: ")
                if user_prompt.lower() == 'quit':
                    break

                retrieved_memories = self.memory.retrieve_relevant_memories(user_prompt)
                print(f"[Recalling {len(retrieved_memories)} long-term memories...]")
                
                memory_context = self._build_memory_context(retrieved_memories)
                agent_response = self._get_model_response(user_prompt, memory_context)
                
                print(f"\nAurora: {agent_response}")
                self.voice.speak(agent_response)

                self._process_new_interaction(user_prompt, agent_response)

            except (KeyboardInterrupt, EOFError):
                break

    def _build_memory_context(self, memories: list) -> str:
        """Constructs the memory context string for the prompt."""
        if not memories:
            return "You have no relevant long-term memories for this topic yet."
        
        context_str = "Here are some relevant long-term memories from our past conversations:\n"
        for mem in memories:
            context_str += f"- {mem['text']}\n"
        return context_str

    def _get_model_response(self, prompt: str, context: str) -> str:
        """Queries the LLM with strict parameters and returns the response."""
        inference_config = {
            "temperature": 0.4,
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.1,
        }
        full_prompt_for_model = f"""--- LONG-TERM MEMORY CONTEXT ---\n{context}\n--------------------\n\nBen's current prompt is: "{prompt}" """
        self.chat_history.add_user_message(full_prompt_for_model)
        response = self.model.respond(self.chat_history, config=inference_config)
        self.chat_history.add_assistant_response(str(response))
        return str(response)

    def _process_new_interaction(self, user_prompt: str, agent_response: str):
        """Logs the interaction, analyzes emotion, and stores it in long-term memory."""
        log_interaction(user_prompt, agent_response)
        
        emotional_data = get_emotional_overlay(agent_response)
        
        if emotional_data:
            top_emotions = ", ".join([f"{e['label']} ({e['score']:.2f})" for e in emotional_data])
            print(f"[Emotional overlay logged: {top_emotions}]")
        else:
            print("[No significant emotional overlay detected.]")
        
        interaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        memory_text = f"Ben said: '{user_prompt}'. I responded: '{agent_response}'."
        
        emotions_json_string = json.dumps(emotional_data)
        
        memory_metadata = {
            "type": "interaction",
            "source": "live_chat",
            "timestamp": timestamp,
            "emotions": emotions_json_string
        }
        
        self.memory.add_memory(
            text=memory_text, 
            doc_id=interaction_id, 
            metadata=memory_metadata
        )

    def shutdown(self):
        """Shuts down all subsystems cleanly."""
        print("\n--- Aurora is going to sleep. ---")
        if self.memory:
            self.memory.shutdown()
        if self.model:
            print(f"Unloading model instance '{self.model.identifier}'...")
            self.model.unload()
            print("✅ Model instance unloaded.")
