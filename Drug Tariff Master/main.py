#!/usr/bin/env python3
"""
Drug Tariff Processor - Main Script

This script handles the downloading of dm+d files from the NHS TRUD service.
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
    if not api_key:
        logger.error("TRUD API key not provided. Use --api-key or set TRUD_API_KEY in .env file")
        sys.exit(1)
    
    try:
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
        
        # Additional processing would go here in future versions
        logger.info("Processing functionality not yet implemented")
        
    except DownloadError as e:
        logger.error(f"Download failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 