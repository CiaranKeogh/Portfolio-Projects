"""
Search module for Drug Tariff Master.
This module builds and maintains the unified search table for quick
lookup of drug information across different data structures.
"""
import logging
import re

import config
import database

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('search')


def clean_search_term(term):
    """
    Clean and normalize a search term for better matching.
    
    Args:
        term (str): The search term to clean.
        
    Returns:
        str: The cleaned search term.
    """
    if not term:
        return ""
    
    # Convert to lowercase
    term = term.lower()
    
    # Remove special characters and extra spaces
    term = re.sub(r'[^\w\s]', ' ', term)
    term = re.sub(r'\s+', ' ', term).strip()
    
    return term


def extract_searchable_terms(name):
    """
    Extract individual terms from a product name for indexed search.
    
    Args:
        name (str): The product name.
        
    Returns:
        list: List of individual searchable terms.
    """
    if not name:
        return []
    
    # Clean the name
    cleaned_name = clean_search_term(name)
    
    # Split into individual terms
    terms = cleaned_name.split()
    
    # Filter out very short terms and common words
    common_words = {'and', 'the', 'with', 'for', 'of', 'in', 'on', 'at', 'by', 'to'}
    terms = [term for term in terms if len(term) > 1 and term not in common_words]
    
    return terms


