"""Local UI entry point: python web.py --port 8765."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from code_agent.web.server import main

if __name__ == "__main__":
    main()
