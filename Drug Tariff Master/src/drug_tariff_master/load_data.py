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
from pathlib import Path
import xml.etree.ElementTree as ET

from drug_tariff_master.config import DATA_DIR, RAW_DATA_DIR, LOGS_DIR
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

    def load_all_data(self):
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
        
        # Check if XML files exist
        required_files = [
            "f_lookup2_3.xml",
            "f_vtm2_3.xml",
            "f_vmp2_3.xml",
            "f_amp2_3.xml",
            "f_vmpp2_3.xml",
            "f_ampp2_3.xml",
            "f_gtin2_0.xml"
        ]
        
        optional_files = ["f_ingredient2_3.xml"]
        
        missing_files = []
        for file in required_files:
            if not (self.raw_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"Required XML files not found: {', '.join(missing_files)}")
            logger.error("Run download_dmd.py first to get the required files.")
            return False
        
        # Load data
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Enable foreign keys
                conn.execute("PRAGMA foreign_keys = ON")
                
                # Load in order
                self._load_lookup_data(conn)
                
                # Load ingredient data if available
                if (self.raw_dir / "f_ingredient2_3.xml").exists():
                    self._load_ingredient_data(conn)
                
                self._load_vtm_data(conn)
                self._load_vmp_data(conn)
                self._load_amp_data(conn)
                self._load_vmpp_data(conn)
                self._load_ampp_data(conn)
                self._load_gtin_data(conn)
                
                logger.info("All data loaded successfully")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"SQLite error during data loading: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during data loading: {e}")
            return False

    def _load_lookup_data(self, conn):
        """Load lookup data from f_lookup2_3.xml."""
        logger.info("Loading lookup data")
        # TODO: Implement loading of lookup data from XML

    def _load_ingredient_data(self, conn):
        """Load ingredient data from f_ingredient2_3.xml."""
        logger.info("Loading ingredient data")
        # TODO: Implement loading of ingredient data from XML

    def _load_vtm_data(self, conn):
        """Load VTM data from f_vtm2_3.xml."""
        logger.info("Loading VTM data")
        # TODO: Implement loading of VTM data from XML

    def _load_vmp_data(self, conn):
        """Load VMP data from f_vmp2_3.xml."""
        logger.info("Loading VMP data")
        # TODO: Implement loading of VMP data and related tables from XML

    def _load_amp_data(self, conn):
        """Load AMP data from f_amp2_3.xml."""
        logger.info("Loading AMP data")
        # TODO: Implement loading of AMP data and related tables from XML

    def _load_vmpp_data(self, conn):
        """Load VMPP data from f_vmpp2_3.xml."""
        logger.info("Loading VMPP data")
        # TODO: Implement loading of VMPP data and related tables from XML

    def _load_ampp_data(self, conn):
        """Load AMPP data from f_ampp2_3.xml."""
        logger.info("Loading AMPP data")
        # TODO: Implement loading of AMPP data and related tables from XML

    def _load_gtin_data(self, conn):
        """Load GTIN data from f_gtin2_0.xml."""
        logger.info("Loading GTIN data")
        # TODO: Implement loading of GTIN data from XML


def main():
    """Main function to load data into the database."""
    try:
        loader = DataLoader()
        success = loader.load_all_data()
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