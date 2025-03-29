"""
Test script for the download_dmd.py module.

This script tests the functionality of the download_dmd.py module
without actually downloading large files from the TRUD API.
"""
import os
import tempfile
import shutil
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import requests
from requests.adapters import HTTPAdapter
import zipfile

from drug_tariff_master.config import REQUIRED_FILE_PATTERNS
from drug_tariff_master import download_dmd


class TestDownloadDmd(unittest.TestCase):
    """Test cases for the download_dmd module."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('drug_tariff_master.download_dmd.create_session_with_retries')
    def test_get_latest_release_url(self, mock_create_session):
        """Test get_latest_release_url function with retry session."""
        # Create a mock session and response
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "releases": [
                {"archiveFileUrl": "https://example.com/test.zip"}
            ]
        }
        mock_session.get.return_value = mock_response
        mock_create_session.return_value = mock_session
        
        # Call the function
        url = download_dmd.get_latest_release_url()
        
        # Check the result
        self.assertEqual(url, "https://example.com/test.zip")
        mock_create_session.assert_called_once()
        mock_session.get.assert_called_once()
    
    @patch('drug_tariff_master.download_dmd.create_session_with_retries')
    def test_get_latest_release_url_error_handling(self, mock_create_session):
        """Test error handling in get_latest_release_url function."""
        # Test case 1: Empty releases array
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"releases": []}
        mock_session.get.return_value = mock_response
        mock_create_session.return_value = mock_session
        
        url = download_dmd.get_latest_release_url()
        self.assertIsNone(url)
        
        # Test case 2: No archiveFileUrl in release
        mock_response.json.return_value = {"releases": [{"someOtherField": "value"}]}
        url = download_dmd.get_latest_release_url()
        self.assertIsNone(url)
        
        # Test case 3: ConnectionError
        mock_session.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        url = download_dmd.get_latest_release_url()
        self.assertIsNone(url)
        
        # Test case 4: Timeout
        mock_session.get.side_effect = requests.exceptions.Timeout("Timeout error")
        url = download_dmd.get_latest_release_url()
        self.assertIsNone(url)
        
        # Test case 5: HTTPError
        mock_response = MagicMock()
        mock_response.status_code = 404
        http_error = requests.exceptions.HTTPError("Not Found")
        http_error.response = mock_response
        mock_session.get.side_effect = http_error
        url = download_dmd.get_latest_release_url()
        self.assertIsNone(url)
    
    @patch('drug_tariff_master.download_dmd.create_session_with_retries')
    def test_download_file(self, mock_create_session):
        """Test download_file function with retry session."""
        # Create a mock session and response
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.headers.get.return_value = '100'
        mock_response.iter_content.return_value = [b'test content']
        mock_session.get.return_value.__enter__.return_value = mock_response
        mock_create_session.return_value = mock_session
        
        # Test file path in the temporary directory
        test_file = self.temp_dir / "test.zip"
        
        # Call the function
        result = download_dmd.download_file("https://example.com/test.zip", test_file)
        
        # Check the result
        self.assertTrue(result)
        mock_create_session.assert_called_once()
        mock_session.get.assert_called_once()
        
        # Verify file content
        self.assertTrue(test_file.exists())
        with open(test_file, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'test content')
    
    @patch('drug_tariff_master.download_dmd.create_session_with_retries')
    def test_download_file_error_handling(self, mock_create_session):
        """Test error handling in download_file function."""
        mock_session = MagicMock()
        mock_create_session.return_value = mock_session
        test_file = self.temp_dir / "test.zip"
        
        # Test case 1: ConnectionError
        mock_session.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        result = download_dmd.download_file("https://example.com/test.zip", test_file)
        self.assertFalse(result)
        
        # Test case 2: Timeout
        mock_session.get.side_effect = requests.exceptions.Timeout("Timeout error")
        result = download_dmd.download_file("https://example.com/test.zip", test_file)
        self.assertFalse(result)
        
        # Test case 3: HTTPError
        mock_response = MagicMock()
        mock_response.status_code = 404
        http_error = requests.exceptions.HTTPError("Not Found")
        http_error.response = mock_response
        mock_session.get.side_effect = http_error
        result = download_dmd.download_file("https://example.com/test.zip", test_file)
        self.assertFalse(result)
    
    def test_create_session_with_retries(self):
        """Test create_session_with_retries function."""
        session = download_dmd.create_session_with_retries()
        self.assertIsNotNone(session)
        self.assertIsInstance(session, requests.Session)
        
        # Check that session has adapters with retries
        for protocol in ['http://', 'https://']:
            self.assertIn(protocol, session.adapters)
            adapter = session.adapters[protocol]
            self.assertIsInstance(adapter, HTTPAdapter)
            self.assertIsNotNone(adapter.max_retries)
    
    def test_verify_required_files(self):
        """Test verify_required_files function with pattern matching."""
        # Create temporary test files to match the required file patterns
        test_files = []
        for pattern in REQUIRED_FILE_PATTERNS:
            # Extract the pattern name without the regex part
            file_prefix = pattern.split('_')[1].split('2')[0]
            # Create a filename that matches the pattern
            filename = f"f_{file_prefix}2_20240101.xml"
            test_file = self.temp_dir / filename
            test_file.touch()
            test_files.append(test_file)
        
        # Call the function
        success, missing_patterns = download_dmd.verify_required_files(self.temp_dir)
        
        # Check the result
        self.assertTrue(success)
        self.assertEqual(len(missing_patterns), 0)
        
        # Remove one file and test again
        test_files[0].unlink()
        success, missing_patterns = download_dmd.verify_required_files(self.temp_dir)
        self.assertFalse(success)
        self.assertEqual(len(missing_patterns), 1)
        self.assertEqual(missing_patterns[0], REQUIRED_FILE_PATTERNS[0])
    
    def test_extract_zip(self):
        """Test extract_zip function."""
        # Create a test ZIP file
        zip_path = self.temp_dir / "test.zip"
        extract_dir = self.temp_dir / "extracted"
        extract_dir.mkdir()
        
        test_content = b"Test file content"
        test_filename = "test.txt"
        
        with zipfile.ZipFile(zip_path, 'w') as test_zip:
            test_zip.writestr(test_filename, test_content)
        
        # Call the function
        result = download_dmd.extract_zip(zip_path, extract_dir)
        
        # Check the result
        self.assertTrue(result)
        extracted_file = extract_dir / test_filename
        self.assertTrue(extracted_file.exists())
        with open(extracted_file, 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_content)
    
    def test_extract_zip_error_handling(self):
        """Test error handling in extract_zip function."""
        # Create an invalid ZIP file
        invalid_zip = self.temp_dir / "invalid.zip"
        with open(invalid_zip, 'wb') as f:
            f.write(b"This is not a valid ZIP file")
        
        extract_dir = self.temp_dir / "extracted"
        extract_dir.mkdir()
        
        # Call the function with invalid ZIP
        result = download_dmd.extract_zip(invalid_zip, extract_dir)
        self.assertFalse(result)
        
        # Call the function with non-existent ZIP
        nonexistent_zip = self.temp_dir / "nonexistent.zip"
        result = download_dmd.extract_zip(nonexistent_zip, extract_dir)
        self.assertFalse(result)
    
    @patch('drug_tariff_master.download_dmd.extract_zip')
    def test_find_and_extract_gtin_zip(self, mock_extract_zip):
        """Test find_and_extract_gtin_zip function."""
        # Set up mock extract_zip
        mock_extract_zip.return_value = True
        
        # Create a test GTIN ZIP file
        gtin_zip_path = self.temp_dir / "f_gtin2_20240101.zip"
        gtin_zip_path.touch()
        
        # Call the function
        result = download_dmd.find_and_extract_gtin_zip(self.temp_dir)
        
        # Check the result
        self.assertTrue(result)
        mock_extract_zip.assert_called_once_with(gtin_zip_path, self.temp_dir)
        
        # Test with no GTIN ZIP
        gtin_zip_path.unlink()
        result = download_dmd.find_and_extract_gtin_zip(self.temp_dir)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main() 