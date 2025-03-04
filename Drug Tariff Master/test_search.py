"""
Test script to diagnose issues with the search function
"""
import sqlite3
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test_search')

def clean_search_term(term):
    """
    Clean and normalize a search term for better matching.
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

def execute_query(query, params=None):
    """
    Execute a SQL query and return the results.
    """
    try:
        conn = sqlite3.connect('data/dmd_data.db')
        conn.row_factory = sqlite3.Row
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

def direct_search(term):
    """
    Direct search in the database tables for the given term
    """
    search_term = f"%{term}%"
    
    # Search in VMPs
    vmp_query = "SELECT VPID, NM FROM vmp WHERE LOWER(NM) LIKE ? LIMIT 5"
    vmp_results = execute_query(vmp_query, (search_term,))
    
    # Search in AMPPs
    ampp_query = "SELECT APPID, NM, PRICE FROM ampp WHERE LOWER(NM) LIKE ? LIMIT 5"
    ampp_results = execute_query(ampp_query, (search_term,))
    
    print(f"\nDirect search results for '{term}':")
    
    print("\nVMP Results:")
    for i, result in enumerate(vmp_results, 1):
        print(f"{i}. {result['NM']} (VPID: {result['VPID']})")
    
    print("\nAMPP Results:")
    for i, result in enumerate(ampp_results, 1):
        price = result['PRICE'] if result['PRICE'] is not None else 'N/A'
        print(f"{i}. {result['NM']} (APPID: {result['APPID']}, Price: {price})")

def search_in_search_data(search_term, record_type=None, limit=5):
    """
    Search for products in the search index table.
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
    
    # Add limit
    sql += " LIMIT ? "
    params.append(limit)
    
    # Execute the search
    results = execute_query(sql, params)
    
    print(f"\nSearch_data table results for '{search_term}':")
    for i, result in enumerate(results, 1):
        name = result['NAME'] or 'N/A'
        price = result['PRICE'] if result['PRICE'] is not None else 'N/A'
        print(f"{i}. {name} ({result['RECORD_TYPE']}, ID: {result['ID']}, Price: {price})")
    
    # If no results from search_data, print a message
    if not results:
        print("No results found in search_data table")

    return results

def simple_ampp_search(term, limit=5):
    """
    Very simple direct search in the AMPP table
    """
    search_term = f"%{term}%"
    query = "SELECT APPID, NM, PRICE FROM ampp WHERE NM LIKE ? LIMIT ?"
    results = execute_query(query, (search_term, limit))
    
    print(f"\nSimple AMPP search results for '{term}':")
    if results:
        for i, result in enumerate(results, 1):
            price = result['PRICE'] if result['PRICE'] is not None else 'N/A'
            print(f"{i}. {result['NM']} (APPID: {result['APPID']}, Price: {price})")
    else:
        print("No results found")

    return results

# Test our search functions
drugs = ['paracetamol', 'insulin', 'amoxicillin']

for drug in drugs:
    # Direct search in main tables
    direct_search(drug)
    
    # Search in search_data table
    search_in_search_data(drug)
    
    # Simple AMPP search
    simple_ampp_search(drug) 