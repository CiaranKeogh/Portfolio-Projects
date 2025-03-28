# Drug Tariff Processor

## Project Overview

This application processes NHS Dictionary of Medicines and Devices (dm+d) data to match various medical product entities and calculate missing drug tariff prices. The system automates the download, parsing, and processing of NHS TRUD data files to create a structured database with comprehensive price information.

### Key Objectives

1. Download and process NHS dm+d XML files weekly
2. Match Actual Medicinal Product Packs (AMPP) to Virtual Medicinal Product Packs (VMPP)
3. Link Global Trade Item Numbers (GTIN) to AMPP
4. Calculate missing drug tariff prices using defined rules
5. Create a unified search table for efficient querying

## Current Implementation Status

- [x] Download functionality to retrieve dm+d files from NHS TRUD
- [x] Extract nested ZIP files and find required XML files
- [x] Process all dm+d XML files, not just the required ones
- [x] Robust error handling and retry logic
- [x] Logging of download process
- [x] Handling of date-suffixed filenames (e.g., f_amp2_3200325.xml)
- [ ] Data parsing and database creation
- [ ] Price calculation for missing tariff prices
- [ ] Search functionality

## Requirements

- Python 3.8 or higher
- NHS TRUD API key (register at [TRUD](https://isd.digital.nhs.uk/))

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd "Drug Tariff Master"
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your TRUD API key:
   ```
   cp .env.example .env
   # Edit .env and add your TRUD_API_KEY
   ```

## Usage

### Downloading dm+d Files

To download the latest dm+d files from NHS TRUD:

```bash
python main.py --download-only
```

You can also provide the API key directly:

```bash
python main.py --download-only --api-key YOUR_API_KEY
```

Additional options:

```
--output-dir DATA_DIR   Directory to save downloaded files (default: data)
--retries COUNT         Number of retries for failed downloads (default: 3)
--retry-delay SECONDS   Delay between retries in seconds (default: 300)
```

### Handling of File Versioning

The NHS TRUD service provides files with date or version suffixes in the filenames (e.g., `f_amp2_3200325.xml`). The download module automatically handles these varying filenames by:

1. Using regular expressions to identify files regardless of their date suffix
2. Standardizing filenames internally to a consistent format (e.g., `f_amp2.xml`)
3. Maintaining a mapping between standardized names and actual files on disk

This approach ensures the application will continue to work correctly with future releases that might use different date or version suffixes.

### Complete Data Processing

The application processes all XML files in the dm+d package, including:

- Core files required for pricing functionality:
  - `f_vmp2_*.xml` (Virtual Medicinal Product)
  - `f_vmpp2_*.xml` (Virtual Medicinal Product Pack)
  - `f_amp2_*.xml` (Actual Medicinal Product)
  - `f_ampp2_*.xml` (Actual Medicinal Product Pack)
  - `f_gtin2_*.xml` (GTIN mappings)

- Additional files for enhanced functionality:
  - `f_ingredient2_*.xml` (Ingredients)
  - `f_lookup2_*.xml` (Lookup tables)
  - `f_vtm2_*.xml` (Virtual Therapeutic Moieties)

This comprehensive approach ensures that all data from the dm+d package is available for advanced features and analysis.

## Detailed Code Architecture

### Project Structure

```
Drug Tariff Master/
├── config/                 # Configuration and settings
│   └── logging_config.py   # Logging setup with timestamped files
├── data/                   # Storage for downloaded and processed data
├── logs/                   # Application logs with timestamps
├── src/                    # Source code modules
│   ├── __init__.py         # Source package initialization
│   └── download/           # Download functionality
│       ├── __init__.py     # Exports download module functions
│       └── downloader.py   # Core download and extraction logic
├── .env                    # Environment variables (API keys)
├── .env.example            # Template for environment variables
├── .gitignore              # Specifies files to exclude from version control
├── main.py                 # Application entry point with CLI
└── requirements.txt        # Python dependencies
```

### Component Details

#### 1. Download Module (`src/download/`)

**Purpose**: Handle downloading and extracting dm+d files from NHS TRUD.

**Key Files**:
- `downloader.py`: Contains functions for:
  - `request_json()`: Fetches JSON data from API endpoints with retry logic
  - `download_file()`: Downloads files with progress tracking and retry logic
  - `extract_zip()`: Extracts files from ZIP archives with specific file selection
  - `download_dmd_files()`: Orchestrates the entire download process

**Flow**:
1. Requests latest release information from NHS TRUD API
2. Downloads the main ZIP file
3. Extracts XML files from the main archive
4. Finds and processes the nested ZIP containing GTIN data
5. Uses regex pattern matching to locate files regardless of date suffixes
6. Processes both core files and additional files from the dm+d package
7. Returns paths to all extracted files with standardized names

#### 2. Configuration Module (`config/`)

**Purpose**: Centralize application configuration.

**Key Files**:
- `logging_config.py`: Sets up logging with:
  - Timestamped log files
  - Both file and console output
  - Configurable log levels

#### 3. Main Application (`main.py`)

**Purpose**: Provide CLI interface and orchestrate application flow.

**Key Features**:
- Command-line argument parsing
- Environment variable loading
- Error handling and logging
- Execution flow control

**Execution Flow**:
1. Loads environment variables
2. Parses command-line arguments
3. Sets up logging
4. Gets API key from arguments or environment
5. Executes download functionality
6. Handles errors and returns appropriate exit codes

## Data Processing (Planned)

The following functionality is planned for future implementation:

### 1. Data Parsing

Will parse XML files into a SQLite database with tables for:
- VMP (Virtual Medicinal Product)
- VMPP (Virtual Medicinal Product Pack)
- AMP (Actual Medicinal Product)
- AMPP (Actual Medicinal Product Pack)
- GTIN (Global Trade Item Number)
- Ingredient (Ingredient details)
- Lookup (Reference data)
- VTM (Virtual Therapeutic Moieties)

### 2. Price Calculation

Will implement logic to calculate missing prices based on:
- Same VMPP calculation method
- Same VMP calculation method
- Default pricing for remaining records

### 3. Search Table

Will create a unified search table joining all product information with:
- Product relationships established
- Brand/Generic classification
- Price information with calculation method
- Therapeutic classification and ingredient information

## API Reference

### Environment Variables

- `TRUD_API_KEY`: Required for accessing NHS TRUD data
- `GEMINI_API_KEY`: For future LLM tasks (not currently used)

### Command-line Arguments

- `--download-only`: Only download files, don't process them
- `--api-key`: TRUD API key (overrides environment variable)
- `--output-dir`: Directory for downloaded files (default: "data")
- `--retries`: Number of download retry attempts (default: 3)
- `--retry-delay`: Delay between retries in seconds (default: 300)

## Error Handling

The application includes robust error handling with:

- Custom `DownloadError` exception for download-related failures
- Automatic retry logic (3 retries with 5-minute delays by default)
- Detailed logging of errors and retry attempts
- Graceful handling of missing files

## Logging

Logs are stored in the `logs/` directory with timestamps for each session. The logging system captures:

- Information messages about process flow
- Warning messages for non-critical issues
- Error messages for failures
- Detailed information about download progress
- Categorized lists of core and additional files processed

## Next Steps

Future development will include:

1. Parsing XML files into a SQLite database
   - Implementation of XSD validation
   - Creation of tables with proper relationships
   - Extraction of relevant fields from all downloaded XML files

2. Implementing price calculation logic based on the PRD rules
   - Initial price assignment from PRICE_INFO and DTINFO
   - Same VMPP calculation method
   - Same VMP calculation method
   - Default pricing for remaining records

3. Creating a unified search table
   - Joining data across product tables
   - Implementing Brand/Generic classification
   - Creating indexes for efficient searches
   - Incorporating therapeutic and ingredient information

4. Developing expanded CLI/API
   - Commands for searching products
   - Options for exporting data
   - Filtering capabilities

## License

[MIT License](LICENSE) 