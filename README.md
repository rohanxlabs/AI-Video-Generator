# HF-AI-Short-Video

A simple AI-driven short video generator that creates an image from text, makes a short zoom-style video, generates speech from text, and merges audio with video.

## Setup

1. Create a Python virtual environment and activate it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Hugging Face token:

```
HF_TOKEN=your_token_here
```

Alternatively, set the environment variable directly:

```bash
set HF_TOKEN=your_token_here
```

## Usage

Generate an image:

```bash
python image_gen.py --prompt "A cinematic 3D scene of a futuristic city" --output frame1.png
```

Create a zoom video:

```bash
python video_gen.py --image outputs/frame1.png --output outputs/short_video.mp4
```

Generate speech:

```bash
python voice.py --text "Welcome to the AI video generator" --output voice.mp3
```

Merge audio and video:

```bash
python merge.py --video outputs/short_video.mp4 --audio outputs/voice.mp3 --output outputs/final_video.mp4
```

## Full Pipeline

Run the full pipeline with one command:

```bash
python main.py --prompt "A magical landscape at sunrise" --text "This short AI video was generated automatically."
```
