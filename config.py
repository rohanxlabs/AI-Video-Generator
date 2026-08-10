import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Keys
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model Configuration
IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
LLM_PROVIDER = "openrouter"  # Options: "groq", "openrouter"
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and capable
OPENROUTER_MODEL = "openrouter/free"  # Free auto-router (smart selection)

# Output Configuration
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
