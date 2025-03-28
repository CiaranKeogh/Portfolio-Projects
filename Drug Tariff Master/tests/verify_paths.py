"""
Simple script to verify paths and imports from the tests directory.
"""
import os
import sys
from pathlib import Path

# Print current directory
print(f"Current directory: {os.getcwd()}")

# Print file location
file_path = Path(__file__).resolve()
print(f"File path: {file_path}")

# Print parent directory (should be tests)
parent_dir = file_path.parent
print(f"Parent directory: {parent_dir}")

# Print project root directory
project_root = file_path.parent.parent
print(f"Project root: {project_root}")

# Print src directory
src_dir = project_root / "src"
print(f"Src directory: {src_dir}")
print(f"Src directory exists: {src_dir.exists()}")

# Add src to path and try to import config
sys.path.insert(0, str(src_dir))
print("\nTrying to import config module...")
try:
    import config
    print("Config module imported successfully!")
    print(f"TRUD API BASE URL: {config.TRUD_API_BASE_URL}")
except ImportError as e:
    print(f"Error importing config: {e}")

print("\nAll paths verified.") 