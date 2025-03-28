#!/usr/bin/env python3
"""
Price Calculator Demo

This script demonstrates the price calculator functionality by analyzing and displaying
information about missing prices and calculation methods.
"""

import os
import sys
import argparse
import sqlite3
from tabulate import tabulate

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.logging_config import setup_logging
from src.calculator import calculate_missing_prices

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Price Calculator Demo')
    parser.add_argument('--db-path', type=str, default='data/dmd.db',
                        help='Path to SQLite database file')
    parser.add_argument('--analyze-only', action='store_true',
                        help='Only analyze missing prices without calculating')
    parser.add_argument('--recalculate', action='store_true',
                        help='Force recalculation of all prices')
    parser.add_argument('--detailed-report', action='store_true',
                        help='Show detailed report of calculated prices')
    
    return parser.parse_args()

def analyze_missing_prices(db_path):
    """
    Analyze missing prices in the database.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        dict: Analysis results
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get total number of AMPPs
    cursor.execute("SELECT COUNT(*) AS count FROM ampp")
    total_ampp = cursor.fetchone()['count']
    
    # Get number of AMPPs with prices
    cursor.execute("""
        SELECT COUNT(*) AS count 
        FROM ampp_price_info 
        WHERE price IS NOT NULL AND price > 0
    """)
    priced_ampp = cursor.fetchone()['count']
    
    # Get number of AMPPs with missing prices
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM ampp a
        LEFT JOIN ampp_price_info p ON a.appid = p.appid
        WHERE p.price IS NULL OR p.price = 0
    """)
    missing_prices = cursor.fetchone()['count']
    
    # Get counts by missing reason
    cursor.execute("""
        SELECT 
            missing_reason, 
            COUNT(*) AS count
        FROM ampp_price_info
        WHERE price_status = 'intentionally_missing'
        GROUP BY missing_reason
    """)
    missing_reasons = {row['missing_reason']: row['count'] for row in cursor.fetchall()}
    
    # Get counts by calculation method
    cursor.execute("""
        SELECT 
            calculation_method, 
            COUNT(*) AS count
        FROM ampp_price_info
        WHERE calculation_method IS NOT NULL
        GROUP BY calculation_method
    """)
    calculation_methods = {row['calculation_method']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        'total_ampp': total_ampp,
        'priced_ampp': priced_ampp,
        'missing_prices': missing_prices,
        'missing_reasons': missing_reasons,
        'calculation_methods': calculation_methods
    }

def display_price_examples(db_path):
    """
    Display examples of calculated prices.
    
    Args:
        db_path (str): Path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get examples for each calculation method
    methods = [
        'same_product_different_size',
        'same_vmpp_different_brand',
        'similar_vmp'
    ]
    
    print("\n\033[1mExamples of Calculated Prices:\033[0m")
    
    for method in methods:
        cursor.execute("""
            SELECT 
                a.name,
                p.price,
                p.calculation_method,
                p.confidence_score
            FROM ampp a
            JOIN ampp_price_info p ON a.appid = p.appid
            WHERE p.calculation_method = ?
            ORDER BY p.confidence_score DESC
            LIMIT 5
        """, (method,))
        
        rows = cursor.fetchall()
        
        if rows:
            print(f"\n\033[1mMethod: {method}\033[0m")
            examples = []
            for row in rows:
                examples.append([
                    row['name'],
                    f"{row['price']/100:.2f} GBP",
                    f"{row['confidence_score']:.2f}"
                ])
            
            print(tabulate(examples, headers=["Product", "Price", "Confidence"], tablefmt="simple"))
    
    conn.close()

def show_detailed_report(db_path):
    """
    Show a detailed report of calculated prices.
    
    Args:
        db_path (str): Path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get confidence score statistics
    cursor.execute("""
        SELECT 
            calculation_method,
            COUNT(*) AS count,
            AVG(confidence_score) AS avg_confidence,
            MIN(confidence_score) AS min_confidence,
            MAX(confidence_score) AS max_confidence
        FROM ampp_price_info
        WHERE calculation_method IS NOT NULL
        GROUP BY calculation_method
    """)
    
    rows = cursor.fetchall()
    
    if rows:
        print("\n\033[1mConfidence Score by Calculation Method:\033[0m")
        stats = []
        for row in rows:
            stats.append([
                row['calculation_method'],
                row['count'],
                f"{row['avg_confidence']:.2f}",
                f"{row['min_confidence']:.2f}",
                f"{row['max_confidence']:.2f}"
            ])
        
        print(tabulate(stats, headers=["Method", "Count", "Avg Confidence", "Min", "Max"], tablefmt="simple"))
    
    # Get price distribution by calculation method
    cursor.execute("""
        SELECT 
            calculation_method,
            COUNT(*) AS count,
            AVG(price) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM ampp_price_info
        WHERE calculation_method IS NOT NULL
        GROUP BY calculation_method
    """)
    
    rows = cursor.fetchall()
    
    if rows:
        print("\n\033[1mPrice Distribution by Calculation Method:\033[0m")
        stats = []
        for row in rows:
            stats.append([
                row['calculation_method'],
                row['count'],
                f"{row['avg_price']/100:.2f} GBP",
                f"{row['min_price']/100:.2f} GBP",
                f"{row['max_price']/100:.2f} GBP"
            ])
        
        print(tabulate(stats, headers=["Method", "Count", "Avg Price", "Min Price", "Max Price"], tablefmt="simple"))
    
    conn.close()

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    # Check if the database exists
    if not os.path.exists(args.db_path):
        print(f"Error: Database file {args.db_path} does not exist")
        sys.exit(1)
    
    # If not analyze-only, calculate missing prices
    if not args.analyze_only:
        print("Calculating missing prices...")
        success = calculate_missing_prices(args.db_path)
        if not success:
            print("Error: Failed to calculate prices")
            sys.exit(1)
        print("Price calculation completed successfully")
    
    # Analyze missing prices
    print("\nAnalyzing price data...")
    analysis = analyze_missing_prices(args.db_path)
    
    # Display results
    print("\n\033[1mPrice Data Analysis:\033[0m")
    print(f"Total AMPPs: {analysis['total_ampp']}")
    print(f"AMPPs with prices: {analysis['priced_ampp']} ({analysis['priced_ampp']/analysis['total_ampp']*100:.1f}%)")
    print(f"AMPPs with missing prices: {analysis['missing_prices']} ({analysis['missing_prices']/analysis['total_ampp']*100:.1f}%)")
    
    if analysis['missing_reasons']:
        print("\n\033[1mMissing Prices by Reason:\033[0m")
        for reason, count in analysis['missing_reasons'].items():
            print(f"- {reason}: {count}")
    
    if analysis['calculation_methods']:
        print("\n\033[1mCalculated Prices by Method:\033[0m")
        for method, count in analysis['calculation_methods'].items():
            print(f"- {method}: {count}")
    
    # Display examples of calculated prices
    display_price_examples(args.db_path)
    
    # Show detailed report if requested
    if args.detailed_report:
        show_detailed_report(args.db_path)

if __name__ == "__main__":
    main() 