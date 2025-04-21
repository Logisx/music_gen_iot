from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from music_generator import MusicGenerator
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize the music generator with debug mode for faster testing
music_generator = MusicGenerator(debug_mode=False)

class MusicPreferences(BaseModel):
    mood: str
    activity: Optional[str] = None
    duration: float = 10.0
    temperature: float = 1.2  # Lowered for more stability
    top_k: int = 100          # Reduced for better control
    top_p: float = 0.9       # Added for nucleus sampling
    cfg_coef: float = 2.0    # Reduced for better balance

@app.post("/generate-music")
async def generate_music(preferences: MusicPreferences):
    try:
        # Convert preferences to dictionary
        pref_dict = preferences.dict(exclude_none=True)
        
        # Generate music
        output_file = music_generator.generate_music(pref_dict)
        
        # Return the file path
        return {"file_path": output_file}
        
    except Exception as e:
        logger.error(f"Error generating music: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Dummy endpoint for IoT control (placeholder)
@app.post("/iot-control")
async def iot_control(command: dict):
    """
    Placeholder for IoT control endpoint.
    In real implementation, this would send commands to your IoT pipeline.
    """
    return {"status": "success", "message": "Command sent to IoT pipeline"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)