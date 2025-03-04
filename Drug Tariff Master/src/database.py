"""
Database module for Drug Tariff Master.
This module handles SQLite database operations, including creation,
inserting data, and querying.
"""
import logging
import sqlite3
from pathlib import Path

import config

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('database')


def get_connection():
    """
    Get a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: A connection to the database.
    """
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def initialize_database():
    """
    Create the database tables if they don't exist.
    
    Returns:
        bool: True if initialization was successful, False otherwise.
    """
    logger.info("Initializing database at {}".format(config.DB_PATH))
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables according to PRD requirements
        
        # VMP table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmp (
            VPID INTEGER PRIMARY KEY,
            NM TEXT NOT NULL
        )
        ''')
        
        # VMPP table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmpp (
            VPPID INTEGER PRIMARY KEY,
            VPID INTEGER NOT NULL,
            NM TEXT NOT NULL,
            QTYVAL REAL NOT NULL,
            QTY_UOMCD INTEGER NOT NULL,
            PRICE INTEGER,
            DT DATE,
            FOREIGN KEY (VPID) REFERENCES vmp(VPID)
        )
        ''')
        
        # AMP table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amp (
            APID INTEGER PRIMARY KEY,
            VPID INTEGER NOT NULL,
            DESC TEXT NOT NULL,
            SUPPCD INTEGER NOT NULL,
            FOREIGN KEY (VPID) REFERENCES vmp(VPID)
        )
        ''')
        
        # AMPP table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ampp (
            APPID INTEGER PRIMARY KEY,
            VPPID INTEGER NOT NULL,
            APID INTEGER NOT NULL,
            NM TEXT NOT NULL,
            PRICE INTEGER,
            PRICE_SOURCE TEXT,
            PRICE_METHOD TEXT,
            FOREIGN KEY (VPPID) REFERENCES vmpp(VPPID),
            FOREIGN KEY (APID) REFERENCES amp(APID)
        )
        ''')
        
        # GTIN table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gtin (
            AMPPID INTEGER NOT NULL,
            GTIN TEXT NOT NULL,
            STARTDT DATE NOT NULL,
            ENDDT DATE,
            PRIMARY KEY (AMPPID, GTIN),
            FOREIGN KEY (AMPPID) REFERENCES ampp(APPID)
        )
        ''')
        
        # Search data table (unified search table)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_data (
            VMPP TEXT NOT NULL,
            VMP TEXT NOT NULL,
            AMPP INTEGER NOT NULL,
            Description TEXT NOT NULL,
            Brand_or_Generic TEXT NOT NULL,
            Drug_Tariff_Price INTEGER,
            Price_Source TEXT,
            Price_Method TEXT,
            PRIMARY KEY (AMPP),
            FOREIGN KEY (AMPP) REFERENCES ampp(APPID)
        )
        ''')
        
        # Create indexes for faster lookups
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ampp_vppid ON ampp(VPPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ampp_apid ON ampp(APID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmpp_vpid ON vmpp(VPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_amp_vpid ON amp(VPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gtin_gtin ON gtin(GTIN)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_data_description ON search_data(Description)')
        
        conn.commit()
        logger.info("Database initialized successfully")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def insert_data(table, data_list):
    """
    Insert a list of data records into the specified table.
    
    Args:
        table (str): The name of the table to insert into.
        data_list (list): A list of dictionaries containing the data to insert.
        
    Returns:
        int: The number of records inserted.
    """
    if not data_list:
        return 0
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Extract column names from the first data dictionary
        columns = list(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in columns])
        column_str = ', '.join(columns)
        
        # Prepare SQL statement
        sql = f"INSERT OR REPLACE INTO {table} ({column_str}) VALUES ({placeholders})"
        
        # Convert list of dictionaries to list of tuples for executemany
        values = [[record.get(column) for column in columns] for record in data_list]
        
        # Execute the insert
        cursor.executemany(sql, values)
        conn.commit()
        
        count = len(data_list)
        logger.info(f"Inserted {count} records into {table}")
        return count
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting data into {table}: {e}")
        if 'conn' in locals():
            conn.rollback()
        return 0
    finally:
        if 'conn' in locals():
            conn.close()


def clear_table(table):
    """
    Clear all data from the specified table.
    
    Args:
        table (str): The name of the table to clear.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DELETE FROM {table}")
        conn.commit()
        
        logger.info(f"Cleared all data from {table}")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Error clearing data from {table}: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def execute_query(query, params=None):
    """
    Execute a SQL query and return the results.
    
    Args:
        query (str): SQL query to execute.
        params (tuple, optional): Parameters for the query.
        
    Returns:
        list: List of row dictionaries with the query results.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return [dict(row) for row in results]
        
    except sqlite3.Error as e:
        logger.error(f"Query execution error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()


def execute_update(query, params=None):
    """
    Execute a SQL update query (INSERT, UPDATE, DELETE).
    
    Args:
        query (str): SQL query to execute.
        params (tuple, optional): Parameters for the query.
        
    Returns:
        int: Number of rows affected.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor.rowcount
        
    except sqlite3.Error as e:
        logger.error(f"Update execution error: {e}")
        if 'conn' in locals():
            conn.rollback()
        return 0
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    # Test database initialization
    initialize_database() 