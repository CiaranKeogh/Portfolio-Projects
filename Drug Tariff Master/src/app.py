"""
Main application entry point for Drug Tariff Master.
This script provides command-line arguments for running different application functions.
"""
import os
import sys
import argparse
import logging
from datetime import datetime

import config
import database
import trud
import parser
import search
import web_app

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def initialize():
    """Initialize the application."""
    logger.info("Initializing application")
    
    # Create data directory if it does not exist
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    # Initialize database
    database.initialize_database()
    
    logger.info("Initialization complete")


def show_search_interface():
    """Show interactive search interface."""
    while True:
        print("\n===== Drug Tariff Master Search =====")
        search_term = input("Enter search term (or 'q' to quit): ")
        
        if search_term.lower() == 'q':
            break
        
        if not search_term:
            print("Please enter a search term.")
            continue
        
        try:
            results = search.search_products(search_term)
            
            if not results:
                print(f"No results found for '{search_term}'")
                continue
            
            print(f"\nFound {len(results)} results for '{search_term}':")
            print("-" * 80)
            
            # Display results
            for i, result in enumerate(results[:10], 1):
                name = result['NAME']
                record_type = result['RECORD_TYPE']
                price = f"£{result['PRICE']/100:.2f}" if result['PRICE'] else "N/A"
                id_field = result['ID']
                
                print(f"{i}. {name} ({record_type}, ID: {id_field}, Price: {price})")
            
            if len(results) > 10:
                print(f"...and {len(results) - 10} more results.")
            
            print("-" * 80)
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("Exiting search interface.")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Drug Tariff Master')
    parser.add_argument('--init', action='store_true', help='Initialize the application')
    parser.add_argument('--update', action='store_true', help='Update data from TRUD')
    parser.add_argument('--build-search', action='store_true', help='Build search index')
    parser.add_argument('--search', action='store_true', help='Interactive search interface')
    parser.add_argument('--web', action='store_true', help='Run web interface')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host for web interface')
    parser.add_argument('--port', type=int, default=5000, help='Port for web interface')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    if args.init:
        initialize()
        
    elif args.update:
        initialize()  # Make sure everything is initialized
        trud.update_from_trud()
        
    elif args.build_search:
        # Rebuild search index
        search.build_search_index()
        
    elif args.search:
        show_search_interface()
        
    elif args.web:
        print(f"Starting web interface on http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        web_app.run_web_app(host=args.host, port=args.port, debug=args.debug)
        
    else:
        parser.print_help()
        

if __name__ == '__main__':
    main() 