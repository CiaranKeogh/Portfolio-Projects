# Drug Tariff Master

An automated system that processes NHS Dictionary of Medicines and Devices (dm+d) data, focusing on downloading specified dm+d XML files, storing them in an SQLite database with correctly defined relationships and integrated lookup data, and providing basic search capabilities on a combined dataset.

## Project Structure

```
Drug Tariff Master/
├── src/                    # Source code
│   ├── main.py             # Main entry point for the application
│   ├── download_dmd.py     # Download mechanism for dm+d files
│   ├── config.py           # Configuration settings
│   ├── utils.py            # Utility functions (logging, etc.)
│   ├── setup_database.py   # Database schema definition (upcoming)
│   ├── load_data.py        # Data parsing and loading (upcoming)
│   ├── search_dmd.py       # Basic search implementation (upcoming)
├── tests/                  # Test scripts
│   ├── test_download.py    # Tests for download mechanism
│   ├── test_api_key.py     # Script to test API key configuration
│   ├── run_test.py         # Script to test application setup and display file info
│   ├── run_tests.py        # Script to run all tests
├── data/                   # Data files
│   ├── raw/                # Raw XML files downloaded from TRUD
├── logs/                   # Log files
├── schemas/                # XSD schema files
├── .env                    # Environment variables (API keys, etc.)
├── .env.example            # Example environment variables file
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Features

### Phase 1: Download Mechanism (Implemented)
- Downloads required dm+d XML files from TRUD API using a registered API key
- Extracts ZIP files and organizes them
- Handles nested GTIN ZIP files
- Verifies the presence of all required files using pattern matching
- Logs progress and errors

### Phase 2: Database Schema Definition (Upcoming)
- Creates SQLite database with tables corresponding to XML structures
- Defines and enforces Primary Key (PK) and Foreign Key (FK) relationships
- Implements appropriate constraints

### Phase 3: Data Parsing & Loading (Upcoming)
- Parses XML files in the correct loading order (respecting FK constraints)
- Efficiently loads data into database tables
- Performs error handling and logging

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
- Required Python libraries: requests, lxml, python-dotenv
- TRUD API key (obtained from https://isd.digital.nhs.uk/trud)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd drug-tariff-master
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your TRUD API key:
   - Edit `.env` and replace `your_trud_api_key_here` with your actual TRUD API key
   - Or set it as an environment variable: `export TRUD_API_KEY=your_api_key` (Linux/macOS) or `set TRUD_API_KEY=your_api_key` (Windows)

4. Test your API key configuration:
   ```
   python -m tests.test_api_key
   ```

5. Run the general test script to verify setup:
   ```
   python -m tests.run_test
   ```

## Usage

### Using the CLI Interface

The application provides a unified command-line interface through `main.py`:

```
python -m src.main [command]
```

Available commands:
- `download`: Download dm+d files from TRUD API

Example:
```
python -m src.main download
```

### Direct Usage

#### Downloading Data
```
python -m src.download_dmd
```

This will:
1. Connect to the TRUD API to get the latest release URL
2. Download the main ZIP file to `data/raw/dmd_release.zip`
3. Extract all files to the `data/raw/` directory
4. Find and extract the nested GTIN ZIP file
5. Verify that all required files are present using pattern matching

### Running Tests

Run all tests:
```
python -m tests.run_tests
```

Run a specific test:
```
python -m unittest tests.test_download
```

Check the API key and system setup:
```
python -m tests.test_api_key
python -m tests.run_test
```

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
2. **Database Creation**: Sets up an SQLite database with tables corresponding to XML structures
3. **Relationship Implementation**: Defines and enforces PK and FK relationships between tables
4. **Data Parsing & Loading**: Reads XML files and inserts data into database tables
5. **Lookup Integration**: Populates descriptive fields by joining main data tables with lookup tables
6. **Search Data Preparation**: Creates a denormalized table for efficient searching
7. **Basic Search**: Implements a simple CLI search tool

## Development Status

- [x] Phase 1: Download Mechanism
- [ ] Phase 2: Database Schema Definition
- [ ] Phase 3: Data Parsing & Loading
- [ ] Phase 4: Search Data Preparation
- [ ] Phase 5: Basic Search Implementation 