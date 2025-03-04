"""
Configuration file for the Drug Tariff Master application.
Contains constants, file paths, and settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project structure
ROOT_DIR = Path(__file__).parent.parent.absolute()
DATA_DIR = ROOT_DIR / 'data'
SCHEMAS_DIR = ROOT_DIR / 'schemas'
LOG_DIR = ROOT_DIR / 'logs'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# API Endpoints
TRUD_API_KEY = os.environ.get('TRUD_API_KEY', '')
TRUD_API_URL = 'https://isd.digital.nhs.uk/trud/api/v1/keys/{}/items/24/releases?latest'.format(TRUD_API_KEY)

# Database
DB_PATH = DATA_DIR / 'dmd_data.db'

# File patterns to process
FILE_PATTERNS = {
    'vtm': {'pattern': 'f_vtm2_*.xml', 'schema': SCHEMAS_DIR / 'vtm_v2_3.xsd'},
    'vmp': {'pattern': 'f_vmp2_*.xml', 'schema': SCHEMAS_DIR / 'vmp_v2_3.xsd'},
    'vmpp': {'pattern': 'f_vmpp2_*.xml', 'schema': SCHEMAS_DIR / 'vmpp_v2_3.xsd'},
    'amp': {'pattern': 'f_amp2_*.xml', 'schema': SCHEMAS_DIR / 'amp_v2_3.xsd'},
    'ampp': {'pattern': 'f_ampp2_*.xml', 'schema': SCHEMAS_DIR / 'ampp_v2_3.xsd'},
    'gtin': {'pattern': 'f_gtin2_*.xml', 'schema': SCHEMAS_DIR / 'gtin_v2_0.xsd'},
    'lookup': {'pattern': 'f_lookup2_*.xml', 'schema': SCHEMAS_DIR / 'lookup_v2_3.xsd'},
    'ingredient': {'pattern': 'f_ingredient*.xml', 'schema': SCHEMAS_DIR / 'ingredient_v2_3.xsd'},
    'bnf': {'pattern': 'f_bnf_*.xml', 'schema': SCHEMAS_DIR / 'bnf_v2_3.xsd'},
    'history': {'pattern': 'f_history_*.xml', 'schema': SCHEMAS_DIR / 'history_v2_3.xsd'},
    'vtming': {'pattern': 'f_vtming_*.xml', 'schema': SCHEMAS_DIR / 'vtming_v2_3.xsd'},
}

# Processing config
CHUNK_SIZE = 1000

# Scheduling
DOWNLOAD_CRON = '0 2 * * 1'  # Every Monday at 02:00 UTC

# Logging config
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOG_DIR / 'app.log'
DOWNLOAD_LOG_FILE = LOG_DIR / 'download.log'

# Download retry settings
MAX_DOWNLOAD_RETRIES = 3
RETRY_DELAY_SECONDS = 300  # 5 minutes 