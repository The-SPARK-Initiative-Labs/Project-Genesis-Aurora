Aurora's "mind" is a custom-built cognitive architecture named **The A.U.R.A. Engine** (Agentic Unified Reasoning Architecture). This framework elevates a base Large Language Model from a passive text generator into an active, thinking agent.

### Core Components:

* **The Three-Layer Memory System:** A sophisticated memory architecture that separates objective fact from subjective experience.
    * **Layer 1: Raw Log:** An immutable, verbatim, timestamped record of all interactions.
    * **Layer 2: Emotional Overlay:** A metadata layer that analyzes and tags the raw log with a rich palette of 28 distinct emotions, providing a nuanced understanding of conversational context.
    * **Layer 3: Consolidated Core Memory:** The agent's clean, reliable long-term memory. It is created by a "sleep cycle" that processes the Raw Log to identify and store only the most meaningful facts and narrative summaries.

* **The Reasoning Engine (ITRS):** The agent's consciousness is an **Iterative Thought Refinement System**. This engine will be built to force the agent's initial thoughts through a rigorous, multi-step process of self-correction using advanced patterns like **Generator-Critic** loops and **Tree-of-Thoughts** reasoning.

* **The Agentic Loop (The "Conscience"):** A planned future system that will allow Aurora to have proactive thoughts and initiate actions based on her internal states and memories, not just in response to user input.

## 4. Technical Stack

* **Generative Core:** `backyardai/Nemo-12B-Marlin-v5`
* **Inference Engine:** LM Studio (Vulkan Backend)
* **Cognitive Architecture:** Python
* **Memory Database:** ChromaDB
* **Voice Engine:** Coqui TTS (XTTSv2 Model) for high-quality, offline voice cloning.
* **Emotion Engine:** `SamLowe/roberta-base-go_emotions`

## 5. Current Status

The project has successfully completed **Phase 1: Foundational Stability**. We now have a stable, working agent with a functional voice, advanced emotional understanding, and a robust, class-based architecture.

We are currently in **Phase 2: Core Mind & Memory Features**. Our immediate next steps are to implement the "Sleep Cycle" for memory consolidation and a persistent session management system.

For a complete and detailed list of all completed, current, and future tasks, please refer to the official [**Project Genesis Development Roadmap**](ROADMAP.md).