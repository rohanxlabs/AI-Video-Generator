"""
Multi-scene video generation with smooth transitions.
Creates a video from multiple scene images with specified durations.
"""

from pathlib import Path
from typing import List, Dict
from PIL import Image
from moviepy import ImageClip, concatenate_videoclips
import numpy as np


def create_zoom_clip(image_path: Path, duration: float, fps: int = 24) -> ImageClip:
    """
    Create a subtle zoom effect clip from an image.
    
    Args:
        image_path: Path to the image file
        duration: Duration of the clip in seconds
        fps: Frames per second
    
    Returns:
        MoviePy ImageClip with zoom effect
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    
    # Create frames with subtle zoom
    frames = []
    num_frames = int(duration * fps)
    
    for i in range(num_frames):
        progress = i / max(num_frames - 1, 1)
        zoom = 1.0 + (progress * 0.05)  # Subtle 5% zoom
        
        new_w, new_h = int(w * zoom), int(h * zoom)
        frame = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        frame = frame.crop((left, top, left + w, top + h))
        
        frames.append(np.array(frame))
    
    # Create clip from frames
    clip = ImageClip(frames[0], duration=duration)
    clip = clip.set_fps(fps)
    
    # Apply manual frame sequence
    def make_frame(t):
        frame_idx = min(int(t * fps), len(frames) - 1)
        return frames[frame_idx]
    
    clip = clip.fl(lambda gf, t: make_frame(t))
    
    return clip


def generate_multi_scene_video(
    image_paths: List[Path],
    scenes: List[Dict],
    output_path: Path,
    fps: int = 24
) -> Path:
    """
    Generate a video from multiple scene images with specified durations.
    
    Args:
        image_paths: List of paths to scene images
        scenes: List of scene dictionaries with duration_seconds
        output_path: Path for the output video
        fps: Frames per second
    
    Returns:
        Path to the generated video
    """
    if len(image_paths) != len(scenes):
        raise ValueError(f"Mismatch: {len(image_paths)} images but {len(scenes)} scenes")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[3/6] Creating multi-scene video...")
    print(f"  - {len(scenes)} scenes")
    print(f"  - {fps} FPS")
    
    clips = []
    total_duration = 0
    
    for i, (image_path, scene) in enumerate(zip(image_paths, scenes), 1):
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        duration = scene.get('duration_seconds', 3)
        total_duration += duration
        
        print(f"  [{i}/{len(scenes)}] Scene {scene.get('scene_number', i)}: {duration}s")
        
        # Create clip with zoom effect
        clip = create_zoom_clip(image_path, duration, fps)
        clips.append(clip)
    
    # Concatenate all clips
    print(f"  - Total duration: {total_duration}s")
    print(f"  - Rendering video...")
    
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio=False,
        fps=fps,
        verbose=False,
        logger=None
    )
    
    print(f"✓ Multi-scene video saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import json
    import argparse
    from config import OUTPUT_DIR
    
    parser = argparse.ArgumentParser(description="Create multi-scene video from generated images.")
    parser.add_argument(
        "--script",
        default="outputs/script.json",
        help="Path to the script JSON file"
    )
    parser.add_argument(
        "--output",
        default="outputs/multi_scene_video.mp4",
        help="Output video filename"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Frames per second"
    )
    
    args = parser.parse_args()
    
    # Load script
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        exit(1)
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # Find generated scene images
    scenes = script['scenes']
    image_paths = []
    for scene in scenes:
        scene_num = scene['scene_number']
        image_path = OUTPUT_DIR / f"scene_{scene_num:02d}.png"
        if not image_path.exists():
            print(f"Error: Scene image not found: {image_path}")
            print("Run multi_image_gen.py first to generate scene images.")
            exit(1)
        image_paths.append(image_path)
    
    # Generate video
    try:
        output_path = Path(args.output)
        generate_multi_scene_video(image_paths, scenes, output_path, args.fps)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
