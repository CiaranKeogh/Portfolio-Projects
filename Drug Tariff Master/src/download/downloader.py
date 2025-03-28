import os
import time
import logging
import requests
import zipfile
import shutil
from tqdm import tqdm

class DownloadError(Exception):
    """Exception raised for errors during download process."""
    pass

def request_json(url, api_key=None, max_retries=3, retry_delay=300):
    """
    Request JSON data from an API endpoint with retry logic.
    
    Args:
        url (str): The URL to request data from
        api_key (str, optional): API key to use in the request
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        dict: The JSON response data
        
    Raises:
        DownloadError: If the request fails after all retries
    """
    logger = logging.getLogger('drug_tariff_processor')
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Requesting data from {url} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached, giving up.")
                raise DownloadError(f"Failed to retrieve data after {max_retries} attempts: {e}")

def download_file(url, output_path, api_key=None, max_retries=3, retry_delay=300):
    """
    Download a file with progress tracking and retry logic.
    
    Args:
        url (str): The URL to download from
        output_path (str): Where to save the downloaded file
        api_key (str, optional): API key to use in the request
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        
    Raises:
        DownloadError: If the download fails after all retries
    """
    logger = logging.getLogger('drug_tariff_processor')
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Downloading file from {url} to {output_path} (attempt {attempt + 1}/{max_retries})")
            
            # Stream the download with progress bar
            with requests.get(url, headers=headers, stream=True, timeout=300) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'wb') as f, tqdm(
                    desc=os.path.basename(output_path),
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            logger.info(f"Download completed: {output_path}")
            return
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached, giving up.")
                raise DownloadError(f"Failed to download file after {max_retries} attempts: {e}")

def extract_zip(zip_path, extract_to, specific_files=None):
    """
    Extract files from a zip archive.
    
    Args:
        zip_path (str): Path to the ZIP file
        extract_to (str): Directory to extract files to
        specific_files (list, optional): List of specific files to extract
        
    Returns:
        list: Paths to extracted files
        
    Raises:
        DownloadError: If extraction fails
    """
    logger = logging.getLogger('drug_tariff_processor')
    
    try:
        logger.info(f"Extracting {zip_path} to {extract_to}")
        os.makedirs(extract_to, exist_ok=True)
        
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files to extract
            all_files = zip_ref.namelist()
            files_to_extract = []
            
            if specific_files:
                # Find files that match the patterns
                for pattern in specific_files:
                    matching = [f for f in all_files if pattern in f]
                    files_to_extract.extend(matching)
                
                if not files_to_extract:
                    logger.warning(f"No files matching {specific_files} found in zip")
                    return []
            else:
                files_to_extract = all_files
            
            # Extract the files
            for file in files_to_extract:
                logger.info(f"Extracting file: {file}")
                zip_ref.extract(file, extract_to)
                extracted_path = os.path.join(extract_to, file)
                extracted_files.append(extracted_path)
        
        logger.info(f"Extracted {len(extracted_files)} files")
        return extracted_files
    
    except (zipfile.BadZipFile, OSError) as e:
        logger.error(f"Failed to extract zip: {e}")
        raise DownloadError(f"Failed to extract zip file {zip_path}: {e}")

def download_dmd_files(api_key, output_dir="data", retry_count=3, retry_delay=300):
    """
    Download and extract the NHS Dictionary of Medicines and Devices (dm+d) files.
    
    Args:
        api_key (str): TRUD API key
        output_dir (str): Directory to save files to
        retry_count (int): Number of retries for failed downloads
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        dict: Paths to extracted files
        
    Raises:
        DownloadError: If download or extraction fails
    """
    logger = logging.getLogger('drug_tariff_processor')
    
    # Ensure output directory exists
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Get the latest release information
        release_url = f"https://isd.digital.nhs.uk/trud/api/v1/keys/{api_key}/items/24/releases?latest"
        release_data = request_json(release_url)
        
        if not release_data or 'releases' not in release_data or not release_data['releases']:
            raise DownloadError("No releases found in the API response")
        
        # Get the archive URL from the latest release
        archive_url = release_data['releases'][0]['archiveFileUrl']
        release_id = release_data['releases'][0]['id']
        logger.info(f"Found latest release: {release_id}")
        
        # Step 2: Download the ZIP file
        zip_path = os.path.join(output_dir, f"dmd_release_{release_id}.zip")
        download_file(archive_url, zip_path)
        
        # Step 3: Extract the main ZIP file
        extract_dir = os.path.join(output_dir, f"dmd_{release_id}")
        extracted_files = extract_zip(zip_path, extract_dir)
        
        # Step 4: Look for the required XML files and nested zips
        files_of_interest = [
            'f_vmp2.xml', 
            'f_vmpp2.xml', 
            'f_amp2.xml', 
            'f_ampp2.xml'
        ]
        
        # Also look for the nested zip containing f_gtin2.xml
        gtin_zip_pattern = 'f_gtin2'
        
        result_files = {}
        
        # Find and process nested zips
        gtin_files = [f for f in extracted_files if gtin_zip_pattern in f and f.endswith('.zip')]
        for gtin_zip in gtin_files:
            gtin_extract_dir = os.path.join(output_dir, f"gtin_{release_id}")
            gtin_extracted = extract_zip(gtin_zip, gtin_extract_dir)
            
            # Find the f_gtin2.xml file in the extracted files
            for f in gtin_extracted:
                if f.endswith('f_gtin2.xml'):
                    result_files['f_gtin2.xml'] = f
                    break
        
        # Process the main XML files
        for file in files_of_interest:
            matching_files = [f for f in extracted_files if f.endswith(file)]
            if matching_files:
                result_files[file] = matching_files[0]
        
        # Verify we have all required files
        required_files = files_of_interest + ['f_gtin2.xml']
        missing_files = [f for f in required_files if f not in result_files]
        
        if missing_files:
            logger.warning(f"Missing required files: {missing_files}")
        
        logger.info(f"Successfully processed all files: {list(result_files.keys())}")
        return result_files
    
    except Exception as e:
        logger.error(f"Error during dm+d download: {e}")
        raise 