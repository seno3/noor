# Noor (MTCHacks 2025 Submission)

# Islamic Truth Verifier

Fast Islamic fact-checking extension for YouTube videos. Validates claims about Islam, Quran, and Hadith against authenticated sources.

## Prerequisites

- Python 3.8+
- Chrome/Edge browser
- Ollama installed locally

## Setup

### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

### 2. Start Ollama

```bash
ollama serve
```

### 3. Pull a Model

```bash
ollama pull mistral
```

Or use another model:
```bash
ollama pull llama2
ollama pull qwen
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
cd server
python3 islamic_fact_check_server.py
```

The server will start on `http://localhost:8004`

## Load Browser Extension

1. Open Chrome/Edge and go to `chrome://extensions/` (or `edge://extensions/`)
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select the `client` folder
5. Extension is ready!

## Usage

1. Go to any YouTube video
2. **Enable captions/subtitles** on the video
3. The extension automatically monitors captions and fact-checks Islamic content
4. Results appear in a popup on the screen

## Optional: Configuration

Create `server/.env` file to customize:

```bash
# AI Provider
AI_PROVIDER=ollama

# Ollama Settings
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Islamic API Keys
SUNNAH_API_KEY=your_key_here
```

## Notes

- The extension only processes Islamic content (automatically filters non-Islamic captions)
- Quick checks are fast (<1 second)
- Comprehensive analysis runs in the background
- Popups stay visible for 60 seconds
