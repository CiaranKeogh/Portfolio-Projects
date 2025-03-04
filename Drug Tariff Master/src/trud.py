"""
TRUD API module for Drug Tariff Master.
This module provides functionality to update data from the TRUD service.
"""
import os
import logging
import time
from datetime import datetime

import config
import downloader
import parser
import search

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('trud')


def update_from_trud():
    """
    Update data from TRUD service.
    This function orchestrates the process of downloading, parsing, and indexing data.
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        logger.info("Starting TRUD update process")
        start_time = time.time()
        
        # Step 1: Download data
        logger.info("Step 1: Downloading data from TRUD")
        if not downloader.validate_api_key():
            logger.error("TRUD API key not set or invalid")
            return False
            
        download_success = downloader.download_and_process_data()
        if not download_success:
            logger.error("Failed to download data from TRUD")
            return False
            
        # Step 2: Parse XML files
        logger.info("Step 2: Parsing XML data")
        parse_success = parser.process_all_files()
        if not parse_success:
            logger.error("Failed to parse XML data")
            return False
            
        # Step 3: Build search index
        logger.info("Step 3: Building search index")
        index_count = search.build_search_index()
        logger.info(f"Search index built with {index_count} records")
        
        # Update last update timestamp
        with open(os.path.join(config.DATA_DIR, 'last_update.txt'), 'w') as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
        elapsed_time = time.time() - start_time
        logger.info(f"TRUD update completed successfully in {elapsed_time:.2f} seconds")
        return True
        
    except Exception as e:
        logger.exception(f"Error in TRUD update process: {e}")
        return False


def get_last_update_time():
    """
    Get the timestamp of the last successful update.
    
    Returns:
        str: Timestamp of the last update or 'Never' if no updates have been performed
    """
    update_file = os.path.join(config.DATA_DIR, 'last_update.txt')
    
    if os.path.exists(update_file):
        with open(update_file, 'r') as f:
            return f.read().strip()
    
    return 'Never' 