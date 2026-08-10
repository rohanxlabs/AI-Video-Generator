# AI Video Generator

> **Transform text prompts into narrated videos using AI-powered script generation, image synthesis, and automated media composition.**

A multimodal generative AI pipeline that orchestrates LLM-based storytelling, visual generation, speech synthesis, and video composition to create engaging short-form videos automatically.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

This project demonstrates **generative AI orchestration** by chaining multiple AI services into a cohesive pipeline:

**Input**: Natural language prompt (e.g., "Explain how photosynthesis works")  
**Output**: Complete video with AI-generated visuals, narration, and background music

The system automatically:
- Generates a structured video script with multiple scenes
- Creates unique images for each scene using text-to-image models
- Synthesizes natural voice narration
- Composes procedural background music
- Renders everything into a polished final video

---

## 🏗️ Architecture

```
User Prompt
    ↓
┌─────────────────────────────────────┐
│  LLM Script Generation              │
│  (Groq/OpenRouter API)              │
│  → Story structure                  │
│  → Scene descriptions               │
│  → Visual prompts                   │
│  → Narration text                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Multi-Scene Image Generation       │
│  (Hugging Face SDXL)                │
│  → One image per scene              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Video Composition                  │
│  (MoviePy)                          │
│  → Scene transitions                │
│  → Zoom effects                     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Voice Synthesis                    │
│  (Google TTS)                       │
│  → Natural narration                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Background Music                   │
│  (Procedural Audio)                 │
│  → Ambient soundscape               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Final Merge                        │
│  (MoviePy + FFmpeg)                 │
│  → Audio mixing                     │
│  → Video encoding                   │
└─────────────────────────────────────┘
    ↓
Final MP4 Video
```

---

## ✨ Features

### Implemented
- ✅ **LLM-Powered Script Generation** - Structured storytelling with Groq/OpenRouter APIs
- ✅ **Multi-Scene Videos** - 3-5 scenes per video with individual visual prompts
- ✅ **AI Image Generation** - Stable Diffusion XL via Hugging Face Inference API
- ✅ **Text-to-Speech** - Natural voice narration using Google TTS
- ✅ **Background Music** - Procedural ambient music generation
- ✅ **Video Composition** - Smooth transitions and zoom effects
- ✅ **Audio Mixing** - Balanced narration and background music
- ✅ **CLI Pipeline** - One-command video generation
- ✅ **Modular Architecture** - Each component can run independently

### Not Implemented (Future Work)
- ⏳ Web API/Frontend - Currently CLI-only
- ⏳ Database - No persistence layer (not needed for core functionality)
- ⏳ Deployment Configuration - Local execution only
- ⏳ Advanced Transitions - Currently using simple zoom effects
- ⏳ Custom Music - Using procedural generation, not AI music models

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq (Llama 3.3 70B) / OpenRouter | Script and scene generation |
| **Image Generation** | Stable Diffusion XL (HF) | Visual content creation |
| **Text-to-Speech** | Google TTS (gTTS) | Voice narration |
| **Video Processing** | MoviePy | Scene composition and transitions |
| **Audio Generation** | SciPy + NumPy | Procedural background music |
| **Media Encoding** | FFmpeg | Video/audio encoding |
| **Environment** | Python 3.8+ | Core runtime |

---

## 📁 Project Structure

```
AI-Video-Generator/
├── pipeline.py              # Complete end-to-end orchestration
├── script_gen.py            # LLM script generation (Groq/OpenRouter)
├── multi_image_gen.py       # Multi-scene image generation
├── multi_video_gen.py       # Multi-scene video composition
├── voice.py                 # Voice narration synthesis
├── music_gen.py             # Procedural background music
├── final_merge.py           # Video + audio merging
├── config.py                # Configuration and API keys
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not committed)
├── .env.example             # Environment template
└── outputs/                 # Generated content
    ├── script.json          # Generated script structure
    ├── scene_*.png          # Scene images
    ├── narration.wav        # Voice narration
    ├── background_music.wav # Background music
    ├── multi_scene_video.mp4# Video without audio
    └── final_video_*.mp4    # Complete final videos
```

