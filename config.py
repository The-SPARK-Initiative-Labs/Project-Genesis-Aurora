# config.py (v3.1 - Voice Config)
#
# This version adds the path to the speaker reference audio file.

# --- Model Configuration ---
LLM_MODEL_IDENTIFIER = "backyardai/Nemo-12B-Marlin-v5-GGUF"
EMBEDDING_MODEL_IDENTIFIER = "nomic-ai/nomic-embed-text-v1.5"

# --- File Paths ---
DB_PATH = "./agent_db"
LOG_FILE_PATH = "raw_log.txt"
SESSIONS_DIR = "./sessions"

# --- Voice Cloning Configuration ---
# The path to the high-quality, 5-25 second WAV file of the target voice.
SPEAKER_WAV_PATH = "her_voice_sample.wav"

# --- Database Collection Name ---
COLLECTION_NAME = "genesis_memory"
