"""
LLM-powered script and scene generation for AI video creation.
Supports Groq and OpenRouter APIs for flexible model selection.
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from config import GROQ_API_KEY, OPENROUTER_API_KEY, LLM_PROVIDER, GROQ_MODEL, OPENROUTER_MODEL, OUTPUT_DIR


SCRIPT_PROMPT_TEMPLATE = """You are a creative video script writer. Create a short, engaging video script based on the user's prompt.

User Prompt: {user_prompt}

Generate a JSON response with the following structure:
{{
  "title": "Video title",
  "overview": "Brief description of the video concept",
  "narration": "The complete narration text that will be spoken (keep it under 30 seconds when spoken)",
  "scenes": [
    {{
      "scene_number": 1,
      "description": "What happens in this scene",
      "image_prompt": "Detailed visual description for image generation (cinematic, detailed, specific style)",
      "duration_seconds": 3
    }}
  ]
}}

Requirements:
- Create 3-5 scenes that tell a cohesive story
- Each scene should have a clear, vivid visual description
- Image prompts should be detailed and cinematic (mention style, lighting, composition)
- Total narration should be 20-40 seconds when spoken
- Keep it engaging and visually interesting
- Ensure scenes flow together logically

Return ONLY valid JSON, no additional text."""


def call_groq_api(prompt: str, system_prompt: str = "") -> str:
    """Call Groq API for LLM inference."""
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY not found in environment variables.")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Groq API call failed: {e}")


def call_openrouter_api(prompt: str, system_prompt: str = "") -> str:
    """Call OpenRouter API for LLM inference."""
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY not found in environment variables.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/rohanxlabs/AI-Video-Generator",
        "X-Title": "AI Video Generator"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"OpenRouter API call failed: {e}")


def generate_script(user_prompt: str, provider: Optional[str] = None) -> Dict:
    """
    Generate a video script with scenes using an LLM.
    
    Args:
        user_prompt: User's description of what video they want
        provider: "groq" or "openrouter" (defaults to config setting)
    
    Returns:
        Dictionary containing title, overview, narration, and scenes
    """
    provider = provider or LLM_PROVIDER
    
    print(f"[1/6] Generating script using {provider.upper()}...")
    
    prompt = SCRIPT_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
    
    # Call the appropriate API
    if provider.lower() == "groq":
        response_text = call_groq_api(prompt)
    elif provider.lower() == "openrouter":
        response_text = call_openrouter_api(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'groq' or 'openrouter'.")
    
    # Parse JSON response
    try:
        # Try to extract JSON if wrapped in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        script = json.loads(response_text)
        
        # Validate required fields
        required_fields = ["title", "overview", "narration", "scenes"]
        for field in required_fields:
            if field not in script:
                raise ValueError(f"Missing required field: {field}")
        
        if not script["scenes"] or len(script["scenes"]) == 0:
            raise ValueError("Script must contain at least one scene")
        
        # Validate each scene
        for scene in script["scenes"]:
            required_scene_fields = ["scene_number", "description", "image_prompt", "duration_seconds"]
            for field in required_scene_fields:
                if field not in scene:
                    raise ValueError(f"Scene missing required field: {field}")
        
        print(f"✓ Script generated: {script['title']}")
        print(f"  - {len(script['scenes'])} scenes")
        print(f"  - Narration length: {len(script['narration'])} characters")
        
        # Save script to file
        script_path = OUTPUT_DIR / "script.json"
        with open(script_path, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        print(f"  - Script saved to: {script_path}")
        
        return script
        
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse LLM response as JSON: {e}\nResponse: {response_text}")
    except Exception as e:
        raise RuntimeError(f"Script generation failed: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate video script using LLM.")
    parser.add_argument(
        "--prompt",
        default="Create a short video explaining how black holes work in space",
        help="User prompt describing the desired video"
    )
    parser.add_argument(
        "--provider",
        choices=["groq", "openrouter"],
        default=LLM_PROVIDER,
        help="LLM provider to use"
    )
    parser.add_argument(
        "--output",
        default="script.json",
        help="Output filename for the generated script"
    )
    
    args = parser.parse_args()
    
    try:
        script = generate_script(args.prompt, args.provider)
        print("\n" + "="*60)
        print(f"Title: {script['title']}")
        print(f"Overview: {script['overview']}")
        print("="*60)
        print(f"\nNarration:\n{script['narration']}")
        print("\n" + "="*60)
        print("Scenes:")
        for scene in script['scenes']:
            print(f"\n  Scene {scene['scene_number']}: {scene['description']}")
            print(f"  Duration: {scene['duration_seconds']}s")
            print(f"  Image Prompt: {scene['image_prompt']}")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
