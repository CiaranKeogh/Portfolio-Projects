import os
import time
import logging
import requests
from pathlib import Path

from ..config.config import (
    TRUD_API_KEY,
    TRUD_API_BASE_URL,
    DOWNLOAD_RETRY_COUNT,
    DOWNLOAD_RETRY_DELAY,
    TRUD_DOWNLOAD_ITEMS
)

logger = logging.getLogger(__name__)

class TRUDClient:
    """Client for interacting with the NHS TRUD API"""
    
    def __init__(self, api_key=None):
        """Initialize the TRUD API client
        
        Args:
            api_key (str, optional): The API key for TRUD. Defaults to the one in config.
        """
        self.api_key = api_key or TRUD_API_KEY
        if not self.api_key:
            raise ValueError("TRUD API key is required")
        
        self.base_url = TRUD_API_BASE_URL
        
    def download_file(self, file_id, output_path, max_retries=None, retry_delay=None):
        """Download a file from TRUD API
        
        Args:
            file_id (str): The ID of the file to download
            output_path (str or Path): Where to save the downloaded file
            max_retries (int, optional): Maximum number of retry attempts. Defaults to DOWNLOAD_RETRY_COUNT.
            retry_delay (int, optional): Delay between retries in seconds. Defaults to DOWNLOAD_RETRY_DELAY.
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        max_retries = max_retries or DOWNLOAD_RETRY_COUNT
        retry_delay = retry_delay or DOWNLOAD_RETRY_DELAY
        
        # Prepare output path
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare request URL and headers
        url = f"{self.base_url}/downloads/{file_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Try to download the file with retries
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Downloading {file_id} (Attempt {attempt}/{max_retries})")
                
                # Stream the download to handle large files
                with requests.get(url, headers=headers, stream=True) as response:
                    response.raise_for_status()
                    
                    # Write the file
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                logger.info(f"Successfully downloaded {file_id} to {output_path}")
                return True
                
            except requests.RequestException as e:
                logger.error(f"Error downloading {file_id}: {str(e)}")
                
                if attempt < max_retries:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Failed to download {file_id} after {max_retries} attempts")
                    return False
    
    def download_all_files(self, output_dir):
        """Download all required files
        
        Args:
            output_dir (str or Path): Directory to save downloaded files
            
        Returns:
            dict: Dictionary mapping file types to download success status
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for file_type, file_info in TRUD_DOWNLOAD_ITEMS.items():
            file_path = output_dir / file_info["name"]
            success = self.download_file(file_info["file_id"], file_path)
            results[file_type] = success
        
        return results 