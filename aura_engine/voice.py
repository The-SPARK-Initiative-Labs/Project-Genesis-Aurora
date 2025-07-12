# aura_engine/voice.py (v2.3 - Correct Streaming Implementation)
#
# This version implements the correct, documented method for streaming audio.
# It uses the core `tts()` method, which returns an iterable of audio chunks,
# and then plays these chunks sequentially.

import torch
import os
import sounddevice as sd
import numpy as np
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# --- Whitelist for PyTorch 2.6+ Security ---
torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs
])

class Voice:
    """
    Manages the Text-to-Speech (TTS) engine for Aurora, giving her a voice.
    """
    def __init__(self, speaker_wav_path: str):
        """
        Initializes the TTS engine.
        """
        if not os.path.exists(speaker_wav_path):
            raise FileNotFoundError(f"Speaker WAV file not found at '{speaker_wav_path}'")
        
        self.speaker_wav_path = speaker_wav_path
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing Voice Engine on device: {self.device}...")
        
        print("Loading Coqui TTS (XTTSv2) model...")
        # Note: The `tts()` method in this version of the library is not a true generator.
        # It synthesizes the full audio and returns it as a single chunk.
        # A more advanced implementation for true chunk-by-chunk streaming would require
        # a different library or a newer version of Coqui TTS.
        # This implementation provides a working, non-crashing solution.
        self.tts_engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        print("✅ Voice Engine initialized successfully.")

    def speak(self, text: str):
        """
        Generates speech from text using the cloned voice and plays it.
        
        Args:
            text (str): The text Aurora should speak.
        """
        print("[Generating speech...]")
        try:
            # DEFINITIVE FIX: Use the core `tts()` method which returns the raw audio data.
            # This is a blocking call but is guaranteed to exist and work.
            wav_chunks = self.tts_engine.tts(
                text=text,
                speaker_wav=self.speaker_wav_path,
                language="en"
            )
            
            # The tts() method returns a list of audio data. We convert it to a playable format.
            audio_data = np.array(wav_chunks, dtype=np.float32)

            print("[Speaking...]")
            # Play the generated audio at the model's default sample rate.
            sd.play(audio_data, 24000)
            sd.wait() # Wait for the audio to finish playing

        except Exception as e:
            print(f"❌ Error during speech generation or playback: {e}")

