import os
import time
# Remove replicate import
# import replicate 
from dotenv import load_dotenv
import torch
from audiocraft.models import MusicGen
import torchaudio
import uuid
import logging
import numpy as np
from audiocraft.data.audio import audio_read, audio_write
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicGenerator:
    def __init__(self, model_id="facebook/musicgen-small", debug_mode=False):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.debug_mode = debug_mode
        self.model = None
        self.output_dir = "output"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not debug_mode:
            try:
                self.model = MusicGen.get_pretrained(model_id, device=self.device)
                # Set optimized parameters for faster generation
                self.model.set_generation_params(
                    use_sampling=True,
                    top_k=50,  # Reduced for faster generation
                    top_p=0.0,
                    temperature=1.0,  # Increased for faster generation
                    cfg_coef=1.5,  # Reduced for faster generation
                    two_step_cfg=True  # Enable two-step CFG for faster generation
                )
                logger.info(f"Model {model_id} loaded successfully on {self.device}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise

    def create_prompt(self, preferences):
        """Create a prompt from user preferences."""
        activity = preferences.get('activity', '')
        mood = preferences.get('mood', '')
        return f"music for {activity} with {mood} mood"

    def generate_dummy_audio(self, duration, sample_rate=32000):
        """Generate a dummy audio file for testing."""
        t = torch.linspace(0, duration, int(duration * sample_rate))
        # Create a simple melody using sine waves
        frequencies = [440, 554, 659, 880]  # A4, C#5, E5, A5
        audio = torch.zeros_like(t)
        for i, freq in enumerate(frequencies):
            # Create a simple melody pattern
            start_time = i * duration / len(frequencies)
            end_time = (i + 1) * duration / len(frequencies)
            mask = (t >= start_time) & (t < end_time)
            audio[mask] = 0.5 * torch.sin(2 * np.pi * freq * t[mask])
        
        # Add some reverb-like effect
        reverb = torch.zeros_like(audio)
        for i in range(1, 10):
            delay = int(0.1 * i * sample_rate)
            if delay < len(audio):
                reverb[delay:] += 0.1 / i * audio[:-delay]
        
        audio = audio + reverb
        audio = audio / torch.max(torch.abs(audio))
        
        # Reshape to match expected format (batch_size, channels, samples)
        return audio.unsqueeze(0).unsqueeze(0)

    def save_audio(self, audio, filename, sample_rate=32000):
        """Save audio using torchaudio."""
        try:
            # Ensure audio is on CPU and has correct shape
            if isinstance(audio, torch.Tensor):
                audio = audio.cpu()
                # If audio is 3D (batch, channels, samples), take first batch
                if audio.dim() == 3:
                    audio = audio[0]  # Remove batch dimension
                # If audio is 1D (samples), add channel dimension
                elif audio.dim() == 1:
                    audio = audio.unsqueeze(0)  # Add channel dimension
            
            # Save using torchaudio
            torchaudio.save(
                filename,
                audio,
                sample_rate,
                format="wav"
            )
            logger.info(f"Audio saved successfully to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return False

    def generate_music(self, preferences):
        """Generate music based on user preferences."""
        try:
            # Get parameters from preferences with defaults
            duration = float(preferences.get('duration', 5.0))
            temperature = float(preferences.get('temperature', 1.0))  # Default to higher temperature
            top_k = int(preferences.get('top_k', 50))  # Default to lower top_k
            top_p = float(preferences.get('top_p', 0.0))
            cfg_coef = float(preferences.get('cfg_coef', 1.5))  # Default to lower cfg_coef
            
            if self.debug_mode:
                # Generate dummy audio for testing
                output = self.generate_dummy_audio(duration)
                audio_to_save = output.cpu()
            else:
                # Create prompt from preferences
                prompt = self.create_prompt(preferences)
                logger.info(f"Generating music for prompt: {prompt}")
                
                # Set generation parameters
                self.model.set_generation_params(
                    duration=duration,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    cfg_coef=cfg_coef
                )
                
                # Generate music
                logger.info("Starting music generation...")
                start_time = time.time()
                
                output = self.model.generate([prompt], progress=True)
                sample_rate = self.model.sample_rate
                
                end_time = time.time()
                logger.info(f"Music generation finished in {end_time - start_time:.2f} seconds.")
                # Get the first sample from the batch and move to CPU
                audio_to_save = output[0].cpu()
            
            # Create filename based on preferences
            activity = preferences.get('activity', 'unknown')
            mood = preferences.get('mood', 'unknown')
            duration_str = f"{int(duration)}s"
            timestamp = datetime.now().strftime("%H-%M_%Y-%m-%d")
            filename = os.path.join(self.output_dir, f"{timestamp}_{mood}_{activity}_music_{duration_str}.wav")
            
            # Save the audio
            logger.info(f"Saving music to {filename} ...")
            
            if self.save_audio(audio_to_save, filename):
                return filename
            else:
                raise Exception("Failed to save audio file")
                
        except Exception as e:
            logger.error(f"Error generating music: {str(e)}", exc_info=True)
            raise 