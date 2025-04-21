# Testing Guide for Neuromusic Server

This guide will help you test the different endpoints of the Neuromusic server.

## 1. Health Check

Test if the server is running properly:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## 2. Generate Music

### Using cURL

```bash
curl -X POST http://localhost:8000/generate-music \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "working",
    "mood": "energetic",
    "duration": 10.0,
    "temperature": 0.8,
    "top_k": 250,
    "top_p": 0.0,
    "cfg_coef": 3.0
  }' \
  --output generated_music.wav
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/generate-music"
preferences = {
    "activity": "working",
    "mood": "energetic",
    "duration": 10.0,
    "temperature": 0.8,
    "top_k": 250,
    "top_p": 0.0,
    "cfg_coef": 3.0
}

response = requests.post(url, json=preferences)

# Save the audio file
if response.status_code == 200:
    with open("generated_music.wav", "wb") as f:
        f.write(response.content)
    print("Music saved as generated_music.wav")
else:
    print(f"Error: {response.text}")
```

### Using FastAPI Swagger UI

1. Open your browser and go to: `http://localhost:8000/docs`
2. Click on the `/generate-music` endpoint
3. Click "Try it out"
4. Enter the following JSON in the request body:
```json
{
  "activity": "working",
  "mood": "energetic",
  "duration": 10.0,
  "temperature": 0.8,
  "top_k": 250,
  "top_p": 0.0,
  "cfg_coef": 3.0
}
```
5. Click "Execute"

## 3. IoT Control (Dummy Endpoint)

### Using cURL

```bash
curl -X POST http://localhost:8000/iot-control \
  -H "Content-Type: application/json" \
  -d '{"command": "play", "device": "speaker"}'
```

Expected response:
```json
{
    "status": "success",
    "message": "Command sent to IoT pipeline"
}
```

## Example Music Generation Parameters

Here are some example combinations you can try:

1. **Calm Work Music**:
```json
{
    "activity": "working",
    "mood": "calm",
    "duration": 15.0,
    "temperature": 0.7,
    "top_k": 250,
    "top_p": 0.0,
    "cfg_coef": 3.0
}
```

2. **Energetic Workout Music**:
```json
{
    "activity": "working out",
    "mood": "energetic",
    "duration": 8.0,
    "temperature": 0.9,
    "top_k": 250,
    "top_p": 0.0,
    "cfg_coef": 3.0
}
```

3. **Relaxing Sleep Music**:
```json
{
    "activity": "sleeping",
    "mood": "calm",
    "duration": 20.0,
    "temperature": 0.6,
    "top_k": 250,
    "top_p": 0.0,
    "cfg_coef": 3.0
}
```

## Notes

- The generated music will be saved as a WAV file
- Generation time may vary depending on your hardware
- If using CUDA, generation will be faster
- The `duration` parameter should be between 1.0 and 30.0 seconds
- Higher `temperature` values (0.8-1.0) create more random/creative outputs
- Lower `temperature` values (0.6-0.7) create more predictable outputs 