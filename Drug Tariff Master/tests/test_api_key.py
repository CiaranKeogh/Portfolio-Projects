"""
Test that the TRUD API key is set correctly.
"""
import sys
import os
from pathlib import Path

# Add the src directory to the path to allow imports from the project
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import TRUD_API_KEY


def main():
    """Check if the TRUD API key is set."""
    if not TRUD_API_KEY:
        print("ERROR: TRUD API key not found.")
        print("Please set the TRUD_API_KEY environment variable or update the .env file.")
        return 1
    
    # Mask most of the API key for security
    if len(TRUD_API_KEY) > 8:
        masked_key = TRUD_API_KEY[:4] + '*' * (len(TRUD_API_KEY) - 8) + TRUD_API_KEY[-4:]
    else:
        masked_key = '****'
    
    print(f"SUCCESS: TRUD API key found: {masked_key}")
    print("You can now run 'python src/main.py download' to download the dm+d files.")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 