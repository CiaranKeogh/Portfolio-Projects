"""
Test script for the download_dmd.py module.

This script tests the functionality of the download_dmd.py module
without actually downloading large files from the TRUD API.
"""
import os
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import requests
from requests.adapters import HTTPAdapter

from drug_tariff_master.config import RAW_DATA_DIR, REQUIRED_FILE_PATTERNS
from drug_tariff_master import download_dmd


class TestDownloadDmd(unittest.TestCase):
    """Test cases for the download_dmd module."""
    
    def setUp(self):
        """Set up test environment."""
        # Create test directory if it doesn't exist
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
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
    def test_download_file(self, mock_create_session):
        """Test download_file function with retry session."""
        # Create a mock session and response
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.headers.get.return_value = '100'
        mock_response.iter_content.return_value = [b'test content']
        mock_session.get.return_value.__enter__.return_value = mock_response
        mock_create_session.return_value = mock_session
        
        # Test file path
        test_file = RAW_DATA_DIR / "test.zip"
        
        # Call the function
        result = download_dmd.download_file("https://example.com/test.zip", test_file)
        
        # Check the result
        self.assertTrue(result)
        mock_create_session.assert_called_once()
        mock_session.get.assert_called_once()
        
        # Clean up
        if test_file.exists():
            test_file.unlink()
    
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
        """Test verify_required_files function."""
        # Create temporary test files to match the required file patterns
        test_files = []
        for pattern in REQUIRED_FILE_PATTERNS:
            # Extract the pattern name without the regex part
            file_prefix = pattern.split('_')[1].split('2')[0]
            # Create a filename that matches the pattern
            filename = f"f_{file_prefix}2_20240101.xml"
            test_file = RAW_DATA_DIR / filename
            test_file.touch()
            test_files.append(test_file)
        
        # Call the function
        success, missing_patterns = download_dmd.verify_required_files(RAW_DATA_DIR)
        
        # Check the result
        self.assertTrue(success)
        self.assertEqual(len(missing_patterns), 0)
        
        # Remove one file and test again
        test_files[0].unlink()
        success, missing_patterns = download_dmd.verify_required_files(RAW_DATA_DIR)
        self.assertFalse(success)
        self.assertEqual(len(missing_patterns), 1)
        
        # Clean up
        for test_file in test_files[1:]:
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    unittest.main() 