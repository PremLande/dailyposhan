#!/usr/bin/env python3
"""
Setup script - Install dependencies for both backend and frontend
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend-django"
FRONTEND_DIR = ROOT_DIR / "frontend-react"

def run_cmd(cmd, cwd, description):
    """Run a command"""
    print(f"\n▶️  {description}...")
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ {result.stderr}")
            return False
        print("✅ Done")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("⚙️  Daily Poshan - Setup")
    print("="*60)
    
    # Backend setup
    print("\n🐍 Backend Setup")
    print("-" * 60)
    if not run_cmd(f"{sys.executable} -m pip install -r requirements.txt",
                  BACKEND_DIR, "Installing Python dependencies"):
        return False
    
    if not run_cmd(f"{sys.executable} manage.py migrate",
                  BACKEND_DIR, "Running database migrations"):
        return False
    
    # Frontend setup
    print("\n⚛️  Frontend Setup")
    print("-" * 60)
    if not run_cmd("npm install", FRONTEND_DIR, "Installing Node dependencies"):
        return False
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\n📝 Next steps:")
    print("   1. Run: python run.py")
    print("   2. Test: python test_api.py")
    print("   3. Browser: http://localhost:5173")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
