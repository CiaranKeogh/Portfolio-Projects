#!/usr/bin/env python3
"""
Simple script to search the Drug Tariff database.
"""

import sqlite3
import argparse
import os
import sys

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Search the Drug Tariff database.")
    parser.add_argument("--db", default="data/dmd.db", help="Path to the database file")
    parser.add_argument("--query", help="General search query")
    parser.add_argument("--gtin", help="Search by GTIN (barcode)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of results")
    
    args = parser.parse_args()
    
    # Make sure at least one search parameter is provided
    if not args.query and not args.gtin:
        parser.print_help()
        print("\nError: Please provide at least one search parameter (--query or --gtin)")
        sys.exit(1)
    
    # Check if database file exists
    if not os.path.exists(args.db):
        print(f"Error: Database file not found at {args.db}")
        sys.exit(1)
    
    try:
        # Connect to the database
        conn = sqlite3.connect(args.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if unified_search table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='unified_search'")
        unified_search_exists = cursor.fetchone() is not None
        
        if args.gtin:
            if unified_search_exists:
                # Search by GTIN in unified_search table
                cursor.execute("""
                    SELECT *
                    FROM unified_search
                    WHERE gtin = ?
                """, (args.gtin,))
                
                results = cursor.fetchall()
                if results:
                    print(f"Found product with GTIN: {args.gtin}")
                    # Get column names
                    column_names = [desc[0] for desc in cursor.description]
                    
                    print("\nResult:")
                    for i, item in enumerate(results, 1):
                        brand_status = "Brand" if 'is_brand' in column_names and item['is_brand'] == 1 else "Generic"
                        print(f"{i}. {item['name']} ({brand_status})")
                        
                        # Handle various optional fields
                        if 'ingredient_list' in column_names and item['ingredient_list']:
                            print(f"   Ingredients: {item['ingredient_list']}")
                        
                        if 'pack_size' in column_names and item['pack_size']:
                            print(f"   Pack Size: {item['pack_size']}")
                        
                        if 'dt_price' in column_names and item['dt_price'] is not None:
                            print(f"   Drug Tariff Price: £{item['dt_price']/100:.2f}")
                        
                        if 'nhs_price' in column_names and item['nhs_price'] is not None:
                            print(f"   NHS Price: £{item['nhs_price']/100:.2f}")
                        
                        print(f"   GTIN: {item['gtin']}")
                        print()
                else:
                    print(f"No product found with GTIN: {args.gtin}")
                    
                    # Check if the GTIN exists in the raw GTIN table
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gtin'")
                    if cursor.fetchone():
                        cursor.execute("""
                            SELECT * FROM gtin WHERE gtin = ?
                        """, (args.gtin,))
                        raw_gtin = cursor.fetchone()
                        
                        if raw_gtin:
                            print("Found in raw GTIN table but not in unified search.")
                            for key in raw_gtin.keys():
                                print(f"   {key}: {raw_gtin[key]}")
            else:
                # Try direct GTIN table if it exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gtin'")
                if cursor.fetchone():
                    cursor.execute("""
                        SELECT * FROM gtin WHERE gtin = ?
                    """, (args.gtin,))
                    gtin_result = cursor.fetchone()
                    
                    if gtin_result:
                        print(f"Found GTIN: {args.gtin}")
                        print("\nGTIN Details:")
                        
                        # Get the related AMPP
                        if 'ampp' in gtin_result.keys():
                            ampp_id = gtin_result['ampp']
                            cursor.execute("""
                                SELECT * FROM ampp WHERE cd = ?
                            """, (ampp_id,))
                            ampp = cursor.fetchone()
                            
                            if ampp:
                                print(f"Product: {ampp['nm']}")
                                print(f"AMPP ID: {ampp['cd']}")
                                
                                # Get pricing info if available
                                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ampp_price_info'")
                                if cursor.fetchone():
                                    cursor.execute("""
                                        SELECT * FROM ampp_price_info WHERE ampp = ?
                                    """, (ampp_id,))
                                    price_info = cursor.fetchone()
                                    
                                    if price_info:
                                        if 'price' in price_info.keys() and price_info['price'] is not None:
                                            print(f"Price: £{price_info['price']/100:.2f}")
                    else:
                        print(f"No product found with GTIN: {args.gtin}")
                else:
                    print("GTIN table not found in database.")
        
        elif args.query:
            if unified_search_exists:
                # Search in the unified_search table
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM unified_search 
                    WHERE name LIKE ?
                """, (f"%{args.query}%",))
                count = cursor.fetchone()['count']
                
                print(f"Found {count} results matching '{args.query}'")
                
                if count > 0:
                    cursor.execute("""
                        SELECT * 
                        FROM unified_search 
                        WHERE name LIKE ? 
                        LIMIT ?
                    """, (f"%{args.query}%", args.limit))
                    
                    # Get column names
                    column_names = [desc[0] for desc in cursor.description]
                    
                    results = cursor.fetchall()
                    print("\nResults:")
                    for i, item in enumerate(results, 1):
                        brand_status = "Brand" if 'is_brand' in column_names and item['is_brand'] == 1 else "Generic"
                        print(f"{i}. {item['name']} ({brand_status})")
                        
                        # Handle various optional fields
                        if 'ingredient_list' in column_names and item['ingredient_list']:
                            print(f"   Ingredients: {item['ingredient_list']}")
                        
                        if 'pack_size' in column_names and item['pack_size']:
                            print(f"   Pack Size: {item['pack_size']}")
                        
                        if 'dt_price' in column_names and item['dt_price'] is not None:
                            print(f"   Drug Tariff Price: £{item['dt_price']/100:.2f}")
                        
                        if 'nhs_price' in column_names and item['nhs_price'] is not None:
                            print(f"   NHS Price: £{item['nhs_price']/100:.2f}")
                        
                        if 'gtin' in column_names and item['gtin']:
                            print(f"   GTIN: {item['gtin']}")
                        
                        print()
                    
                    if count > args.limit:
                        print(f"Showing {args.limit} of {count} matches. Use --limit to see more.")
            else:
                # Try alternative approaches if unified_search doesn't exist
                print("The unified_search table does not exist. Trying to search directly in product tables.")
                
                # Try to search in AMPP table (Actual Medicinal Product Pack)
                cursor.execute("""
                    SELECT COUNT(*) as count FROM ampp WHERE nm LIKE ?
                """, (f"%{args.query}%",))
                count = cursor.fetchone()['count']
                
                print(f"Found {count} matching AMPPs containing '{args.query}'")
                
                if count > 0:
                    cursor.execute("""
                        SELECT cd, nm, vmpp, invalid
                        FROM ampp
                        WHERE nm LIKE ?
                        LIMIT ?
                    """, (f"%{args.query}%", args.limit))
                    
                    results = cursor.fetchall()
                    print("\nResults:")
                    for i, result in enumerate(results, 1):
                        print(f"{i}. {result['nm']}")
                        print(f"   ID: {result['cd']}")
                        print(f"   VMPP: {result['vmpp']}")
                        print(f"   Invalid: {'Yes' if result['invalid'] else 'No'}")
                        print()
                
                # Try to search in AMP table (Actual Medicinal Product)
                cursor.execute("""
                    SELECT COUNT(*) as count FROM amp WHERE nm LIKE ?
                """, (f"%{args.query}%",))
                count = cursor.fetchone()['count']
                
                print(f"Found {count} matching AMPs containing '{args.query}'")
                
                if count > 0:
                    cursor.execute("""
                        SELECT cd, nm, vmp, invalid
                        FROM amp
                        WHERE nm LIKE ?
                        LIMIT ?
                    """, (f"%{args.query}%", args.limit))
                    
                    results = cursor.fetchall()
                    print("\nResults:")
                    for i, result in enumerate(results, 1):
                        print(f"{i}. {result['nm']}")
                        print(f"   ID: {result['cd']}")
                        print(f"   VMP: {result['vmp']}")
                        print(f"   Invalid: {'Yes' if result['invalid'] else 'No'}")
                        print()
                        
                # Try ingredient search if ingredient table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ingredient'")
                if cursor.fetchone():
                    cursor.execute("""
                        SELECT COUNT(*) as count FROM ingredient WHERE nm LIKE ?
                    """, (f"%{args.query}%",))
                    count = cursor.fetchone()['count']
                    
                    print(f"Found {count} matching ingredients containing '{args.query}'")
                    
                    if count > 0:
                        cursor.execute("""
                            SELECT cd, nm
                            FROM ingredient
                            WHERE nm LIKE ?
                            LIMIT ?
                        """, (f"%{args.query}%", args.limit))
                        
                        results = cursor.fetchall()
                        print("\nIngredient Results:")
                        for i, result in enumerate(results, 1):
                            print(f"{i}. {result['nm']} (ID: {result['cd']})")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 