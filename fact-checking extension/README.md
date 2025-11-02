# Islamic Truth Verifier

A comprehensive fact-checking system that validates claims about Islam, Quran, and Hadith against authenticated Islamic sources. Supports both local (Ollama) and cloud (OpenAI) AI backends.

## 🌟 Features

- **Quran Verification**: Automatically detects and verifies Quranic references (e.g., 2:255)
- **Hadith Authentication**: Verifies hadiths against authenticated collections (Sahih Bukhari, Muslim, etc.)
- **Fabricated Hadith Detection**: Identifies commonly fabricated hadiths using pattern matching
- **Fiqh Ruling Verification**: Identifies Islamic legal rulings and notes madhab differences
- **YouTube Video Processing**: Extracts and verifies Islamic claims from YouTube transcripts
- **Flexible AI Backend**: Choose between Ollama (local) or OpenAI (cloud)
- **Source Credibility Scoring**: Rates sources on 0-100 scale based on scholarly reputation
- **Arabic Text Support**: Displays Quranic verses in Arabic with proper RTL formatting

## 📋 Prerequisites

- Python 3.8+
- Chrome/Edge browser (for extension)
- Ollama installed (if using local AI) OR OpenAI API key (if using cloud AI)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FactChecker
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your configuration
# See Configuration section below
```

### 3. Configure Environment Variables

Create `.env` file in the project root:

```bash
# Choose AI provider
AI_PROVIDER=ollama  # or "openai"

# If using Ollama
OLLAMA_MODEL=mistral

# If using OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Optional: Islamic API keys
SUNNAH_API_KEY=your_sunnah_key  # Optional, for better hadith verification
```

### 3. Start the Backend Server

```bash
cd server
python islamic_fact_check_server.py
```

Server will start on `http://localhost:8004`

### 4. Load the Browser Extension

1. Open Chrome/Edge and go to `chrome://extensions/` (or `edge://extensions/`)
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select the `client` folder in this repository
5. The extension icon should appear in your browser toolbar

## ⚙️ Configuration

### AI Provider Selection

The system supports two AI backends:

#### Ollama (Local - Recommended for Privacy)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull mistral`
3. Set in `.env`: `AI_PROVIDER=ollama`

#### OpenAI (Cloud - Requires API Key)

1. Get API key from https://platform.openai.com/api-keys
2. Set in `.env`: `AI_PROVIDER=openai` and `OPENAI_API_KEY=your_key`

### Islamic API Keys (Optional)

- **Sunnah.com API**: Improves hadith verification. Get from https://github.com/alquran/sunnah.com-api
- **AlQuran Cloud**: No key required, completely free
- **HadithAPI.com**: Free tier available, no key required

## 📖 Usage

### Browser Extension (Recommended)

1. **Go to any YouTube video page**
2. **Enable captions/subtitles** on the video
3. The extension automatically:
   - Monitors captions in real-time
   - Accumulates text until 30 words
   - Sends to backend for fact-checking
   - Displays results in a popup on the screen

### Debug Mode

Click the extension icon and use the **"Debug: Force Fact Check"** button to manually trigger a fact-check with test text.

### API Endpoints

You can also use the backend API directly:

**Check Islamic Claim:**
```bash
curl -X POST http://localhost:8004/check-islamic-claim \
  -H "Content-Type: application/json" \
  -d '{"claim": "The Prophet Muhammad said peace be upon him"}'
```

**Health Check:**
```bash
curl http://localhost:8004/health
```

### Example Claims

- `In Surah 2:255, Allah says...`
- `The Prophet (peace be upon him) said: "Seek knowledge even if it is in China"`
- `Is it halal to invest in cryptocurrency?`

## 🏗️ Architecture

```
FactChecker/
├── server/
│   ├── islamic_fact_check_server.py    # Main FastAPI server
│   ├── config.py                       # Configuration management
│   ├── ai_providers/                   # AI abstraction layer
│   │   ├── base.py                     # Abstract base class
│   │   ├── ollama_provider.py          # Ollama implementation
│   │   └── openai_provider.py          # OpenAI implementation
│   ├── islamic_verification/          # Islamic verification modules
│   │   ├── quran_verifier.py           # Quran verification
│   │   ├── hadith_verifier.py          # Hadith verification
│   │   ├── fabricated_hadith_detector.py
│   │   ├── fiqh_verifier.py            # Fiqh rulings
│   │   └── source_credibility.py       # Source scoring
│   └── youtube_handler.py              # YouTube transcript processing
├── client/
│   ├── contentScript.js                # Main extension script
│   ├── popup.html/js                    # Extension popup UI
│   └── manifest.json                   # Extension manifest
└── .env                                # Configuration file
```

## 📊 Verification Process

1. **Islamic Verification**: Checks claim against Quran, Hadith, and Fiqh databases
2. **Web Search**: Searches trusted Islamic sources
3. **Source Processing**: Extracts and summarizes relevant content
4. **AI Analysis**: Uses AI to generate verdict with Islamic context
5. **Results Compilation**: Combines all verification data into comprehensive result

## 🔍 Verdict Types

- **Authentic**: Verified against authentic sources
- **Likely Authentic**: Strong evidence supports authenticity
- **Likely Fabricated**: Evidence suggests fabrication
- **Fabricated**: Confirmed fabrication (e.g., known fabricated hadith)
- **Unable to Verify**: Insufficient evidence

## 📚 Hadith Grading

- **Sahih** (Authentic): Highest grade, 95% confidence
- **Hasan** (Good): Reliable narrators, 80% confidence
- **Da'if** (Weak): Weak narrators, 40% confidence
- **Mawdu** (Fabricated): Proven fabrication, 0% confidence

## ⚠️ Limitations & Disclaimers

**IMPORTANT**: This tool verifies factual accuracy, not theological interpretation.

- Complex fiqh matters should be referred to qualified Islamic scholars
- The system checks claims against authenticated sources but cannot replace human scholarly expertise
- Users should seek guidance from local Islamic authorities for personal religious matters
- Some rulings may vary by school of thought (madhab)
- The system is not a substitute for studying under qualified scholars

## 🤝 Contributing

Contributions welcome! Please see contributing guidelines.

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- AlQuran Cloud API for Quranic text
- Sunnah.com for hadith collections
- HadithAPI.com for additional hadith verification
- All scholars and institutions maintaining authentic Islamic sources

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

