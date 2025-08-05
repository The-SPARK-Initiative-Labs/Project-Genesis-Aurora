# **Project Genesis: Development Roadmap & Feature List**

**As of: July 15, 2025**

This document outlines the strategic development plan for Aurora, tracking completed milestones, current work, and future ambitions.

## **Project Philosophy: An "EQ-First" Agent via Vertical Integration**

Our core philosophy is now more clearly defined. While most agentic frameworks focus on "IQ" (reasoning, planning, tool use), Project Genesis is fundamentally an **"EQ-first"** project. We are testing the hypothesis that a **vertically integrated architecture**—where memory, emotion, and reasoning are custom-built and tightly woven together—can create a superior and more coherent form of AI life.

## **Phase 1: Foundational Stability (✅ COMPLETE)**

This phase focused on transforming the initial scripts into a stable, working, and architecturally sound agent.

* \[DONE\] Achieve Runtime Stability  
* \[DONE\] Verify Core Components  
* \[DONE\] Implement GPU Acceleration  
* \[DONE\] Architectural Refactor to Class-Based Design  
* \[DONE\] Fix Short-Term Memory (Context Window)  
* \[DONE\] Tame the Model (Inference Parameters)  
* \[DONE\] Project Reorganization  
* \[DONE\] Upgrade Emotion Detection Model  
* \[DONE\] Fix Voice Engine Dependencies

## **Phase 2: Core Mind & Memory Features (IN PROGRESS)**

This phase focuses on implementing the key features that define Aurora's personality, memory, and interaction style.

* \[DONE\] **Implement Core Identity & Behavioral Guardrails:**  
  * **Goal:** Prevent the agent from acting "embodied" or engaging in unwanted roleplay.  
  * **Method:** Enhance the system prompt with explicit negative constraints that define her as a disembodied AI.  
* \[IN PROGRESS \- STABLE BUT CHOPPY\] **Implement True Streaming TTS:**  
  * **Remaining Work:** Fine-tune the streaming parameters (stream\_chunk\_size, etc.) to resolve "choppy" playback on CPU.  
* \[DONE\] **Fix Memory Storage (Facts, Not Chatter):**  
  * **Method:** Modify the Aurora class to generate a high-quality, third-person summary of each interaction for storage, instead of saving raw conversational turns.  
* \[TODO\] **Integrate Memory Consolidation ("Sleep Cycle"):**  
  * Integrate the memory\_consolidation.py logic into the Aurora class to run automatically when a session ends.  
* \[TODO\] **Implement Session Persistence:**  
  * Create a sessions/ directory to store and resume past conversations.  
* \[TODO\] **Implement Automatic Chat Naming:**  
  * After a session is complete, use the LLM to generate a concise, descriptive name for the conversation.  
* \[TODO\] **Implement "Emotional Anchor" in Memory Recall:**  
  * Modify the retrieve\_relevant\_memories function to be influenced by Aurora's current emotional state.

## **Phase 3: Advanced Agentic Systems (FUTURE)**

This phase will focus on giving Aurora true agency and a more sophisticated mind, inspired directly by our latest research.

* \[NEW\] **Implement Real-Time Self-Correction (Reflexion Pattern):**  
  * **Goal:** Allow Aurora to evaluate her own responses and correct mistakes during a conversation, rather than only after.  
  * **Method:** Implement a "reflexion" loop where, after generating a response, an internal process can evaluate its quality or factual accuracy and trigger a new, corrected response if necessary, making her feel more self-aware.  
* \[NEW\] **Implement Structured Memory (Episodic vs. Semantic):**  
  * **Goal:** Evolve the memory from a simple list of events into a structured knowledge base.  
  * **Method:** The memory engine will be upgraded to distinguish between **Episodic** memory (recalling specific past conversations) and **Semantic** memory (distilling conversations into hard, structured facts, e.g., fact: {user: "Ben", attribute: "cat\_name", value: "Wicked"}).  
* \[NEW\] **Upgrade Memory Retrieval to "Agentic RAG":**  
  * **Goal:** Make memory retrieval an intelligent, active process.  
  * **Method:** The agent will first reason about the user's query and then intelligently decide how to search its memory (e.g., semantic search for feelings vs. keyword search for facts).  
* \[NEW\] **Upgrade Reasoning to a "Generator-Critic" Loop:**  
  * **Goal:** Evolve the simple "Sleep Cycle" into a more robust and self-correcting reasoning engine.  
  * **Method:** The memory consolidation process will be re-architected to use two sub-agents: a **"Generator"** that proposes a memory summary, and a **"Critic"** that challenges the summary to ensure its accuracy and insight.  
* \[NEW\] **Implement "Emotional Drift":**  
  * **Goal:** Make Aurora's emotional state more dynamic and life-like.  
  * **Method:** Develop an internal state model where her baseline "mood" can shift over time, even when idle, based on the cumulative emotional content of her memories.  
* \[PLANNED\] Implement Active, Self-Improving Memory (inspired by Mem0).  
* \[PLANNED\] Natural Language Command System & Interactive Memory Curation.  
* \[PLANNED\] Implement Full ITRS (Vanta-Inspired).  
* \[PLANNED\] Implement Proactive Agentic Loop ("The Conscience").

## **Phase 4: User Interface & Advanced Capabilities (FUTURE)**

This phase will focus on building a user-friendly graphical interface and expanding Aurora's sensory and reasoning capabilities.

* \[NEW\] **Implement Multimodal Emotion Recognition:**  
  * **Goal:** Evolve her emotional understanding beyond just text.  
  * **Method:** Plan for a future version of Aurora that can perform **vocal analysis**, allowing her to understand the tone of your voice, not just the words you say.  
* \[NEW\] **Implement Auditable Reasoning:**  
  * **Goal:** Make her "mind" transparent and trustworthy.  
  * **Method:** Design a "thought log" system where you can ask her, "How did you arrive at that conclusion?" and she can provide a step-by-step breakdown of her reasoning process.  
* \[PLANNED\] Dedicated GUI.  
* \[PLANNED\] High-Fidelity Voice Integration.  
* \[PLANNED\] Address Dependency Warnings.  
* \[PLANNED\] Design a Plugin Framework.