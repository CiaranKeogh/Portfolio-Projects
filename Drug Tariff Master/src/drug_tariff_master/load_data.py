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
from lxml import etree

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
                
                # Clear existing data if requested
                if clear_existing:
                    self._clear_existing_data(conn)
                
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
                
                # Report final counts
                self._report_table_counts(conn)
                
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
        
    def _execute_batch(self, conn, sql, batch_data):
        """
        Execute a batch insert operation with error handling.
        
        This method attempts to insert multiple rows at once for efficiency.
        If a batch operation fails (e.g., due to integrity constraints),
        it falls back to inserting records individually to maximize data loading.
        
        Args:
            conn: The active sqlite3.Connection object.
            sql: The parameterized INSERT SQL statement.
            batch_data: A list of tuples, where each tuple represents a row.
            
        Returns:
            int: Number of rows successfully inserted.
        """
        # If batch is empty, return 0 (no rows processed)
        if not batch_data:
            return 0
            
        # Get a database cursor
        cursor = conn.cursor()
        
        try:
            # Attempt batch insert
            cursor.executemany(sql, batch_data)
            logger.debug(f"Batch inserted {len(batch_data)} rows using: {sql[:50]}...")
            return len(batch_data)
            
        except sqlite3.IntegrityError as e:
            # Handle integrity errors (like constraint violations, duplicate keys)
            logger.warning(f"Batch insert failed ({e}). Falling back to individual inserts for {len(batch_data)} records.")
            
            # Fall back to individual inserts
            inserted_count = 0
            for record in batch_data:
                try:
                    cursor.execute(sql, record)
                    inserted_count += 1
                except sqlite3.Error as inner_e:
                    logger.error(f"Failed to insert record {record}: {inner_e}")
                    # Continue to next record, don't stop the process
            
            logger.warning(f"Inserted {inserted_count} rows individually after batch failure.")
            return inserted_count
            
        except sqlite3.Error as e:
            # Handle other SQLite errors during batch attempt
            logger.error(f"Batch insert failed with SQLite error: {e}")
            return 0

    def _clear_existing_data(self, conn):
        """
        Clear all data from existing tables in the correct order.
        
        This method removes all data from the tables while preserving the table structure.
        Tables are cleared in the reverse order of dependencies to avoid foreign key constraint violations.
        
        Args:
            conn: The active sqlite3.Connection object.
        """
        logger.info("Clearing existing data from database tables...")
        
        cursor = conn.cursor()
        
        # Tables in reverse dependency order (same as in setup_database.py)
        tables_in_reverse_dependency_order = [
            # AMPP detail/linking tables
            "ampp_gtin",
            "ampp_combination_content",
            "ampp_reimbursement_info",
            "ampp_price_info",
            "ampp_prescribing_info",
            "ampp_appliance_pack_info",
            "ampp",
            
            # VMPP detail/linking tables
            "vmpp_combination_content",
            "vmpp_drug_tariff_info",
            "vmpp",
            
            # AMP detail/linking tables
            "amp_information",
            "amp_licensed_route",
            "amp_ingredient",
            "amp",
            
            # VMP detail/linking tables
            "vmp_control_drug_info",
            "vmp_drug_route",
            "vmp_drug_form",
            "vmp_ontology_form_route",
            "vmp_ingredient",
            "vmp",
            
            # VTM tables
            "vtm",
            
            # Ingredient tables
            "ingredient",
            
            # Lookup tables
            "lookup_licensing_authority_change_reason",
            "lookup_availability_restriction",
            "lookup_legal_category",
            "lookup_price_basis",
            "lookup_df_indicator",
            "lookup_discontinued_indicator",
            "lookup_virtual_product_non_avail",
            "lookup_dnd",
            "lookup_special_container",
            "lookup_reimbursement_status",
            "lookup_basis_of_strength",
            "lookup_colour",
            "lookup_flavour",
            "lookup_supplier",
            "lookup_drug_tariff_payment_category",
            "lookup_route",
            "lookup_ontology_form_route",
            "lookup_form",
            "lookup_unit_of_measure",
            "lookup_licensing_authority",
            "lookup_control_drug_category",
            "lookup_virtual_product_pres_status",
            "lookup_name_change_reason",
            "lookup_basis_of_name",
            "lookup_combination_product_indicator",
            "lookup_combination_pack_indicator"
        ]
        
        for table_name in tables_in_reverse_dependency_order:
            try:
                cursor.execute(f"DELETE FROM {table_name};")
                logger.debug(f"Cleared data from table {table_name}")
            except sqlite3.Error as e:
                logger.error(f"Error clearing data from table {table_name}: {e}")
        
        # Commit is not done here as this method should be part of a larger transaction
        
        logger.info("Finished clearing existing data.")

    def _report_table_counts(self, conn):
        """
        Query and log the number of rows in each relevant table.
        
        This serves as a basic validation and summary after the data loading process.
        
        Args:
            conn: The active sqlite3.Connection object.
        """
        logger.info("Reporting final table counts...")
        
        cursor = conn.cursor()
        
        # Use the same table list as in _clear_existing_data but order doesn't matter for counting
        all_dmd_tables = [
            # AMPP detail/linking tables
            "ampp_gtin",
            "ampp_combination_content",
            "ampp_reimbursement_info",
            "ampp_price_info",
            "ampp_prescribing_info",
            "ampp_appliance_pack_info",
            "ampp",
            
            # VMPP detail/linking tables
            "vmpp_combination_content",
            "vmpp_drug_tariff_info",
            "vmpp",
            
            # AMP detail/linking tables
            "amp_information",
            "amp_licensed_route",
            "amp_ingredient",
            "amp",
            
            # VMP detail/linking tables
            "vmp_control_drug_info",
            "vmp_drug_route",
            "vmp_drug_form",
            "vmp_ontology_form_route",
            "vmp_ingredient",
            "vmp",
            
            # VTM tables
            "vtm",
            
            # Ingredient tables
            "ingredient",
            
            # Lookup tables
            "lookup_licensing_authority_change_reason",
            "lookup_availability_restriction",
            "lookup_legal_category",
            "lookup_price_basis",
            "lookup_df_indicator",
            "lookup_discontinued_indicator",
            "lookup_virtual_product_non_avail",
            "lookup_dnd",
            "lookup_special_container",
            "lookup_reimbursement_status",
            "lookup_basis_of_strength",
            "lookup_colour",
            "lookup_flavour",
            "lookup_supplier",
            "lookup_drug_tariff_payment_category",
            "lookup_route",
            "lookup_ontology_form_route",
            "lookup_form",
            "lookup_unit_of_measure",
            "lookup_licensing_authority",
            "lookup_control_drug_category",
            "lookup_virtual_product_pres_status",
            "lookup_name_change_reason",
            "lookup_basis_of_name",
            "lookup_combination_product_indicator",
            "lookup_combination_pack_indicator"
        ]
        
        total_rows = 0
        
        for table_name in all_dmd_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                logger.info(f"Table '{table_name}': {count} rows")
                total_rows += count
            except sqlite3.Error as e:
                logger.error(f"Error counting rows in table {table_name}: {e}")
        
        logger.info(f"Total rows loaded across relevant tables: {total_rows}")

    def _validate_xml(self, xml_path, xsd_path):
        """
        Validate an XML file against its corresponding XSD schema.
        
        This validation ensures the XML file conforms to the expected structure
        before attempting to parse and load it.
        
        Args:
            xml_path: A pathlib.Path object to the XML file.
            xsd_path: A pathlib.Path object to the corresponding XSD file.
            
        Returns:
            bool: True if validation passes or is skipped, False if validation fails.
        """
        # Check if XSD path exists
        if not xsd_path.exists():
            logger.warning(f"XSD schema not found at {xsd_path}, skipping validation for {xml_path.name}")
            return True
            
        try:
            # Parse the XSD schema
            xmlschema_doc = etree.parse(str(xsd_path))
            
            # Create a schema object
            xmlschema = etree.XMLSchema(xmlschema_doc)
            
            # Parse the XML document
            xml_doc = etree.parse(str(xml_path))
            
            # Validate the XML against the schema
            is_valid = xmlschema.validate(xml_doc)
            
            if not is_valid:
                # Log validation errors
                logger.error(f"XML validation failed for {xml_path.name} against {xsd_path.name}:\n{xmlschema.error_log}")
                return False
            else:
                logger.info(f"XML validation successful for {xml_path.name}")
                return True
                
        except Exception as e:
            # Log any errors during the validation process
            logger.error(f"Error during XML validation for {xml_path.name}: {e}")
            return False


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