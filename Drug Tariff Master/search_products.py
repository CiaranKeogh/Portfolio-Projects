#!/usr/bin/env python3
"""
Search utility for the Drug Tariff database.
Allows users to search for products by name, ingredient, or GTIN.
"""

import sqlite3
import argparse
import os
import sys
from tabulate import tabulate

def get_db_connection(db_path):
    """Get a connection to the SQLite database."""
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def search_by_name(conn, name, limit=10):
    """Search for products by name."""
    # First get the total count
    count_query = """
    SELECT COUNT(*) as total
    FROM unified_search
    WHERE name LIKE ?
    """
    cursor = conn.cursor()
    cursor.execute(count_query, (f"%{name}%",))
    total_count = cursor.fetchone()['total']
    
    # Then get the limited results
    query = """
    SELECT
        name,
        CASE WHEN is_brand = 1 THEN 'Brand' ELSE 'Generic' END as type,
        ingredient_list,
        pack_size,
        dt_price / 100.0 as dt_price,
        nhs_price / 100.0 as nhs_price,
        gtin
    FROM
        unified_search
    WHERE
        name LIKE ?
    ORDER BY
        name
    LIMIT ?
    """
    cursor.execute(query, (f"%{name}%", limit))
    return cursor.fetchall(), total_count

def search_by_ingredient(conn, ingredient, limit=10):
    """Search for products by ingredient."""
    # First get the total count
    count_query = """
    SELECT COUNT(*) as total
    FROM unified_search
    WHERE ingredient_list LIKE ?
    """
    cursor = conn.cursor()
    cursor.execute(count_query, (f"%{ingredient}%",))
    total_count = cursor.fetchone()['total']
    
    # Then get the limited results
    query = """
    SELECT
        name,
        CASE WHEN is_brand = 1 THEN 'Brand' ELSE 'Generic' END as type,
        ingredient_list,
        pack_size,
        dt_price / 100.0 as dt_price,
        nhs_price / 100.0 as nhs_price,
        gtin
    FROM
        unified_search
    WHERE
        ingredient_list LIKE ?
    ORDER BY
        name
    LIMIT ?
    """
    cursor.execute(query, (f"%{ingredient}%", limit))
    return cursor.fetchall(), total_count

def search_by_gtin(conn, gtin):
    """Search for a product by GTIN (barcode)."""
    query = """
    SELECT
        name,
        CASE WHEN is_brand = 1 THEN 'Brand' ELSE 'Generic' END as type,
        ingredient_list,
        pack_size,
        dt_price / 100.0 as dt_price,
        nhs_price / 100.0 as nhs_price,
        gtin
    FROM
        unified_search
    WHERE
        gtin = ?
    LIMIT 1
    """
    cursor = conn.cursor()
    cursor.execute(query, (gtin,))
    results = cursor.fetchall()
    return results, len(results)

def search_by_date(conn, date, limit=10):
    """Search for products updated after a specific date (YYYY-MM-DD)."""
    # First get the total count
    count_query = """
    SELECT COUNT(*) as total
    FROM unified_search
    WHERE date(last_updated) >= date(?)
    """
    cursor = conn.cursor()
    cursor.execute(count_query, (date,))
    total_count = cursor.fetchone()['total']
    
    # Then get the limited results
    query = """
    SELECT
        name,
        CASE WHEN is_brand = 1 THEN 'Brand' ELSE 'Generic' END as type,
        ingredient_list,
        pack_size,
        dt_price / 100.0 as dt_price,
        nhs_price / 100.0 as nhs_price,
        gtin
    FROM
        unified_search
    WHERE
        date(last_updated) >= date(?)
    ORDER BY
        date(last_updated) DESC
    LIMIT ?
    """
    cursor.execute(query, (date, limit))
    return cursor.fetchall(), total_count

def format_results(results):
    """Format the results for display."""
    # Convert the results to a list of dicts for tabulate
    rows = []
    headers = ["Name", "Type", "Ingredients", "Pack Size", "DT Price (£)", "NHS Price (£)", "GTIN"]
    
    for row in results:
        # Format prices as currency strings
        dt_price = f"£{row['dt_price']:.2f}" if row['dt_price'] is not None else "N/A"
        nhs_price = f"£{row['nhs_price']:.2f}" if row['nhs_price'] is not None else "N/A"
        
        # Handle missing or empty ingredient lists
        ingredients = row['ingredient_list'] if row['ingredient_list'] is not None else ""
        if ingredients and len(ingredients) > 30:
            ingredients = ingredients[:30] + "..."
        
        # Handle missing pack size
        pack_size = row['pack_size'] if row['pack_size'] is not None else ""
        
        # Handle missing GTIN
        gtin = row['gtin'] if row['gtin'] is not None else ""
        
        rows.append([
            row['name'],
            row['type'],
            ingredients,
            pack_size,
            dt_price,
            nhs_price,
            gtin
        ])
    
    if not rows:
        return "No results found."
    
    return tabulate(rows, headers=headers, tablefmt="grid")

def main():
    parser = argparse.ArgumentParser(description="Search the Drug Tariff database.")
    parser.add_argument("--db", default="data/dmd.db", help="Path to the database file")
    parser.add_argument("--name", help="Search by product name")
    parser.add_argument("--ingredient", help="Search by ingredient name")
    parser.add_argument("--gtin", help="Search by GTIN (barcode)")
    parser.add_argument("--date", help="Search for products updated after date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of results to return")
    
    args = parser.parse_args()
    
    # Make sure at least one search parameter is provided
    if not args.name and not args.ingredient and not args.gtin and not args.date:
        parser.print_help()
        print("\nError: Please provide at least one search parameter (--name, --ingredient, --gtin, or --date)")
        sys.exit(1)
    
    conn = get_db_connection(args.db)
    
    try:
        if args.gtin:
            results, total_count = search_by_gtin(conn, args.gtin)
            print(f"Searching for product with GTIN: {args.gtin}")
        elif args.name:
            results, total_count = search_by_name(conn, args.name, args.limit)
            print(f"Searching for products with name containing: {args.name}")
        elif args.ingredient:
            results, total_count = search_by_ingredient(conn, args.ingredient, args.limit)
            print(f"Searching for products with ingredient containing: {args.ingredient}")
        elif args.date:
            results, total_count = search_by_date(conn, args.date, args.limit)
            print(f"Searching for products updated after: {args.date}")
        
        # Debug: print total count and results length
        print(f"DEBUG: total_count = {total_count}, len(results) = {len(results)}")
        
        formatted_results = format_results(results)
        print(formatted_results)
        
        # Show total count information if there are more results than displayed
        if total_count > len(results):
            print(f"\nShowing {len(results)} of {total_count} total matches. Use --limit to see more.")
        elif total_count > 0:
            print(f"\nFound {total_count} {'match' if total_count == 1 else 'matches'}.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 