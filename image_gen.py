from pathlib import Path
from huggingface_hub import InferenceClient
from PIL import Image
from config import HF_TOKEN, IMAGE_MODEL, OUTPUT_DIR


def generate_image(prompt, filename="frame1.png"):
    """
    Generate an image from a text prompt using Hugging Face Inference API.
    
    Args:
        prompt: Text description of the image to generate
        filename: Output filename for the image
    
    Returns:
        Path to the generated image
    
    Raises:
        EnvironmentError: If HF_TOKEN is not set
        RuntimeError: If image generation fails
    """
    if not HF_TOKEN:
        raise EnvironmentError(
            "HF_TOKEN environment variable is required to generate images.\n"
            "Get your token from: https://huggingface.co/settings/tokens\n"
            "Set it in your .env file: HF_TOKEN=your_token_here"
        )
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    
    try:
        client = InferenceClient(model=IMAGE_MODEL, token=HF_TOKEN)
        image = client.text_to_image(prompt)
        
        if not isinstance(image, Image.Image):
            raise RuntimeError("Unexpected response from the image generation model.")
        
        image.save(output_path)
        print(f"✓ Image saved to {output_path}")
        return output_path
        
    except Exception as e:
        raise RuntimeError(f"Image generation failed: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a single image from a text prompt.")
    parser.add_argument(
        "--prompt",
        default="Pixar style cute horse running in city street, cinematic 3D, vibrant colors",
        help="Text prompt to generate the image.",
    )
    parser.add_argument("--output", default="frame1.png", help="Output image filename.")
    args = parser.parse_args()
    generate_image(args.prompt, args.output)
