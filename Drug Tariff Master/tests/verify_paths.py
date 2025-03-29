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

# Print package directory
package_dir = project_root / "src" / "drug_tariff_master"
print(f"Package directory: {package_dir}")
print(f"Package directory exists: {package_dir.exists()}")

# Try to import the package
print("\nTrying to import drug_tariff_master package...")
try:
    import drug_tariff_master.config as config
    print("Config module imported successfully!")
    print(f"TRUD API BASE URL: {config.TRUD_API_BASE_URL}")
except ImportError as e:
    print(f"Error importing config: {e}")

print("\nAll paths verified.") 