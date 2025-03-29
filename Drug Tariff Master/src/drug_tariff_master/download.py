"""
Download mechanism for dm+d files from TRUD API.

This script:
1. Calls TRUD API to get the latest release URL
2. Downloads the ZIP file
3. Extracts the contents
4. Handles the nested GTIN ZIP file
5. Verifies the presence of all required files
"""
import os
import sys
import zipfile
import requests
import shutil
import re
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from drug_tariff_master.config import (
    TRUD_API_KEY, TRUD_API_BASE_URL, DMD_ITEM_ID,
    RAW_DATA_DIR, REQUIRED_FILE_PATTERNS, matches_required_pattern
)
from drug_tariff_master.utils import setup_logger

# Set up logger
logger = setup_logger("download", "download.log")

# Default retry configuration
DEFAULT_RETRY_CONFIG = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "HEAD"],
    respect_retry_after_header=True
)


def create_session_with_retries(retries=None):
    """
    Create a requests session with retry functionality.
    
    Args:
        retries: A urllib3.util.retry.Retry configuration. If None, DEFAULT_RETRY_CONFIG is used.
    
    Returns:
        A requests.Session with retry functionality.
    """
    if retries is None:
        retries = DEFAULT_RETRY_CONFIG
        
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session


def get_latest_release_url() -> Optional[str]:
    """
    Get the URL for the latest dm+d release from TRUD API.
    
    Returns:
        The URL string for the latest release or None if the request fails.
    """
    if not TRUD_API_KEY:
        logger.error("TRUD API key not found. Set the TRUD_API_KEY environment variable.")
        return None
    
    # Construct the API endpoint URL for the latest release
    # According to the documentation, the URL should be:
    # https://isd.digital.nhs.uk/trud/api/v1/keys/{api_key}/items/{item_id}/releases?latest
    releases_url = f"{TRUD_API_BASE_URL}/{TRUD_API_KEY}/items/{DMD_ITEM_ID}/releases?latest"
    
    try:
        logger.info(f"Requesting latest release information from TRUD API")
        session = create_session_with_retries()
        response = session.get(releases_url, timeout=60)
        response.raise_for_status()
        
        # Parse response JSON
        releases_data = response.json()
        
        # Check if the response contains releases
        if "releases" in releases_data and releases_data["releases"]:
            latest_release = releases_data["releases"][0]  # Get the first (latest) release
            
            # Check if the release has an archive file URL
            if "archiveFileUrl" in latest_release:
                return latest_release["archiveFileUrl"]
            else:
                logger.error("No archive file URL found in the latest release")
                return None
        else:
            logger.error("No releases found in the API response")
            return None
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error while requesting from TRUD API: {e}")
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout while requesting from TRUD API: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from TRUD API (status code {e.response.status_code}): {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error requesting from TRUD API: {e}")
        return None
    except ValueError as e:
        logger.error(f"Error parsing JSON response: {e}")
        return None
    except KeyError as e:
        logger.error(f"Missing key in API response: {e}")
        return None


def download_file(url: str, output_path: Path) -> bool:
    """
    Download a file from the specified URL to the output path.
    
    Args:
        url: The URL to download from.
        output_path: The path to save the downloaded file to.
    
    Returns:
        True if download successful, False otherwise.
    """
    try:
        logger.info(f"Downloading file from {url}")
        
        # Create a session with retries for resilience
        session = create_session_with_retries(
            Retry(
                total=5,
                backoff_factor=1,  # Wait 1, 2, 4, 8, 16 seconds between retries
                status_forcelist=[500, 502, 503, 504, 429],  # Also retry on 429 Too Many Requests
                allowed_methods=["GET"]
            )
        )
        
        # Use requests with stream=True for large files
        with session.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            
            # Get total file size if available
            total_size = int(r.headers.get('content-length', 0))
            
            # Open output file and write the response content
            with open(output_path, 'wb') as f:
                if total_size == 0:
                    # No content length header, download directly
                    f.write(r.content)
                else:
                    # Use tqdm to display a nice progress bar
                    desc = f"Downloading {output_path.name}"
                    chunk_size = 8192  # 8KB chunks
                    
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=desc,
                        miniters=1,
                        leave=True
                    ) as pbar:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
        
        logger.info(f"Download completed: {output_path}")
        return True
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error while downloading file: {e}")
        return False
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout while downloading file: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while downloading file (status code {e.response.status_code}): {e}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        return False
    except IOError as e:
        logger.error(f"Error writing file: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """
    Extract a ZIP file to the specified directory.
    
    Args:
        zip_path: Path to the ZIP file.
        extract_to: Directory to extract to.
    
    Returns:
        True if extraction successful, False otherwise.
    """
    try:
        logger.info(f"Extracting {zip_path} to {extract_to}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files in the ZIP
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            
            # Use tqdm to show extraction progress
            with tqdm(total=total_files, desc="Extracting files", unit="files") as pbar:
                for file in file_list:
                    zip_ref.extract(file, extract_to)
                    pbar.update(1)
        
        logger.info(f"Extraction completed")
        return True
    
    except zipfile.BadZipFile as e:
        logger.error(f"Invalid ZIP file: {e}")
        return False
    except IOError as e:
        logger.error(f"Error extracting ZIP: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error extracting ZIP: {e}")
        return False


def find_and_extract_gtin_zip(extract_dir: Path) -> bool:
    """
    Find and extract the nested GTIN ZIP file.
    
    Args:
        extract_dir: Directory containing the extracted main ZIP contents.
    
    Returns:
        True if GTIN ZIP found and extracted, False otherwise.
    """
    try:
        logger.info("Searching for GTIN ZIP file")
        
        # Look for any ZIP file that might contain GTIN data
        gtin_zip_paths = list(extract_dir.glob("*gtin*.zip"))
        
        if not gtin_zip_paths:
            logger.warning("No GTIN ZIP file found")
            return False
        
        gtin_zip_path = gtin_zip_paths[0]
        logger.info(f"Found GTIN ZIP file: {gtin_zip_path}")
        
        # Extract the GTIN ZIP file
        extract_zip(gtin_zip_path, extract_dir)
        
        return True
    
    except Exception as e:
        logger.error(f"Error handling GTIN ZIP: {e}")
        return False


def verify_required_files(directory: Path) -> Tuple[bool, List[str]]:
    """
    Verify that all required files are present in the directory using pattern matching.
    
    Args:
        directory: Directory to check for files.
    
    Returns:
        A tuple with (success_flag, list_of_missing_patterns). 
        If all required patterns are matched, success_flag is True and the list is empty.
    """
    logger.info("Verifying required files")
    
    try:
        # Get all XML files in the directory
        xml_files = [f.name for f in directory.glob("*.xml")]
        
        # Check each required pattern against the files
        missing_patterns = []
        matched_patterns = []
        
        # Use tqdm to show verification progress
        with tqdm(total=len(REQUIRED_FILE_PATTERNS), desc="Verifying files", unit="patterns") as pbar:
            for pattern in REQUIRED_FILE_PATTERNS:
                # Check if any of the files match this pattern
                matched = False
                for filename in xml_files:
                    if re.match(pattern, filename):
                        matched = True
                        matched_patterns.append(f"{pattern} -> {filename}")
                        break
                
                if not matched:
                    missing_patterns.append(pattern)
                    logger.warning(f"No file matching pattern '{pattern}' found")
                
                pbar.update(1)
        
        # Log the results
        if missing_patterns:
            logger.error(f"Missing required file patterns: {', '.join(missing_patterns)}")
            return False, missing_patterns
        else:
            logger.info("All required file patterns matched")
            for match in matched_patterns:
                logger.info(f"Matched: {match}")
            return True, []
    except Exception as e:
        logger.error(f"Error verifying required files: {e}")
        return False, ["Error occurred during verification"]


def main() -> int:
    """
    Main function to orchestrate the download process.
    
    Returns:
        0 for success, 1 for failure.
    """
    try:
        logger.info("Starting dm+d download process")
        
        # Get the latest release URL
        release_url = get_latest_release_url()
        if not release_url:
            logger.error("Failed to get latest release URL")
            return 1
        
        # Create a temporary directory for the download
        download_dir = RAW_DATA_DIR
        os.makedirs(download_dir, exist_ok=True)
        
        # Download the ZIP file
        zip_path = download_dir / "dmd_latest.zip"
        if not download_file(release_url, zip_path):
            logger.error("Failed to download the file")
            return 1
        
        # Extract the ZIP file
        if not extract_zip(zip_path, download_dir):
            logger.error("Failed to extract the ZIP file")
            return 1
        
        # Handle nested GTIN ZIP file
        find_and_extract_gtin_zip(download_dir)
        
        # Verify required files are present
        success, missing_patterns = verify_required_files(download_dir)
        if not success:
            logger.error("Not all required files were found")
            return 1
        
        # Clean up
        if zip_path.exists():
            logger.info(f"Removing ZIP file: {zip_path}")
            zip_path.unlink()
        
        logger.info("dm+d download process completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return 1 