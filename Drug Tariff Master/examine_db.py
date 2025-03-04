import sqlite3
import os
import json

def examine_database():
    db_path = os.path.join('data', 'dmd_data.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return
    
    print(f"Examining database at {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(tables)} tables: {', '.join(tables)}")
    
    # Examine each table structure
    table_schemas = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        table_schemas[table] = []
        
        print(f"\nTable: {table}")
        print("Columns:")
        for col in columns:
            column_info = {
                "cid": col[0],
                "name": col[1],
                "type": col[2],
                "notnull": col[3],
                "default_value": col[4],
                "pk": col[5]
            }
            table_schemas[table].append(column_info)
            print(f"  - {col[1]} ({col[2]}){' PRIMARY KEY' if col[5] else ''}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Row count: {count}")
        
        # Get sample data (first row)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            sample = cursor.fetchone()
            column_names = [description[0] for description in cursor.description]
            print("Sample row:")
            for i, value in enumerate(sample):
                print(f"  - {column_names[i]}: {value}")
    
    # Look for foreign keys and relationships
    print("\nForeign Key Relationships:")
    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        foreign_keys = cursor.fetchall()
        if foreign_keys:
            print(f"Table {table} has {len(foreign_keys)} foreign key(s):")
            for fk in foreign_keys:
                print(f"  - Column {fk[3]} references {fk[2]}({fk[4]})")
        
    # Check if lookup tables exist
    lookup_tables = [t for t in tables if 'lookup' in t.lower()]
    if lookup_tables:
        print(f"\nPotential Lookup Tables: {', '.join(lookup_tables)}")
        
        # Sample from each lookup table
        for table in lookup_tables:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            
            print(f"\nSample from {table}:")
            for row in rows:
                row_data = {}
                for i, value in enumerate(row):
                    row_data[column_names[i]] = value
                print(f"  {row_data}")
    
    conn.close()
    print("\nDatabase examination complete")

if __name__ == "__main__":
    examine_database() 