import os
import time
import logging
import requests
import zipfile
import shutil
import re
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
    
    This function processes all XML files in the package, including:
    - f_vmp2_*.xml (Virtual Medicinal Product)
    - f_vmpp2_*.xml (Virtual Medicinal Product Pack)
    - f_amp2_*.xml (Actual Medicinal Product)
    - f_ampp2_*.xml (Actual Medicinal Product Pack)
    - f_gtin2_*.xml (GTIN mappings)
    - f_ingredient2_*.xml (Ingredients)
    - f_lookup2_*.xml (Lookup tables)
    - f_vtm2_*.xml (Virtual Therapeutic Moieties)
    
    Where * is a date or version identifier that may change with each release.
    
    Args:
        api_key (str): TRUD API key
        output_dir (str): Directory to save files to
        retry_count (int): Number of retries for failed downloads
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        dict: Paths to extracted files, mapped to standardized names
        
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
        
        # Step 4: Look for all XML files and nested zips
        # List of all possible base patterns for dm+d files
        core_files_base_patterns = [
            'f_vmp2', 
            'f_vmpp2', 
            'f_amp2', 
            'f_ampp2'
        ]
        
        additional_files_base_patterns = [
            'f_ingredient2',
            'f_lookup2',
            'f_vtm2'
        ]
        
        all_files_base_patterns = core_files_base_patterns + additional_files_base_patterns
        
        # Look for the nested zip containing GTIN data
        gtin_zip_pattern = 'GTIN'
        
        result_files = {}
        
        # Find and process nested zips for GTIN
        gtin_files = [f for f in extracted_files if gtin_zip_pattern in f and f.endswith('.zip')]
        for gtin_zip in gtin_files:
            gtin_extract_dir = os.path.join(output_dir, f"gtin_{release_id}")
            gtin_extracted = extract_zip(gtin_zip, gtin_extract_dir)
            
            # Find the f_gtin2.xml file in the extracted files with regex to handle date suffixes
            gtin_matches = [f for f in gtin_extracted if re.match(r'.*f_gtin2(_\d+)?\.xml$', os.path.basename(f))]
            if gtin_matches:
                result_files['f_gtin2.xml'] = gtin_matches[0]
                logger.info(f"Found GTIN file: {gtin_matches[0]}")
            else:
                # Extract nested ZIPs within the GTIN folder if the XML wasn't found directly
                nested_zips = [f for f in gtin_extracted if f.endswith('.zip')]
                for nested_zip in nested_zips:
                    nested_dir = os.path.join(gtin_extract_dir, 'nested')
                    nested_files = extract_zip(nested_zip, nested_dir)
                    gtin_matches = [f for f in nested_files if re.match(r'.*f_gtin2(_\d+)?\.xml$', os.path.basename(f))]
                    if gtin_matches:
                        result_files['f_gtin2.xml'] = gtin_matches[0]
                        logger.info(f"Found GTIN file in nested ZIP: {gtin_matches[0]}")
                        break
        
        # Process all XML files with flexible pattern matching
        # First, find all XML files in the extracted files
        xml_files = [f for f in extracted_files if f.endswith('.xml')]
        
        # Then, process known file patterns
        for base_pattern in all_files_base_patterns:
            # Use regex to find files that match the pattern with optional date suffix
            regex_pattern = f"^{base_pattern}(_\\d+)?\\.xml$"
            matching_files = [f for f in xml_files if re.match(regex_pattern, os.path.basename(f))]
            if matching_files:
                # Standardize to the basic pattern without date suffix
                standard_name = f"{base_pattern}.xml"
                result_files[standard_name] = matching_files[0]
                logger.info(f"Found {standard_name} file: {matching_files[0]}")
        
        # Also include any other XML files we might have found but not recognized
        for xml_file in xml_files:
            basename = os.path.basename(xml_file)
            # Skip files we've already processed
            if not any(basename.startswith(pattern) for pattern in all_files_base_patterns):
                # Use the actual basename as the key
                result_files[basename] = xml_file
                logger.info(f"Found additional XML file: {xml_file}")
        
        # Verify we have all required core files
        required_files = [f"{pattern}.xml" for pattern in core_files_base_patterns] + ['f_gtin2.xml']
        missing_files = [f for f in required_files if f not in result_files]
        
        if missing_files:
            logger.warning(f"Missing required files: {missing_files}")
        
        # Log all found files, categorized by type
        core_files = [f for f in result_files.keys() if any(f.startswith(pattern) for pattern in core_files_base_patterns) or f == 'f_gtin2.xml']
        additional_files = [f for f in result_files.keys() if f not in core_files]
        
        logger.info(f"Found core files: {core_files}")
        logger.info(f"Found additional files: {additional_files}")
        logger.info(f"Successfully processed all files: {list(result_files.keys())}")
        
        return result_files
    
    except Exception as e:
        logger.error(f"Error during dm+d download: {e}")
        raise 