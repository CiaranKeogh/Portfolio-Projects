#!/usr/bin/env python3
"""
Drug Tariff Processor - Main Script

This script handles the downloading and processing of dm+d files from the NHS TRUD service.
For the complete functionality, refer to the README.md file.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.logging_config import setup_logging
from src.download import download_dmd_files, DownloadError
from src.database import create_database, load_data
from src.calculator import calculate_missing_prices

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Drug Tariff Processor')
    parser.add_argument('--download-only', action='store_true', 
                        help='Only download the files, do not process them')
    parser.add_argument('--api-key', type=str, help='TRUD API key (overrides env variable)')
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Directory to save downloaded files')
    parser.add_argument('--retries', type=int, default=3,
                        help='Number of retries for failed downloads')
    parser.add_argument('--retry-delay', type=int, default=300,
                        help='Delay between retries in seconds')
    parser.add_argument('--db-path', type=str, default='data/dmd.db',
                        help='Path to SQLite database file')
    parser.add_argument('--rebuild-db', action='store_true',
                        help='Rebuild the database from scratch')
    parser.add_argument('--calculate-prices', action='store_true',
                        help='Only calculate missing prices without downloading/processing files')
    parser.add_argument('--recalculate-prices', action='store_true',
                        help='Force recalculation of all prices')
    parser.add_argument('--skip-price-calculation', action='store_true',
                        help='Skip automatic price calculation after data loading')
    
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    # Get the API key from arguments or environment
    api_key = args.api_key or os.getenv('TRUD_API_KEY')
    if not args.calculate_prices and not args.recalculate_prices and not api_key:
        logger.error("TRUD API key not provided. Use --api-key or set TRUD_API_KEY in .env file")
        sys.exit(1)
    
    try:
        # If we're only calculating prices, skip download and processing
        if args.calculate_prices or args.recalculate_prices:
            logger.info("Running in price calculation mode")
            if not os.path.exists(args.db_path):
                logger.error(f"Database file {args.db_path} does not exist")
                sys.exit(1)
            
            # Calculate missing prices
            success = calculate_missing_prices(args.db_path)
            if not success:
                logger.error("Failed to calculate prices")
                sys.exit(1)
            
            logger.info("Price calculation completed successfully")
            return
        
        # Download and process files
        logger.info("Starting download of dm+d files")
        
        # Download the files
        files = download_dmd_files(
            api_key=api_key,
            output_dir=args.output_dir,
            retry_count=args.retries,
            retry_delay=args.retry_delay
        )
        
        logger.info(f"Download completed successfully. Files: {list(files.keys())}")
        
        # If we're only downloading, exit here
        if args.download_only:
            logger.info("Download-only mode, exiting")
            return
        
        # Create or check the database
        logger.info(f"Setting up database at {args.db_path}")
        if args.rebuild_db or not os.path.exists(args.db_path):
            success = create_database(args.db_path)
            if not success:
                logger.error("Failed to create database")
                sys.exit(1)
        
        # Process the files and load into database
        logger.info("Processing files and loading to database")
        success = load_data(args.db_path, files)
        if not success:
            logger.error("Failed to load data into database")
            sys.exit(1)
        
        logger.info("Data processing completed successfully")
        
        # Automatically calculate missing prices unless explicitly skipped
        if not args.skip_price_calculation:
            logger.info("Starting automatic price calculation")
            success = calculate_missing_prices(args.db_path)
            if not success:
                logger.error("Failed to calculate prices")
                sys.exit(1)
            logger.info("Automatic price calculation completed successfully")
        
    except DownloadError as e:
        logger.error(f"Download failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 