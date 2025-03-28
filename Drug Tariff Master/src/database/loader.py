"""
XML data loader for the Drug Tariff Processor.

This module provides functions to parse dm+d XML files and load the data
into the SQLite database.
"""

import os
import logging
import xml.etree.ElementTree as ET
import sqlite3
from datetime import datetime

logger = logging.getLogger('drug_tariff_processor')

def load_data(db_path, file_paths):
    """
    Load data from dm+d XML files into the database.
    
    This function processes the XML files in the correct order to maintain referential integrity
    and builds a unified search table for efficient querying. After this process completes,
    the price calculation can be performed separately to fill in missing prices.
    
    Args:
        db_path (str): Path to the SQLite database
        file_paths (dict): Dict mapping standardized file names to actual file paths
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create XML parsers for each file
        parsers = {
            'f_vtm2.xml': parse_vtm,
            'f_vmp2.xml': parse_vmp,
            'f_vmpp2.xml': parse_vmpp,
            'f_amp2.xml': parse_amp,
            'f_ampp2.xml': parse_ampp,
            'f_gtin2.xml': parse_gtin,
            'f_ingredient2.xml': parse_ingredient,
        }
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = OFF")  # Temporarily disable foreign key constraints for bulk loading
        
        # Process files in a specific order to maintain relational integrity
        processing_order = [
            'f_ingredient2.xml',
            'f_vtm2.xml',
            'f_vmp2.xml',
            'f_vmpp2.xml',
            'f_amp2.xml',
            'f_ampp2.xml',
            'f_gtin2.xml',
        ]
        
        for file_name in processing_order:
            if file_name in file_paths and file_name in parsers:
                file_path = file_paths[file_name]
                logger.info(f"Processing {file_name}...")
                
                try:
                    parsers[file_name](conn, file_path)
                except Exception as e:
                    logger.error(f"Error processing {file_name}: {e}")
                    conn.rollback()
                    return False
        
        # Build the unified search table
        build_unified_search_table(conn)
        
        # Enable foreign key constraints and commit
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()
        logger.info("Data loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def parse_vtm(conn, file_path):
    """Parse VTM XML and load into database."""
    logger.info(f"Parsing VTM data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    for vtm in root.findall('.//VTM'):
        vtm_data = {
            'vtmid': get_element_text(vtm, 'VTMID'),
            'name': get_element_text(vtm, 'NM'),
            'abbrev_name': get_element_text(vtm, 'ABBREVNM'),
            'invalid': get_element_text(vtm, 'INVALID'),
            'vtmid_prev': get_element_text(vtm, 'VTMIDPREV'),
            'vtmid_date': parse_date(get_element_text(vtm, 'VTMIDDT')),
        }
        
        insert_record(cursor, 'vtm', vtm_data)
    
    conn.commit()
    logger.info(f"Inserted {cursor.rowcount} VTM records")

def parse_vmp(conn, file_path):
    """Parse VMP XML and load into database."""
    logger.info(f"Parsing VMP data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    # Process VMP main records
    for vmp in root.findall('.//VMP'):
        vmp_data = {
            'vpid': get_element_text(vmp, 'VPID'),
            'vtmid': get_element_text(vmp, 'VTMID'),
            'name': get_element_text(vmp, 'NM'),
            'abbrev_name': get_element_text(vmp, 'ABBREVNM'),
            'basis_code': get_element_text(vmp, 'BASISCD'),
            'name_prev': get_element_text(vmp, 'NMPREV'),
            'name_change_reason_code': get_element_text(vmp, 'NMCHANGECD'),
            'invalid': get_element_text(vmp, 'INVALID'),
            'non_avail_code': get_element_text(vmp, 'NON_AVAILCD'),
            'non_avail_date': parse_date(get_element_text(vmp, 'NON_AVAILDT')),
            'df_indicator_code': get_element_text(vmp, 'DF_INDCD'),
            'pres_status_code': get_element_text(vmp, 'PRES_STATCD'),
            'comb_prod_code': get_element_text(vmp, 'COMBPRODCD'),
            'sugar_free': get_element_text(vmp, 'SUG_F'),
            'gluten_free': get_element_text(vmp, 'GLU_F'),
            'preservative_free': get_element_text(vmp, 'PRES_F'),
            'cfc_free': get_element_text(vmp, 'CFC_F'),
        }
        
        insert_record(cursor, 'vmp', vmp_data)
    
    # Process VMP ingredients
    for vpi in root.findall('.//VPI'):
        vpi_data = {
            'vpid': get_element_text(vpi, 'VPID'),
            'isid': get_element_text(vpi, 'ISID'),
            'basis_strnt_code': get_element_text(vpi, 'BASIS_STRNTCD'),
            'bs_subid': get_element_text(vpi, 'BS_SUBID'),
            'strnt_nmrtr_val': get_element_text(vpi, 'STRNT_NMRTR_VAL'),
            'strnt_nmrtr_uom_code': get_element_text(vpi, 'STRNT_NMRTR_UOMCD'),
            'strnt_dnmtr_val': get_element_text(vpi, 'STRNT_DNMTR_VAL'),
            'strnt_dnmtr_uom_code': get_element_text(vpi, 'STRNT_DNMTR_UOMCD'),
        }
        
        insert_record(cursor, 'vmp_ingredient', vpi_data)
    
    # Process drug forms
    for dform in root.findall('.//DFORM'):
        form_data = {
            'vpid': get_element_text(dform, 'VPID'),
            'form_code': get_element_text(dform, 'FORMCD'),
        }
        
        insert_record(cursor, 'vmp_form', form_data)
    
    # Process drug routes
    for droute in root.findall('.//DROUTE'):
        route_data = {
            'vpid': get_element_text(droute, 'VPID'),
            'route_code': get_element_text(droute, 'ROUTECD'),
        }
        
        insert_record(cursor, 'vmp_route', route_data)
    
    conn.commit()
    logger.info(f"Processed VMP data")

def parse_vmpp(conn, file_path):
    """Parse VMPP XML and load into database."""
    logger.info(f"Parsing VMPP data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    # Process VMPP main records
    for vmpp in root.findall('.//VMPP'):
        vmpp_data = {
            'vppid': get_element_text(vmpp, 'VPPID'),
            'vpid': get_element_text(vmpp, 'VPID'),
            'name': get_element_text(vmpp, 'NM'),
            'abbrev_name': get_element_text(vmpp, 'ABBREVNM'),
            'qty_value': get_element_text(vmpp, 'QTYVAL'),
            'qty_uom_code': get_element_text(vmpp, 'QTY_UOMCD'),
            'comb_pack_code': get_element_text(vmpp, 'COMBPACKCD'),
            'invalid': get_element_text(vmpp, 'INVALID'),
        }
        
        insert_record(cursor, 'vmpp', vmpp_data)
    
    # Process drug tariff info
    for dtinfo in root.findall('.//DTINFO'):
        dt_data = {
            'vppid': get_element_text(dtinfo, 'VPPID'),
            'pay_cat_code': get_element_text(dtinfo, 'PAY_CATCD'),
            'price': get_element_text(dtinfo, 'PRICE'),
            'dt': parse_date(get_element_text(dtinfo, 'DT')),
            'prev_price': get_element_text(dtinfo, 'PREVPRICE'),
        }
        
        insert_record(cursor, 'vmpp_dt_info', dt_data)
    
    conn.commit()
    logger.info(f"Processed VMPP data")

def parse_amp(conn, file_path):
    """Parse AMP XML and load into database."""
    logger.info(f"Parsing AMP data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    # Process AMP main records
    for amp in root.findall('.//AMP'):
        amp_data = {
            'apid': get_element_text(amp, 'APID'),
            'vpid': get_element_text(amp, 'VPID'),
            'name': get_element_text(amp, 'NM'),
            'abbrev_name': get_element_text(amp, 'ABBREVNM'),
            'desc': get_element_text(amp, 'DESC'),
            'name_prev': get_element_text(amp, 'NM_PREV'),
            'supp_code': get_element_text(amp, 'SUPPCD'),
            'lic_auth_code': get_element_text(amp, 'LIC_AUTHCD'),
            'lic_auth_prev_code': get_element_text(amp, 'LIC_AUTH_PREVCD'),
            'lic_auth_change_code': get_element_text(amp, 'LIC_AUTHCHANGECD'),
            'lic_auth_change_date': parse_date(get_element_text(amp, 'LIC_AUTHCHANGEDT')),
            'comb_prod_code': get_element_text(amp, 'COMBPRODCD'),
            'flavor_code': get_element_text(amp, 'FLAVOURCD'),
            'ema': get_element_text(amp, 'EMA'),
            'parallel_import': get_element_text(amp, 'PARALLEL_IMPORT'),
            'avail_restrict_code': get_element_text(amp, 'AVAIL_RESTRICTCD'),
            'invalid': get_element_text(amp, 'INVALID'),
        }
        
        insert_record(cursor, 'amp', amp_data)
    
    # Process AMP ingredients
    for ap_ing in root.findall('.//AP_ING'):
        api_data = {
            'apid': get_element_text(ap_ing, 'APID'),
            'isid': get_element_text(ap_ing, 'ISID'),
            'strength': get_element_text(ap_ing, 'STRNTH'),
            'uom_code': get_element_text(ap_ing, 'UOMCD'),
        }
        
        insert_record(cursor, 'amp_ingredient', api_data)
    
    # Process licensed routes
    for lic_route in root.findall('.//LIC_ROUTE'):
        route_data = {
            'apid': get_element_text(lic_route, 'APID'),
            'route_code': get_element_text(lic_route, 'ROUTECD'),
        }
        
        insert_record(cursor, 'amp_route', route_data)
    
    conn.commit()
    logger.info(f"Processed AMP data")

def parse_ampp(conn, file_path):
    """Parse AMPP XML and load into database."""
    logger.info(f"Parsing AMPP data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    # Process AMPP main records
    for ampp in root.findall('.//AMPP'):
        ampp_data = {
            'appid': get_element_text(ampp, 'APPID'),
            'apid': get_element_text(ampp, 'APID'),
            'vppid': get_element_text(ampp, 'VPPID'),
            'name': get_element_text(ampp, 'NM'),
            'abbrev_name': get_element_text(ampp, 'ABBREVNM'),
            'subpack': get_element_text(ampp, 'SUBP'),
            'legal_cat_code': get_element_text(ampp, 'LEGAL_CATCD'),
            'comb_pack_code': get_element_text(ampp, 'COMBPACKCD'),
            'disc_code': get_element_text(ampp, 'DISCCD'),
            'disc_date': parse_date(get_element_text(ampp, 'DISCDT')),
            'invalid': get_element_text(ampp, 'INVALID'),
        }
        
        insert_record(cursor, 'ampp', ampp_data)
    
    # Process price info
    for price_info in root.findall('.//PRICE_INFO'):
        price_data = {
            'appid': get_element_text(price_info, 'APPID'),
            'price': get_element_text(price_info, 'PRICE'),
            'price_date': parse_date(get_element_text(price_info, 'PRICEDT')),
            'price_prev': get_element_text(price_info, 'PRICE_PREV'),
            'price_basis_code': get_element_text(price_info, 'PRICE_BASISCD'),
        }
        
        insert_record(cursor, 'ampp_price_info', price_data)
    
    # Process reimbursement info
    for reimb_info in root.findall('.//REIMB_INFO'):
        reimb_data = {
            'appid': get_element_text(reimb_info, 'APPID'),
            'px_chrgs': get_element_text(reimb_info, 'PX_CHRGS'),
            'disp_fees': get_element_text(reimb_info, 'DISP_FEES'),
            'bb': get_element_text(reimb_info, 'BB'),
            'ltd_stab': get_element_text(reimb_info, 'LTD_STAB'),
            'cal_pack': get_element_text(reimb_info, 'CAL_PACK'),
            'spec_cont_code': get_element_text(reimb_info, 'SPEC_CONTCD'),
            'dnd': get_element_text(reimb_info, 'DND'),
            'fp34d': get_element_text(reimb_info, 'FP34D'),
        }
        
        insert_record(cursor, 'ampp_reimb_info', reimb_data)
    
    # Process prescribing info
    for prescrib_info in root.findall('.//PRESCRIB_INFO'):
        prescrib_data = {
            'appid': get_element_text(prescrib_info, 'APPID'),
            'sched_2': get_element_text(prescrib_info, 'SCHED_2'),
            'acbs': get_element_text(prescrib_info, 'ACBS'),
            'padm': get_element_text(prescrib_info, 'PADM'),
            'fp10_mda': get_element_text(prescrib_info, 'FP10_MDA'),
            'sched_1': get_element_text(prescrib_info, 'SCHED_1'),
            'hosp': get_element_text(prescrib_info, 'HOSP'),
            'nurse_f': get_element_text(prescrib_info, 'NURSE_F'),
            'enurse_f': get_element_text(prescrib_info, 'ENURSE_F'),
            'dent_f': get_element_text(prescrib_info, 'DENT_F'),
        }
        
        insert_record(cursor, 'ampp_prescrib_info', prescrib_data)
    
    # Process pack info
    for pack_info in root.findall('.//PACK_INFO'):
        pack_data = {
            'appid': get_element_text(pack_info, 'APPID'),
            'reimb_stat_code': get_element_text(pack_info, 'REIMB_STATCD'),
            'reimb_stat_date': parse_date(get_element_text(pack_info, 'REIMB_STATDT')),
            'reimb_stat_prev_code': get_element_text(pack_info, 'REIMB_STATPREVCD'),
            'pack_order_no': get_element_text(pack_info, 'PACK_ORDER_NO'),
        }
        
        insert_record(cursor, 'ampp_pack_info', pack_data)
    
    conn.commit()
    logger.info(f"Processed AMPP data")

def parse_gtin(conn, file_path):
    """Parse GTIN XML and load into database."""
    logger.info(f"Parsing GTIN data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    for ampp in root.findall('.//AMPP'):
        appid = get_element_text(ampp, 'AMPPID')
        
        for gtin_data in ampp.findall('.//GTINDATA'):
            gtin_code = get_element_text(gtin_data, 'GTIN')
            start_date = parse_date(get_element_text(gtin_data, 'STARTDT'))
            end_date = parse_date(get_element_text(gtin_data, 'ENDDT'))
            
            gtin_record = {
                'appid': appid,
                'gtin': gtin_code,
                'start_date': start_date,
                'end_date': end_date,
            }
            
            insert_record(cursor, 'gtin', gtin_record)
    
    conn.commit()
    logger.info(f"Processed GTIN data")

def parse_ingredient(conn, file_path):
    """Parse Ingredient XML and load into database."""
    logger.info(f"Parsing Ingredient data from {file_path}")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    cursor = conn.cursor()
    
    for ing in root.findall('.//ING'):
        ing_data = {
            'isid': get_element_text(ing, 'ISID'),
            'name': get_element_text(ing, 'NM'),
            'isid_date': parse_date(get_element_text(ing, 'ISIDDT')),
            'isid_prev': get_element_text(ing, 'ISIDPREV'),
            'invalid': get_element_text(ing, 'INVALID'),
        }
        
        insert_record(cursor, 'ingredient', ing_data)
    
    conn.commit()
    logger.info(f"Processed Ingredient data")

def build_unified_search_table(conn):
    """Build the unified search table by joining data from all tables."""
    logger.info("Building unified search table...")
    
    cursor = conn.cursor()
    
    # Clear the table first
    cursor.execute("DELETE FROM unified_search")
    
    # Insert data from VMPs (generic products)
    cursor.execute("""
        INSERT INTO unified_search (
            vtmid, vpid, name, is_brand, ingredient_list, form
        )
        SELECT 
            v.vtmid, 
            v.vpid, 
            v.name, 
            0 AS is_brand,
            GROUP_CONCAT(i.name, ', ') AS ingredient_list,
            GROUP_CONCAT(DISTINCT f.form_code) AS form
        FROM vmp v
        LEFT JOIN vmp_ingredient vi ON v.vpid = vi.vpid
        LEFT JOIN ingredient i ON vi.isid = i.isid
        LEFT JOIN vmp_form f ON v.vpid = f.vpid
        WHERE v.invalid IS NULL OR v.invalid = 0
        GROUP BY v.vpid
    """)
    
    # Insert data from AMPs (branded products)
    cursor.execute("""
        INSERT INTO unified_search (
            vtmid, vpid, apid, name, is_brand, ingredient_list, form
        )
        SELECT 
            v.vtmid, 
            a.vpid, 
            a.apid, 
            a.name, 
            1 AS is_brand,
            GROUP_CONCAT(i.name, ', ') AS ingredient_list,
            GROUP_CONCAT(DISTINCT f.form_code) AS form
        FROM amp a
        JOIN vmp v ON a.vpid = v.vpid
        LEFT JOIN amp_ingredient ai ON a.apid = ai.apid
        LEFT JOIN ingredient i ON ai.isid = i.isid
        LEFT JOIN vmp_form f ON v.vpid = f.vpid
        WHERE a.invalid IS NULL OR a.invalid = 0
        GROUP BY a.apid
    """)
    
    # Insert data from VMPPs (generic packs)
    cursor.execute("""
        INSERT INTO unified_search (
            vtmid, vpid, vppid, name, is_brand, ingredient_list, form, pack_size, dt_price
        )
        SELECT 
            v.vtmid, 
            vp.vpid, 
            vp.vppid, 
            vp.name, 
            0 AS is_brand,
            GROUP_CONCAT(i.name, ', ') AS ingredient_list,
            GROUP_CONCAT(DISTINCT f.form_code) AS form,
            vp.qty_value || ' ' || vp.qty_uom_code AS pack_size,
            dti.price AS dt_price
        FROM vmpp vp
        JOIN vmp v ON vp.vpid = v.vpid
        LEFT JOIN vmp_ingredient vi ON v.vpid = vi.vpid
        LEFT JOIN ingredient i ON vi.isid = i.isid
        LEFT JOIN vmp_form f ON v.vpid = f.vpid
        LEFT JOIN vmpp_dt_info dti ON vp.vppid = dti.vppid
        WHERE vp.invalid IS NULL OR vp.invalid = 0
        GROUP BY vp.vppid
    """)
    
    # Insert data from AMPPs (branded packs)
    cursor.execute("""
        INSERT INTO unified_search (
            vtmid, vpid, vppid, apid, appid, name, is_brand, ingredient_list, form, pack_size, dt_price, nhs_price, gtin
        )
        SELECT 
            v.vtmid, 
            a.vpid, 
            ap.vppid, 
            a.apid, 
            ap.appid, 
            ap.name, 
            1 AS is_brand,
            GROUP_CONCAT(i.name, ', ') AS ingredient_list,
            GROUP_CONCAT(DISTINCT f.form_code) AS form,
            vp.qty_value || ' ' || vp.qty_uom_code AS pack_size,
            dti.price AS dt_price,
            pi.price AS nhs_price,
            g.gtin
        FROM ampp ap
        JOIN amp a ON ap.apid = a.apid
        JOIN vmp v ON a.vpid = v.vpid
        JOIN vmpp vp ON ap.vppid = vp.vppid
        LEFT JOIN amp_ingredient ai ON a.apid = ai.apid
        LEFT JOIN ingredient i ON ai.isid = i.isid
        LEFT JOIN vmp_form f ON v.vpid = f.vpid
        LEFT JOIN vmpp_dt_info dti ON vp.vppid = dti.vppid
        LEFT JOIN ampp_price_info pi ON ap.appid = pi.appid
        LEFT JOIN gtin g ON ap.appid = g.appid
        WHERE (ap.invalid IS NULL OR ap.invalid = 0)
          AND (g.end_date IS NULL OR g.end_date >= date('now'))
        GROUP BY ap.appid, g.gtin
    """)
    
    conn.commit()
    logger.info("Unified search table built successfully")

def get_element_text(element, tag_name):
    """Get text content of an XML element, or None if it doesn't exist."""
    tag = element.find(tag_name)
    if tag is not None:
        return tag.text
    return None

def parse_date(date_str):
    """Parse date string to SQLite compatible format."""
    if not date_str:
        return None
    try:
        # Expected format: YYYY-MM-DD
        return date_str
    except ValueError:
        logger.warning(f"Failed to parse date: {date_str}")
        return None

def insert_record(cursor, table, data):
    """Insert a record into a table."""
    # Filter out None values
    filtered_data = {k: v for k, v in data.items() if v is not None}
    
    if not filtered_data:
        return
    
    columns = ', '.join(filtered_data.keys())
    placeholders = ', '.join(['?' for _ in filtered_data])
    values = list(filtered_data.values())
    
    query = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(query, values)
    except sqlite3.Error as e:
        logger.error(f"Error inserting into {table}: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Values: {values}")
        raise