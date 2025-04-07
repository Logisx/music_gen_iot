# AI-Generated README

**Disclaimer:** This README was generated with the assistance of AI. It is a work in progress and part of a larger project.

## Overview

This project is a music generation system designed for cabin hotels in Northern Finland, near lakes and forests. It uses AI to generate music based on user preferences, focusing on mood and activity.

## Features

- Generate music based on mood and optional activity
- Customizable duration and generation parameters
- Simple API for easy integration

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the server:
```bash
python server.py
```

### Example Curl Commands

1. **Fun Mood:**
   ```bash
   curl -X POST "http://localhost:8000/generate-music" \
     -H "Content-Type: application/json" \
     -d '{
       "mood": "fun"
     }'
   ```

2. **Energetic Mood:**
   ```bash
   curl -X POST "http://localhost:8000/generate-music" \
     -H "Content-Type: application/json" \
     -d '{
       "mood": "energetic"
     }'
   ```

3. **Calm Mood:**
   ```bash
   curl -X POST "http://localhost:8000/generate-music" \
     -H "Content-Type: application/json" \
     -d '{
       "mood": "calm"
     }'
   ```

4. **Romantic Mood:**
   ```bash
   curl -X POST "http://localhost:8000/generate-music" \
     -H "Content-Type: application/json" \
     -d '{
       "mood": "romantic"
     }'
   ```

**Note:** Additional parameters like `duration`, `temperature`, `top_k`, `top_p`, and `cfg_coef` are optional and will use default values if not specified.

## Notes

- This project is a work in progress and part of a larger initiative.
- The music generation parameters can be adjusted to suit specific needs.
- For more details, refer to the `INSTALLATION.md` and `TESTING.md` files.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 