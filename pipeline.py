"""
Complete AI Video Generation Pipeline

Orchestrates the full workflow:
1. Generate script from user prompt using LLM
2. Generate images for each scene
3. Create multi-scene video with transitions
4. Generate voice narration
5. Generate background music
6. Merge everything into final video
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import OUTPUT_DIR, LLM_PROVIDER
from script_gen import generate_script
from multi_image_gen import generate_scene_images
from multi_video_gen import generate_multi_scene_video
from voice import generate_voice
from music_gen import generate_simple_music
from final_merge import merge_video_with_audio


def run_full_pipeline(
    user_prompt: str,
    llm_provider: Optional[str] = None,
    music_volume: float = 0.2,
    fps: int = 24,
    output_name: Optional[str] = None
) -> Path:
    """
    Run the complete AI video generation pipeline.
    
    Args:
        user_prompt: User's description of desired video
        llm_provider: LLM provider to use ("groq" or "openrouter")
        music_volume: Background music volume (0.0 to 1.0)
        fps: Frames per second for video
        output_name: Custom name for final video (optional)
    
    Returns:
        Path to the final generated video
    """
    print("="*70)
    print("🎬 AI VIDEO GENERATOR - FULL PIPELINE")
    print("="*70)
    print(f"Prompt: {user_prompt}")
    print(f"LLM Provider: {llm_provider or LLM_PROVIDER}")
    print("="*70)
    
    start_time = datetime.now()
    
    try:
        # Step 1: Generate script
        script = generate_script(user_prompt, llm_provider)
        
        # Step 2: Generate scene images
        image_paths = generate_scene_images(script['scenes'])
        
        # Step 3: Create multi-scene video
        video_path = OUTPUT_DIR / "multi_scene_video.mp4"
        generate_multi_scene_video(image_paths, script['scenes'], video_path, fps)
        
        # Step 4: Generate voice narration
        voice_path = generate_voice(script['narration'], "narration.wav")
        
        # Step 5: Generate background music
        # Calculate total video duration
        total_duration = sum(scene['duration_seconds'] for scene in script['scenes'])
        music_path = OUTPUT_DIR / "background_music.wav"
        generate_simple_music(total_duration, music_path)
        
        # Step 6: Merge everything
        if output_name:
            final_path = OUTPUT_DIR / output_name
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = OUTPUT_DIR / f"final_video_{timestamp}.mp4"
        
        merge_video_with_audio(
            video_path,
            voice_path,
            music_path,
            final_path,
            music_volume
        )
        
        # Calculate elapsed time
        elapsed = datetime.now() - start_time
        
        print("\n" + "="*70)
        print("✅ PIPELINE COMPLETE!")
        print("="*70)
        print(f"📹 Final Video: {final_path}")
        print(f"📝 Script: {OUTPUT_DIR / 'script.json'}")
        print(f"🖼️  Scene Images: {len(image_paths)} images in {OUTPUT_DIR}")
        print(f"⏱️  Total Time: {elapsed.total_seconds():.1f} seconds")
        print("="*70)
        
        # Print video details
        print("\n📊 VIDEO DETAILS:")
        print(f"  Title: {script['title']}")
        print(f"  Scenes: {len(script['scenes'])}")
        print(f"  Duration: {total_duration}s")
        print(f"  Resolution: Based on generated images")
        print(f"  FPS: {fps}")
        print("="*70)
        
        return final_path
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ PIPELINE FAILED")
        print("="*70)
        print(f"Error: {e}")
        print("="*70)
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Complete AI video generation pipeline from text prompt to final video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py --prompt "Explain how photosynthesis works"
  python pipeline.py --prompt "A journey through the solar system" --provider openrouter
  python pipeline.py --prompt "The water cycle explained" --fps 30 --music-volume 0.3
        """
    )
    
    parser.add_argument(
        "--prompt",
        required=True,
        help="Your video description/topic"
    )
    parser.add_argument(
        "--provider",
        choices=["groq", "openrouter"],
        default=None,
        help="LLM provider (default: from config)"
    )
    parser.add_argument(
        "--music-volume",
        type=float,
        default=0.2,
        help="Background music volume 0.0-1.0 (default: 0.2)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="Video frames per second (default: 24)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Custom output filename (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    try:
        final_video = run_full_pipeline(
            args.prompt,
            args.provider,
            args.music_volume,
            args.fps,
            args.output
        )
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
