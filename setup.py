#!/usr/bin/env python3
"""
Setup script for ESG Recommender with Ollama
"""

import subprocess
import sys
import osollama --version


def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    print("🔧 ESG Recommender Setup")
    print("=" * 40)
    
    # Check if Ollama is installed
    print("1. Checking Ollama installation...")
    if not run_command("ollama --version", check=False):
        print("❌ Ollama not found. Please install from https://ollama.ai/")
        print("   After installation, run this script again.")
        return
    
    # Check available models
    print("2. Checking available models...")
    result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
    
    if "llama2" not in result.stdout:
        print("3. Pulling llama2:7b model (this may take a few minutes)...")
        if run_command("ollama pull llama2:7b"):
            print("✅ Model downloaded successfully")
        else:
            print("❌ Failed to download model")
            return
    else:
        print("✅ Model found")
    
    # Install Python dependencies
    print("4. Installing Python dependencies...")
    if run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("✅ Dependencies installed")
    else:
        print("❌ Failed to install dependencies")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python main.py")
    print("\nMake sure Ollama is running:")
    print("  ollama serve")

if __name__ == "__main__":
    main()