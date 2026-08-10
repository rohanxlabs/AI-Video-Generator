# 🚀 Quick Start Guide

Get your AI Video Generator running in 5 minutes!

---

## ⚡ Super Quick Setup

### Step 1: Install Dependencies
```bash
python setup.py
```

### Step 2: Activate Virtual Environment
```bash
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Configure API Keys

Edit `.env` file and add:
```env
HF_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_key_here
```

**Get Your Keys:**
- Hugging Face: https://huggingface.co/settings/tokens
- Groq: https://console.groq.com/

### Step 4: Run!
```bash
python pipeline.py --prompt "Explain how photosynthesis works"
```

---

## 📋 Command Reference

### Full Pipeline
```bash
python pipeline.py --prompt "Your video topic"
```

### With Options
```bash
python pipeline.py --prompt "Your topic" --provider groq --fps 30 --music-volume 0.3
```

### Individual Components

**Generate Script:**
```bash
python script_gen.py --prompt "Your topic"
```

**Generate Images:**
```bash
python multi_image_gen.py --script outputs/script.json
```

**Generate Voice:**
```bash
python voice.py --text "Your narration text"
```

**Generate Music:**
```bash
python music_gen.py --duration 20
```

---

## 📁 Output Location

All generated files go to `outputs/` directory:
- `script.json` - Generated script
- `scene_*.png` - Scene images
- `narration.wav` - Voice narration
- `background_music.wav` - Background music
- `final_video_*.mp4` - **YOUR FINAL VIDEO**

---

## ⚙️ Configuration

Edit `config.py` to change:
- LLM provider (Groq or OpenRouter)
- LLM model
- Image generation model
- Output directory

---

## 🐛 Troubleshooting

**"HF_TOKEN not found"**
→ Add your Hugging Face token to `.env`

**"GROQ_API_KEY not found"**
→ Add your Groq API key to `.env`

**FFmpeg errors**
→ Install FFmpeg:
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**Import errors**
→ Make sure venv is activated:
- Windows: `.\venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

---

## 💡 Examples

### Educational Content
```bash
python pipeline.py --prompt "Explain the water cycle for kids"
```

### Science Topics
```bash
python pipeline.py --prompt "How do black holes form in space"
```

### Story-Driven
```bash
python pipeline.py --prompt "A journey through the solar system"
```

---

## 📊 What to Expect

**Processing Time**: 3-6 minutes per video

**Video Length**: 20-40 seconds (3-5 scenes)

**Output Quality**:
- Resolution: Based on generated images (typically 1024x1024)
- FPS: 24 (configurable)
- Audio: Voice narration + background music
- Format: MP4 (H.264 video, AAC audio)

---

## 🎯 Next Steps

1. ✅ Run the pipeline with your own prompt
2. ✅ Check the `outputs/` directory for results
3. ✅ Experiment with different topics
4. ✅ Share your generated videos!

---

Need more help? Check:
- `README.md` - Full documentation
- `IMPLEMENTATION_REPORT.md` - Technical details
- GitHub Issues - Report problems

Happy video generating! 🎬
