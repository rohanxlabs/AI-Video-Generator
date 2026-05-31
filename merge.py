from pathlib import Path
from moviepy.editor import AudioFileClip, VideoFileClip


def merge_audio_video(video_path, audio_path, output_path="outputs/final_video.mp4"):
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    output_path = Path(output_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with VideoFileClip(str(video_path)) as video_clip, AudioFileClip(str(audio_path)) as audio_clip:
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None,
        )

    print(f"Merged video saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Combine a generated video and audio file into one output.")
    parser.add_argument("--video", default="outputs/short_video.mp4", help="Path to the video file.")
    parser.add_argument("--audio", default="outputs/voice.mp3", help="Path to the audio file.")
    parser.add_argument("--output", default="outputs/final_video.mp4", help="Output merged video filename.")
    args = parser.parse_args()
    merge_audio_video(args.video, args.audio, args.output)
