# config.py (v3.0 - Final Verified)
#
# This file contains the final, verified configuration for the Genesis Agent.

# --- Model Configuration ---
# This points to our high-performance Nemo model, which will be the base for our LoRA fine-tune.
LLM_MODEL_IDENTIFIER = "backyardai/Nemo-12B-Marlin-v5-GGUF"

# The identifier for the embedding model we will use for our RAG memory system.
# This has been corrected to match the identifier used by the LM Studio server.
EMBEDDING_MODEL_IDENTIFIER = "nomic-ai/nomic-embed-text-v1.5"

# --- File Paths ---
DB_PATH = "./agent_db"
LOG_FILE_PATH = "raw_log.txt"

# --- Database Collection Name ---
COLLECTION_NAME = "genesis_memory"
