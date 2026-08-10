"""
Final video composition with voice narration and background music.
Merges video, voice, and music with proper audio mixing.
"""

from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip


def merge_video_with_audio(
    video_path: Path,
    voice_path: Path,
    music_path: Path,
    output_path: Path,
    music_volume: float = 0.2
) -> Path:
    """
    Merge video with voice narration and background music.
    
    Args:
        video_path: Path to the video file
        voice_path: Path to the voice narration file
        music_path: Path to the background music file
        output_path: Path for the final merged video
        music_volume: Volume level for background music (0.0 to 1.0)
    
    Returns:
        Path to the final video
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not voice_path.exists():
        raise FileNotFoundError(f"Voice file not found: {voice_path}")
    if not music_path.exists():
        raise FileNotFoundError(f"Music file not found: {music_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[5/6] Merging video with audio...")
    print(f"  - Video: {video_path.name}")
    print(f"  - Voice: {voice_path.name}")
    print(f"  - Music: {music_path.name} (volume: {music_volume*100:.0f}%)")
    
    # Load video
    video_clip = VideoFileClip(str(video_path))
    video_duration = video_clip.duration
    
    # Load voice narration
    voice_clip = AudioFileClip(str(voice_path))
    
    # Load background music
    music_clip = AudioFileClip(str(music_path))
    
    # Adjust music to match video duration
    if music_clip.duration < video_duration:
        # Loop music if it's shorter than video
        num_loops = int(np.ceil(video_duration / music_clip.duration))
        music_clip = music_clip.loop(n=num_loops)
    
    # Trim music to video duration
    music_clip = music_clip.subclip(0, video_duration)
    
    # Adjust music volume
    music_clip = music_clip.volumex(music_volume)
    
    # Composite audio tracks
    # Voice takes priority, music is background
    composite_audio = CompositeAudioClip([voice_clip, music_clip])
    
    # Set audio to video
    final_clip = video_clip.set_audio(composite_audio)
    
    # Write final video
    print(f"  - Rendering final video ({video_duration:.1f}s)...")
    final_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    # Close clips
    video_clip.close()
    voice_clip.close()
    music_clip.close()
    final_clip.close()
    
    print(f"✓ Final video saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    import numpy as np
    
    parser = argparse.ArgumentParser(description="Merge video with voice and music.")
    parser.add_argument(
        "--video",
        default="outputs/multi_scene_video.mp4",
        help="Path to the video file"
    )
    parser.add_argument(
        "--voice",
        default="outputs/voice.wav",
        help="Path to the voice narration file"
    )
    parser.add_argument(
        "--music",
        default="outputs/background_music.wav",
        help="Path to the background music file"
    )
    parser.add_argument(
        "--output",
        default="outputs/final_video.mp4",
        help="Output filename for final video"
    )
    parser.add_argument(
        "--music-volume",
        type=float,
        default=0.2,
        help="Background music volume (0.0 to 1.0)"
    )
    
    args = parser.parse_args()
    
    try:
        video_path = Path(args.video)
        voice_path = Path(args.voice)
        music_path = Path(args.music)
        output_path = Path(args.output)
        
        merge_video_with_audio(
            video_path,
            voice_path,
            music_path,
            output_path,
            args.music_volume
        )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
