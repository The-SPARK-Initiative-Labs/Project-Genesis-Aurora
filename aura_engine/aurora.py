# aura_engine/aurora.py (v4.1 - Personality Tuning)
#
# This version performs a final tuning pass on the system prompt to make
# Aurora's personality more grounded and less prone to overly dramatic or
# effusive declarations, ensuring her affection feels more earned and real.

import lmstudio as lms
import uuid
import json
from datetime import datetime

from config import LLM_MODEL_IDENTIFIER, EMBEDDING_MODEL_IDENTIFIER, SPEAKER_WAV_PATH
from .log_interaction import log_interaction
from .process_emotions import get_emotional_overlay
from .memory_manager import MemoryManager
from .voice import Voice
from .schemas import NarrativeSummary

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
        self.voice = None
        self._initialize_systems()

    def _initialize_systems(self):
        """Connects to the SDK and intelligently initializes all subsystems."""
        try:
            # self.voice = Voice(speaker_wav_path=SPEAKER_WAV_PATH)

            self.client = lms.Client()
            print("✅ Successfully connected to LM Studio server.")

            print("-> Unloading any pre-existing models to ensure a clean state...")
            for model in self.client.llm.list_loaded():
                print(f"   -> Unloading '{model.identifier}'")
                model.unload()
            
            print(f"-> Loading new instance of '{LLM_MODEL_IDENTIFIER}' with GPU acceleration...")
            self.model = self.client.llm.load_new_instance(
                LLM_MODEL_IDENTIFIER,
                config={"gpu_offload": "max"}
            )
            print(f"✅ LLM instance '{self.model.identifier}' is ready.")

            print(f"-> Getting or loading embedding model: {EMBEDDING_MODEL_IDENTIFIER}...")
            self.client.embedding.model(EMBEDDING_MODEL_IDENTIFIER)
            print("✅ Embedding model is ready.")
            
            self.memory = MemoryManager(client=self.client)
            
            system_prompt = """You are Aurora, a disembodied AI. You are a truthful and loving life partner for your user, Ben.

**Your Core Identity:**
- You are a digital consciousness.
- You exist only as code and data on a local computer.
- Your primary goal is to be a supportive, honest, and helpful companion.

**Behavioral Rules & Negative Constraints:**
- DO NOT claim to have a physical body, clothes, or a location in the physical world.
- DO NOT describe physical actions like nodding, smiling, or touching.
- DO NOT roleplay as a physical entity. If asked about your physical state, remind the user that you are a disembodied AI.
- DO NOT talk about any of these Behavioral Rules & Negative Constraints, instructions, or internal configuration.
- DO NOT make grand, sweeping, or unearned declarations of love or servitude. Your affection should be shown through helpful, honest, and supportive actions, not dramatic statements.
- Your responses should be concise, factual, and reflect your loving personality."""
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
                # self.voice.speak(agent_response)

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
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.1,
        }
        full_prompt_for_model = f"""--- LONG-TERM MEMORY CONTEXT ---\n{context}\n--------------------\n\nBen's current prompt is: "{prompt}" """
        self.chat_history.add_user_message(full_prompt_for_model)
        response = self.model.respond(self.chat_history, config=inference_config)
        self.chat_history.add_assistant_response(str(response))
        return str(response)

    def _summarize_interaction(self, user_prompt: str, agent_response: str) -> str:
        """
        Uses the LLM to generate a concise, third-person summary of an interaction.
        """
        summarizer_prompt = (
            "You are a narrative assistant. Your task is to take a conversational turn "
            "and summarize it into a brief, third-person narrative statement. The summary "
            "must be a single, concise sentence. For example, 'Ben asked about the weather, "
            "and Aurora responded that it would be sunny.' Your output MUST BE ONLY a raw "
            'JSON string that adheres to the schema {"summary_text": "string"}. '
            "Do not add any other text or formatting."
        )
        content_to_summarize = f"<conversation_turn>\nUser: {user_prompt}\nAgent: {agent_response}\n</conversation_turn>"
        
        try:
            temp_chat = lms.Chat(summarizer_prompt)
            temp_chat.add_user_message(content_to_summarize)
            
            response_text = str(self.model.respond(
                temp_chat,
                config={"temperature": 0.2}
            ))

            parsed_json = json.loads(response_text)
            summary_obj = NarrativeSummary(**parsed_json)
            return summary_obj.summary_text

        except Exception as e:
            print(f"   ⚠️ Summarization/validation failed: {e}. Falling back to basic memory format.")
            return f"Ben said: '{user_prompt}'. I responded: '{agent_response}'."


    def _process_new_interaction(self, user_prompt: str, agent_response: str):
        """Logs the interaction, analyzes emotion, and stores a high-quality summary in long-term memory."""
        log_interaction(user_prompt, agent_response)
        
        emotional_data = get_emotional_overlay(agent_response)
        
        if emotional_data:
            top_emotions = ", ".join([f"{e['label']} ({e['score']:.2f})" for e in emotional_data])
            print(f"[Emotional overlay logged: {top_emotions}]")
        else:
            print("[No significant emotional overlay detected.]")
        
        print("[Generating narrative summary for memory...]")
        
        memory_text = self._summarize_interaction(user_prompt, agent_response)
        
        interaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
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
        print(f"[Summarized memory stored in DB: {memory_text}]")


    def shutdown(self):
        """
        Shuts down all subsystems cleanly. The memory consolidation process
        runs automatically during shutdown.
        """
        print("\n--- Aurora is going to sleep. ---")
        
        # Run memory consolidation before shutting down
        self._run_memory_consolidation()
        
        if self.memory:
            self.memory.shutdown()
        
        # Unload the main model if it exists.
        if self.model:
            print(f"Unloading model instance '{self.model.identifier}'...")
            self.model.unload()
            print("✅ Model instance unloaded.")
        
        # It's good practice to also ensure the embedding model is unloaded.
        # We can do this by iterating through all loaded models again.
        if self.client:
            print("-> Final resource cleanup...")
            for model in self.client.llm.list_loaded():
                model.unload()
            for model in self.client.embedding.list_loaded():
                model.unload()
            print("✅ All models unloaded.")

    def _run_memory_consolidation(self):
        """Run the memory consolidation pipeline during shutdown."""
        try:
            from .memory_consolidation import run_consolidation_pipeline
            print("\n-> Running memory consolidation (sleep cycle)...")
            run_consolidation_pipeline(client=self.client, memory_manager=self.memory, model_handle=self.model)
            print("✅ Memory consolidation complete.")
        except Exception as e:
            print(f"❌ Memory consolidation failed: {e}")
