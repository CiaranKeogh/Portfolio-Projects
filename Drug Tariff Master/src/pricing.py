"""
Pricing module for Drug Tariff Master.
This module implements the price calculation algorithms for AMPP records
with missing prices, according to the rules specified in the PRD.
"""
import logging

import config
import database

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('pricing')


def update_initial_prices():
    """
    Implement Rule 1: Initial Price Assignment
    - If ampp.PRICE exists (from PRICE_INFO), already set with PRICE_SOURCE = 'initial', PRICE_METHOD = null
    - If ampp.PRICE is null but vmpp.PRICE exists, use vmpp.PRICE, set PRICE_SOURCE = 'initial', PRICE_METHOD = null
    
    Returns:
        int: Number of records updated.
    """
    logger.info("Applying Rule 1: Initial Price Assignment")
    
    # AMPP records already have their PRICE set from PRICE_INFO (if available) during parsing
    # Now we need to fill in prices from VMPP records where AMPP prices are missing
    
    query = """
    UPDATE ampp
    SET PRICE = (
        SELECT vmpp.PRICE
        FROM vmpp
        WHERE vmpp.VPPID = ampp.VPPID AND vmpp.PRICE IS NOT NULL
    ),
    PRICE_SOURCE = 'initial',
    PRICE_METHOD = NULL
    WHERE PRICE IS NULL
    AND EXISTS (
        SELECT 1
        FROM vmpp
        WHERE vmpp.VPPID = ampp.VPPID AND vmpp.PRICE IS NOT NULL
    )
    """
    
    updated_count = database.execute_update(query)
    logger.info(f"Updated {updated_count} AMPP records with VMPP prices")
    
    return updated_count


def calculate_same_vmpp_prices():
    """
    Implement Rule 2: Same VMPP (Primary Calculation)
    - For ampp records with null PRICE:
      - Calculate average PRICE of other ampp records with same VPPID and non-null PRICE
      - Update PRICE with average, set PRICE_SOURCE = 'calculated', PRICE_METHOD = 'Same VMPP'
      - Apply only if at least one other AMPP with same VPPID has a PRICE
    
    Returns:
        int: Number of records updated.
    """
    logger.info("Applying Rule 2: Same VMPP Calculation")
    
    # Get AMPPs with null prices
    ampp_null_price_query = """
    SELECT a.APPID, a.VPPID
    FROM ampp a
    WHERE a.PRICE IS NULL
    """
    
    ampp_records = database.execute_query(ampp_null_price_query)
    
    if not ampp_records:
        logger.info("No AMPP records with null prices found for Same VMPP calculation")
        return 0
    
    logger.info(f"Found {len(ampp_records)} AMPP records with null prices")
    
    # Process each AMPP record with null price
    updates = 0
    
    for ampp in ampp_records:
        appid = ampp['APPID']
        vppid = ampp['VPPID']
        
        # Check if there are other AMPPs with the same VPPID and non-null prices
        avg_price_query = """
        SELECT AVG(PRICE) as avg_price, COUNT(*) as count
        FROM ampp
        WHERE VPPID = ? AND PRICE IS NOT NULL AND APPID != ?
        """
        
        result = database.execute_query(avg_price_query, (vppid, appid))
        
        if result and result[0]['count'] > 0 and result[0]['avg_price'] is not None:
            avg_price = round(result[0]['avg_price'])
            
            # Update the AMPP price
            update_query = """
            UPDATE ampp
            SET PRICE = ?,
                PRICE_SOURCE = 'calculated',
                PRICE_METHOD = 'Same VMPP'
            WHERE APPID = ?
            """
            
            database.execute_update(update_query, (avg_price, appid))
            updates += 1
            logger.info(f"Updated AMPP {appid} with calculated price {avg_price} from Same VMPP calculation")
    
    logger.info(f"Updated {updates} AMPP records using Same VMPP calculation")
    return updates


