"""
Downloader module for Drug Tariff Master.
This module handles downloading files from the TRUD API and extracting them.
"""
import os
import json
import time
import logging
import zipfile
import requests
from pathlib import Path

import config

# Set up logging
logging.basicConfig(
    filename=config.DOWNLOAD_LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('downloader')


def validate_api_key():
    """
    Validate that the TRUD API key is set.
    
    Returns:
        bool: True if the API key is set, False otherwise.
    """
    if not config.TRUD_API_KEY:
        logger.error("TRUD API key is not set. Please add it to the .env file.")
        return False
    return True


def get_latest_release_url():
    """
    Get the URL for the latest dm+d release from the TRUD API.
    
    Returns:
        str: The archive file URL or None if there's an error.
    """
    if not validate_api_key():
        return None
    
    logger.info("Fetching latest release information from TRUD API")
    
    try:
        response = requests.get(config.TRUD_API_URL)
        response.raise_for_status()
        
        data = response.json()
        if 'releases' not in data or not data['releases']:
            logger.error("No releases found in TRUD API response")
            return None
        
        latest_release = data['releases'][0]
        if 'archiveFileUrl' not in latest_release:
            logger.error("Archive file URL not found in latest release")
            return None
        
        return latest_release['archiveFileUrl']
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching release information: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")
        return None


def download_file(url, target_path):
    """
    Download a file from the given URL with retries.
    
    Args:
        url (str): URL to download from.
        target_path (Path): Where to save the downloaded file.
        
    Returns:
        bool: True if download was successful, False otherwise.
    """
    logger.info(f"Downloading from {url} to {target_path}")
    
    for attempt in range(1, config.MAX_DOWNLOAD_RETRIES + 1):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Ensure the target directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the content to the file
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            logger.info(f"Download completed successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Download attempt {attempt} failed: {e}")
            
            if attempt < config.MAX_DOWNLOAD_RETRIES:
                logger.info(f"Retrying in {config.RETRY_DELAY_SECONDS} seconds...")
                time.sleep(config.RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Download failed after {config.MAX_DOWNLOAD_RETRIES} attempts")
                return False


def extract_zip(zip_path, extract_dir):
    """
    Extract a ZIP file to the specified directory.
    
    Args:
        zip_path (Path): Path to the ZIP file.
        extract_dir (Path): Directory to extract to.
        
    Returns:
        bool: True if extraction was successful, False otherwise.
    """
    logger.info(f"Extracting {zip_path} to {extract_dir}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        logger.info(f"Extraction successful")
        return True
    
    except zipfile.BadZipFile as e:
        logger.error(f"Bad ZIP file: {e}")
        return False
    except Exception as e:
        logger.error(f"Error extracting ZIP file: {e}")
        return False


def extract_nested_zip(extract_dir):
    """
    Extract any nested ZIP files (like the f_gtin2.zip file).
    
    Args:
        extract_dir (Path): Directory containing extracted files.
        
    Returns:
        bool: True if all nested extractions were successful.
    """
    logger.info(f"Looking for nested ZIP files in {extract_dir}")
    
    success = True
    for zip_file in extract_dir.glob('**/*.zip'):
        logger.info(f"Found nested ZIP file: {zip_file}")
        extract_subdir = zip_file.parent / zip_file.stem
        extract_subdir.mkdir(exist_ok=True)
        
        if not extract_zip(zip_file, extract_subdir):
            success = False
    
    return success


def download_and_process_data():
    """
    Main function to download the latest dm+d data and extract it.
    
    Returns:
        bool: True if download and extraction were successful, False otherwise.
    """
    # Get the URL for the latest release
    archive_url = get_latest_release_url()
    if not archive_url:
        return False
    
    # Define paths
    zip_path = config.DATA_DIR / "latest_dmd.zip"
    extract_path = config.DATA_DIR / "extracted"
    
    # Download the ZIP file
    if not download_file(archive_url, zip_path):
        return False
    
    # Extract the main ZIP file
    if not extract_zip(zip_path, extract_path):
        return False
    
    # Handle nested ZIP files (like f_gtin2.zip)
    if not extract_nested_zip(extract_path):
        logger.warning("Some nested ZIP files could not be extracted")
    
    logger.info("Download and extraction process completed successfully")
    return True


if __name__ == "__main__":
    download_and_process_data() 