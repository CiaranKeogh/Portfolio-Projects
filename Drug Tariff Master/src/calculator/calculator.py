"""
Price calculator module for the Drug Tariff Processor.

This module provides functions to calculate missing prices for AMPPs and VMPPs
based on comparable products with known prices.
"""

import logging
import sqlite3
from datetime import datetime

logger = logging.getLogger('drug_tariff_processor')

# Constants for price calculation
CALCULATION_METHODS = {
    'SAME_PRODUCT_DIFFERENT_SIZE': 'same_product_different_size',
    'SAME_VMPP_DIFFERENT_BRAND': 'same_vmpp_different_brand',
    'SIMILAR_VMP': 'similar_vmp',
    'DEFAULT': 'default'
}

MISSING_PRICE_REASONS = {
    'NON_REIMBURSABLE': 'non_reimbursable',
    'DISCONTINUED': 'discontinued',
    'HOSPITAL_ONLY': 'hospital_only',
    'NOT_AVAILABLE': 'not_available',
    'UNKNOWN': 'unknown'
}

PRICE_STATUS = {
    'CALCULATED': 'calculated',
    'INTENTIONALLY_MISSING': 'intentionally_missing',
    'UNKNOWN': 'unknown'
}

def calculate_missing_prices(db_path):
    """
    Calculate missing prices for AMPPs based on comparable products.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Starting calculation of missing prices")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # First, update the database schema to add new fields if needed
        _update_schema(conn)
        
        # Identify all AMPPs with missing prices and classify them
        classified_ampp = _classify_missing_prices(conn)
        
        # Count of each category 
        status_counts = {
            'needs_calculation': 0,
            'intentionally_missing': 0,
            'unknown': 0
        }
        
        for category in classified_ampp:
            status_counts[category] = len(classified_ampp[category])
            
        logger.info(f"Classification complete: {status_counts['needs_calculation']} need calculation, "
                    f"{status_counts['intentionally_missing']} intentionally missing, "
                    f"{status_counts['unknown']} unknown")
        
        # Calculate prices for AMPPs that need calculation
        calculation_counts = {method: 0 for method in CALCULATION_METHODS.values()}
        
        # Keep track of failed calculations
        failed_calculations = 0
        
        for i, appid in enumerate(classified_ampp['needs_calculation']):
            try:
                # Add progress logging for every 1000 items
                if i % 1000 == 0:
                    logger.info(f"Processing item {i} of {len(classified_ampp['needs_calculation'])}")
                
                # Try different calculation methods in order
                price, method = _calculate_price_for_ampp(conn, appid)
                
                if price and method:
                    _update_ampp_price(conn, appid, price, method)
                    calculation_counts[method] += 1
                else:
                    failed_calculations += 1
            except Exception as e:
                logger.error(f"Error calculating price for AMPP {appid}: {e}")
                failed_calculations += 1
                
        # Commit the changes
        conn.commit()
        
        # Update the unified search table with the new prices
        _update_unified_search_table(conn)
        
        # Log the results
        logger.info("Price calculation complete:")
        for method, count in calculation_counts.items():
            logger.info(f"  - {method}: {count} prices calculated")
        logger.info(f"  - Failed calculations: {failed_calculations}")
            
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database error during price calculation: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        logger.error(f"Error during price calculation: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def _update_schema(conn):
    """
    Update the database schema to add new fields for price calculation.
    
    Args:
        conn (sqlite3.Connection): Database connection
    """
    logger.info("Updating database schema for price calculation")
    
    cursor = conn.cursor()
    
    # Check if the ampp_price_info table has the calculation fields
    cursor.execute("PRAGMA table_info(ampp_price_info)")
    columns = {row['name'] for row in cursor.fetchall()}
    
    # Add new columns if they don't exist
    if 'calculation_method' not in columns:
        cursor.execute("ALTER TABLE ampp_price_info ADD COLUMN calculation_method TEXT")
    
    if 'price_status' not in columns:
        cursor.execute("ALTER TABLE ampp_price_info ADD COLUMN price_status TEXT")
    
    if 'missing_reason' not in columns:
        cursor.execute("ALTER TABLE ampp_price_info ADD COLUMN missing_reason TEXT")
    
    if 'confidence_score' not in columns:
        cursor.execute("ALTER TABLE ampp_price_info ADD COLUMN confidence_score REAL")
    
    if 'calculation_date' not in columns:
        cursor.execute("ALTER TABLE ampp_price_info ADD COLUMN calculation_date DATE")
    
    # Create an index for faster lookups
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ampp_price_info_calc_method ON ampp_price_info(calculation_method)")
    
    conn.commit()

def _classify_missing_prices(conn):
    """
    Classify AMPPs with missing prices into categories.
    
    Args:
        conn (sqlite3.Connection): Database connection
        
    Returns:
        dict: Dictionary with AMPPs classified by category
    """
    logger.info("Classifying AMPPs with missing prices")
    
    cursor = conn.cursor()
    
    # Find all AMPPs with missing prices
    cursor.execute("""
        SELECT a.appid
        FROM ampp a
        LEFT JOIN ampp_price_info p ON a.appid = p.appid
        WHERE p.price IS NULL OR p.price = 0 OR p.appid IS NULL
    """)
    
    missing_price_ampp = {row['appid'] for row in cursor.fetchall() if row['appid'] is not None}
    logger.info(f"Found {len(missing_price_ampp)} AMPPs with missing prices")
    
    classified_ampp = {
        'needs_calculation': set(),
        'intentionally_missing': set(),
        'unknown': set()
    }
    
    # Check reimbursement status
    for appid in missing_price_ampp:
        if appid is None:
            continue
            
        reason = _check_missing_price_reason(conn, appid)
        
        if reason == MISSING_PRICE_REASONS['UNKNOWN']:
            classified_ampp['needs_calculation'].add(appid)
        else:
            classified_ampp['intentionally_missing'].add(appid)
            
            # Update the record with the reason
            cursor.execute("""
                INSERT INTO ampp_price_info 
                (appid, price_status, missing_reason, calculation_date, price_basis_code)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(appid) DO UPDATE SET
                price_status = excluded.price_status,
                missing_reason = excluded.missing_reason,
                calculation_date = excluded.calculation_date
            """, (
                appid, 
                PRICE_STATUS['INTENTIONALLY_MISSING'], 
                reason,
                datetime.now().strftime('%Y-%m-%d'),
                4  # Using 4 as code for intentionally missing prices
            ))
    
    return classified_ampp

def _check_missing_price_reason(conn, appid):
    """
    Check why an AMPP might have a missing price.
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to check
        
    Returns:
        str: Reason code for the missing price
    """
    cursor = conn.cursor()
    
    # Check reimbursement status
    cursor.execute("""
        SELECT r.reimb_stat_code 
        FROM ampp_pack_info r
        WHERE r.appid = ?
    """, (appid,))
    
    row = cursor.fetchone()
    if row and row['reimb_stat_code'] not in (1, 11):  # Assuming 1 and 11 are reimbursable
        return MISSING_PRICE_REASONS['NON_REIMBURSABLE']
    
    # Check if the product is discontinued
    cursor.execute("""
        SELECT disc_code, disc_date
        FROM ampp
        WHERE appid = ? AND disc_code IS NOT NULL
    """, (appid,))
    
    if cursor.fetchone():
        return MISSING_PRICE_REASONS['DISCONTINUED']
    
    # Check if it's hospital only
    cursor.execute("""
        SELECT hosp
        FROM ampp_prescrib_info
        WHERE appid = ? AND hosp = 1
    """, (appid,))
    
    if cursor.fetchone():
        return MISSING_PRICE_REASONS['HOSPITAL_ONLY']
    
    # Check availability status
    cursor.execute("""
        SELECT amp.avail_restrict_code
        FROM ampp
        JOIN amp ON ampp.apid = amp.apid
        WHERE ampp.appid = ? AND amp.avail_restrict_code != 1
    """, (appid,))
    
    if cursor.fetchone():
        return MISSING_PRICE_REASONS['NOT_AVAILABLE']
    
    return MISSING_PRICE_REASONS['UNKNOWN']

def _calculate_price_for_ampp(conn, appid):
    """
    Calculate the price for an AMPP using different methods.
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to calculate price for
        
    Returns:
        tuple: (price, method) if calculation was successful, (None, None) otherwise
    """
    if appid is None:
        logger.warning("Received None AMPP ID for calculation")
        return None, None
        
    logger.debug(f"Calculating price for AMPP {appid}")
    
    # Try calculation methods in order of reliability
    try:
        price, method, confidence = _try_same_product_different_size(conn, appid)
        if price:
            return price, method
    except Exception as e:
        logger.error(f"Error in same_product_different_size for AMPP {appid}: {e}")
    
    try:
        price, method, confidence = _try_same_vmpp_different_brand(conn, appid)
        if price:
            return price, method
    except Exception as e:
        logger.error(f"Error in same_vmpp_different_brand for AMPP {appid}: {e}")
    
    try:
        price, method, confidence = _try_similar_vmp(conn, appid)
        if price:
            return price, method
    except Exception as e:
        logger.error(f"Error in similar_vmp for AMPP {appid}: {e}")
    
    # If all else fails, return None
    return None, None

def _try_same_product_different_size(conn, appid):
    """
    Try to calculate price based on the same product with different pack size.
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to calculate price for
        
    Returns:
        tuple: (price, method, confidence) if successful, (None, None, None) otherwise
    """
    cursor = conn.cursor()
    
    # Get the product details
    cursor.execute("""
        SELECT 
            ampp.appid, 
            ampp.apid, 
            ampp.name,
            vmpp.vppid,
            vmpp.qty_value AS pack_size,
            vmpp.qty_uom_code
        FROM ampp
        JOIN vmpp ON ampp.vppid = vmpp.vppid
        WHERE ampp.appid = ?
    """, (appid,))
    
    target_ampp = cursor.fetchone()
    if not target_ampp:
        return None, None, None
    
    # Find other pack sizes of the same product (same AMP)
    cursor.execute("""
        SELECT 
            a.appid, 
            a.name,
            v.qty_value AS pack_size,
            v.qty_uom_code,
            p.price
        FROM ampp a
        JOIN vmpp v ON a.vppid = v.vppid
        JOIN ampp_price_info p ON a.appid = p.appid
        WHERE 
            a.apid = ? AND
            a.appid != ? AND
            p.price IS NOT NULL AND 
            p.price > 0 AND
            v.qty_uom_code = ?
        ORDER BY ABS(v.qty_value - ?) ASC
    """, (
        target_ampp['apid'], 
        appid, 
        target_ampp['qty_uom_code'],
        target_ampp['pack_size']
    ))
    
    comparables = cursor.fetchall()
    
    if not comparables:
        return None, None, None
    
    # Calculate per-unit price from the closest pack size
    comparable = comparables[0]
    
    # Ensure pack size and price are valid numbers
    pack_size = comparable['pack_size']
    price = comparable['price']
    
    if pack_size is None or price is None or pack_size <= 0:
        return None, None, None
        
    unit_price = price / pack_size
    target_pack_size = target_ampp['pack_size']
    
    if target_pack_size is None or target_pack_size <= 0:
        return None, None, None
        
    calculated_price = round(unit_price * target_pack_size)
    
    # Higher confidence for closer pack sizes
    pack_size_ratio = min(pack_size / target_pack_size, 
                         target_pack_size / pack_size) if pack_size > 0 and target_pack_size > 0 else 0.5
    confidence = 0.9 * pack_size_ratio  # Max confidence of 0.9 for this method
    
    logger.debug(f"Calculated price for AMPP {appid} using same product, different size: "
                f"{calculated_price} (from {comparable['name']} with price {comparable['price']})")
    
    return calculated_price, CALCULATION_METHODS['SAME_PRODUCT_DIFFERENT_SIZE'], confidence

def _try_same_vmpp_different_brand(conn, appid):
    """
    Try to calculate price based on different brands of the same VMPP.
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to calculate price for
        
    Returns:
        tuple: (price, method, confidence) if successful, (None, None, None) otherwise
    """
    cursor = conn.cursor()
    
    # Get the product details
    cursor.execute("""
        SELECT 
            ampp.appid, 
            ampp.vppid,
            vmpp.qty_value AS pack_size,
            vmpp.qty_uom_code
        FROM ampp
        JOIN vmpp ON ampp.vppid = vmpp.vppid
        WHERE ampp.appid = ?
    """, (appid,))
    
    target_ampp = cursor.fetchone()
    if not target_ampp:
        return None, None, None
    
    # Find different brands with the same VMPP
    cursor.execute("""
        SELECT 
            a.appid, 
            a.name,
            p.price
        FROM ampp a
        JOIN ampp_price_info p ON a.appid = p.appid
        WHERE 
            a.vppid = ? AND
            a.appid != ? AND
            p.price IS NOT NULL AND 
            p.price > 0
    """, (
        target_ampp['vppid'], 
        appid
    ))
    
    comparables = cursor.fetchall()
    
    if not comparables:
        return None, None, None
    
    # Calculate average price of comparable brands
    prices = [comp['price'] for comp in comparables if comp['price'] is not None and comp['price'] > 0]
    
    if not prices:
        return None, None, None
        
    avg_price = round(sum(prices) / len(prices))
    
    # Confidence based on number of comparables and price variance
    if avg_price <= 0:
        return None, None, None
        
    std_dev = (sum((p - avg_price) ** 2 for p in prices) / len(prices)) ** 0.5
    variance_factor = 1 - min(std_dev / avg_price, 0.5) if avg_price > 0 else 0.5
    confidence = 0.7 * min(1, len(comparables) / 5) * variance_factor  # Max confidence of 0.7
    
    logger.debug(f"Calculated price for AMPP {appid} using same VMPP, different brand: "
                f"{avg_price} (average of {len(comparables)} comparable products)")
    
    return avg_price, CALCULATION_METHODS['SAME_VMPP_DIFFERENT_BRAND'], confidence

def _try_similar_vmp(conn, appid):
    """
    Try to calculate price based on similar VMPs (same ingredient, form, similar strength).
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to calculate price for
        
    Returns:
        tuple: (price, method, confidence) if successful, (None, None, None) otherwise
    """
    cursor = conn.cursor()
    
    # Get the product details including VMP
    cursor.execute("""
        SELECT 
            ampp.appid, 
            amp.vpid,
            vmpp.qty_value AS pack_size,
            vmpp.qty_uom_code
        FROM ampp
        JOIN amp ON ampp.apid = amp.apid
        JOIN vmpp ON ampp.vppid = vmpp.vppid
        WHERE ampp.appid = ?
    """, (appid,))
    
    target_ampp = cursor.fetchone()
    if not target_ampp:
        return None, None, None
    
    # Get the ingredients for this VMP
    cursor.execute("""
        SELECT 
            i.name,
            vi.strnt_nmrtr_val AS strength,
            vi.strnt_nmrtr_uom_code AS uom_code
        FROM vmp_ingredient vi
        JOIN ingredient i ON vi.isid = i.isid
        WHERE vi.vpid = ?
    """, (target_ampp['vpid'],))
    
    ingredients = cursor.fetchall()
    if not ingredients:
        return None, None, None
    
    # Get the form for this VMP
    cursor.execute("""
        SELECT form_code
        FROM vmp_form
        WHERE vpid = ?
    """, (target_ampp['vpid'],))
    
    forms = cursor.fetchall()
    if not forms:
        return None, None, None
    
    # Find similar VMPs with the same main ingredient and form
    main_ingredient = ingredients[0]['name']
    main_strength = ingredients[0]['strength']
    main_uom = ingredients[0]['uom_code']
    main_form = forms[0]['form_code']
    
    # Look for AMPPs with similar VMPs
    cursor.execute("""
        SELECT 
            a2.appid,
            a2.name,
            v2.qty_value AS pack_size,
            p.price,
            ABS(vi.strnt_nmrtr_val - ?) / ? AS strength_diff
        FROM vmp_ingredient vi
        JOIN ingredient i ON vi.isid = i.isid
        JOIN vmp_form vf ON vi.vpid = vf.vpid
        JOIN amp a ON vi.vpid = a.vpid
        JOIN ampp a2 ON a.apid = a2.apid
        JOIN vmpp v2 ON a2.vppid = v2.vppid
        JOIN ampp_price_info p ON a2.appid = p.appid
        WHERE 
            i.name LIKE ? AND
            vi.strnt_nmrtr_uom_code = ? AND
            vf.form_code = ? AND
            a2.appid != ? AND
            p.price IS NOT NULL AND 
            p.price > 0 AND
            v2.qty_uom_code = ?
        ORDER BY 
            strength_diff ASC,
            ABS(v2.qty_value - ?) ASC
        LIMIT 5
    """, (
        main_strength,
        max(1, main_strength),
        f"%{main_ingredient}%",
        main_uom,
        main_form,
        appid,
        target_ampp['qty_uom_code'],
        target_ampp['pack_size']
    ))
    
    comparables = cursor.fetchall()
    
    if not comparables:
        return None, None, None
    
    # Calculate average price adjusted for pack size
    total_price = 0
    total_units = 0
    
    for comp in comparables:
        # Skip records with missing or invalid values
        if comp['pack_size'] is None or comp['pack_size'] <= 0 or comp['price'] is None or comp['price'] <= 0:
            continue
            
        # Normalize price by pack size
        unit_price = comp['price'] / comp['pack_size']
        
        # Skip if strength_diff is None
        if comp['strength_diff'] is None:
            continue
            
        # Weight by similarity (inverse of strength difference)
        weight = 1 / (1 + comp['strength_diff'])
        total_price += unit_price * weight
        total_units += weight
    
    if total_units <= 0:
        return None, None, None
        
    avg_unit_price = total_price / total_units
    
    target_pack_size = target_ampp['pack_size']
    if target_pack_size is None or target_pack_size <= 0:
        return None, None, None
        
    calculated_price = round(avg_unit_price * target_pack_size)
    
    # Lower confidence for this method
    if comparables and comparables[0]['strength_diff'] is not None:
        confidence = 0.5 * (1 / (1 + comparables[0]['strength_diff']))  # Max confidence of 0.5
    else:
        confidence = 0.3  # Default lower confidence if strength_diff is not available
    
    logger.debug(f"Calculated price for AMPP {appid} using similar VMP: "
                f"{calculated_price} (based on {len(comparables)} similar products)")
    
    return calculated_price, CALCULATION_METHODS['SIMILAR_VMP'], confidence

def _update_ampp_price(conn, appid, price, method):
    """
    Update the price for an AMPP in the database.
    
    Args:
        conn (sqlite3.Connection): Database connection
        appid (int): AMPP ID to update
        price (int): Calculated price
        method (str): Calculation method used
    """
    cursor = conn.cursor()
    
    # Get the current price if any
    cursor.execute("""
        SELECT price
        FROM ampp_price_info
        WHERE appid = ?
    """, (appid,))
    
    row = cursor.fetchone()
    prev_price = row['price'] if row else None
    
    # Set confidence score based on method
    confidence_scores = {
        CALCULATION_METHODS['SAME_PRODUCT_DIFFERENT_SIZE']: 0.9,
        CALCULATION_METHODS['SAME_VMPP_DIFFERENT_BRAND']: 0.7,
        CALCULATION_METHODS['SIMILAR_VMP']: 0.5,
        CALCULATION_METHODS['DEFAULT']: 0.3
    }
    
    confidence = confidence_scores.get(method, 0.5)
    
    # Update or insert the price
    cursor.execute("""
        INSERT INTO ampp_price_info 
        (appid, price, price_prev, price_date, price_basis_code, calculation_method, price_status, confidence_score, calculation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(appid) DO UPDATE SET
        price_prev = price,
        price = excluded.price,
        price_date = excluded.price_date,
        calculation_method = excluded.calculation_method,
        price_status = excluded.price_status,
        confidence_score = excluded.confidence_score,
        calculation_date = excluded.calculation_date
    """, (
        appid,
        price,
        prev_price,
        datetime.now().strftime('%Y-%m-%d'),
        3,  # Assuming 3 is the code for calculated prices
        method,
        PRICE_STATUS['CALCULATED'],
        confidence,
        datetime.now().strftime('%Y-%m-%d')
    ))
    
    logger.debug(f"Updated price for AMPP {appid} to {price} using method {method}")

def _update_unified_search_table(conn):
    """
    Update the unified search table with the new calculated prices.
    
    Args:
        conn (sqlite3.Connection): Database connection
    """
    logger.info("Updating unified search table with calculated prices")
    
    cursor = conn.cursor()
    
    # Update the unified search table
    cursor.execute("""
        UPDATE unified_search
        SET nhs_price = (
            SELECT price 
            FROM ampp_price_info 
            WHERE ampp_price_info.appid = unified_search.appid
        ),
        calculation_method = (
            SELECT calculation_method 
            FROM ampp_price_info 
            WHERE ampp_price_info.appid = unified_search.appid
        )
        WHERE appid IS NOT NULL
    """)
    
    logger.info(f"Updated {cursor.rowcount} records in unified search table") 