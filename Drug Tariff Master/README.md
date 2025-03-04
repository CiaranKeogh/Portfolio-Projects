# Drug Tariff Master

A comprehensive application for searching, viewing, and analyzing NHS Drug Tariff data. This project provides tools for managing and exploring UK medicinal product information, including pricing data.

## Features

- **Data Management**
  - Import and parse NHS Dictionary of Medicines and Devices (dm+d) data from TRUD
  - Automatic database initialization and schema management
  - Support for all standard dm+d entities: VMP, VMPP, AMP, AMPP, and GTIN

- **Advanced Search**
  - Fast text-based search across all product types
  - Filter by product type (VMP, VMPP, AMP, AMPP)
  - Detailed product information with relationships
  - Command-line and web-based interfaces

- **Pricing Analysis**
  - Display pricing information for Actual Medicinal Product Packs (AMPPs)
  - Pricing sources clearly indicated (Drug Tariff, SAME VMPP, etc.)
  - Support for historical pricing data

- **Web Interface**
  - Modern, responsive design using Bootstrap 5
  - Interactive search with real-time filtering
  - Detailed product information views
  - Database statistics dashboard
  - CSV export and print functionality

## Getting Started

### Prerequisites

- Python 3.8 or higher
- SQLite3
- Internet connection (for initial data download)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/drug-tariff-master.git
   cd drug-tariff-master
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the application:
   ```
   python src/app.py --init
   ```

4. Update data from TRUD:
   ```
   python src/app.py --update
   ```

### Running the Application

#### Command-line Interface

```
# Interactive search interface
python src/app.py --search

# Build or rebuild search index
python src/app.py --build-search
```

#### Web Interface

```
# Start the web interface
python src/app.py --web

# Specify host and port
python src/app.py --web --host=0.0.0.0 --port=8080

# Run in debug mode
python src/app.py --web --debug
```

Alternatively, use the convenience script:

```
python run_web_app.py
```

## Latest Updates

### Search Improvements

- **Enhanced Search Algorithm**: Improved search quality by focusing on the NAME field for more accurate results
- **Fallback Mechanism**: If no results are found in the search_data table, the system now searches directly in the main tables (AMPP and VMP)
- **Better Parameter Handling**: Improved search parameter handling and error reporting

### New Web Interface

- **Modern UI**: Clean, responsive design using Bootstrap 5
- **Interactive Search**: Real-time filtering and pagination of search results
- **Detailed Product Views**: Complete product information with related entities
- **Statistics Dashboard**: Overview of database contents and record counts
- **Export Options**: Download search results as CSV or print them directly

### API Endpoints

The web interface provides RESTful API endpoints:

- `/api/search`: Search for medicinal products
  - Parameters: `q` (search term), `type` (product type), `limit`, `page`
- `/api/product/<record_type>/<product_id>`: Get detailed information about a specific product
- `/api/stats`: Get database statistics

## Project Structure

```
drug-tariff-master/
│
├── src/                   # Source code
│   ├── app.py             # Application entry point
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database management
│   ├── downloader.py      # Data download utilities
│   ├── parser.py          # XML parsing utilities
│   ├── pricing.py         # Price calculation algorithms
│   ├── scheduler.py       # Scheduled task management
│   ├── search.py          # Search functionality
│   ├── trud.py            # TRUD API interaction
│   └── web_app.py         # Web interface
│
├── web/                   # Web interface assets
│   ├── static/            # Static files
│   │   ├── css/           # CSS stylesheets
│   │   └── js/            # JavaScript files
│   ├── templates/         # HTML templates
│   └── README.md          # Web interface documentation
│
├── data/                  # Data directory (created on initialization)
│   ├── dmd_data.db        # SQLite database
│   └── logs/              # Log files
│
├── check_db.py            # Database check utility
├── check_port.py          # Network port testing utility
├── run_debug.py           # Debug script for troubleshooting
├── run_web_app.py         # Convenience script for web interface
├── test_search.py         # Search testing utility
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Data Structure

The application works with the following data entities:

- **VMP** (Virtual Medicinal Products): Conceptual products without a supplier
- **VMPP** (Virtual Medicinal Product Packs): Conceptual packs of a VMP
- **AMP** (Actual Medicinal Products): Actual products from specific suppliers
- **AMPP** (Actual Medicinal Product Packs): Actual packs of an AMP with pricing
- **GTIN** (Global Trade Item Numbers): Standardized identifiers for medicinal products

## VMPP Pricing Calculation

When an AMPP doesn't have a direct price specified, the system can derive its price based on other AMPPs that belong to the same VMPP through the "SAME VMPP" pricing calculation:

1. For AMPPs missing direct price information
2. The system identifies the VMPP it belongs to
3. It finds other AMPPs that belong to the same VMPP and have known prices
4. It calculates a reference price from these similar products
5. This reference price is assigned with "SAME VMPP" as the price source

This ensures pricing consistency across different brands of the same medicinal product.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NHS Business Services Authority (NHSBSA) for providing the TRUD data service
- UK NHS Dictionary of Medicines and Devices (dm+d) for the data structure 