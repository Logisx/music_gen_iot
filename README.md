# NeuroMusic Generator

A proof-of-concept service that generates music based on user preferences using AI. This project uses Facebook's MusicGen model to generate short music clips based on text descriptions derived from user preferences.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

The server will start on `http://localhost:8000`

## API Usage

### Generate Music

Send a POST request to `/generate-music` with JSON body containing preferences:

```json
{
    "activity": "waking up",
    "character": "unfamiliar",
    "mood": "cheerful",
    "language": "wordless"
}
```

The server will return a WAV audio file containing the generated music.

## Technical Details

- Uses Facebook's MusicGen model (small version) for music generation
- Generates 8-second music clips
- Output is in WAV format
- Preferences are converted into text prompts for the model

## Notes

- This is a proof-of-concept implementation
- The model runs locally and requires sufficient computational resources
- First generation might take longer as it downloads the model 