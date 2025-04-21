## AI Music Generation

The AI-related code is located in the `Machine Learning` folder.

This section is divided into two parts: 
1. **Showcase Workflow** - A simplified version of the implementation used for demonstration purposes.
2. **Planned Implementation Design** - A detailed plan for the full implementation.

![Architecture Diagram](assets/Smart%20Environment%20Architecture%20Diagram%20-%20visual%20selection%20(2).png)

---

### Showcase Workflow

Due to server memory limitations, the music generation model cannot be stored on the server. For the showcase, music samples were pre-generated and installed on a Raspberry Pico. 

The workflow is as follows:
1. The frontend sends a request in JSON format (specified below).
2. The backend processes the request and forwards the mood setting to the Raspberry Pico.
3. The Pico activates the corresponding music track and light settings.

---

### Implementation Design

The current model is not optimized for real-time music generation. To address this, the following design is proposed:
1. **Background Generation**: Music generation will be performed in the background, and the results will be cached in a dedicated database.
2. **Request Handling**: Upon receiving a request from the frontend, the system will:
   - Search the cache for the relevant audio.
   - Stream the audio to the Raspberry Pico.

---

### Code Key components:
- **`music_generator.py`**: Handles the music generation model. The `generate_music` function in the `MusicGenerator` class is responsible for setting parameters, running the generation process, and saving the output file.
- **`server.py`**: Simulates a simple server with an API endpoint for testing the system independently of the main application server. Example usage is provided below.

Generated audio files are saved in the `output` folder.


---

### MusicGen Model

This project relies on the **MusicGen model** from [Audiocraft](https://github.com/facebookresearch/audiocraft), an open-source library developed by Meta. MusicGen is a state-of-the-art model for music generation, capable of producing high-quality audio based on input parameters such as mood, duration, and temperature. For more details, visit the [Audiocraft repository](https://github.com/facebookresearch/audiocraft).

---

## Dependencies

Refer to `AI_INSTALLATION.md` for detailed dependency installation instructions.

---

### Example Curl Command

Use the following command to test the system:

```bash
curl -X POST "http://localhost:8000/generate-music" \
-H "Content-Type: application/json" \
-d '{
  "mood": "fun",
  "activity": "",
  "duration": 10.0,
  "temperature": 1.2,
  "top_k": 100,
  "top_p": 0.9,
  "cfg_coef": 2.0
}'
```

**Note:** Additional parameters like `duration`, `temperature`, `top_k`, `top_p`, and `cfg_coef` are optional and will use default values if not specified. Reference [Audiocraft](https://github.com/facebookresearch/audiocraft) repository for more information.

Refer to `AI_TESTING.md` for detailed testing instructions.