from pathlib import Path
from PIL import Image
from moviepy.editor import ImageSequenceClip
import numpy as np


def generate_video_from_images(image_path, output_path="outputs/short_video.mp4", fps=8, frames=24):
    image_path = Path(image_path)
    output_path = Path(output_path)

    print("Loading image:", image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    frame_images = []
    print("Generating video frames...")
    for i in range(frames):
        zoom = 1 + (i * 0.003)
        new_w, new_h = int(w * zoom), int(h * zoom)
        frame = img.resize((new_w, new_h))
        frame = frame.crop(
            (
                (new_w - w) // 2,
                (new_h - h) // 2,
                (new_w + w) // 2,
                (new_h + h) // 2,
            )
        )
        frame_images.append(np.array(frame))

    if not frame_images:
        raise RuntimeError("No frames were generated for the video.")

    clip = ImageSequenceClip(frame_images, fps=fps)
    clip.write_videofile(str(output_path), codec="libx264", audio=False, verbose=False, logger=None)
    print(f"Video saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a short zoom-style video from an image.")
    parser.add_argument("--image", default="outputs/frame1.png", help="Path to the source image.")
    parser.add_argument("--output", default="outputs/short_video.mp4", help="Output video filename.")
    parser.add_argument("--fps", type=int, default=8, help="Frames per second for the output video.")
    parser.add_argument("--frames", type=int, default=24, help="Number of frames to generate.")
    args = parser.parse_args()
    generate_video_from_images(args.image, args.output, args.fps, args.frames)
