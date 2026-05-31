from pathlib import Path
from image_gen import generate_image
from video_gen import generate_video_from_images
from voice import generate_voice
from merge import merge_audio_video
from config import OUTPUT_DIR


def run(prompt, text, image_name='frame1.png', video_name='short_video.mp4', audio_name='voice.mp3', final_name='final_video.mp4', fps=8, frames=24):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image_path = generate_image(prompt, image_name)
    video_path = generate_video_from_images(image_path, OUTPUT_DIR / video_name, fps=fps, frames=frames)
    audio_path = generate_voice(text, audio_name)
    merged_path = merge_audio_video(video_path, audio_path, OUTPUT_DIR / final_name)
    print(f'Final output: {merged_path}')
    return merged_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run the full AI video generation pipeline.')
    parser.add_argument('--prompt', default='A cinematic 3D scene of a futuristic city', help='Text prompt for the image generator.')
    parser.add_argument('--text', default='Welcome to the AI video generator.', help='Speech text for the voice generator.')
    parser.add_argument('--image', default='frame1.png', help='Generated image filename.')
    parser.add_argument('--video', default='short_video.mp4', help='Generated video filename.')
    parser.add_argument('--audio', default='voice.mp3', help='Generated audio filename.')
    parser.add_argument('--output', default='final_video.mp4', help='Final merged video filename.')
    parser.add_argument('--fps', type=int, default=8, help='Video fps.')
    parser.add_argument('--frames', type=int, default=24, help='Video frame count.')
    args = parser.parse_args()
    run(args.prompt, args.text, args.image, args.video, args.audio, args.output, fps=args.fps, frames=args.frames)
