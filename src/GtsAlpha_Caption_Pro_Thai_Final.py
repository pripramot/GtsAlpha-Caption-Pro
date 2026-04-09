# src/GtsAlpha_Caption_Pro_Thai_Final.py
# Backward-compatible entry point — delegates to the modular package.
# Usage:  python src/GtsAlpha_Caption_Pro_Thai_Final.py

import os
import sys

# Ensure the src directory is on the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gtsalpha.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
