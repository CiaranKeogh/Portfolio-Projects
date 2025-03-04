import argparse
import logging
import sys
from pathlib import Path

from config.logging_config import setup_logging
from config.config import (
    RAW_DATA_DIR, VMP_FILE_PATH, VMPP_FILE_PATH, AMP_FILE_PATH, AMPP_FILE_PATH, GTIN_FILE_PATH
)
from api.trud_client import TRUDClient
from api.download_manager import DownloadManager
from processing.xml_parser import XMLParser
from processing.product_matcher import ProductMatcher
from processing.price_calculator import PriceCalculator
from processing.search_table_builder import SearchTableBuilder
from database.models import init_db

# Set up logging
logger = setup_logging()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Drug Tariff Master - Process NHS dm+d data')
    
    parser.add_argument('--download-only', action='store_true', help='Only download files')
    parser.add_argument('--process-only', action='store_true', help='Only process existing files')
    parser.add_argument('--calculate-prices-only', action='store_true', help='Only calculate missing prices')
    parser.add_argument('--build-search-only', action='store_true', help='Only build search table')
    parser.add_argument('--schedule', action='store_true', help='Start the scheduler and keep running')
    
    return parser.parse_args()

def download_files():
    """Download all required files"""
    logger.info("Starting file downloads")
    
    try:
        # Create TRUD client
        trud_client = TRUDClient()
        
        # Download files
        results = trud_client.download_all_files(RAW_DATA_DIR)
        
        # Check results
        success = all(results.values())
        if success:
            logger.info("All files downloaded successfully")
        else:
            failed_files = [file_type for file_type, success in results.items() if not success]
            logger.error(f"Failed to download some files: {', '.join(failed_files)}")
            
        return success
    
    except Exception as e:
        logger.error(f"Error downloading files: {str(e)}")
        return False

def process_files():
    """Process downloaded XML files"""
    logger.info("Starting file processing")
    
    try:
        # Check if files exist
        files = [VMP_FILE_PATH, VMPP_FILE_PATH, AMP_FILE_PATH, AMPP_FILE_PATH, GTIN_FILE_PATH]
        missing_files = [str(f) for f in files if not Path(f).exists()]
        
        if missing_files:
            logger.error(f"Missing files: {', '.join(missing_files)}")
            return False
        
        # Initialize database
        init_db()
        
        # Create XML parser
        xml_parser = XMLParser()
        
        # Parse files
        results = xml_parser.parse_all_files(
            VMP_FILE_PATH, VMPP_FILE_PATH, AMP_FILE_PATH, AMPP_FILE_PATH, GTIN_FILE_PATH
        )
        
        # Log results
        for entity_type, count in results.items():
            logger.info(f"Processed {count} {entity_type} records")
        
        return True
    
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return False

def match_products():
    """Match products (AMPP to VMPP, GTIN to AMPP)"""
    logger.info("Starting product matching")
    
    try:
        # Create product matcher
        matcher = ProductMatcher()
        
        # Run matching
        results = matcher.run_all_matching()
        
        # Log results
        for match_type, count in results.items():
            logger.info(f"Matched {count} records for {match_type}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error matching products: {str(e)}")
        return False

def calculate_prices():
    """Calculate missing drug tariff prices"""
    logger.info("Starting price calculation")
    
    try:
        # Create price calculator
        calculator = PriceCalculator()
        
        # Calculate prices
        results = calculator.calculate_all_prices()
        
        # Log results
        for rule, count in results.items():
            logger.info(f"Applied {rule} rule to {count} records")
        
        return True
    
    except Exception as e:
        logger.error(f"Error calculating prices: {str(e)}")
        return False

def build_search_table():
    """Build the unified search table"""
    logger.info("Starting search table build")
    
    try:
        # Create search table builder
        builder = SearchTableBuilder()
        
        # Build search table
        count = builder.build_search_table()
        
        # Create indexes
        builder.create_indexes()
        
        logger.info(f"Built search table with {count} records")
        return True
    
    except Exception as e:
        logger.error(f"Error building search table: {str(e)}")
        return False

def start_scheduler():
    """Start the scheduler for regular downloads"""
    logger.info("Starting scheduler")
    
    try:
        # Create download manager
        download_manager = DownloadManager()
        
        # Start scheduler
        download_manager.start_scheduler()
        
        # Keep the process running
        logger.info("Scheduler running. Press Ctrl+C to stop.")
        
        try:
            # This will keep the process running until interrupted
            import time
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")
            download_manager.stop_scheduler()
        
        return True
    
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
        return False

def run_full_pipeline():
    """Run the full data processing pipeline"""
    logger.info("Starting full pipeline")
    
    # Download files
    if not download_files():
        logger.error("File download failed, stopping pipeline")
        return False
    
    # Process files
    if not process_files():
        logger.error("File processing failed, stopping pipeline")
        return False
    
    # Match products
    if not match_products():
        logger.error("Product matching failed, stopping pipeline")
        return False
    
    # Calculate prices
    if not calculate_prices():
        logger.error("Price calculation failed, stopping pipeline")
        return False
    
    # Build search table
    if not build_search_table():
        logger.error("Search table build failed, stopping pipeline")
        return False
    
    logger.info("Full pipeline completed successfully")
    return True

def main():
    """Main entry point"""
    args = parse_arguments()
    
    try:
        # Handle specific command line arguments
        if args.download_only:
            return download_files()
        
        elif args.process_only:
            return process_files()
        
        elif args.calculate_prices_only:
            return calculate_prices()
        
        elif args.build_search_only:
            return build_search_table()
        
        elif args.schedule:
            return start_scheduler()
        
        # Run full pipeline by default
        else:
            return run_full_pipeline()
    
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 