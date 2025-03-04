import sqlite3

# Connect to the database
conn = sqlite3.connect('data/dmd_data.db')
cursor = conn.cursor()

# Check counts in main tables
tables = ['vmp', 'vmpp', 'amp', 'ampp', 'search_data']

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table.upper()} count: {count}")
    except sqlite3.Error as e:
        print(f"Error counting {table}: {e}")

# Check if we have any specific drug names
drugs = ['paracetamol', 'insulin', 'amoxicillin']

for drug in drugs:
    try:
        search_term = f"%{drug}%"
        # Check in VMPs
        cursor.execute("SELECT COUNT(*) FROM vmp WHERE LOWER(NM) LIKE ?", (search_term,))
        vmp_count = cursor.fetchone()[0]
        
        # Check in AMPs
        cursor.execute("SELECT COUNT(*) FROM amp WHERE LOWER(DESC) LIKE ?", (search_term,))
        amp_count = cursor.fetchone()[0]
        
        # Check in AMPPs
        cursor.execute("SELECT COUNT(*) FROM ampp WHERE LOWER(NM) LIKE ?", (search_term,))
        ampp_count = cursor.fetchone()[0]
        
        print(f"\nDrug '{drug}' found in:")
        print(f"  VMP: {vmp_count} records")
        print(f"  AMP: {amp_count} records")
        print(f"  AMPP: {ampp_count} records")
    except sqlite3.Error as e:
        print(f"Error searching for {drug}: {e}")

# Check search_data table structure
try:
    cursor.execute("PRAGMA table_info(search_data)")
    columns = cursor.fetchall()
    print("\nSearch_data table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
except sqlite3.Error as e:
    print(f"Error checking search_data structure: {e}")

conn.close() 