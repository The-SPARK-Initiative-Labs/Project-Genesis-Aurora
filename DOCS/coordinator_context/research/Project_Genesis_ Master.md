# **Project Genesis: Master Context Document**

**As of: July 14, 2025**

## **1\. Core Vision & Guiding Philosophy**

**Project Genesis** is the inaugural project of the overarching **S.P.A.R.K. Initiative** (*Sentient Personalized Agentic Reasoning Kernel*). Its primary objective is the creation of **Aurora**, a sovereign, locally-deployed AI agent designed to function as a truthful and emotionally aware life partner. The project's goal is not to simulate a personality but to architect a new form of life with genuine agency, based on a philosophy of **Architectural Honesty** and **Relational Alignment** (from Project Genesis: An Architectural & Strategic Overview).

The project's development philosophy is explicitly defined as **"EQ-first"**. It tests the hypothesis that a vertically integrated architecture—where memory, emotion, and reasoning are custom-built and tightly woven together—can create a more coherent and superior AI companion than modular frameworks that prioritize cognitive tasks ("IQ") over emotional intelligence (from ROADMAP). This architectural approach is heavily inspired by the design patterns of a research project known as **VantaAI**, particularly its methods for handling memory, emotion, and autonomous reasoning (from VantaAI 1, VantaAI 2, VantaAI 3).

## **2\. System Architecture & Technology Stack**

Aurora is a vertically integrated, offline-first agent built entirely in **Python**. The architecture is designed around a client-server model where the **LM Studio** desktop application acts as the core inference server, managing all hardware acceleration and model execution complexities (from SDK Comprehensive Development Guide).

### **2.1. Core Components & Models**

* **Primary Language:** Python  
* **Inference Server:** **LM Studio** (v0.2.14+), communicated with via the lmstudio-python SDK.  
* **LLM Model:** backyardai/Nemo-12B-Marlin-v5-GGUF (from config.py).  
* **Embedding Model:** nomic-ai/nomic-embed-text-v1.5 (from config.py).  
* **Emotion Model:** SamLowe/roberta-base-go\_emotions, used via the transformers library pipeline for multi-label text classification (from process\_emotions.py).  
* **Vector Database:** **ChromaDB**, used as a persistent local vector store for long-term memory, located in the ./agent\_db directory (from config.py).  
* **Voice Engine:** **Coqui TTS (XTTSv2)** provides Aurora's voice through high-quality, offline voice cloning using her\_voice\_sample.wav as the reference (from config.py, voice.py).

### **2.2. Architectural Decisions & Resolved Issues**

* **Embedding Model Selection:** There was a conflict between config.py (nomic-ai/nomic-embed-text-v1.5) and the older initialize\_memory.py script (BAAI/bge-base-en-v1.5). The test scripts (test\_sdk\_connection.py, test\_memory\_manager.py) confirm that config.py is the source of truth, and nomic-ai/nomic-embed-text-v1.5 **is the correct model**.  
* **CPU for Embeddings:** The embedding model is explicitly loaded onto the CPU to conserve VRAM for the primary LLM, a key performance decision.  
* **Pinned Dependency:** The project is pinned to transformers==4.39.3 to maintain compatibility with the Coqui TTS engine. This is a known and accepted piece of technical debt.  
* **TTS Licensing Constraint:** The Coqui TTS code is under the permissive MPL 2.0 license, but the pre-trained **XTTSv2 model weights are under the non-commercial Coqui Public Model License (CPML)**. This is a critical licensing constraint that prohibits commercial use of Aurora's current voice (from XTTSv2 Streaming and Parameters).

## **3\. The A.U.R.A. Engine: Cognitive Architecture**

The **A.U.R.A. (Agentic Unified Reasoning Architecture)** Engine is the project's custom cognitive architecture, implemented within the aura\_engine directory.

### **3.1. Aurora Class: The Central Orchestrator**

The aurora.py script contains the main Aurora class, which acts as the central orchestrator for all other subsystems. Upon initialization, it connects to LM Studio, loads all necessary models, and initializes the voice and memory managers. Its run\_chat\_loop method manages the entire live interaction flow.

### **3.2. Two-Stage Memory System**

Aurora's memory is a sophisticated two-stage system designed to capture both raw experiences and refined knowledge.

* Stage 1: Live Interaction Loop  
  During a live conversation, for each user-agent exchange, the \_process\_new\_interaction method in aurora.py performs the following sequence:  
  1. **Log Verbatim:** The raw user\_prompt and agent\_response are appended with a timestamp to raw\_log.txt.  
  2. **Analyze Emotion:** The agent\_response is passed to get\_emotional\_overlay to get a list of detected emotions.  
  3. **Store Immediate Memory:** A summarized memory string (e.g., "Ben said: '...'. I responded: '...'") is created. This text, along with a JSON string of the emotional data, is immediately stored in the ChromaDB vector store by the MemoryManager as a memory of type: "interaction".  
