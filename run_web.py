#!/usr/bin/env python3
"""
ESG Recommender Web Application Launcher
"""

import os
import sys
import subprocess
from app import app

def check_ollama_setup():
    """Check if Ollama is properly set up"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Ollama is not installed or not in PATH")
            print("Please install Ollama from https://ollama.ai/")
            return False
        
        # Check if we have at least one model
        if "llama2" not in result.stdout and "gemma" not in result.stdout and "mistral" not in result.stdout:
            print("⚠️  No suitable models found.")
            print("Please install a model with: ollama pull llama2:7b")
            return False
        
        return True
        
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("Please install Ollama from https://ollama.ai/")
        return False

def main():
    print("🚀 ESG Recommender Web Application")
    print("=" * 50)
    
    # Check Ollama setup
    if not check_ollama_setup():
        print("\n💡 To use the AI recommendations, please:")
        print("1. Install Ollama from https://ollama.ai/")
        print("2. Pull a model: ollama pull llama2:7b")
        print("3. Start Ollama service: ollama serve")
        print("\n🌐 Starting web app anyway (browse-only mode)...")
    else:
        print("✅ Ollama is ready for AI recommendations")
    
    print("\n🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5550")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5550)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
