# Drug Tariff Master

An automated system that processes NHS Dictionary of Medicines and Devices (dm+d) data, focusing on downloading specified dm+d XML files, storing them in an SQLite database with correctly defined relationships and integrated lookup data, and providing basic search capabilities on a combined dataset.

## Project Structure

```
Drug Tariff Master/
├── src/                      # Source code
│   └── drug_tariff_master/   # Package directory
│       ├── __init__.py       # Package initialization
│       ├── main.py           # CLI entry point with command handling
│       ├── config.py         # Configuration settings including database path
│       ├── download.py       # Download mechanism for dm+d files
│       ├── setup_database.py # Database schema creation
│       ├── load_data.py      # XML parsing and database loading
│       └── utils.py          # Utility functions (logging, XML processing)
├── tests/                    # Test scripts
│   ├── unit/                 # Unit tests
│   │   ├── test_download.py  # Tests for download mechanism
│   │   └── __init__.py       # Unit test package initialization
│   ├── __init__.py           # Test package initialization
│   └── run_tests.py          # Test runner
├── data/                     # Data directory
│   ├── raw/                  # Raw XML files downloaded from TRUD
│   └── dmd.db                # SQLite database (created by setup-db)
├── logs/                     # Log files directory
│   └── *.log                 # Various log files
├── schemas/                  # XSD schema files for XML validation
│   └── *.xsd                 # Schema files for each XML type
├── .env                      # Environment variables (API keys)
├── .env.example              # Example environment variables file
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml            # Project metadata and build configuration
├── setup.cfg                 # Package configuration
└── README.md                 # This documentation file
```

## Features

### Phase 1: Download Mechanism (Implemented)
- Downloads required dm+d XML files from TRUD API using a registered API key
- Extracts ZIP files and organizes them
- Handles nested GTIN ZIP files
- Verifies the presence of all required files using pattern matching
- Logs progress and errors
- Provides visual progress bars for downloads, extraction, and verification

### Phase 2: Database Schema Definition (Implemented)
- Creates SQLite database with tables corresponding to XML structures
- Defines and enforces Primary Key (PK) and Foreign Key (FK) relationships
- Implements appropriate constraints

### Phase 3: Data Parsing & Loading (In Progress)
- Parses XML files in the correct loading order (respecting FK constraints)
- Efficiently loads data into database tables with batch processing
- Implements robust error handling and transaction management
- Validates XML files against schema definitions (XSD) before loading
- Provides detailed logging and table row counts for validation

### Phase 4: Search Data Preparation (Upcoming)
- Creates a denormalized search_data table for efficient searching
- Aggregates data from multiple related tables
- Creates appropriate indexes for search performance

### Phase 5: Basic Search Implementation (Upcoming)
- Provides a Command Line Interface (CLI) for searching the database
- Supports searching by various fields

## Setup and Requirements

### Prerequisites
- Python 3.8+
- Required Python libraries: requests, lxml, python-dotenv, urllib3, tqdm
- TRUD API key (obtained from https://isd.digital.nhs.uk/trud)

### Installation

#### Development Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd drug-tariff-master
   ```

2. Install the package in development mode:
   ```
   pip install -e .
   ```

3. Set up your TRUD API key:
   - Edit `.env` and replace `your_trud_api_key_here` with your actual TRUD API key
   - Or set it as an environment variable: `export TRUD_API_KEY=your_api_key` (Linux/macOS) or `set TRUD_API_KEY=your_api_key` (Windows)

#### Regular Installation

1. Install the package from the repository:
   ```
   pip install git+<repository-url>
   ```

2. Set your TRUD API key as an environment variable:
   - `export TRUD_API_KEY=your_api_key` (Linux/macOS)
   - `set TRUD_API_KEY=your_api_key` (Windows)

## Usage

### Using the CLI Interface

After installation, you can use the `dmd` command directly:

```
dmd [command]
```

Available commands:
- `download`: Download dm+d files from TRUD API
- `setup-db`: Set up the SQLite database schema
- `load`: Load downloaded data into the database with XML validation and transaction management

Examples:
```
# Download dm+d files
dmd download

# Set up the database schema
dmd setup-db

# Load data from downloaded files
dmd load
```

### Using the Package in Python

You can also use the package in your Python code:

```python
from drug_tariff_master import download, setup_database, load_data

# Download dm+d files
download_result = download.main()

# Set up the database schema
setup_result = setup_database.main()

# Load data into the database
loader = load_data.DataLoader()
load_result = loader.load_data()
```

### Running as a Module

If you prefer to run the code as a module without installing it:

```
python -m drug_tariff_master.main [command]
```

Example:
```
python -m drug_tariff_master.main download
```

### Running Tests

Run all tests:
```
python -m unittest discover tests
```

Run a specific test:
```
python -m unittest tests.unit.test_download
```

## User Experience Improvements

The download process includes several user experience enhancements:

1. **Progress Bars**: Visual progress bars for file downloads, ZIP extraction, and file verification
2. **Network Retries**: Automatic retry mechanism for network requests to handle transient issues
3. **Detailed Error Messages**: Specific error messages for different network or file-related issues

These features make the download process more user-friendly and robust against common failures.

## Downloaded Files

The download mechanism retrieves the following XML files:

- **VTM Files**: Virtual Therapeutic Moiety (f_vtm2_*.xml)
- **VMP Files**: Virtual Medicinal Product (f_vmp2_*.xml)
- **VMPP Files**: Virtual Medicinal Product Pack (f_vmpp2_*.xml)
- **AMP Files**: Actual Medicinal Product (f_amp2_*.xml)
- **AMPP Files**: Actual Medicinal Product Pack (f_ampp2_*.xml)
- **GTIN Files**: Global Trade Item Number (f_gtin2_*.xml)
- **Lookup Files**: Reference data (f_lookup2_*.xml)

The dates in the filenames are automatically handled by the application using pattern matching.

## Technical Details

The project follows a strict implementation plan to ensure data integrity and efficient processing:

1. **Download Handling**: Gets required files (f_vtm2_*.xml, f_vmp2_*.xml, f_vmpp2_*.xml, f_amp2_*.xml, f_ampp2_*.xml, f_gtin2_*.xml, f_lookup2_*.xml)
2. **Database Creation**: Sets up an SQLite database with tables corresponding to XML structures in the `data/` directory
3. **Relationship Implementation**: Defines and enforces PK and FK relationships between tables
4. **Data Parsing & Loading**: Reads XML files and inserts data into database tables with these features:
   - XML validation against schemas
   - Safe text extraction with error handling
   - Batch processing with fallback to individual inserts
   - Complete transaction management (all-or-nothing loading)
   - Table counts reporting and validation
5. **Lookup Integration**: Populates descriptive fields by joining main data tables with lookup tables
6. **Search Data Preparation**: Creates a denormalized table for efficient searching
7. **Basic Search**: Implements a simple CLI search tool

## Development Status

- [x] Phase 1: Download Mechanism
- [x] Phase 2: Database Schema Definition
- [ ] Phase 3: Data Parsing & Loading
- [ ] Phase 4: Search Data Preparation
- [ ] Phase 5: Basic Search Implementation 