def build_search_index():
    """
    Build the unified search index by populating the search_data table
    with records from VMP, VMPP, AMP, and AMPP tables.
    
    Returns:
        int: Number of records added to the search index.
    """
    logger.info("Starting to build search index")
    
    # Clear existing search data
    database.clear_table('search_data')
    logger.info("Cleared existing search data")
    
    # Update the search_data table schema to match our needs
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Drop the existing search_data table
        cursor.execute("DROP TABLE IF EXISTS search_data")
        
        # Create a new search_data table with proper schema
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_data (
            ID INTEGER PRIMARY KEY,
            RECORD_TYPE TEXT NOT NULL,
            NAME TEXT NOT NULL,
            STRENGTH TEXT,
            FORM TEXT,
            ROUTE TEXT,
            SUPPLIER TEXT,
            PRICE INTEGER,
            SEARCH_TEXT TEXT,
            SEARCH_TERMS TEXT
        )
        ''')
        
        # Create indexes for faster search
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_data_text ON search_data(SEARCH_TEXT)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_data_terms ON search_data(SEARCH_TERMS)')
        
        conn.commit()
        logger.info("Search data table recreated with proper schema")
    except Exception as e:
        logger.error(f"Error recreating search_data table: {e}")
        return 0
    finally:
        if 'conn' in locals():
            conn.close()
    
    # Build index from VMP records
    vmp_query = """
    SELECT VPID as id, 'VMP' as record_type, NM as name,
           '' as strength, '' as form, 
           '' as route, NULL as supplier, NULL as price
    FROM vmp
    """
    vmp_records = database.execute_query(vmp_query)
    
    if vmp_records:
        logger.info(f"Found {len(vmp_records)} VMP records for search index")
        vmp_index_data = []
        
        for record in vmp_records:
            # Prepare searchable terms
            name = record['name'] or ""
            strength = record['strength'] or ""
            form = record['form'] or ""
            
            # Combine all fields for full text search
            full_text = f"{name} {strength} {form}".strip()
            search_terms = clean_search_term(full_text)
            
            # Extract individual terms for term-based search
            individual_terms = extract_searchable_terms(full_text)
            terms_json = "|".join(individual_terms)
            
            vmp_index_data.append({
                'ID': record['id'],
                'RECORD_TYPE': record['record_type'],
                'NAME': name,
                'STRENGTH': strength,
                'FORM': form,
                'ROUTE': record['route'],
                'SUPPLIER': record['supplier'],
                'PRICE': record['price'],
                'SEARCH_TEXT': search_terms,
                'SEARCH_TERMS': terms_json
            })
        
        database.insert_data('search_data', vmp_index_data)
        logger.info(f"Added {len(vmp_index_data)} VMP records to search index")
    
    # Build index from VMPP records
    vmpp_query = """
    SELECT vmpp.VPPID as id, 'VMPP' as record_type, 
           vmpp.NM as name, '' as strength, '' as form,
           '' as route, NULL as supplier, vmpp.PRICE as price
    FROM vmpp
    """
    vmpp_records = database.execute_query(vmpp_query)
    
    if vmpp_records:
        logger.info(f"Found {len(vmpp_records)} VMPP records for search index")
        vmpp_index_data = []
        
        for record in vmpp_records:
            # Prepare searchable terms
            name = record['name'] or ""
            strength = record['strength'] or ""
            form = record['form'] or ""
            
            # Combine all fields for full text search
            full_text = f"{name} {strength} {form}".strip()
            search_terms = clean_search_term(full_text)
            
            # Extract individual terms for term-based search
            individual_terms = extract_searchable_terms(full_text)
            terms_json = "|".join(individual_terms)
            
            vmpp_index_data.append({
                'ID': record['id'],
                'RECORD_TYPE': record['record_type'],
                'NAME': name,
                'STRENGTH': strength,
                'FORM': form,
                'ROUTE': record['route'],
                'SUPPLIER': record['supplier'],
                'PRICE': record['price'],
                'SEARCH_TEXT': search_terms,
                'SEARCH_TERMS': terms_json
            })
        
        database.insert_data('search_data', vmpp_index_data)
        logger.info(f"Added {len(vmpp_index_data)} VMPP records to search index")
    
    # Build index from AMP records
    amp_query = """
    SELECT amp.APID as id, 'AMP' as record_type, 
           amp.DESC as name, '' as strength, '' as form,
           '' as route, amp.SUPPCD as supplier, NULL as price
    FROM amp
    """
    amp_records = database.execute_query(amp_query)
    
    if amp_records:
        logger.info(f"Found {len(amp_records)} AMP records for search index")
        amp_index_data = []
        
        for record in amp_records:
            # Prepare searchable terms
            name = record['name'] or ""
            strength = record['strength'] or ""
            form = record['form'] or ""
            supplier = str(record['supplier']) if record['supplier'] is not None else ""
            
            # Combine all fields for full text search
            full_text = f"{name} {strength} {form} {supplier}".strip()
            search_terms = clean_search_term(full_text)
            
            # Extract individual terms for term-based search
            individual_terms = extract_searchable_terms(full_text)
            terms_json = "|".join(individual_terms)
            
            amp_index_data.append({
                'ID': record['id'],
                'RECORD_TYPE': record['record_type'],
                'NAME': name,
                'STRENGTH': strength,
                'FORM': form,
                'ROUTE': record['route'],
                'SUPPLIER': supplier,
                'PRICE': record['price'],
                'SEARCH_TEXT': search_terms,
                'SEARCH_TERMS': terms_json
            })
        
        database.insert_data('search_data', amp_index_data)
        logger.info(f"Added {len(amp_index_data)} AMP records to search index")
    
    # Build index from AMPP records
    ampp_query = """
    SELECT ampp.APPID as id, 'AMPP' as record_type, 
           ampp.NM as name, '' as strength, '' as form,
           '' as route, a.SUPPCD as supplier, ampp.PRICE as price
    FROM ampp
    JOIN amp a ON ampp.APID = a.APID
    """
    ampp_records = database.execute_query(ampp_query)
    
    if ampp_records:
        logger.info(f"Found {len(ampp_records)} AMPP records for search index")
        ampp_index_data = []
        
        for record in ampp_records:
            # Prepare searchable terms
            name = record['name'] or ""
            strength = record['strength'] or ""
            form = record['form'] or ""
            supplier = str(record['supplier']) if record['supplier'] is not None else ""
            
            # Combine all fields for full text search
            full_text = f"{name} {strength} {form} {supplier}".strip()
            search_terms = clean_search_term(full_text)
            
            # Extract individual terms for term-based search
            individual_terms = extract_searchable_terms(full_text)
            terms_json = "|".join(individual_terms)
            
            ampp_index_data.append({
                'ID': record['id'],
                'RECORD_TYPE': record['record_type'],
                'NAME': name,
                'STRENGTH': strength,
                'FORM': form,
                'ROUTE': record['route'],
                'SUPPLIER': supplier,
                'PRICE': record['price'],
                'SEARCH_TEXT': search_terms,
                'SEARCH_TERMS': terms_json
            })
        
        database.insert_data('search_data', ampp_index_data)
        logger.info(f"Added {len(ampp_index_data)} AMPP records to search index")
    
    # Get total count
    count_query = "SELECT COUNT(*) as count FROM search_data"
    result = database.execute_query(count_query)
    total_count = result[0]['count'] if result else 0
    
    logger.info(f"Search index build complete. Total records: {total_count}")
    return total_count


def search_products(search_term, record_type=None, limit=50):
    """
    Search for products in the search index.
    
    Args:
        search_term (str): The term to search for.
        record_type (str, optional): Filter by record type (VMP, VMPP, AMP, AMPP).
        limit (int, optional): Maximum number of results to return.
        
    Returns:
        list: List of matching records.
    """
    if not search_term:
        logger.warning("Empty search term provided")
        return []
    
    # Clean and normalize the search term
    cleaned_term = clean_search_term(search_term)
    
    if not cleaned_term:
        logger.warning("Search term contains only invalid characters")
        return []
    
    logger.info(f"Searching for: '{cleaned_term}', record_type: {record_type}")
    
    # Simple search - just look for the term in the NAME field
    sql = """
    SELECT ID, RECORD_TYPE, NAME, STRENGTH, FORM, ROUTE, SUPPLIER, PRICE
    FROM search_data
    WHERE NAME LIKE ?
    """
    
    params = [f"%{cleaned_term}%"]
    
    # Add record type filter if specified
    if record_type:
        sql += " AND RECORD_TYPE = ? "
        params.append(record_type)
    
    # Add ordering and limit
    sql += """
    ORDER BY 
        CASE 
            WHEN NAME LIKE ? THEN 1
            ELSE 2
        END,
        PRICE DESC
    LIMIT ?
    """
    
    # Add params for ordering
    params.append(f"{cleaned_term}%")  # Starts with exact term
    params.append(limit)
    
    results = database.execute_query(sql, params)
    
    if results:
        logger.info(f"Found {len(results)} results for '{search_term}'")
    else:
        # If no results in search_data, try a direct search in the main tables
        logger.info(f"No results found in search_data for '{search_term}', trying direct search")
        
        search_param = f"%{cleaned_term}%"
        
        if not record_type or record_type == 'AMPP':
            # Try direct search in AMPP table
            ampp_query = """
            SELECT APPID as ID, 'AMPP' as RECORD_TYPE, NM as NAME,
                   '' as STRENGTH, '' as FORM, '' as ROUTE, 
                   '' as SUPPLIER, PRICE
            FROM ampp
            WHERE LOWER(NM) LIKE ?
            ORDER BY PRICE DESC
            LIMIT ?
            """
            results = database.execute_query(ampp_query, (search_param, limit))
            
            if results:
                logger.info(f"Found {len(results)} results in AMPP table for '{search_term}'")
        
        if not results and (not record_type or record_type == 'VMP'):
            # Try direct search in VMP table
            vmp_query = """
            SELECT VPID as ID, 'VMP' as RECORD_TYPE, NM as NAME,
                   '' as STRENGTH, '' as FORM, '' as ROUTE, 
                   '' as SUPPLIER, NULL as PRICE
            FROM vmp
            WHERE LOWER(NM) LIKE ?
            LIMIT ?
            """
            results = database.execute_query(vmp_query, (search_param, limit))
            
            if results:
                logger.info(f"Found {len(results)} results in VMP table for '{search_term}'")
    
    if not results:
        logger.info(f"No results found for '{search_term}'")
    
    return results


if __name__ == "__main__":
    # Test search index build
    build_search_index()
    
    # Test search functionality
    test_searches = [
        "paracetamol",
        "amoxicillin",
        "insulin",
        "500mg tablet"
    ]
    
    for test in test_searches:
        print(f"\nSearch results for '{test}':")
        results = search_products(test, limit=5)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['NAME']} - {result['STRENGTH']} {result['FORM']} - £{result['PRICE'] if result['PRICE'] is not None else 'N/A'}") 