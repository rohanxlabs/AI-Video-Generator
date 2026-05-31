import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
VIDEO_MODEL = "cerspense/zeroscope_v2_576w"
VOICE_MODEL = "facebook/mms-tts-eng"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