---

## 🚀 Setup

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video encoding)

### 1. Clone Repository
```bash
git clone https://github.com/rohanxlabs/AI-Video-Generator.git
cd AI-Video-Generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required for image generation
HF_TOKEN=your_huggingface_token_here

# Required for script generation (choose one)
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Get API Keys:**
- **Hugging Face**: https://huggingface.co/settings/tokens (free)
- **Groq**: https://console.groq.com/ (free tier available)
- **OpenRouter**: https://openrouter.ai/ (pay-per-use)

---

## 🎬 Usage

### Full Pipeline (Recommended)

Generate a complete video with one command:

```bash
python pipeline.py --prompt "Explain how black holes work in space"
```

**Options:**
```bash
python pipeline.py --prompt "Your video topic" \
  --provider groq \              # or "openrouter"
  --fps 30 \                     # frames per second
  --music-volume 0.3 \           # background music volume (0.0-1.0)
  --output my_video.mp4          # custom filename
```

**Examples:**
```bash
# Educational content
python pipeline.py --prompt "The water cycle explained for kids"

# Story-driven
python pipeline.py --prompt "A journey through the solar system"

# Science topic
python pipeline.py --prompt "How photosynthesis works in plants"
```

### Individual Components

You can also run each component separately for testing:

**1. Generate Script:**
```bash
python script_gen.py --prompt "Explain photosynthesis" --provider groq
```

**2. Generate Scene Images:**
```bash
python multi_image_gen.py --script outputs/script.json
```

**3. Create Video from Images:**
```bash
python multi_video_gen.py --script outputs/script.json --fps 24
```

**4. Generate Voice Narration:**
```bash
python voice.py --text "Your narration text" --output narration.wav
```

**5. Generate Background Music:**
```bash
python music_gen.py --duration 20 --tempo 120
```

**6. Merge Everything:**
```bash
python final_merge.py --video outputs/multi_scene_video.mp4 \
  --voice outputs/narration.wav \
  --music outputs/background_music.wav \
  --output final_video.mp4
```

---

## 📊 Example Output

### Input Prompt
```
"Create a short educational video about how photosynthesis works in plants"
```

### Generated Script Structure
```json
{
  "title": "The Magic of Photosynthesis",
  "overview": "A short educational video explaining how photosynthesis works",
  "narration": "Welcome to the world of plants...",
  "scenes": [
    {
      "scene_number": 1,
      "description": "Intro scene with a plant leaf",
      "image_prompt": "A close-up shot of a plant leaf with warm golden lighting...",
      "duration_seconds": 3
    },
    // ... more scenes
  ]
}
```

### Pipeline Output
- **Script**: `outputs/script.json`
- **Scene Images**: `outputs/scene_01.png`, `scene_02.png`, etc.
- **Video**: `outputs/multi_scene_video.mp4`
- **Audio**: `outputs/narration.wav`, `outputs/background_music.wav`
- **Final Video**: `outputs/final_video_20260810_143022.mp4`

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# LLM Provider
LLM_PROVIDER = "groq"  # or "openrouter"
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"

# Image Generation
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Output Directory
OUTPUT_DIR = Path("outputs")
```

---

## 🐛 Troubleshooting

### "HF_TOKEN environment variable is required"
- Set your Hugging Face token in `.env`
- Get a free token from: https://huggingface.co/settings/tokens

### "GROQ_API_KEY not found"
- Add your Groq API key to `.env`
- Get a free API key from: https://console.groq.com/

### FFmpeg Errors
- Ensure FFmpeg is installed and in your PATH
- Test with: `ffmpeg -version`

### Image Generation Fails
- Check your HF token is valid
- Verify internet connection
- Hugging Face may rate limit free tier usage

