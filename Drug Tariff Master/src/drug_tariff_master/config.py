"""
Configuration settings for the Drug Tariff Master application.
"""
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
LOGS_DIR = BASE_DIR / "logs"
SCHEMAS_DIR = BASE_DIR / "schemas"

# Database settings
DATABASE_FILE = BASE_DIR / "dmd.db"

# TRUD API settings
TRUD_API_KEY = os.getenv("TRUD_API_KEY")
TRUD_API_BASE_URL = "https://isd.digital.nhs.uk/trud/api/v1/keys"
# DMD item ID on TRUD (from URL: https://isd.digital.nhs.uk/trud/user/guest/group/0/pack/6/subpack/24/releases)
DMD_ITEM_ID = "24"

# According to TRUD API docs, the correct URL format is:
# https://isd.digital.nhs.uk/trud/api/v1/keys/{api_key}/items/{item_id}/releases

# Required file patterns (using regular expressions to match files with date suffixes)
# Based on the actual files in the download
REQUIRED_FILE_PATTERNS = [
    r"f_vtm2_\d+\.xml",      # VTM file
    r"f_vmp2_\d+\.xml",      # VMP file
    r"f_vmpp2_\d+\.xml",     # VMPP file
    r"f_amp2_\d+\.xml",      # AMP file
    r"f_ampp2_\d+\.xml",     # AMPP file
    r"f_gtin2_\d+\.xml",     # GTIN file
    r"f_lookup2_\d+\.xml",   # Lookup file
]

# Function to check if a filename matches one of our required patterns
def matches_required_pattern(filename):
    for pattern in REQUIRED_FILE_PATTERNS:
        if re.match(pattern, filename):
            return True
    return False

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCHEMAS_DIR, exist_ok=True) 