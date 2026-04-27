#!/usr/bin/env python3
"""
Start the Container Inspection API Backend
"""
import subprocess
import sys
import time

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting Container Inspection API Backend...")
    print("📍 API will be available at: http://127.0.0.1:8000")
    print("📖 API Documentation: http://127.0.0.1:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped.")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

if __name__ == "__main__":
    start_backend()
