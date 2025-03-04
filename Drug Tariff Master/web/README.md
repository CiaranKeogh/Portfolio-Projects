# Drug Tariff Master Web Interface

This directory contains the web interface files for the Drug Tariff Master application.

## Directory Structure

- `templates/`: Contains HTML templates for the web interface
- `static/`: Contains static assets for the web interface
  - `css/`: CSS stylesheets
  - `js/`: JavaScript files

## Running the Web Interface

To run the web interface, use one of the following methods:

### Method 1: Using the run_web_app.py script

```bash
# From the project root directory
python run_web_app.py
```

### Method 2: Using the app.py script with the --web flag

```bash
# From the project root directory
python src/app.py --web
```

You can specify additional options:

```bash
# Run on a different host and port
python src/app.py --web --host=0.0.0.0 --port=8080

# Run in debug mode
python src/app.py --web --debug
```

## Web Interface Features

The web interface provides the following features:

1. **Search**: Search for medicinal products by name, form, or strength
2. **Filtering**: Filter search results by product type (VMP, VMPP, AMP, AMPP)
3. **Pagination**: Navigate through search results with pagination
4. **Product Details**: View detailed information about products
5. **Statistics**: View database statistics
6. **Export**: Export search results as CSV or print them

## API Endpoints

The web interface provides the following API endpoints:

- `/api/search`: Search for medicinal products
  - Parameters: `q` (search term), `type` (product type), `limit`, `page`
- `/api/product/<record_type>/<product_id>`: Get detailed information about a specific product
- `/api/stats`: Get database statistics

## Technologies Used

- Backend: Flask
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Icons: Font Awesome 