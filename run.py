#!/usr/bin/env python3
"""
Start both Django backend and React frontend dev servers
Usage: python run.py
"""

import subprocess
import sys
import time
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend-django"
FRONTEND_DIR = ROOT_DIR / "frontend-react"

def run_command(cmd, cwd, name):
    """Run command in subprocess"""
    print(f"\n▶️  Starting {name}...")
    try:
        if sys.platform == "win32":
            subprocess.Popen(cmd, cwd=cwd, shell=True)
        else:
            subprocess.Popen(cmd.split(), cwd=cwd)
        return True
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 Daily Poshan - Local Development Server")
    print("="*60)
    
    # Start backend
    backend_cmd = f"{sys.executable} manage.py runserver 0.0.0.0:8000"
    if not run_command(backend_cmd, BACKEND_DIR, "Backend (Django)"):
        return False
    
    time.sleep(2)
    
    # Start frontend on fixed port 5173
    frontend_cmd = "npm run dev -- --port 5173"
    if not run_command(frontend_cmd, FRONTEND_DIR, "Frontend (React)"):
        return False
    
    print("\n" + "="*60)
    print("✅ Servers started!")
    print("="*60)
    print("\n📍 Access points:")
    print("   Frontend: http://localhost:5173")
    print("   Backend:  http://localhost:8000")
    print("   API:      http://localhost:8000/api")
    print("\n💡 Frontend proxy: /api → http://localhost:8000/api")
    print("\nPress Ctrl+C to stop servers")
    print("="*60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
