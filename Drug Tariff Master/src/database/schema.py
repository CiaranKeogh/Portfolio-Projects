"""
Database schema for the Drug Tariff Processor.

This module defines the SQLite database schema for storing dm+d data
and provides functions to create and connect to the database.
"""

import os
import sqlite3
import logging

logger = logging.getLogger('drug_tariff_processor')

def get_connection(db_path):
    """
    Get a connection to the SQLite database.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        sqlite3.Connection: Connection to the database
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    return conn

def create_database(db_path):
    """
    Create the SQLite database with the dm+d schema.
    
    Args:
        db_path (str): Path to create the SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        
        # Create the tables
        cursor.executescript("""
            -- Virtual Therapeutic Moiety (VTM)
            CREATE TABLE IF NOT EXISTS vtm (
                vtmid INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                abbrev_name TEXT,
                invalid INTEGER,
                vtmid_prev TEXT,
                vtmid_date DATE
            );

            -- Virtual Medicinal Product (VMP)
            CREATE TABLE IF NOT EXISTS vmp (
                vpid INTEGER PRIMARY KEY,
                vtmid INTEGER,
                name TEXT NOT NULL,
                abbrev_name TEXT,
                basis_code INTEGER NOT NULL,
                name_prev TEXT,
                name_change_reason_code INTEGER,
                invalid INTEGER,
                non_avail_code INTEGER,
                non_avail_date DATE,
                df_indicator_code INTEGER,
                pres_status_code INTEGER NOT NULL,
                comb_prod_code INTEGER,
                sugar_free INTEGER,
                gluten_free INTEGER,
                preservative_free INTEGER,
                cfc_free INTEGER,
                
                FOREIGN KEY (vtmid) REFERENCES vtm(vtmid)
            );

            -- Virtual Medicinal Product Pack (VMPP)
            CREATE TABLE IF NOT EXISTS vmpp (
                vppid INTEGER PRIMARY KEY,
                vpid INTEGER NOT NULL,
                name TEXT NOT NULL,
                abbrev_name TEXT,
                qty_value REAL NOT NULL,
                qty_uom_code INTEGER NOT NULL,
                comb_pack_code INTEGER,
                invalid INTEGER,
                
                FOREIGN KEY (vpid) REFERENCES vmp(vpid)
            );

            -- Actual Medicinal Product (AMP)
            CREATE TABLE IF NOT EXISTS amp (
                apid INTEGER PRIMARY KEY,
                vpid INTEGER NOT NULL,
                name TEXT NOT NULL,
                abbrev_name TEXT,
                desc TEXT NOT NULL,
                name_prev TEXT,
                supp_code INTEGER NOT NULL,
                lic_auth_code INTEGER NOT NULL,
                lic_auth_prev_code INTEGER,
                lic_auth_change_code INTEGER,
                lic_auth_change_date DATE,
                comb_prod_code INTEGER,
                flavor_code INTEGER,
                ema INTEGER,
                parallel_import INTEGER,
                avail_restrict_code INTEGER NOT NULL,
                invalid INTEGER,
                
                FOREIGN KEY (vpid) REFERENCES vmp(vpid)
            );

            -- Actual Medicinal Product Pack (AMPP)
            CREATE TABLE IF NOT EXISTS ampp (
                appid INTEGER PRIMARY KEY,
                apid INTEGER NOT NULL,
                vppid INTEGER NOT NULL,
                name TEXT NOT NULL,
                abbrev_name TEXT,
                subpack TEXT,
                legal_cat_code INTEGER NOT NULL,
                comb_pack_code INTEGER,
                disc_code INTEGER,
                disc_date DATE,
                invalid INTEGER,
                
                FOREIGN KEY (apid) REFERENCES amp(apid),
                FOREIGN KEY (vppid) REFERENCES vmpp(vppid)
            );

            -- Ingredient
            CREATE TABLE IF NOT EXISTS ingredient (
                isid INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                isid_date DATE,
                isid_prev INTEGER,
                invalid INTEGER
            );

            -- VMP Ingredient
            CREATE TABLE IF NOT EXISTS vmp_ingredient (
                vpid INTEGER NOT NULL,
                isid INTEGER NOT NULL,
                basis_strnt_code INTEGER,
                bs_subid INTEGER,
                strnt_nmrtr_val REAL,
                strnt_nmrtr_uom_code INTEGER,
                strnt_dnmtr_val REAL,
                strnt_dnmtr_uom_code INTEGER,
                
                PRIMARY KEY (vpid, isid),
                FOREIGN KEY (vpid) REFERENCES vmp(vpid),
                FOREIGN KEY (isid) REFERENCES ingredient(isid)
            );

            -- AMP Ingredient
            CREATE TABLE IF NOT EXISTS amp_ingredient (
                apid INTEGER NOT NULL,
                isid INTEGER NOT NULL,
                strength REAL,
                uom_code INTEGER,
                
                PRIMARY KEY (apid, isid),
                FOREIGN KEY (apid) REFERENCES amp(apid),
                FOREIGN KEY (isid) REFERENCES ingredient(isid)
            );

            -- Drug Form (for VMP)
            CREATE TABLE IF NOT EXISTS vmp_form (
                vpid INTEGER NOT NULL,
                form_code INTEGER NOT NULL,
                
                PRIMARY KEY (vpid, form_code),
                FOREIGN KEY (vpid) REFERENCES vmp(vpid)
            );

            -- Drug Route (for VMP)
            CREATE TABLE IF NOT EXISTS vmp_route (
                vpid INTEGER NOT NULL,
                route_code INTEGER NOT NULL,
                
                PRIMARY KEY (vpid, route_code),
                FOREIGN KEY (vpid) REFERENCES vmp(vpid)
            );

            -- Licensed Route (for AMP)
            CREATE TABLE IF NOT EXISTS amp_route (
                apid INTEGER NOT NULL,
                route_code INTEGER NOT NULL,
                
                PRIMARY KEY (apid, route_code),
                FOREIGN KEY (apid) REFERENCES amp(apid)
            );

            -- GTIN
            CREATE TABLE IF NOT EXISTS gtin (
                gtin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                appid INTEGER NOT NULL,
                gtin TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Drug Tariff Info (for VMPP)
            CREATE TABLE IF NOT EXISTS vmpp_dt_info (
                vppid INTEGER NOT NULL,
                pay_cat_code INTEGER NOT NULL,
                price INTEGER,
                dt DATE,
                prev_price INTEGER,
                
                PRIMARY KEY (vppid, pay_cat_code),
                FOREIGN KEY (vppid) REFERENCES vmpp(vppid)
            );

            -- Price Info (for AMPP)
            CREATE TABLE IF NOT EXISTS ampp_price_info (
                appid INTEGER NOT NULL,
                price INTEGER,
                price_date DATE,
                price_prev INTEGER,
                price_basis_code INTEGER NOT NULL,
                
                PRIMARY KEY (appid),
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Reimbursement Info (for AMPP)
            CREATE TABLE IF NOT EXISTS ampp_reimb_info (
                appid INTEGER NOT NULL,
                px_chrgs INTEGER,
                disp_fees INTEGER,
                bb INTEGER,
                ltd_stab INTEGER,
                cal_pack INTEGER,
                spec_cont_code INTEGER,
                dnd INTEGER,
                fp34d INTEGER,
                
                PRIMARY KEY (appid),
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Prescribing Info (for AMPP)
            CREATE TABLE IF NOT EXISTS ampp_prescrib_info (
                appid INTEGER NOT NULL,
                sched_2 INTEGER,
                acbs INTEGER,
                padm INTEGER,
                fp10_mda INTEGER,
                sched_1 INTEGER,
                hosp INTEGER,
                nurse_f INTEGER,
                enurse_f INTEGER,
                dent_f INTEGER,
                
                PRIMARY KEY (appid),
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Pack Info (for AMPP)
            CREATE TABLE IF NOT EXISTS ampp_pack_info (
                appid INTEGER NOT NULL,
                reimb_stat_code INTEGER NOT NULL,
                reimb_stat_date DATE,
                reimb_stat_prev_code INTEGER,
                pack_order_no TEXT,
                
                PRIMARY KEY (appid),
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Unified Search Table
            CREATE TABLE IF NOT EXISTS unified_search (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vtmid INTEGER,
                vpid INTEGER,
                vppid INTEGER,
                apid INTEGER,
                appid INTEGER,
                gtin TEXT,
                name TEXT NOT NULL,
                is_brand INTEGER NOT NULL,
                ingredient_list TEXT,
                form TEXT,
                strength TEXT,
                pack_size TEXT,
                dt_price INTEGER,
                nhs_price INTEGER,
                calculation_method TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (vtmid) REFERENCES vtm(vtmid),
                FOREIGN KEY (vpid) REFERENCES vmp(vpid),
                FOREIGN KEY (vppid) REFERENCES vmpp(vppid),
                FOREIGN KEY (apid) REFERENCES amp(apid),
                FOREIGN KEY (appid) REFERENCES ampp(appid)
            );

            -- Create indexes for better query performance
            CREATE INDEX IF NOT EXISTS idx_vmp_vtmid ON vmp(vtmid);
            CREATE INDEX IF NOT EXISTS idx_vmpp_vpid ON vmpp(vpid);
            CREATE INDEX IF NOT EXISTS idx_amp_vpid ON amp(vpid);
            CREATE INDEX IF NOT EXISTS idx_ampp_apid ON ampp(apid);
            CREATE INDEX IF NOT EXISTS idx_ampp_vppid ON ampp(vppid);
            CREATE INDEX IF NOT EXISTS idx_gtin_appid ON gtin(appid);
            CREATE INDEX IF NOT EXISTS idx_gtin_gtin ON gtin(gtin);
            CREATE INDEX IF NOT EXISTS idx_unified_search_name ON unified_search(name);
            CREATE INDEX IF NOT EXISTS idx_unified_search_gtin ON unified_search(gtin);
            
            -- Additional indexes for web application performance
            CREATE INDEX IF NOT EXISTS idx_unified_search_ingredient_form ON unified_search(ingredient_list, form);
            CREATE INDEX IF NOT EXISTS idx_unified_search_price_range ON unified_search(dt_price, nhs_price);
            CREATE INDEX IF NOT EXISTS idx_unified_search_calculation ON unified_search(calculation_method);

            -- Create view for common web queries
            CREATE VIEW IF NOT EXISTS web_product_view AS
            SELECT 
                id, 
                name, 
                is_brand, 
                ingredient_list, 
                form, 
                strength, 
                pack_size, 
                dt_price/100.0 AS dt_price_gbp,
                nhs_price/100.0 AS nhs_price_gbp,
                calculation_method,
                gtin
            FROM 
                unified_search;
        """)
        
        conn.commit()
        logger.info(f"Database created successfully at {db_path}")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Error creating database: {e}")
        return False
    finally:
        if conn:
            conn.close() 