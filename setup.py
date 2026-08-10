"""
Setup script for AI Video Generator
Handles virtual environment creation and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("="*60)
    print("🎬 AI Video Generator - Setup")
    print("="*60)
    
    project_dir = Path(__file__).parent
    venv_dir = project_dir / "venv"
    
    # Check if venv exists
    if venv_dir.exists():
        print(f"\n✓ Virtual environment already exists at: {venv_dir}")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_dir)
        else:
            print("Using existing virtual environment.")
    
    # Create virtual environment if needed
    if not venv_dir.exists():
        if not run_command(
            f'python -m venv venv',
            "Creating virtual environment"
        ):
            print("\n❌ Failed to create virtual environment")
            return False
    
    # Determine Python executable in venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Upgrade pip
    if not run_command(
        f'"{python_exe}" -m pip install --upgrade pip',
        "Upgrading pip"
    ):
        print("\n⚠️  Warning: Failed to upgrade pip, continuing anyway...")
    
    # Install requirements
    requirements_file = project_dir / "requirements.txt"
    if not requirements_file.exists():
        print(f"\n❌ requirements.txt not found at: {requirements_file}")
        return False
    
    if not run_command(
        f'"{python_exe}" -m pip install -r requirements.txt',
        "Installing dependencies from requirements.txt"
    ):
        print("\n❌ Failed to install dependencies")
        return False
    
    # Check if .env exists
    env_file = project_dir / ".env"
    env_example = project_dir / ".env.example"
    
    if not env_file.exists():
        print("\n" + "="*60)
        print("⚠️  API Keys Configuration Needed")
        print("="*60)
        print(f"\nNo .env file found. Creating from template...")
        
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print(f"✓ Created .env file from .env.example")
        else:
            print("❌ .env.example not found")
        
        print("\n📝 You need to configure API keys in .env file:")
        print("   1. HF_TOKEN - Get from: https://huggingface.co/settings/tokens")
        print("   2. GROQ_API_KEY - Get from: https://console.groq.com/")
        print("   3. OPENROUTER_API_KEY - Get from: https://openrouter.ai/")
        print("\nEdit .env and add your API keys before running the pipeline.")
    else:
        print(f"\n✓ .env file found at: {env_file}")
    
    # Check FFmpeg
    print("\n" + "="*60)
    print("🎥 Checking FFmpeg Installation")
    print("="*60)
    try:
        result = subprocess.run(
            "ffmpeg -version",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ FFmpeg is installed")
        # Show first line with version
        first_line = result.stdout.split('\n')[0]
        print(f"  {first_line}")
    except subprocess.CalledProcessError:
        print("❌ FFmpeg is NOT installed")
        print("\nFFmpeg is required for video processing.")
        print("\nInstall FFmpeg:")
        if sys.platform == "win32":
            print("  - Using Chocolatey: choco install ffmpeg")
            print("  - Or download from: https://ffmpeg.org/download.html")
        elif sys.platform == "darwin":
            print("  - Using Homebrew: brew install ffmpeg")
        else:
            print("  - Using apt: sudo apt install ffmpeg")
    
    # Success message
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print(f"  1. Activate the virtual environment:")
    if sys.platform == "win32":
        print(f"     .\\venv\\Scripts\\activate")
    else:
        print(f"     source venv/bin/activate")
    print(f"\n  2. Configure your API keys in .env file")
    print(f"\n  3. Run the pipeline:")
    print(f'     python pipeline.py --prompt "Your video topic"')
    print("\n" + "="*60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
