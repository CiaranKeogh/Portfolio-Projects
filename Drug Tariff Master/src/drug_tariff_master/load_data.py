#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Loading Script for Drug Tariff Master

This script loads data from XML files into the SQLite database in the correct order
to respect foreign key constraints.

Usage:
    python -m drug_tariff_master.load_data

"""

import os
import sys
import sqlite3
import logging
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from drug_tariff_master.config import DATA_DIR, RAW_DATA_DIR, LOGS_DIR, REQUIRED_FILE_PATTERNS
from drug_tariff_master.utils import setup_logger

# Setup logging
logger = logging.getLogger(__name__)
logger = setup_logger(__name__, "data_loading.log")


class DataLoader:
    """Class to handle loading data from XML files into the database."""

    def __init__(self, db_path=None):
        """Initialize with the path to the SQLite database."""
        self.db_path = db_path or DATA_DIR / "dmd.db"
        self.raw_dir = RAW_DATA_DIR

    def load_data(self, clear_existing=False):
        """
        Load all data from XML files into the database in the correct order.
        
        The loading order respects foreign key constraints:
        1. Lookup tables (f_lookup.xml)
        2. Ingredient (f_ingredient2.xml) - Optional
        3. VTM (f_vtm2.xml)
        4. VMP (f_vmp2.xml)
        5. AMP (f_amp2.xml)
        6. VMPP (f_vmpp2.xml)
        7. AMPP (f_ampp2.xml)
        8. GTIN (f_gtin2.xml)
        """
        logger.info("Starting data loading process")
        
        # Check if database exists
        if not self.db_path.exists():
            logger.error(f"Database not found at {self.db_path}. Run setup_database.py first.")
            return False
        
        # Find all XML files in the raw directory
        xml_files = [f for f in self.raw_dir.glob("*.xml")]
        
        # Check if required file patterns are present
        missing_patterns = []
        file_mapping = {}  # Map from pattern to actual file
        
        for pattern in REQUIRED_FILE_PATTERNS:
            pattern_regex = re.compile(pattern)
            matches = [f for f in xml_files if pattern_regex.match(f.name)]
            if not matches:
                missing_patterns.append(pattern)
            else:
                # Use the first match for each pattern
                file_mapping[pattern] = matches[0]
        
        if missing_patterns:
            logger.error(f"Required file patterns not found: {', '.join(missing_patterns)}")
            logger.error("Run download_dmd.py first to get the required files.")
            return False
        
        # Load data
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Enable foreign keys
                conn.execute("PRAGMA foreign_keys = ON")
                
                # Load in order
                lookup_file = file_mapping[r"f_lookup2_\d+\.xml"]
                self._load_lookup_data(conn, lookup_file)
                
                # Load ingredient data if available
                ingredient_pattern = r"f_ingredient2_\d+\.xml"
                if ingredient_pattern in file_mapping:
                    self._load_ingredient_data(conn, file_mapping[ingredient_pattern])
                
                vtm_file = file_mapping[r"f_vtm2_\d+\.xml"]
                self._load_vtm_data(conn, vtm_file)
                
                vmp_file = file_mapping[r"f_vmp2_\d+\.xml"]
                self._load_vmp_data(conn, vmp_file)
                
                amp_file = file_mapping[r"f_amp2_\d+\.xml"]
                self._load_amp_data(conn, amp_file)
                
                vmpp_file = file_mapping[r"f_vmpp2_\d+\.xml"]
                self._load_vmpp_data(conn, vmpp_file)
                
                ampp_file = file_mapping[r"f_ampp2_\d+\.xml"]
                self._load_ampp_data(conn, ampp_file)
                
                gtin_file = file_mapping[r"f_gtin2_\d+\.xml"]
                self._load_gtin_data(conn, gtin_file)
                
                logger.info("All data loaded successfully")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"SQLite error during data loading: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during data loading: {e}")
            return False

    def _load_lookup_data(self, conn, file_path):
        """Load lookup data from lookup XML file."""
        logger.info(f"Loading lookup data from {file_path.name}")
        # TODO: Implement loading of lookup data from XML

    def _load_ingredient_data(self, conn, file_path):
        """Load ingredient data from ingredient XML file."""
        logger.info(f"Loading ingredient data from {file_path.name}")
        # TODO: Implement loading of ingredient data from XML

    def _load_vtm_data(self, conn, file_path):
        """Load VTM data from VTM XML file."""
        logger.info(f"Loading VTM data from {file_path.name}")
        # TODO: Implement loading of VTM data from XML

    def _load_vmp_data(self, conn, file_path):
        """Load VMP data from VMP XML file."""
        logger.info(f"Loading VMP data from {file_path.name}")
        # TODO: Implement loading of VMP data and related tables from XML

    def _load_amp_data(self, conn, file_path):
        """Load AMP data from AMP XML file."""
        logger.info(f"Loading AMP data from {file_path.name}")
        # TODO: Implement loading of AMP data and related tables from XML

    def _load_vmpp_data(self, conn, file_path):
        """Load VMPP data from VMPP XML file."""
        logger.info(f"Loading VMPP data from {file_path.name}")
        # TODO: Implement loading of VMPP data and related tables from XML

    def _load_ampp_data(self, conn, file_path):
        """Load AMPP data from AMPP XML file."""
        logger.info(f"Loading AMPP data from {file_path.name}")
        # TODO: Implement loading of AMPP data and related tables from XML

    def _load_gtin_data(self, conn, file_path):
        """Load GTIN data from GTIN XML file."""
        logger.info(f"Loading GTIN data from {file_path.name}")
        # TODO: Implement loading of GTIN data from XML


def main():
    """Main function to load data into the database."""
    try:
        loader = DataLoader()
        success = loader.load_data()
        if success:
            print("Data loading completed successfully.")
            return 0
        else:
            print("Data loading failed. Check the logs for details.")
            return 1
    except Exception as e:
        print(f"Error during data loading: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 