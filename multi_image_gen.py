"""
Multi-scene image generation for video creation.
Generates multiple images based on scene descriptions from LLM script.
"""

from pathlib import Path
from typing import List, Dict
from huggingface_hub import InferenceClient
from PIL import Image
from config import HF_TOKEN, IMAGE_MODEL, OUTPUT_DIR
import time


def generate_scene_images(scenes: List[Dict], output_dir: Path = OUTPUT_DIR) -> List[Path]:
    """
    Generate images for multiple scenes.
    
    Args:
        scenes: List of scene dictionaries with 'image_prompt' and 'scene_number'
        output_dir: Directory to save generated images
    
    Returns:
        List of paths to generated images
    """
    if not HF_TOKEN:
        raise EnvironmentError("HF_TOKEN environment variable is required to generate images.")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    client = InferenceClient(model=IMAGE_MODEL, token=HF_TOKEN)
    
    image_paths = []
    total_scenes = len(scenes)
    
    print(f"\n[2/6] Generating {total_scenes} scene images...")
    
    for i, scene in enumerate(scenes, 1):
        scene_num = scene.get('scene_number', i)
        prompt = scene.get('image_prompt', scene.get('description', ''))
        
        if not prompt:
            raise ValueError(f"Scene {scene_num} has no image_prompt or description")
        
        filename = f"scene_{scene_num:02d}.png"
        output_path = output_dir / filename
        
        print(f"  [{i}/{total_scenes}] Generating scene {scene_num}...")
        print(f"       Prompt: {prompt[:80]}...")
        
        try:
            # Generate image
            image = client.text_to_image(prompt)
            
            if not isinstance(image, Image.Image):
                raise RuntimeError(f"Unexpected response from image generation model for scene {scene_num}")
            
            # Save image
            image.save(output_path)
            image_paths.append(output_path)
            print(f"       ✓ Saved to {output_path}")
            
            # Rate limiting - wait between requests to avoid API throttling
            if i < total_scenes:
                time.sleep(1)
                
        except Exception as e:
            raise RuntimeError(f"Failed to generate image for scene {scene_num}: {e}")
    
    print(f"✓ All {total_scenes} scene images generated")
    return image_paths


if __name__ == "__main__":
    import json
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate images for multiple scenes from a script.")
    parser.add_argument(
        "--script",
        default="outputs/script.json",
        help="Path to the script JSON file"
    )
    
    args = parser.parse_args()
    
    # Load script
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        print("Run script_gen.py first to generate a script.")
        exit(1)
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # Generate images
    try:
        image_paths = generate_scene_images(script['scenes'])
        print("\nGenerated images:")
        for path in image_paths:
            print(f"  - {path}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
