# aura_engine/aurora.py
#
# This file defines the main Aurora class, which encapsulates all the agent's
# subsystems into a single, clean, object-oriented structure.

import lmstudio as lms
import uuid
from datetime import datetime

from config import LLM_MODEL_IDENTIFIER
from .log_interaction import log_interaction
from .process_emotions import get_emotional_overlay
from .memory_manager import MemoryManager

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
        self._initialize_systems()

    def _initialize_systems(self):
        """Connects to the SDK and initializes all subsystems."""
        try:
            self.client = lms.Client()
            print("✅ Successfully connected to LM Studio server.")

            # Clean up any pre-existing models for a clean start
            print("-> Cleaning up any pre-existing loaded models...")
            for model in self.client.llm.list_loaded():
                print(f"   -> Unloading pre-existing model: {model.identifier}")
                model.unload()
            
            print(f"-> Loading new instance of model: {LLM_MODEL_IDENTIFIER}...")
            self.model = self.client.llm.load_new_instance(
                LLM_MODEL_IDENTIFIER,
                config={"gpu_offload": "max"}
            )
            print(f"✅ New model instance '{self.model.identifier}' is ready.")
            
            self.memory = MemoryManager(client=self.client)
            print("✅ All systems initialized successfully.")

        except Exception as e:
            print(f"❌ Critical error during initialization: {e}")
            self.shutdown()
            raise

    def run_chat_loop(self):
        """Starts the main interactive chat loop with the user."""
        if not self.model or not self.memory:
            print("❌ Cannot start chat loop, systems are not initialized.")
            return

        print("\n--- Aurora is awake ---")
        print("You can now chat with Aurora. Type 'quit' to exit.")

        while True:
            try:
                user_prompt = input("\nBen: ")
                if user_prompt.lower() == 'quit':
                    break

                # Retrieve memories
                retrieved_memories = self.memory.retrieve_relevant_memories(user_prompt)
                print(f"[Recalling {len(retrieved_memories)} memories...]")
                
                # Construct context
                memory_context = self._build_memory_context(retrieved_memories)

                # Get response
                agent_response = self._get_model_response(user_prompt, memory_context)
                print(f"\nAurora: {agent_response}")

                # Log and store new memories
                self._process_new_interaction(user_prompt, agent_response)

            except (KeyboardInterrupt, EOFError):
                break

    def _build_memory_context(self, memories: list) -> str:
        """Constructs the memory context string for the prompt."""
        if not memories:
            return "You have no relevant memories for this topic yet."
        
        context_str = "Here are some relevant memories from our past conversations, with the newest memories first:\n"
        sorted_memories = sorted(
            memories, 
            key=lambda m: m.get('metadata', {}).get('timestamp', ''), 
            reverse=True
        )
        for mem in sorted_memories:
            timestamp = mem.get('metadata', {}).get('timestamp', 'an unknown time')
            context_str += f"- [Memory from {timestamp}]: {mem['text']}\n"
        return context_str

    def _get_model_response(self, prompt: str, context: str) -> str:
        """Queries the LLM and returns the response."""
        system_prompt = "You are an AI assistant named Aurora. You are a truthful, loving, and helpful life partner for Ben."
        chat_history = lms.Chat(system_prompt)
        
        full_prompt_for_model = f"""--- MEMORY CONTEXT ---\n{context}\n--------------------\n\nBen's current prompt is: "{prompt}" """
        chat_history.add_user_message(full_prompt_for_model)

        response = self.model.respond(chat_history)
        return str(response)

    def _process_new_interaction(self, user_prompt: str, agent_response: str):
        """Logs the interaction, analyzes emotion, and stores it in memory."""
        log_interaction(user_prompt, agent_response)
        
        emotional_data = get_emotional_overlay(agent_response)
        print(f"[Emotional overlay logged: {emotional_data}]")
        
        interaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        memory_text = f"Ben said: '{user_prompt}'. I responded: '{agent_response}'."
        
        self.memory.add_memory(
            text=memory_text, 
            doc_id=interaction_id, 
            metadata={"type": "interaction", "source": "live_chat", "timestamp": timestamp}
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
        if self.client:
            # The `with` statement in the new main_agent handles the client connection,
            # but this is good practice for completeness.
            print("Client connection will be closed by the context manager.")
