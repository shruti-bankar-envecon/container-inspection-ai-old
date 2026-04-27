#!/usr/bin/env python3
"""
Start the Container Inspection Streamlit Frontend
"""
import subprocess
import sys
import time

def start_frontend():
    """Start the Streamlit frontend."""
    print("🎨 Starting Container Inspection Frontend...")
    print("🌐 Frontend will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "ui/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped.")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

if __name__ == "__main__":
    start_frontend()
