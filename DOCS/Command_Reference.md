# Command Reference for Aurora Development

## Testing Commands (Run from C:\GenesisAgent in venv)

### Memory Consolidation Test
```bash
python test_consolidation_fix.py
```

### Standalone Memory Consolidation
```bash
python aura_engine/memory_consolidation.py
```

### Individual Component Tests
```bash
python tests/test_sdk_connection.py
python tests/test_memory_manager.py
python tests/test_emotion_model.py
```

### Main Aurora Launch
```bash
python main_agent.py
```

## Note
All commands assume you're in the project venv via your batch file.
