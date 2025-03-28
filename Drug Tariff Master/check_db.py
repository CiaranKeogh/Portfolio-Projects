#!/usr/bin/env python3
"""
Simple script to check the drug tariff database structure and content.
"""

import sqlite3

def check_database(db_path='data/dmd.db'):
    """Check the database structure and content."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Database at {db_path}")
    print(f"Found {len(tables)} tables")
    
    # Check row counts in main tables
    main_tables = ['vtm', 'vmp', 'vmpp', 'amp', 'ampp', 'gtin', 'ingredient', 'unified_search']
    for table in main_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} rows")
    
    # Check for any data in unified search
    cursor.execute("SELECT COUNT(*) FROM unified_search")
    unified_count = cursor.fetchone()[0]
    print(f"Total unified search records: {unified_count}")
    
    conn.close()

if __name__ == "__main__":
    check_database() 