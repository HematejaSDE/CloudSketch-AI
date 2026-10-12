"""
CloudSketch AI - Streamlit Community Cloud Entrypoint
Delegates execution to frontend/app.py
"""
import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from frontend.app import main

if __name__ == "__main__":
    main()
