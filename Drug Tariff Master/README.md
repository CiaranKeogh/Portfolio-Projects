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
- [x] Data parsing and database creation
- [x] Unified search table for efficient querying
- [ ] Price calculation for missing tariff prices
- [ ] API for accessing the data

## Requirements

- Python 3.8 or higher
- NHS TRUD API key (register at [TRUD](https://isd.digital.nhs.uk/))
- SQLite 3

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

### Downloading and Processing dm+d Files

To download the latest dm+d files and load them into the database:

```bash
python main.py
```

To only download files without processing:

```bash
python main.py --download-only
```

To rebuild the database from scratch:

```bash
python main.py --rebuild-db
```

Additional options:

```
--output-dir DATA_DIR   Directory to save downloaded files (default: data)
--db-path DB_PATH       Path to SQLite database file (default: data/dmd.db)
--retries COUNT         Number of retries for failed downloads (default: 3)
--retry-delay SECONDS   Delay between retries in seconds (default: 300)
--api-key KEY           TRUD API key (overrides env variable)
```

### Handling of File Versioning

The NHS TRUD service provides files with date or version suffixes in the filenames (e.g., `f_amp2_3200325.xml`). The download module automatically handles these varying filenames by:

1. Using regular expressions to identify files regardless of their date suffix
2. Standardizing filenames internally to a consistent format (e.g., `f_amp2.xml`)
3. Maintaining a mapping between standardized names and actual files on disk

This approach ensures the application will continue to work correctly with future releases that might use different date or version suffixes.

## Database Schema

The application uses a SQLite database with the following schema structure:

### Core Entity Tables

- **vtm** (Virtual Therapeutic Moiety): The primary therapeutic substance
  - Fields: vtmid (PK), name, abbrev_name, invalid, vtmid_prev, vtmid_date

- **vmp** (Virtual Medicinal Product): Generic product concept
  - Fields: vpid (PK), vtmid (FK), name, abbrev_name, basis_code, various flags for product features
  - Linked to vtm via vtmid

- **vmpp** (Virtual Medicinal Product Pack): Generic pack information
  - Fields: vppid (PK), vpid (FK), name, abbrev_name, qty_value, qty_uom_code, etc.
  - Linked to vmp via vpid

- **amp** (Actual Medicinal Product): Branded product from a specific manufacturer
  - Fields: apid (PK), vpid (FK), name, abbrev_name, desc, supp_code, license info, etc.
  - Linked to vmp via vpid

- **ampp** (Actual Medicinal Product Pack): Branded pack with specific pricing
  - Fields: appid (PK), apid (FK), vppid (FK), name, legal_cat_code, etc.
  - Linked to amp via apid and vmpp via vppid

- **ingredient**: Active substances
  - Fields: isid (PK), name, isid_date, isid_prev, invalid

- **gtin**: Global Trade Item Numbers for product identification
  - Fields: gtin_id (PK), appid (FK), gtin, start_date, end_date
  - Linked to ampp via appid

### Relationship Tables

- **vmp_ingredient**: Links VMPs to ingredients
  - Fields: vpid (PK, FK), isid (PK, FK), strength information

- **amp_ingredient**: Links AMPs to ingredients
  - Fields: apid (PK, FK), isid (PK, FK), strength, uom_code

- **vmp_form**: Forms for VMP products
  - Fields: vpid (PK, FK), form_code (PK)

- **vmp_route**: Routes of administration for VMP
  - Fields: vpid (PK, FK), route_code (PK)

- **amp_route**: Licensed routes for AMP
  - Fields: apid (PK, FK), route_code (PK)

### Supplementary Information Tables

- **vmpp_dt_info**: Drug tariff information for VMPP
  - Fields: vppid (PK, FK), pay_cat_code (PK), price, dt, prev_price

- **ampp_price_info**: Pricing info for AMPP
  - Fields: appid (PK, FK), price, price_date, price_prev, price_basis_code

- **ampp_reimb_info**: Reimbursement info for AMPP
  - Fields: appid (PK, FK), various reimbursement flags

- **ampp_prescrib_info**: Prescribing info for AMPP
  - Fields: appid (PK, FK), various prescribing flags

- **ampp_pack_info**: Pack info for AMPP
  - Fields: appid (PK, FK), reimb_stat_code, reimb_stat_date, etc.

### Search Table

- **unified_search**: Denormalized table for efficient searching
  - Fields: id (PK), vtmid, vpid, vppid, apid, appid, gtin, name, is_brand, ingredient_list, form, etc.
  - Combines data from multiple tables for fast querying
  - Contains calculated fields like is_brand, ingredient_list, and pack_size

### Database Relationships

The database follows the dm+d data model hierarchical structure:

1. VTM (therapeutic substance) → VMP (generic product)
2. VMP → VMPP (generic pack)
3. VMP → AMP (branded product)
4. AMP → AMPP (branded pack)
5. VMPP → AMPP (cross-relationship)
6. AMPP → GTIN (product identification)

Ingredients and routes can be associated with both VMPs and AMPs, while pricing information is associated with VMPPs (drug tariff) and AMPPs (actual prices).

## Data Processing Flow

1. **Download**: The application first downloads the latest dm+d files from NHS TRUD
2. **Extraction**: It extracts both the main ZIP file and the nested GTIN ZIP file
3. **Database Creation**: If needed, it creates a new SQLite database with the proper schema
4. **Data Loading**: Files are processed in a specific order to maintain referential integrity:
   - Ingredients first (as they are referenced by VMPs and AMPs)
   - VTM (as they are referenced by VMPs)
   - VMP (as they are referenced by AMPs and VMPPs)
   - VMPP (as they are referenced by AMPPs)
   - AMP (as they are referenced by AMPPs)
   - AMPP (as they reference both AMPs and VMPPs)
   - GTIN (as they reference AMPPs)
5. **Search Table Building**: After all data is loaded, the unified search table is built for efficient querying

## Detailed Code Architecture

### Project Structure

```
Drug Tariff Master/
├── config/                 # Configuration and settings
│   └── logging_config.py   # Logging setup with timestamped files
├── data/                   # Storage for downloaded and processed data
│   └── dmd.db              # SQLite database with processed data
├── logs/                   # Application logs with timestamps
├── src/                    # Source code modules
│   ├── __init__.py         # Source package initialization
│   ├── database/           # Database functionality
│   │   ├── __init__.py     # Exports database module functions
│   │   ├── loader.py       # XML parsing and database loading
│   │   └── schema.py       # Database schema definition
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

**Key Functions**:
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

#### 2. Database Module (`src/database/`)

**Purpose**: Define database schema and load data from XML files.

**Key Files**:
- `schema.py`: Contains functions for:
  - `create_database()`: Creates the SQLite database with proper schema
  - `get_connection()`: Establishes connections to the database

- `loader.py`: Contains functions for:
  - `load_data()`: Orchestrates the data loading process
  - `parse_vtm()`, `parse_vmp()`, etc.: Parse specific XML file types
  - `build_unified_search_table()`: Creates the denormalized search table
  - Helper functions for XML parsing and SQL operations

**Flow**:
1. Creates database tables with appropriate foreign key relationships
2. Processes XML files in order to maintain referential integrity
3. Parses XML elements and inserts them into the appropriate tables
4. Builds a unified search table for efficient querying
5. Handles data validation and error cases

#### 3. Configuration Module (`config/`)

**Purpose**: Centralize application configuration.

**Key Files**:
- `logging_config.py`: Sets up logging with:
  - Timestamped log files
  - Both file and console output
  - Configurable log levels

#### 4. Main Application (`main.py`)

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
6. Creates/updates database and loads data (if not download-only)
7. Handles errors and returns appropriate exit codes

## Planned Features

The following functionality is planned for future implementation:

### 1. Price Calculator

Will implement logic to calculate missing prices based on:
- Same VMPP calculation method
- Same VMP calculation method
- Default pricing for remaining records

### 2. Expanded Search Capabilities

- Search products by ingredient, form, or brand
- Filter by price range or availability
- Find potential substitutes for specific products

### 3. API Access

- REST API for accessing the data programmatically
- Endpoints for searching products and retrieving pricing information

## Error Handling

The application includes robust error handling with:

- Custom `DownloadError` exception for download-related failures
- Automatic retry logic (3 retries with 5-minute delays by default)
- Detailed logging of errors and retry attempts
- Graceful handling of missing files or database errors
- Transaction rollback on database errors

## Logging

Logs are stored in the `logs/` directory with timestamps for each session. The logging system captures:

- Information messages about process flow
- Warning messages for non-critical issues
- Error messages for failures
- Detailed information about download progress
- Database operations and error details

## License

[MIT License](LICENSE) 