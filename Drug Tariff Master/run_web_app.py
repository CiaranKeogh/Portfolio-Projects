#!/usr/bin/env python
"""
Run the Drug Tariff Master web interface.
This is a simple wrapper script to start the web application.
"""
import os
import sys
from src import web_app

# Check if the data directory exists
from src import config
if not os.path.exists(config.DATA_DIR):
    print("Error: Data directory does not exist. Please run 'python src/app.py --init' first.")
    sys.exit(1)

# Check if the database file exists
db_path = os.path.join(config.DATA_DIR, 'dmd_data.db')
if not os.path.exists(db_path):
    print("Error: Database file does not exist. Please run 'python src/app.py --init' first.")
    sys.exit(1)

if __name__ == '__main__':
    print("Starting Drug Tariff Master web interface...")
    print("Access the web interface at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    web_app.run_web_app(debug=True) 