### Audio/Video Out of Sync
- This is rare but can happen with very long narrations
- Try adjusting scene durations in the generated script

---

## 🎓 How It Works

### 1. Script Generation
The LLM (Groq/OpenRouter) receives your prompt and generates a structured JSON response containing:
- Video title and overview
- Complete narration text (spoken throughout the video)
- 3-5 scenes with individual visual prompts and durations

### 2. Image Generation
For each scene, the system:
- Sends the detailed image prompt to Stable Diffusion XL
- Receives a high-quality generated image
- Saves it with proper scene numbering

### 3. Video Composition
MoviePy creates the video by:
- Loading each scene image
- Applying subtle zoom effects for visual interest
- Concatenating scenes with proper durations
- Rendering to MP4 format

### 4. Audio Generation
- **Voice**: gTTS converts the narration text to natural speech
- **Music**: Procedural generation creates ambient background audio using sine waves and envelopes

### 5. Final Merge
FFmpeg combines:
- Video track (multi-scene composition)
- Voice track (narration)
- Music track (background, reduced volume)
- Outputs final MP4 with AAC audio

---

## 📈 Performance

Typical generation times (approximate):
- **Script Generation**: 5-15 seconds
- **Image Generation**: 30-60 seconds per scene (3-5 scenes = 2-5 minutes)
- **Video Composition**: 10-30 seconds
- **Voice Generation**: 5-10 seconds
- **Audio Merge**: 10-20 seconds

**Total**: ~3-6 minutes for a complete 20-30 second video

Performance depends on:
- API response times
- Internet connection speed
- Image resolution and scene count
- Local CPU for video encoding

---

## 🔒 Security Notes

- **Never commit `.env` files** - Contains API keys
- **API keys in `.env` are gitignored** by default
- **Use `.env.example` as template** for new setups
- **Rotate API keys regularly** if exposed
- **Monitor API usage** to avoid unexpected costs

---

## 🚧 Limitations

### Current Constraints
- **Single-image scenes**: Each scene uses one static image with zoom effect
- **Basic transitions**: No complex scene transitions or animations
- **Procedural music**: Simple ambient audio, not AI-generated music
- **No video editing**: Cannot modify generated videos post-creation
- **API dependencies**: Requires active internet and valid API keys
- **Rate limits**: Free tier APIs may limit generation speed

### Known Issues
- Very long narrations may not perfectly sync with video duration
- Image generation can occasionally fail due to API rate limits
- Background music is basic ambient sound, not professionally composed

---

## 🛣️ Future Improvements

Potential enhancements (not currently implemented):
- [ ] Advanced scene transitions (cross-fade, wipe, etc.)
- [ ] AI-generated background music using MusicGen or similar
- [ ] Voice customization (different voices, accents, emotions)
- [ ] Multi-image per scene (true video generation)
- [ ] Real-time preview during generation
- [ ] Web interface for easier usage
- [ ] Video editing capabilities
- [ ] Custom branding/overlays
- [ ] Subtitle generation
- [ ] Multiple language support
- [ ] Longer video support (currently optimized for 20-40s)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- Improved transition effects
- Better music generation
- Additional LLM providers
- Enhanced error handling
- Performance optimizations

---

## 👨‍💻 Author

**Rohan**  
GitHub: [@rohanxlabs](https://github.com/rohanxlabs)

---

## 🙏 Acknowledgments

- **Hugging Face** - Image generation infrastructure
- **Groq** - Fast LLM inference
- **OpenRouter** - Multi-model LLM access
- **MoviePy** - Video processing framework
- **gTTS** - Text-to-speech synthesis
- **FFmpeg** - Media encoding

---

## 📚 Related Projects

Check out my other AI/ML projects:
- **FarmLens** - AI-powered agricultural monitoring
- **LearnPath** - Personalized learning recommendations
- **Sentinel** - ML model monitoring and observability
- **PerceptAgent** - Agentic AI for robotics
