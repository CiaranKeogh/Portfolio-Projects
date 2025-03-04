# Drug Tariff Master

A comprehensive system for processing NHS dm+d (Dictionary of Medicines and Devices) data, matching products, calculating prices, and building a unified search database.

## Overview

The Drug Tariff Master automates the process of downloading, parsing, and processing NHS dm+d data. It handles the following tasks:

1. **Data Acquisition**: Automatically downloads the latest dm+d data files from the TRUD API
2. **Data Processing**: Parses XML files and loads data into a structured database
3. **Product Matching**: Links AMPPs to VMPPs and GTINs to AMPPs using NLP techniques
4. **Price Calculation**: Fills in missing drug tariff prices using various rules
5. **Search Table**: Builds a unified search table for efficient querying

## Project Structure

```
Drug Tariff Master/
├── data/                  # Data storage
│   ├── raw/               # Raw downloaded files
│   └── processed/         # Processed data files
├── logs/                  # Log files
├── src/                   # Source code
│   ├── api/               # API clients
│   │   ├── download_manager.py  # Manages scheduled downloads
│   │   └── trud_client.py       # TRUD API client
│   ├── config/            # Configuration
│   │   ├── config.py      # General configuration
│   │   └── logging_config.py  # Logging configuration
│   ├── database/          # Database models and utilities
│   │   └── models.py      # SQLAlchemy models
│   ├── processing/        # Data processing modules
│   │   ├── price_calculator.py     # Calculates missing prices
│   │   ├── product_matcher.py      # Matches products
│   │   ├── search_table_builder.py # Builds search table
│   │   └── xml_parser.py           # Parses XML files
│   ├── utils/             # Utility functions
│   │   └── llm_processor.py  # LLM processing utilities
│   └── main.py            # Main entry point
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
└── requirements.txt       # Python dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Drug-Tariff-Master
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your API keys:
   ```
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Usage

### Command Line Interface

The system provides a command-line interface with several options:

```
python src/main.py [options]
```

Options:
- `--download-only`: Only download files from TRUD API
- `--process-only`: Only process existing files
- `--calculate-prices-only`: Only calculate missing prices
- `--build-search-only`: Only build search table
- `--schedule`: Start the scheduler and keep running

### Running the Full Pipeline

To run the complete data processing pipeline:

```
python src/main.py
```

This will:
1. Download the latest dm+d files
2. Process the XML files into the database
3. Match products (AMPP to VMPP, GTIN to AMPP)
4. Calculate missing drug tariff prices
5. Build the unified search table

### Scheduling Regular Updates

To set up regular downloads of updated dm+d data:

```
python src/main.py --schedule
```

This will start a scheduler that runs in the background, checking for updates according to the configured schedule.

## Configuration

Configuration settings are stored in the following files:

- `.env`: Environment variables (API keys, etc.)
- `src/config/config.py`: General configuration settings
- `src/config/logging_config.py`: Logging configuration

## Dependencies

- Python 3.8+
- SQLAlchemy
- lxml
- requests
- tqdm
- APScheduler
- python-dotenv
- google-generativeai (for Gemini LLM integration)

## License

[Specify your license here]

## Contributing

[Specify contribution guidelines here] 