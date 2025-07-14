# aura_engine/voice.py (v4.3 - Sprinter Tuning)
#
# This version tunes the streaming parameters based on the "Sprinter" hypothesis.
# It uses a smaller `stream_chunk_size` to test if faster, smaller chunks
# can create a smoother audio stream on the target hardware.

import torch
import os
import pyaudio
import numpy as np
import threading
import queue
from TTS.api import TTS

# --- Whitelist for PyTorch 2.6+ Security ---
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
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
        Initializes the TTS engine in a robust way for streaming.
        """
        print("Initializing Voice Engine for Streaming...")
        
        if not os.path.exists(speaker_wav_path):
            raise FileNotFoundError(f"Speaker WAV file not found at '{speaker_wav_path}'")
        self.speaker_wav_path = speaker_wav_path
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"-> Loading model on {self.device.upper()}...")
        
        self.tts_engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        print("   ✅ High-level TTS engine loaded.")
        
        self.model = self.tts_engine.synthesizer.tts_model
        
        print("-> Computing speaker latents... (this may take a moment)")
        try:
            self.gpt_cond_latent, self.speaker_embedding = self.model.get_conditioning_latents(audio_path=[self.speaker_wav_path])
        except Exception as e:
            print(f"❌ Error computing speaker latents: {e}")
            raise
            
        print("✅ Voice Engine initialized successfully.")

    def _producer(self, q, text):
        """
        The "Generator" worker. Runs in a separate thread.
        Generates audio chunks and puts them into the queue.
        """
        try:
            # This is the generator that yields audio chunks.
            chunks = self.model.inference_stream(
                text,
                "en",
                self.gpt_cond_latent,
                self.speaker_embedding,
                enable_text_splitting=True,
                # --- DEFINITIVE TUNING ---
                # Testing the "Sprinter" hypothesis with a smaller chunk size.
                stream_chunk_size=20,
                overlap_wav_len=1024
            )
            # Place each generated chunk into the queue.
            for chunk in chunks:
                q.put(chunk.cpu().numpy())
        except Exception as e:
            print(f"❌ Error in TTS producer thread: {e}")
        finally:
            q.put(None) # Use None as a sentinel to signal the end of the stream

    def _consumer(self, q):
        """
        The "Player" worker. Runs in the main thread.
        Takes audio chunks from the queue and plays them.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=24000,
                        output=True)
        
        print("[Speaking...]")
        while True:
            chunk = q.get()
            if chunk is None: # Check for the sentinel value
                break
            # Convert the audio chunk to the correct format and play it.
            audio_data = (chunk * 32767).astype(np.int16)
            stream.write(audio_data.tobytes())
        
        # Clean up the audio stream.
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("[Finished speaking.]")

    def speak(self, text: str):
        """
        Generates and plays speech using the parallel two-worker model.
        
        Args:
            text (str): The text Aurora should speak.
        """
        print("[Generating speech stream...]")
        
        # Create the shared "basket" (queue) for audio chunks.
        q = queue.Queue(maxsize=20)
        
        # Create and start the "Generator" thread.
        producer_thread = threading.Thread(target=self._producer, args=(q, text))
        producer_thread.start()
        
        # The "Player" runs in the main thread, blocking until the stream is finished.
        self._consumer(q)
        
        # Wait for the producer thread to finish its work cleanly.
        producer_thread.join()