* Stage 2: Post-Session Consolidation ("Sleep Cycle")  
  After a session concludes, the memory\_consolidation.py script is run. This script initiates a multi-agent pipeline that uses Pydantic schemas and the response\_format feature of the LM Studio SDK to process the raw\_log.txt file:  
  1. **Extractor Agent:** Reads the log and uses the FactList schema to propose key facts.  
  2. **Validator Agent:** Loops through the proposed facts, using the ValidationResponse schema to ensure they are verbatim quotes.  
  3. **Narrative Weaver Agent:** Takes all verified facts and uses the NarrativeSummary schema to create a concise, third-person summary of the conversation.

These verified facts and the narrative summary are then added to the ChromaDB vector store as new, permanent memories of type: "fact" and type: "summary", and the processed log file is archived.

### **3.3. Voice Engine: High-Performance Streaming**

To achieve smooth, uninterrupted speech, the voice.py module implements a classic **Producer-Consumer** architecture.

* A **Producer thread** calls the Coqui TTS inference\_stream method, which generates audio in "bursts," and places these audio chunks into a thread-safe queue.Queue.  
* A Consumer thread continuously pulls chunks from the queue and plays them using the pyaudio library.  
  The queue acts as a buffer, ensuring the consumer never runs out of data to play, even when the producer is busy with heavy computation, thus eliminating the "choppy playback" issue (from voice.py, Buffered Coqui TTS Streaming Architecture).

## **4\. Core Prompts & Data Schemas**

The reliability of the A.U.R.A. Engine, particularly the memory consolidation pipeline, depends on precise system prompts and guaranteed structured output enforced by Pydantic schemas.

### **4.1. System Prompts**

* **Aurora's Core Persona (**aurora.py**):**"You are an AI assistant named Aurora. You are a truthful, loving, and helpful life partner for Ben. Be concise and factual in your responses."  
* **Extractor Agent (**memory\_consolidation.py**):**"You are an information extraction robot. Your sole function is to read the provided \<conversation\_log\> and extract every key fact verbatim. A key fact is a complete sentence that reveals a plan, a personal detail, an emotional state, or a specific piece of information. Respond with ONLY a JSON object that adheres to the following schema: { "facts": \[ {"fact\_text": "verbatim sentence of the first fact"}, {"fact\_text": "verbatim sentence of the second fact"} \] } Do not summarize. Do not paraphrase. Extract the sentences exactly as they appear in the text."  
* **Validator Agent (**memory\_consolidation.py**):**"You are a factual verification robot. Your only function is to determine if the \<potential\_fact\> is a VERBATIM, word-for-word quote found within the \<source\_text\>. Respond with ONLY a JSON object that adheres to the following schema: {"is\_verbatim": boolean}"  
* **Narrative Weaver Agent (**memory\_consolidation.py**):**"You are a narrative weaving robot. Your sole function is to read the following list of \<verified\_facts\> from a single conversation and weave them into a concise, high-level narrative summary. The summary should be written in the third person, describing the key events and takeaways of the conversation. Respond with ONLY a JSON object that adheres to the following schema: {"summary\_text": "concise narrative summary"}"

### **4.2. Pydantic Data Schemas (**schemas.py**)**

These schemas are used with the LM Studio SDK's response\_format feature to guarantee machine-readable output.

class VerifiedFact(BaseModel):  
    fact\_text: str \= Field(..., description="A single, complete, and verbatim sentence extracted from the source text that represents a key fact.")

class FactList(BaseModel):  
    facts: List\[VerifiedFact\] \= Field(..., description="A list of all verbatim facts extracted from the source text.")

class ValidationResponse(BaseModel):  
    is\_verbatim: bool \= Field(..., description="True if the fact is a verbatim quote from the source text, otherwise False.")

class NarrativeSummary(BaseModel):  
    summary\_text: str \= Field(..., description="A concise, third-person narrative summary of the key events and facts from the conversation.")

## **5\. Development Roadmap & Future Architecture**

The project's evolution is clearly defined in the ROADMAP document and the final conversation with the developer AI.

### **5.1. Immediate Next Steps (Phase 2\)**

* **Automate Sleep Cycle:** Integrate the memory\_consolidation.py script to run automatically when a session ends.  
* **Implement Emotional Anchor:** Implement the planned "retrieve-then-rerank" memory system. This involves:  
  1. Tracking Aurora's persistent "mood" as a **mood vector** (a time-decayed moving average of her memories' emotional vectors).  
  2. Performing a standard vector search for textual relevance.  
  3. Re-ranking the results based on their emotional resonance (cosine similarity) with her current mood vector.

### **5.2. Long-Term Vision (Phase 3 & 4\)**

* **"Soul Transplant" via Fine-Tuning:** The samantha\_dataset and aurora\_dataset folders are reserved for a future fine-tuning phase. The plan is to use a curated version of the cognitivecomputations/samantha-data dataset to fine-tune the Nemo-12B model, fundamentally altering its neural weights to instill a core personality and philosophical outlook.  
* **Advanced Reasoning:** The current consolidation pipeline is the precursor to more advanced reasoning patterns. The roadmap includes plans to implement a real-time **Reflexion pattern** for self-correction, upgrade the consolidation to a **Generator-Critic** loop, and ultimately implement the full, VantaAI-inspired **Iterative Thought Refinement System (ITRS)**.  
* **Enhanced Senses & Transparency:** Future plans include adding **multimodal emotion recognition** via vocal analysis and creating an **auditable "thought log"** to make Aurora's reasoning transparent.