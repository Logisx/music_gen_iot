# Installation Guide for Neuromusic Project

This guide will help you set up the development environment for the Neuromusic project from scratch.

## Prerequisites

- Windows 10 or later
- Python 3.9.13
- Git Bash (or similar terminal)

## Step 1: Create and Activate Virtual Environment

1. Open Git Bash and navigate to your project directory:
```bash
cd /path/to/your/project
```

2. Create a new virtual environment with Python 3.9:
```bash
py -3.9 -m venv venv_py39
```

3. Activate the virtual environment:
```bash
source venv_py39/Scripts/activate
```

## Step 2: Install Dependencies

1. Make sure you're in the virtual environment (you should see `(venv_py39)` in your terminal)

2. Install the required packages from requirements.txt:
```bash
pip install -r requirements.txt
```

The key dependencies that will be installed include:
- torch==2.1.0
- torchvision==0.16.0
- torchaudio==2.1.0
- audiocraft==1.4.0a2
- fastapi
- uvicorn
- python-dotenv

## Step 3: Verify Installation

1. Check Python version:
```bash
python --version  # Should show Python 3.9.13
```

2. Verify torch and audiocraft installation:
```bash
pip list | grep -E "torch|audiocraft"
```

You should see:
- torch 2.1.0
- torchvision 0.16.0
- torchaudio 2.1.0
- audiocraft 1.4.0a2

## Step 4: Run the Server

1. Make sure you're in the virtual environment:
```bash
source venv_py39/Scripts/activate
```

2. Start the FastAPI server:
```bash
python server.py
```

The server will start on `http://localhost:8000`

## Troubleshooting

### Common Issues

1. **Python Version Mismatch**
   - Make sure you have Python 3.9.13 installed
   - Verify with `py -3.9 --version`

2. **Package Installation Errors**
   - If you encounter conflicts, try installing packages one by one:
   ```bash
   pip install torch==2.1.0
   pip install torchvision==0.16.0
   pip install torchaudio==2.1.0
   pip install audiocraft==1.4.0a2
   ```

3. **CUDA Issues**
   - The code will automatically use CUDA if available
   - Falls back to CPU if CUDA is not available

### Getting Help

If you encounter any issues:
1. Check the error message carefully
2. Make sure all prerequisites are installed
3. Verify you're using the correct Python version
4. Ensure you're in the virtual environment

## Additional Notes

- The project uses FastAPI for the web server
- Music generation is handled by the audiocraft library
- Generated music files are saved in WAV format
- The server includes endpoints for:
  - `/generate-music` (POST)
  - `/health` (GET)
  - `/iot-control` (POST) 