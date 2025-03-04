import os
import sys
import logging
import sqlite3
from pathlib import Path
from lxml import etree

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import config
import database
import parser

# Set up logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('process_lookup')

def debug_lookup_xml(xml_path):
    """Debug the lookup XML file structure."""
    try:
        print(f"Debugging lookup XML file: {xml_path}")
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        print(f"XML root tag: {root.tag}")
        
        # Check for lookup categories
        lookup_categories = [
            "CONTROL_DRUG_CATEGORY",
            "LEGAL_CATEGORY",
            "FORM",
            "ROUTE",
            "UNIT_OF_MEASURE",
            "SUPPLIER",
        ]
        
        for category in lookup_categories:
            elements = root.xpath(f"//{category}/INFO")
            print(f"Category {category}: {len(elements)} elements found")
            
            if elements and len(elements) > 0:
                # Show sample of first element
                sample = elements[0]
                print(f"Sample element for {category}:")
                for child in sample:
                    print(f"  {child.tag}: {child.text}")
    
    except Exception as e:
        print(f"Error debugging lookup XML: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Process the lookup XML file."""
    print("Starting to process lookup XML file")
    
    # Check if database exists
    db_path = config.DB_PATH
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"Database file does not exist at {db_path}")
        return False
    
    # Connect to the database directly
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Connected to database successfully")
        
        # Check if lookup tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'lookup_%'")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} lookup tables: {[t[0] for t in tables]}")
        
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Find the lookup XML file
    lookup_pattern = config.FILE_PATTERNS['lookup']['pattern']
    lookup_schema = config.FILE_PATTERNS['lookup']['schema']
    
    print(f"Looking for files matching pattern: {lookup_pattern}")
    print(f"In directory: {config.DATA_DIR}")
    
    lookup_file = None
    for file_path in Path(config.DATA_DIR).glob(f"**/{lookup_pattern}"):
        print(f"Found lookup file: {file_path}")
        
        # Validate the file against its schema
        if parser.validate_xml_against_xsd(file_path, lookup_schema):
            lookup_file = file_path
            break
    
    if not lookup_file:
        print("Lookup file not found or did not validate")
        return False
    
    # Debug the lookup XML structure
    debug_lookup_xml(lookup_file)
    
    # Process the lookup file
    print(f"Processing lookup file: {lookup_file}")
    if parser.parse_lookup_data(lookup_file):
        print("Lookup file processed successfully")
        
        # Check if data was inserted
        conn = database.get_connection()
        cursor = conn.cursor()
        
        lookup_tables = [
            "lookup_form",
            "lookup_route",
            "lookup_supplier",
            "lookup_control_drug_category",
            "lookup_legal_category",
            "lookup_unit_of_measure",
        ]
        
        for table in lookup_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Table {table} has {count} rows")
            except Exception as e:
                print(f"Error checking table {table}: {e}")
        
        conn.close()
        return True
    else:
        print("Failed to process lookup file")
        return False

if __name__ == "__main__":
    main() 