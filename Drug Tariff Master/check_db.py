import sqlite3
import os

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")

try:
    # Connect to the database
    conn = sqlite3.connect('data/dmd_data.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Check if lookup tables exist
    lookup_tables = [
        'lookup_form', 
        'lookup_route', 
        'lookup_supplier'
    ]
    
    for table in lookup_tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"Table {table} has {count} rows")
    
    # Close the connection
    conn.close()
    
except Exception as e:
    print(f"Error: {e}") 