def calculate_same_vmp_prices():
    """
    Implement Rule 3: Same VMP (Fallback Calculation)
    - If no prices exist for the VMPP:
      - Calculate price per unit from other VMPPs with same VPID
      - Multiply by quantity to get estimated price
      - Update PRICE, set PRICE_SOURCE = 'calculated', PRICE_METHOD = 'Same VMP'
    
    Returns:
        int: Number of records updated.
    """
    logger.info("Applying Rule 3: Same VMP Calculation")
    
    # Get AMPPs with null prices
    ampp_null_price_query = """
    SELECT a.APPID, a.VPPID
    FROM ampp a
    WHERE a.PRICE IS NULL
    """
    
    ampp_records = database.execute_query(ampp_null_price_query)
    
    if not ampp_records:
        logger.info("No AMPP records with null prices found for Same VMP calculation")
        return 0
    
    logger.info(f"Found {len(ampp_records)} AMPP records with null prices")
    
    # Process each AMPP record with null price
    updates = 0
    
    for ampp in ampp_records:
        appid = ampp['APPID']
        vppid = ampp['VPPID']
        
        # Get the VPID and quantity for this VPPID
        vmpp_info_query = """
        SELECT v.VPID, v.QTYVAL, v.QTY_UOMCD
        FROM vmpp v
        WHERE v.VPPID = ?
        """
        
        vmpp_info = database.execute_query(vmpp_info_query, (vppid,))
        
        if not vmpp_info:
            logger.warning(f"Could not find VMPP info for VPPID {vppid}")
            continue
        
        vpid = vmpp_info[0]['VPID']
        target_qtyval = vmpp_info[0]['QTYVAL']
        qty_uomcd = vmpp_info[0]['QTY_UOMCD']
        
        # Find other VMPPs with the same VPID and same unit of measure, that have prices
        price_per_unit_query = """
        SELECT vmpp.VPPID, vmpp.QTYVAL, vmpp.PRICE, 
               CAST(vmpp.PRICE AS REAL) / vmpp.QTYVAL AS price_per_unit
        FROM vmpp
        WHERE vmpp.VPID = ?
        AND vmpp.QTY_UOMCD = ?
        AND vmpp.PRICE IS NOT NULL
        AND vmpp.VPPID != ?
        """
        
        price_info = database.execute_query(price_per_unit_query, (vpid, qty_uomcd, vppid))
        
        if not price_info:
            logger.warning(f"No pricing information found for other VMPPs with VPID {vpid}")
            continue
        
        # Calculate average price per unit
        total_price_per_unit = sum(item['price_per_unit'] for item in price_info)
        avg_price_per_unit = total_price_per_unit / len(price_info)
        
        # Calculate estimated price based on quantity
        estimated_price = round(avg_price_per_unit * target_qtyval)
        
        # Update the AMPP price
        update_query = """
        UPDATE ampp
        SET PRICE = ?,
            PRICE_SOURCE = 'calculated',
            PRICE_METHOD = 'Same VMP'
        WHERE APPID = ?
        """
        
        database.execute_update(update_query, (estimated_price, appid))
        updates += 1
        logger.info(f"Updated AMPP {appid} with calculated price {estimated_price} from Same VMP calculation")
    
    logger.info(f"Updated {updates} AMPP records using Same VMP calculation")
    return updates


def apply_default_prices():
    """
    Implement Rule 4: Default (Last Resort)
    - For any remaining records with null PRICE:
      - Set PRICE = 0, PRICE_SOURCE = 'calculated', PRICE_METHOD = 'None'
      - Log for manual review
    
    Returns:
        int: Number of records updated.
    """
    logger.info("Applying Rule 4: Default Pricing")
    
    # Get remaining AMPPs with null prices
    ampp_null_price_query = """
    SELECT APPID, NM
    FROM ampp
    WHERE PRICE IS NULL
    """
    
    ampp_records = database.execute_query(ampp_null_price_query)
    
    if not ampp_records:
        logger.info("No AMPP records with null prices remain")
        return 0
    
    logger.info(f"Found {len(ampp_records)} AMPP records with null prices for default pricing")
    
    # Update all remaining null-price AMPPs
    update_query = """
    UPDATE ampp
    SET PRICE = 0,
        PRICE_SOURCE = 'calculated',
        PRICE_METHOD = 'None'
    WHERE PRICE IS NULL
    """
    
    updated_count = database.execute_update(update_query)
    
    # Log records for manual review
    for ampp in ampp_records:
        logger.warning(f"Default price applied to AMPP ID {ampp['APPID']}: {ampp['NM']} - manual review required")
    
    logger.info(f"Applied default price to {updated_count} AMPP records")
    return updated_count


def calculate_all_prices():
    """
    Apply all pricing rules in sequence.
    
    Returns:
        dict: Statistics on how many records were updated by each rule.
    """
    logger.info("Starting price calculation process")
    
    stats = {
        'initial_price': 0,
        'same_vmpp': 0,
        'same_vmp': 0,
        'default': 0
    }
    
    # Apply rules in sequence
    stats['initial_price'] = update_initial_prices()
    stats['same_vmpp'] = calculate_same_vmpp_prices()
    stats['same_vmp'] = calculate_same_vmp_prices()
    stats['default'] = apply_default_prices()
    
    total_updated = sum(stats.values())
    logger.info(f"Price calculation complete. Updated {total_updated} AMPP records in total.")
    logger.info(f"Statistics: {stats}")
    
    return stats


if __name__ == "__main__":
    # Test price calculation
    calculate_all_prices() 