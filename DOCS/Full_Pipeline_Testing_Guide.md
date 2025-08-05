# Full Aurora Pipeline Testing Guide

## Purpose
Test the complete Aurora pipeline: conversation → memory formation → sleep cycle → ChromaDB storage

## Current Status
- **Memory consolidation pipeline**: ✅ WORKING (tested in isolation)
- **Individual components**: ✅ WORKING (Extractor, Validator, Narrative Weaver)
- **Ready for**: Full end-to-end pipeline test

## Testing Protocol

### Step 1: Start Aurora
```bash
python main_agent.py
```

### Step 2: Scripted Conversation
Use this exact conversation script to create clear, extractable facts:

```
"Hi Aurora, I need to tell you about my work schedule this week."

"I have a meeting with the development team on Thursday at 2 PM."

"My cat's name is Whiskers and she's 3 years old."

"I decided to switch my project from React to Vue.js because of better performance."

"The budget for the solar panel research is $50,000."

"I'm planning to visit Tokyo in December for the AI conference."

quit
```

### Step 3: What Should Happen
1. **During conversation**: Aurora logs each interaction to `raw_log.txt`
2. **When typing 'quit'**: Aurora.shutdown() automatically triggers memory consolidation
3. **Sleep cycle runs**: Extractor → Validator → Narrative Weaver pipeline
4. **Results stored**: Facts and summaries added to ChromaDB

### Step 4: Verification
Check console output for:
- ✅ Facts extracted from conversation
- ✅ Facts validated (some may be rejected if not verbatim)
- ✅ Narrative summary generated
- ✅ Memories stored in ChromaDB
- ✅ Log file archived

### Expected Results
- **Specific facts** like "meeting Thursday 2 PM", "cat named Whiskers", "$50,000 budget"
- **Some rejections** (validator is strict about verbatim quotes)
- **Clean narrative** (no hallucination, only verified facts)

### Why This Script Works
- Contains specific facts (names, dates, numbers, decisions)
- Direct statements (likely to be extracted)
- Different categories (schedule, personal, technical, financial, travel)
- Clear enough for validator to verify against conversation log

### If It Fails
- Check Aurora initialization
- Verify LM Studio is running
- Check memory consolidation errors in console
- Validate ChromaDB connectivity

## Post-Test Next Steps
If pipeline test successful:
1. Optimize TTS streaming for smooth playback
2. Implement session persistence
3. Add emotional anchor memory retrieval

## Context for Next AI Partner
The memory consolidation system is working in isolation but needs full integration testing with Aurora's main conversation loop. This test validates the complete memory formation process works end-to-end.
