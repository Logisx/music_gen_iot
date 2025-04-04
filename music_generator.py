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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicGenerator:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        # Default generation parameters (can be overridden per request)
        self.default_duration = 8.0
        self.default_temperature = 1.0
        self.default_top_k = 250
        self.default_top_p = 0.0
        self.default_cfg_coef = 3.0
        
        if debug_mode:
            logger.info("Running in DEBUG mode - will generate dummy files quickly")
            self.device = 'cpu'
            self.sample_rate = 32000 # Default sample rate for dummy audio
        else:
            # Initialize the model
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Using device: {self.device}")
            
            # Load the model
            self.model = MusicGen.get_pretrained('facebook/musicgen-small', device=self.device)
            self.sample_rate = self.model.sample_rate
            
            # Set default generation parameters (can be overridden)
            self.model.set_generation_params(
                duration=self.default_duration,
                temperature=self.default_temperature,
                top_k=self.default_top_k,
                top_p=self.default_top_p,
                cfg_coef=self.default_cfg_coef
            )
        
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        logger.info(f"Creating output directory at: {self.output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_prompt(self, preferences):
        """Create a prompt from user preferences"""
        prompt_parts = []
        
        if preferences.get('activity'):
            prompt_parts.append(f"music for {preferences['activity']}")
        if preferences.get('mood'):
            prompt_parts.append(f"with {preferences['mood']} mood")
        if preferences.get('character'):
            prompt_parts.append(f"that is {preferences['character']}")
            
        return " ".join(prompt_parts) if prompt_parts else "calm music"
    
    def generate_dummy_audio(self, duration):
        """Generate a dummy audio file for testing"""
        # Create a simple sine wave
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Generate a simple melody using different frequencies
        frequencies = [440, 550, 660, 880]  # A4, C#5, E5, A5
        audio = np.zeros_like(t)
        for i, freq in enumerate(frequencies):
            start = i * len(t) // len(frequencies)
            end = (i + 1) * len(t) // len(frequencies)
            audio[start:end] = 0.5 * np.sin(2 * np.pi * freq * t[start:end])
        
        # Convert to torch tensor
        audio_tensor = torch.from_numpy(audio).float()
        return audio_tensor.unsqueeze(0), self.sample_rate
    
    def save_audio(self, audio_tensor, sample_rate, output_path):
        """Save audio using torchaudio"""
        try:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the audio file using torchaudio
            torchaudio.save(
                output_path,
                audio_tensor,  # Expects 2D tensor (channels, samples)
                sample_rate,
                format="wav"
            )
            
            logger.info(f"Audio saved successfully to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return False
    
    def generate_music(self, preferences):
        """Generate music based on user preferences"""
        try:
            # Create prompt from preferences
            prompt = self.create_prompt(preferences)
            logger.info(f"Generating music for prompt: {prompt}")
            
            # Get generation parameters from preferences or use defaults
            duration = preferences.get('duration', self.default_duration)
            temperature = preferences.get('temperature', self.default_temperature)
            top_k = preferences.get('top_k', self.default_top_k)
            top_p = preferences.get('top_p', self.default_top_p)
            cfg_coef = preferences.get('cfg_coef', self.default_cfg_coef)
            
            if self.debug_mode:
                # Generate dummy audio quickly
                logger.info("DEBUG MODE: Generating dummy audio...")
                start_time = time.time()
                output, current_sample_rate = self.generate_dummy_audio(duration)
                end_time = time.time()
                logger.info(f"DEBUG MODE: Dummy audio generation finished in {end_time - start_time:.2f} seconds.")
                audio_to_save = output.cpu() 
            else:
                # Generate music using the model
                logger.info("Starting music generation...")
                start_time = time.time()
                
                # Pass parameters directly to generate
                output = self.model.generate(
                    descriptions=[prompt],
                    duration=duration,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    cfg_coef=cfg_coef,
                    progress=True # Show progress bar if available
                )
                current_sample_rate = self.sample_rate
                
                end_time = time.time()
                logger.info(f"Music generation finished in {end_time - start_time:.2f} seconds.")
                audio_to_save = output[0].cpu()
            
            # Generate unique filename
            filename = f"generated_{uuid.uuid4().hex[:8]}.wav"
            output_path = os.path.join(self.output_dir, filename)
            
            # Save the generated audio
            logger.info(f"Saving music to {output_path} ...")
            
            # Save using torchaudio
            if not self.save_audio(audio_to_save, current_sample_rate, output_path):
                raise FileNotFoundError(f"Failed to save audio file at {output_path}")
            
            # Verify the file was created
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Failed to save audio file at {output_path}")
            
            file_size = os.path.getsize(output_path)
            logger.info(f"File saved successfully. Size: {file_size} bytes")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error in generate_music: {str(e)}", exc_info=True)
            raise 