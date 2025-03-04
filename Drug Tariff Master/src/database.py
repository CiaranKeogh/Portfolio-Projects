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
        
        # Create lookup tables
        
        # Control Drug Category
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_control_drug_category (
            CD TEXT PRIMARY KEY,
            DESC TEXT NOT NULL
        )
        ''')
        
        # Legal Category
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_legal_category (
            CD TEXT PRIMARY KEY,
            DESC TEXT NOT NULL
        )
        ''')
        
        # Form
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_form (
            CD INTEGER PRIMARY KEY,
            DESC TEXT NOT NULL,
            CDDT DATE,
            CDPREV INTEGER
        )
        ''')
        
        # Route
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_route (
            CD INTEGER PRIMARY KEY,
            DESC TEXT NOT NULL,
            CDDT DATE,
            CDPREV INTEGER
        )
        ''')
        
        # Unit of Measure
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_unit_of_measure (
            CD INTEGER PRIMARY KEY,
            DESC TEXT NOT NULL,
            CDDT DATE,
            CDPREV INTEGER
        )
        ''')
        
        # Supplier
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookup_supplier (
            CD INTEGER PRIMARY KEY,
            DESC TEXT NOT NULL,
            CDDT DATE,
            CDPREV INTEGER,
            INVALID INTEGER
        )
        ''')
        
        # Create VTM table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vtm (
            VTMID INTEGER PRIMARY KEY,
            NM TEXT NOT NULL,
            ABBREVNM TEXT,
            VTMIDPREV INTEGER,
            VTMIDDT DATE,
            INVALID INTEGER
        )
        ''')
        
        # Create ingredient table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredient (
            ISID INTEGER PRIMARY KEY,
            ISIDDT DATE,
            ISIDPREV INTEGER,
            NM TEXT NOT NULL,
            INVALID INTEGER
        )
        ''')
        
        # Create VMP table with enhanced fields
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmp (
            VPID INTEGER PRIMARY KEY,
            VPIDDT DATE,
            VPIDPREV INTEGER,
            VTMID INTEGER,
            NM TEXT NOT NULL,
            ABBREVNM TEXT,
            BASISCD TEXT,
            NMDT DATE,
            NMPREV TEXT,
            BASIS_PREVCD TEXT,
            NMCHANGECD TEXT,
            COMBPRODCD TEXT,
            PRES_STATCD TEXT,
            SUG_F INTEGER,
            GLU_F INTEGER,
            PRES_F INTEGER,
            CFC_F INTEGER,
            NON_AVAILCD TEXT,
            NON_AVAILDT DATE,
            DF_INDCD TEXT,
            UDFS REAL,
            UDFS_UOMCD INTEGER,
            UNIT_DOSE_UOMCD INTEGER,
            INVALID INTEGER,
            FOREIGN KEY (VTMID) REFERENCES vtm(VTMID),
            FOREIGN KEY (UDFS_UOMCD) REFERENCES lookup_unit_of_measure(CD),
            FOREIGN KEY (UNIT_DOSE_UOMCD) REFERENCES lookup_unit_of_measure(CD)
        )
        ''')
        
        # Create VMPP table with enhanced fields
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmpp (
            VPPID INTEGER PRIMARY KEY,
            VPID INTEGER NOT NULL,
            NM TEXT NOT NULL,
            QTYVAL REAL NOT NULL,
            QTY_UOMCD INTEGER NOT NULL,
            COMBPACKCD TEXT,
            EMA INTEGER,
            NMDT DATE,
            NM_PREV TEXT,
            PRICE INTEGER,
            DT DATE,
            INVALID INTEGER,
            FOREIGN KEY (VPID) REFERENCES vmp(VPID),
            FOREIGN KEY (QTY_UOMCD) REFERENCES lookup_unit_of_measure(CD)
        )
        ''')
        
        # Create AMP table with enhanced fields
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amp (
            APID INTEGER PRIMARY KEY,
            VPID INTEGER NOT NULL,
            NM TEXT NOT NULL,
            ABBREVNM TEXT,
            DESC TEXT NOT NULL,
            NMDT DATE,
            NM_PREV TEXT,
            SUPPCD INTEGER NOT NULL,
            LIC_AUTHCD TEXT,
            LIC_AUTH_PREVCD TEXT,
            LIC_AUTHCHANGECD TEXT,
            LIC_AUTHCHANGEDT DATE,
            COMBPRODCD TEXT,
            FLAVOURCD TEXT,
            EMA INTEGER,
            PARALLEL_IMPORT INTEGER,
            AVAIL_RESTRICTCD TEXT,
            INVALID INTEGER,
            FOREIGN KEY (VPID) REFERENCES vmp(VPID),
            FOREIGN KEY (SUPPCD) REFERENCES lookup_supplier(CD)
        )
        ''')
        
        # Create AMPP table with enhanced fields
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ampp (
            APPID INTEGER PRIMARY KEY,
            VPPID INTEGER NOT NULL,
            APID INTEGER NOT NULL,
            NM TEXT NOT NULL,
            NMDT DATE,
            NM_PREV TEXT,
            DISC INTEGER,
            DISCDT DATE,
            PRICE INTEGER,
            PRICE_SOURCE TEXT,
            PRICE_METHOD TEXT,
            REIMB_STATCD TEXT,
            REIMB_STATDT DATE,
            AVAIL_RESTRICTCD TEXT,
            INVALID INTEGER,
            FOREIGN KEY (VPPID) REFERENCES vmpp(VPPID),
            FOREIGN KEY (APID) REFERENCES amp(APID)
        )
        ''')
        
        # Create GTIN table
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
        
        # Create relationship tables
        
        # VMP to Ingredient
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmp_ingredient (
            VPID INTEGER NOT NULL,
            ISID INTEGER NOT NULL,
            BASIS_STRNTCD TEXT,
            BS_SUBID INTEGER,
            STRNT_NMRTR_VAL REAL,
            STRNT_NMRTR_UOMCD INTEGER,
            STRNT_DNMTR_VAL REAL,
            STRNT_DNMTR_UOMCD INTEGER,
            PRIMARY KEY (VPID, ISID),
            FOREIGN KEY (VPID) REFERENCES vmp(VPID),
            FOREIGN KEY (ISID) REFERENCES ingredient(ISID),
            FOREIGN KEY (BS_SUBID) REFERENCES ingredient(ISID),
            FOREIGN KEY (STRNT_NMRTR_UOMCD) REFERENCES lookup_unit_of_measure(CD),
            FOREIGN KEY (STRNT_DNMTR_UOMCD) REFERENCES lookup_unit_of_measure(CD)
        )
        ''')
        
        # VMP to Form
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmp_form (
            VPID INTEGER NOT NULL,
            FORMCD INTEGER NOT NULL,
            PRIMARY KEY (VPID, FORMCD),
            FOREIGN KEY (VPID) REFERENCES vmp(VPID),
            FOREIGN KEY (FORMCD) REFERENCES lookup_form(CD)
        )
        ''')
        
        # VMP to Route
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vmp_route (
            VPID INTEGER NOT NULL,
            ROUTECD INTEGER NOT NULL,
            PRIMARY KEY (VPID, ROUTECD),
            FOREIGN KEY (VPID) REFERENCES vmp(VPID),
            FOREIGN KEY (ROUTECD) REFERENCES lookup_route(CD)
        )
        ''')
        
        # AMP to Ingredient
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amp_ingredient (
            APID INTEGER NOT NULL,
            ISID INTEGER NOT NULL,
            STRNTH TEXT,
            UOMCD INTEGER,
            PRIMARY KEY (APID, ISID),
            FOREIGN KEY (APID) REFERENCES amp(APID),
            FOREIGN KEY (ISID) REFERENCES ingredient(ISID),
            FOREIGN KEY (UOMCD) REFERENCES lookup_unit_of_measure(CD)
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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmp_vtmid ON vmp(VTMID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmp_ingredient_vpid ON vmp_ingredient(VPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmp_ingredient_isid ON vmp_ingredient(ISID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmp_form_vpid ON vmp_form(VPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vmp_route_vpid ON vmp_route(VPID)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_amp_ingredient_apid ON amp_ingredient(APID)')
        
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