# app.py (à la racine)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from api.streamlit_app import main

if __name__ == "__main__":
    main()