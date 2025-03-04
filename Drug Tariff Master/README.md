# Drug Tariff Master

A comprehensive system for downloading, processing, and searching medicinal product price data from the NHS Dictionary of Medicines and Devices (dm+d) via the TRUD service.

## Overview

Drug Tariff Master is a Python application that manages medicinal product pricing information. It automates the process of:

1. Downloading the latest dm+d data from the TRUD service
2. Parsing XML files according to their schema definitions
3. Storing structured data in a SQLite database
4. Calculating missing prices using configurable algorithms
5. Providing a search interface for quick access to product information

## Features

- **Automated Updates**: Scheduled downloads of the latest dm+d releases
- **XML Validation**: Validates all XML files against their XSD schemas
- **Price Calculation**: Implements multiple algorithms to fill in missing pricing data
- **Fast Search**: Unified search across VMP, VMPP, AMP, and AMPP records
- **Command-line Interface**: Easy-to-use commands for updates and searches
- **Comprehensive Logging**: Detailed logs for all operations and decisions

## System Requirements

- Python 3.8 or higher
- Internet connection for downloading data
- TRUD API key (register at https://isd.digital.nhs.uk/)

## Directory Structure

```
Drug Tariff Master/
├── data/                  # Downloaded and extracted data files
├── logs/                  # Application logs
├── schemas/               # XSD schema definitions
├── src/                   # Source code
│   ├── app.py             # Main application entry point
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database operations
│   ├── downloader.py      # Data download and extraction
│   ├── parser.py          # XML parsing and validation
│   ├── pricing.py         # Price calculation algorithms
│   ├── scheduler.py       # Scheduled task management
│   └── search.py          # Search functionality
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore file
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd "Drug Tariff Master"
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your TRUD API key:
   ```
   TRUD_API_KEY=your_api_key_here
   ```

## Usage

### Initialize the Environment

Before first use, initialize the application environment:

```
python src/app.py --init
```

This creates necessary directories and initializes the database.

### Download and Process Data

To download the latest data, parse it, and calculate prices:

```
python src/app.py --update
```

This will:
1. Download the latest dm+d release from TRUD
2. Extract the ZIP files
3. Parse the XML files into the database
4. Apply price calculation algorithms
5. Build the search index

### Interactive Search

To search for products interactively:

```
python src/app.py --search
```

This opens an interactive prompt where you can search for products by name, strength, form, etc.

Search tips:
- Enter drug names, strengths, or forms (e.g., "paracetamol", "amoxicillin 500mg")
- Filter by type with `--type=` flag (e.g., "insulin --type=AMPP")
- Type 'help' for search tips
- Type 'exit' or 'quit' to end the session

### Schedule Automated Updates

To start the scheduler for automated updates:

```
python src/app.py --schedule
```

This runs the application in the background and performs updates according to the schedule defined in `config.py` (default is weekly).

## Price Calculation Rules

The system implements the following rules for calculating missing prices:

1. **Initial Price Assignment**:
   - If AMPP has PRICE_INFO, use that price
   - If AMPP price is missing but VMPP has a price, use the VMPP price

2. **Same VMPP (Primary Calculation)**:
   - Calculate the average price of other AMPPs with the same VPPID

3. **Same VMP (Fallback Calculation)**:
   - Calculate the price per unit from other VMPPs with the same VPID
   - Multiply by the quantity to get an estimated price

4. **Default (Last Resort)**:
   - Set price to 0 and flag for manual review

## XML Schema Structure

The application uses the following XSD schemas to validate and process XML data:

- **vmp_v2_3.xsd**: Virtual Medicinal Products
- **vmpp_v2_3.xsd**: Virtual Medicinal Product Packs
- **amp_v2_3.xsd**: Actual Medicinal Products
- **ampp_v2_3.xsd**: Actual Medicinal Product Packs
- **lookup_v2_3.xsd**: Reference data for lookups

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NHS Digital for providing the dm+d data through TRUD
- All contributors to the open-source libraries used in this project 