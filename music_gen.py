"""
Background music generation for videos.
Uses procedural audio generation to create simple royalty-free background music.
"""

from pathlib import Path
import numpy as np
from scipy.io import wavfile
from config import OUTPUT_DIR


def generate_simple_music(duration: float, output_path: Path, tempo: int = 120, key: str = "C") -> Path:
    """
    Generate simple procedural background music.
    
    Args:
        duration: Duration in seconds
        output_path: Path for output audio file
        tempo: Beats per minute
        key: Musical key (not currently used in simple generation)
    
    Returns:
        Path to generated music file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[4/6] Generating background music...")
    print(f"  - Duration: {duration}s")
    print(f"  - Tempo: {tempo} BPM")
    
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # Generate a simple ambient pad sound
    # Using multiple sine waves with slow frequency modulation
    t = np.linspace(0, duration, num_samples)
    
    # Base frequencies for a peaceful chord (C major triad with extensions)
    frequencies = [261.63, 329.63, 392.00, 523.25]  # C4, E4, G4, C5
    
    audio = np.zeros(num_samples)
    
    # Create layered ambient tones
    for i, freq in enumerate(frequencies):
        # Add slight frequency modulation for more organic sound
        modulation = 1 + 0.002 * np.sin(2 * np.pi * 0.1 * t)
        wave = np.sin(2 * np.pi * freq * modulation * t)
        
        # Apply envelope (fade in/out)
        envelope = np.ones(num_samples)
        fade_samples = int(0.5 * sample_rate)  # 0.5 second fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        # Adjust amplitude based on layer (lower frequencies louder)
        amplitude = 0.15 / (i + 1)
        audio += wave * envelope * amplitude
    
    # Add subtle rhythm with soft pulses
    pulse_freq = tempo / 60.0  # Convert BPM to Hz
    pulse = 0.05 * (1 + 0.3 * np.sin(2 * np.pi * pulse_freq * t))
    audio = audio * pulse
    
    # Normalize and convert to 16-bit integers
    audio = audio / np.max(np.abs(audio))  # Normalize to [-1, 1]
    audio = (audio * 0.3 * 32767).astype(np.int16)  # Scale to 30% volume
    
    # Save as WAV file
    wavfile.write(str(output_path), sample_rate, audio)
    
    print(f"✓ Background music saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate simple background music.")
    parser.add_argument(
        "--duration",
        type=float,
        default=20.0,
        help="Duration in seconds"
    )
    parser.add_argument(
        "--output",
        default="outputs/background_music.wav",
        help="Output audio filename"
    )
    parser.add_argument(
        "--tempo",
        type=int,
        default=120,
        help="Tempo in BPM"
    )
    
    args = parser.parse_args()
    
    try:
        output_path = Path(args.output)
        generate_simple_music(args.duration, output_path, args.tempo)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
