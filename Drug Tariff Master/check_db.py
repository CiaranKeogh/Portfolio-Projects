#!/usr/bin/env python3
"""
Simple script to check the database and show some basic query results.
"""

import sqlite3
import os
import sys

def main():
    db_path = "data/dmd.db"
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get table counts
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]
        
        print(f"Database contains {len(tables)} tables:")
        
        # Print the count of rows in each table
        for table in sorted(tables):
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"  - {table}: {count} rows")
        
        print("\n--- Sample data queries ---\n")
        
        # Get column names for vmp table
        cursor.execute("PRAGMA table_info(vmp)")
        vmp_columns = [row['name'] for row in cursor.fetchall()]
        print(f"VMP table columns: {', '.join(vmp_columns)}")
        
        # Show a sample of the VMP table
        print("\nSample VMPs (Virtual Medicinal Products):")
        cursor.execute("""
            SELECT *
            FROM vmp
            LIMIT 5
        """)
        vmps = cursor.fetchall()
        for vmp in vmps:
            print(f"  VMP ID: {vmp['cd']}, Name: {vmp['nm']}")
        
        # Get column names for amp table
        cursor.execute("PRAGMA table_info(amp)")
        amp_columns = [row['name'] for row in cursor.fetchall()]
        print(f"\nAMP table columns: {', '.join(amp_columns)}")
        
        # Show a sample from the AMP table
        print("\nSample AMPs (Actual Medicinal Products):")
        cursor.execute("""
            SELECT *
            FROM amp
            LIMIT 5
        """)
        amps = cursor.fetchall()
        for amp in amps:
            print(f"  AMP ID: {amp['cd']}, Name: {amp['nm']}, VMP ID: {amp['vmp']}")
        
        # Show a sample from the ingredient table
        print("\nSample Ingredients (if table exists):")
        if 'ing' in tables:
            cursor.execute("""
                SELECT *
                FROM ing
                LIMIT 5
            """)
            ingredients = cursor.fetchall()
            for ing in ingredients:
                print(f"  Ingredient ID: {ing['cd']}, Name: {ing['nm']}")
        else:
            print("  Ingredient table not found. Looking for alternative tables...")
            for table in tables:
                if 'ing' in table.lower():
                    print(f"  Found potential ingredient table: {table}")
        
        print("\nSample search lookup:")
        if 'unified_search' in tables:
            cursor.execute("""
                SELECT *
                FROM unified_search
                WHERE name LIKE '%paracetamol%'
                LIMIT 5
            """)
            results = cursor.fetchall()
            # Get column names
            column_names = [desc[0] for desc in cursor.description]
            print(f"  Unified search columns: {', '.join(column_names)}")
            
            for item in results:
                brand_type = "Brand" if item['is_brand'] == 1 else "Generic"
                dt_price = item['dt_price']
                price = f"£{dt_price/100:.2f}" if dt_price is not None else "N/A"
                
                print(f"  • {item['name']} ({brand_type})")
                if 'ingredient_list' in column_names:
                    print(f"    Ingredients: {item['ingredient_list'] or 'N/A'}")
                if 'pack_size' in column_names:
                    print(f"    Pack Size: {item['pack_size'] or 'N/A'}")
                print(f"    Price: {price}")
                print("")
        else:
            print("  Unified search table not found.")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 