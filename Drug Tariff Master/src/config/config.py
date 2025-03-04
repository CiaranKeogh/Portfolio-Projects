import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API Keys
TRUD_API_KEY = os.getenv("TRUD_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database Configuration
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "src" / "data" / "processed" / "dmd_data.db"))

# Paths
RAW_DATA_DIR = BASE_DIR / "src" / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "src" / "data" / "processed"
LOGS_DIR = BASE_DIR / "logs"

# File paths (to be downloaded)
VMP_FILE_PATH = RAW_DATA_DIR / "f_vmp2.xml"
VMPP_FILE_PATH = RAW_DATA_DIR / "f_vmpp2.xml"
AMP_FILE_PATH = RAW_DATA_DIR / "f_amp2.xml"
AMPP_FILE_PATH = RAW_DATA_DIR / "f_ampp2.xml"
GTIN_FILE_PATH = RAW_DATA_DIR / "f_gtin2.xml"

# Download Configuration
DOWNLOAD_RETRY_COUNT = int(os.getenv("DOWNLOAD_RETRY_COUNT", 3))
DOWNLOAD_RETRY_DELAY = int(os.getenv("DOWNLOAD_RETRY_DELAY", 300))  # in seconds (5 minutes)

# TRUD API Configuration
TRUD_API_BASE_URL = "https://isd.digital.nhs.uk/trud/api/v1/"
TRUD_DOWNLOAD_ITEMS = {
    "vmp": {"name": "f_vmp2.xml", "file_id": "VMP_FILE_ID"},  # Placeholder, needs real ID
    "vmpp": {"name": "f_vmpp2.xml", "file_id": "VMPP_FILE_ID"},  # Placeholder, needs real ID
    "amp": {"name": "f_amp2.xml", "file_id": "AMP_FILE_ID"},  # Placeholder, needs real ID
    "ampp": {"name": "f_ampp2.xml", "file_id": "AMPP_FILE_ID"},  # Placeholder, needs real ID
    "gtin": {"name": "f_gtin2.xml", "file_id": "GTIN_FILE_ID"},  # Placeholder, needs real ID
}

# XML Processing Configuration
XML_CHUNK_SIZE = 1000

# Batch Processing Configuration
LLM_BATCH_SIZE = int(os.getenv("LLM_BATCH_SIZE", 50))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "app.log"

# Create necessary directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True) 