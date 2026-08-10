from pathlib import Path
from gtts import gTTS
from config import OUTPUT_DIR


def generate_voice(text, filename="voice.wav", lang="en", slow=False):
    """
    Generate voice narration from text using Google Text-to-Speech.
    
    Args:
        text: Text to convert to speech
        filename: Output filename for audio
        lang: Language code (default: "en")
        slow: Whether to speak slowly
    
    Returns:
        Path to the generated audio file
    
    Raises:
        ValueError: If text is empty
        RuntimeError: If TTS generation fails
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(str(output_path))
        print(f"✓ Voice file saved at: {output_path}")
        return output_path
        
    except Exception as e:
        raise RuntimeError(f"Voice generation failed: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a short voice audio file from text.")
    parser.add_argument("--text", default="Hello, this is a test voice message.", help="Text to synthesize.")
    parser.add_argument("--output", default="voice.wav", help="Output audio filename.")
    parser.add_argument("--lang", default="en", help="Language code for speech synthesis.")
    parser.add_argument("--slow", action="store_true", help="Read text more slowly.")
    args = parser.parse_args()
    generate_voice(args.text, args.output, args.lang, args.slow)
