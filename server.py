from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from music_generator import MusicGenerator
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
# Initialize with debug mode set to False to use the real model
music_generator = MusicGenerator(debug_mode=False)

class MusicPreferences(BaseModel):
    activity: Optional[str] = ""  # e.g., "waking up", "working", "traveling"
    character: Optional[str] = ""  # e.g., "unfamiliar", "popular", "favorite"
    mood: Optional[str] = ""      # e.g., "energetic", "cheerful", "calm", "sad"
    duration: Optional[float] = Field(8.0, ge=1.0, le=30.0)  # Duration in seconds
    temperature: Optional[float] = Field(1.0, ge=0.0, le=1.0)  # Controls randomness
    top_k: Optional[int] = Field(250, ge=0)  # Top-k sampling
    top_p: Optional[float] = Field(0.0, ge=0.0, le=1.0)  # Nucleus sampling
    cfg_coef: Optional[float] = Field(3.0, ge=0.0)  # Classifier-free guidance coefficient

@app.post("/generate-music")
async def generate_music(preferences: MusicPreferences):
    try:
        # Convert preferences to dict
        pref_dict = preferences.dict(exclude_none=True)
        
        # Generate music
        output_file = music_generator.generate_music(pref_dict)
        output_file = os.path.abspath(output_file)
        
        # Verify file exists and has content
        if not os.path.exists(output_file):
            logger.error(f"Generated file not found at: {output_file}")
            raise HTTPException(status_code=500, detail="Generated file not found")
            
        file_size = os.path.getsize(output_file)
        if file_size == 0:
            logger.error(f"Generated file is empty at: {output_file}")
            raise HTTPException(status_code=500, detail="Generated file is empty")
            
        logger.info(f"Serving file: {output_file} (size: {file_size} bytes)")
        
        # Return the generated audio file
        return FileResponse(
            output_file,
            media_type="audio/wav",
            filename="generated_music.wav",
            headers={
                "Content-Disposition": f'attachment; filename="generated_music.wav"'
            }
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating music: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating music: {str(e)}")

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