# Aurora System Architecture Schema

## Core Directory Structure
```
C:\GenesisAgent\
├── aura_engine/          # Core cognitive architecture
├── agent_db/            # ChromaDB vector memory storage
├── tests/               # Comprehensive test suite
├── context/             # LCMP context management (this directory)
├── DOCS/               # Research and documentation
├── archive/            # Archived raw logs
├── config.py           # System configuration
├── main_agent.py       # Application entry point
└── raw_log.txt         # Layer 1 memory (active interactions)
```

## A.U.R.A. Engine Components

### Core Classes
- **Aurora** (`aura_engine/aurora.py`): Main orchestrator class
- **MemoryManager** (`aura_engine/memory_manager.py`): ChromaDB interface
- **Voice** (`aura_engine/voice.py`): TTS streaming system
- **Emotion Analysis** (`aura_engine/process_emotions.py`): 28-emotion classification

### Data Schemas (Pydantic)
- **VerifiedFact**: Single extracted fact from consolidation
- **FactList**: Container for multiple facts
- **ValidationResponse**: Boolean validation result
- **NarrativeSummary**: Consolidated memory narrative

## Three-Layer Memory System

### Layer 1: Raw Log
- **File**: `raw_log.txt`
- **Function**: `log_interaction()` in `log_interaction.py`
- **Purpose**: Immutable timestamped interaction record
- **Format**: Timestamped user/agent conversation pairs

### Layer 2: Emotional Overlay
- **Model**: `SamLowe/roberta-base-go_emotions`
- **Function**: `get_emotional_overlay()` in `process_emotions.py`
- **Purpose**: 28-emotion classification with confidence scores
- **Output**: JSON metadata attached to memories

### Layer 3: Consolidated Core Memory
- **Database**: ChromaDB at `./agent_db`
- **Collection**: `genesis_memory`
- **Process**: Multi-agent pipeline (Extractor → Validator → Narrative Weaver)
- **Storage**: Vector embeddings with metadata

## Key Configuration Values
```python
# Model identifiers
LLM_MODEL_IDENTIFIER = "backyardai/Nemo-12B-Marlin-v5-GGUF"
EMBEDDING_MODEL_IDENTIFIER = "nomic-ai/nomic-embed-text-v1.5"

# File paths
DB_PATH = "./agent_db"
LOG_FILE_PATH = "raw_log.txt"
SPEAKER_WAV_PATH = "her_voice_sample.wav"
COLLECTION_NAME = "genesis_memory"
```

## Critical Dependencies
- **lmstudio**: LM Studio Python SDK for model interaction
- **chromadb**: Vector database for persistent memory
- **transformers**: Hugging Face for emotion analysis
- **TTS**: Coqui TTS for voice synthesis (XTTSv2)
- **pydantic**: Data validation and schema enforcement

## Data Flow Architecture
1. **User Input** → Raw Log → Emotional Analysis → Memory Storage
2. **Memory Retrieval** → Embedding Search → Context Assembly → LLM Response
3. **Sleep Cycle** → Raw Log Analysis → Fact Extraction → Narrative Generation

## System Boundaries
- **Local-First**: All processing on local hardware
- **No External APIs**: Complete privacy and control
- **Vertically Integrated**: Custom components vs. framework approach
- **EQ-First**: Emotion analysis drives memory and response patterns

## Current Architecture Status
- **Phase 1 Complete**: Foundational stability achieved
- **Phase 2 Active**: Core mind & memory features implementation
- **Known Issues**: Memory embedding bugs, TTS optimization needed
- **Working Systems**: Basic conversation, emotion analysis, memory consolidation
