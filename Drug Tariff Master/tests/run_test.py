"""
Script to test the functionality of the application.
"""
import os
import sys
import re
from pathlib import Path

# Print Python version and environment information
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test API key configuration
print("\nTesting API key configuration:")
from drug_tariff_master.config import TRUD_API_KEY, RAW_DATA_DIR, REQUIRED_FILE_PATTERNS

if not TRUD_API_KEY:
    print("ERROR: TRUD API key not found.")
    print("Please set the TRUD_API_KEY environment variable or update the .env file.")
    sys.exit(1)

# Mask most of the API key for security
if len(TRUD_API_KEY) > 8:
    masked_key = TRUD_API_KEY[:4] + '*' * (len(TRUD_API_KEY) - 8) + TRUD_API_KEY[-4:]
else:
    masked_key = '****'

print(f"SUCCESS: TRUD API key found: {masked_key}")

# Test imports
print("\nTesting module imports:")
print("Importing drug_tariff_master.download_dmd...", end="")
from drug_tariff_master import download_dmd
print(" OK")

print("Importing drug_tariff_master.utils...", end="")
from drug_tariff_master import utils
print(" OK")

# Test directory structure
print("\nTesting directory structure:")
directories = ["data/raw", "logs", "schemas", "src/drug_tariff_master", "tests"]
for directory in directories:
    path = Path(__file__).resolve().parent.parent / directory
    if path.exists() and path.is_dir():
        print(f"Directory {directory} exists: OK")
    else:
        print(f"Directory {directory} does not exist: ERROR")

# Check downloaded files
print("\nChecking for downloaded dm+d files:")
xml_files = list(RAW_DATA_DIR.glob("*.xml"))
if xml_files:
    print(f"Found {len(xml_files)} XML files in data/raw directory:")
    total_size = 0
    
    # Create a dictionary of file patterns
    pattern_dict = {}
    for pattern in REQUIRED_FILE_PATTERNS:
        pattern_dict[pattern] = []
    
    # Match files to patterns
    for file_path in xml_files:
        file_name = file_path.name
        file_size = file_path.stat().st_size
        total_size += file_size
        
        # Check which pattern this file matches
        for pattern in REQUIRED_FILE_PATTERNS:
            if re.match(pattern, file_name):
                pattern_dict[pattern].append((file_name, file_size))
                break
    
    # Display the files grouped by pattern
    for pattern, files in pattern_dict.items():
        print(f"\n  Pattern: {pattern}")
        for file_name, file_size in files:
            size_mb = file_size / (1024 * 1024)
            print(f"    - {file_name} ({size_mb:.2f} MB)")
    
    print(f"\nTotal XML data size: {total_size / (1024 * 1024):.2f} MB")
else:
    print("No dm+d XML files found in data/raw directory. Run 'dmd download' first.")

print("\nAll tests completed. The application is ready to use.")
print("You can now run 'dmd download' to download the dm+d files.") 