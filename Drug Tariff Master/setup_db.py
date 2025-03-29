#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone script to set up the SQLite database for the Drug Tariff Master project.
This script is a wrapper around drug_tariff_master.setup_database.
"""

import os
import sqlite3
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)

# Create SQLite database
db_path = data_dir / "dmd.db"
print(f"Creating database at {db_path}")

try:
    # Create tables directly here
    with sqlite3.connect(db_path) as conn:
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create lookup tables
        print("Creating lookup tables...")
        
        # Lookup tables with no dependencies
        lookup_tables = [
            """
            CREATE TABLE lookup_combination_pack_indicator (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_combination_product_indicator (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_basis_of_name (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_name_change_reason (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_virtual_product_pres_status (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_control_drug_category (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_licensing_authority (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_unit_of_measure (
                CD        INTEGER PRIMARY KEY NOT NULL,
                CDDT      TEXT,
                CDPREV    INTEGER,
                DESC      TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_form (
                CD        INTEGER PRIMARY KEY NOT NULL,
                CDDT      TEXT,
                CDPREV    INTEGER,
                DESC      TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_ontology_form_route (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_route (
                CD        INTEGER PRIMARY KEY NOT NULL,
                CDDT      TEXT,
                CDPREV    INTEGER,
                DESC      TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_drug_tariff_payment_category (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_supplier (
                CD       INTEGER PRIMARY KEY NOT NULL,
                CDDT     TEXT,
                CDPREV   INTEGER,
                INVALID  INTEGER,
                DESC     TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_flavour (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_colour (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_basis_of_strength (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_reimbursement_status (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_special_container (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_dnd (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_virtual_product_non_avail (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_discontinued_indicator (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_df_indicator (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_price_basis (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_legal_category (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_availability_restriction (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE lookup_licensing_authority_change_reason (
                CD    INTEGER PRIMARY KEY NOT NULL,
                DESC  TEXT NOT NULL
            )
            """
        ]
        
        for statement in lookup_tables:
            conn.execute(statement)
        
        # Create ingredient table
        print("Creating ingredient table...")
        conn.execute("""
        CREATE TABLE ingredient (
            ISID      INTEGER PRIMARY KEY NOT NULL,
            ISIDDT    TEXT,
            ISIDPREV  INTEGER,
            INVALID   INTEGER,
            NM        TEXT NOT NULL
        )
        """)
        
        # Create VTM table
        print("Creating VTM table...")
        conn.execute("""
        CREATE TABLE vtm (
            VTMID       INTEGER PRIMARY KEY NOT NULL,
            INVALID     INTEGER,
            NM          TEXT NOT NULL,
            ABBREVNM    TEXT,
            VTMIDPREV   TEXT,
            VTMIDDT     TEXT
        )
        """)
        
        # Create VMP tables
        print("Creating VMP tables...")
        vmp_tables = [
            """
            CREATE TABLE vmp (
                VPID           INTEGER PRIMARY KEY NOT NULL,
                VPIDDT         TEXT,
                VPIDPREV       INTEGER,
                VTMID          INTEGER,
                INVALID        INTEGER,
                NM             TEXT NOT NULL,
                ABBREVNM       TEXT,
                BASISCD        INTEGER NOT NULL,
                NMDT           TEXT,
                NMPREV         TEXT,
                BASIS_PREVCD   INTEGER,
                NMCHANGECD     INTEGER,
                COMBPRODCD     INTEGER,
                PRES_STATCD    INTEGER NOT NULL,
                SUG_F          INTEGER,
                GLU_F          INTEGER,
                PRES_F         INTEGER,
                CFC_F          INTEGER,
                NON_AVAILCD    INTEGER,
                NON_AVAILDT    TEXT,
                DF_INDCD       INTEGER,
                UDFS           REAL,
                UDFS_UOMCD     INTEGER,
                UNIT_DOSE_UOMCD INTEGER,

                FOREIGN KEY (VTMID) REFERENCES vtm(VTMID) ON DELETE RESTRICT,
                FOREIGN KEY (BASISCD) REFERENCES lookup_basis_of_name(CD) ON DELETE RESTRICT,
                FOREIGN KEY (BASIS_PREVCD) REFERENCES lookup_basis_of_name(CD) ON DELETE RESTRICT,
                FOREIGN KEY (NMCHANGECD) REFERENCES lookup_name_change_reason(CD) ON DELETE RESTRICT,
                FOREIGN KEY (COMBPRODCD) REFERENCES lookup_combination_product_indicator(CD) ON DELETE RESTRICT,
                FOREIGN KEY (PRES_STATCD) REFERENCES lookup_virtual_product_pres_status(CD) ON DELETE RESTRICT,
                FOREIGN KEY (NON_AVAILCD) REFERENCES lookup_virtual_product_non_avail(CD) ON DELETE RESTRICT,
                FOREIGN KEY (DF_INDCD) REFERENCES lookup_df_indicator(CD) ON DELETE RESTRICT,
                FOREIGN KEY (UDFS_UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT,
                FOREIGN KEY (UNIT_DOSE_UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmp_ingredient (
                VPID              INTEGER NOT NULL,
                ISID              INTEGER NOT NULL,
                BASIS_STRNTCD     INTEGER,
                BS_SUBID          INTEGER,
                STRNT_NMRTR_VAL   REAL,
                STRNT_NMRTR_UOMCD INTEGER,
                STRNT_DNMTR_VAL   REAL,
                STRNT_DNMTR_UOMCD INTEGER,

                PRIMARY KEY (VPID, ISID),
                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE CASCADE,
                FOREIGN KEY (ISID) REFERENCES ingredient(ISID) ON DELETE RESTRICT,
                FOREIGN KEY (BASIS_STRNTCD) REFERENCES lookup_basis_of_strength(CD) ON DELETE RESTRICT,
                FOREIGN KEY (BS_SUBID) REFERENCES ingredient(ISID) ON DELETE RESTRICT,
                FOREIGN KEY (STRNT_NMRTR_UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT,
                FOREIGN KEY (STRNT_DNMTR_UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmp_ontology_form_route (
                VPID      INTEGER NOT NULL,
                FORMCD    INTEGER NOT NULL,

                PRIMARY KEY (VPID, FORMCD),
                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE CASCADE,
                FOREIGN KEY (FORMCD) REFERENCES lookup_ontology_form_route(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmp_drug_form (
                VPID      INTEGER NOT NULL,
                FORMCD    INTEGER NOT NULL,

                PRIMARY KEY (VPID, FORMCD),
                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE CASCADE,
                FOREIGN KEY (FORMCD) REFERENCES lookup_form(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmp_drug_route (
                VPID      INTEGER NOT NULL,
                ROUTECD   INTEGER NOT NULL,

                PRIMARY KEY (VPID, ROUTECD),
                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE CASCADE,
                FOREIGN KEY (ROUTECD) REFERENCES lookup_route(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmp_control_drug_info (
                VPID        INTEGER NOT NULL,
                CATCD       INTEGER NOT NULL,
                CATDT       TEXT,
                CAT_PREVCD  INTEGER,

                PRIMARY KEY (VPID, CATCD),
                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE CASCADE,
                FOREIGN KEY (CATCD) REFERENCES lookup_control_drug_category(CD) ON DELETE RESTRICT,
                FOREIGN KEY (CAT_PREVCD) REFERENCES lookup_control_drug_category(CD) ON DELETE RESTRICT
            )
            """
        ]
        
        for statement in vmp_tables:
            conn.execute(statement)
        
        # Create AMP tables
        print("Creating AMP tables...")
        amp_tables = [
            """
            CREATE TABLE amp (
                APID               INTEGER PRIMARY KEY NOT NULL,
                INVALID            INTEGER,
                VPID               INTEGER NOT NULL,
                NM                 TEXT NOT NULL,
                ABBREVNM           TEXT,
                DESC               TEXT NOT NULL,
                NMDT               TEXT,
                NM_PREV            TEXT,
                SUPPCD             INTEGER NOT NULL,
                LIC_AUTHCD         INTEGER NOT NULL,
                LIC_AUTH_PREVCD    INTEGER,
                LIC_AUTHCHANGECD   INTEGER,
                LIC_AUTHCHANGEDT   TEXT,
                COMBPRODCD         INTEGER,
                FLAVOURCD          INTEGER,
                EMA                INTEGER,
                PARALLEL_IMPORT    INTEGER,
                AVAIL_RESTRICTCD   INTEGER NOT NULL,

                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE RESTRICT,
                FOREIGN KEY (SUPPCD) REFERENCES lookup_supplier(CD) ON DELETE RESTRICT,
                FOREIGN KEY (LIC_AUTHCD) REFERENCES lookup_licensing_authority(CD) ON DELETE RESTRICT,
                FOREIGN KEY (LIC_AUTH_PREVCD) REFERENCES lookup_licensing_authority(CD) ON DELETE RESTRICT,
                FOREIGN KEY (LIC_AUTHCHANGECD) REFERENCES lookup_licensing_authority_change_reason(CD) ON DELETE RESTRICT,
                FOREIGN KEY (COMBPRODCD) REFERENCES lookup_combination_product_indicator(CD) ON DELETE RESTRICT,
                FOREIGN KEY (FLAVOURCD) REFERENCES lookup_flavour(CD) ON DELETE RESTRICT,
                FOREIGN KEY (AVAIL_RESTRICTCD) REFERENCES lookup_availability_restriction(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE amp_ingredient (
                APID      INTEGER NOT NULL,
                ISID      INTEGER NOT NULL,
                STRNTH    REAL,
                UOMCD     INTEGER,

                PRIMARY KEY (APID, ISID),
                FOREIGN KEY (APID) REFERENCES amp(APID) ON DELETE CASCADE,
                FOREIGN KEY (ISID) REFERENCES ingredient(ISID) ON DELETE RESTRICT,
                FOREIGN KEY (UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE amp_licensed_route (
                APID      INTEGER NOT NULL,
                ROUTECD   INTEGER NOT NULL,

                PRIMARY KEY (APID, ROUTECD),
                FOREIGN KEY (APID) REFERENCES amp(APID) ON DELETE CASCADE,
                FOREIGN KEY (ROUTECD) REFERENCES lookup_route(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE amp_information (
                APID            INTEGER PRIMARY KEY NOT NULL,
                SZ_WEIGHT       TEXT,
                COLOURCD        INTEGER,
                PROD_ORDER_NO   TEXT,

                FOREIGN KEY (APID) REFERENCES amp(APID) ON DELETE CASCADE,
                FOREIGN KEY (COLOURCD) REFERENCES lookup_colour(CD) ON DELETE RESTRICT
            )
            """
        ]
        
        for statement in amp_tables:
            conn.execute(statement)
        
        # Create VMPP tables
        print("Creating VMPP tables...")
        vmpp_tables = [
            """
            CREATE TABLE vmpp (
                VPPID        INTEGER PRIMARY KEY NOT NULL,
                INVALID      INTEGER,
                NM           TEXT NOT NULL,
                VPID         INTEGER NOT NULL,
                QTYVAL       REAL NOT NULL,
                QTY_UOMCD    INTEGER NOT NULL,
                COMBPACKCD   INTEGER,

                FOREIGN KEY (VPID) REFERENCES vmp(VPID) ON DELETE RESTRICT,
                FOREIGN KEY (QTY_UOMCD) REFERENCES lookup_unit_of_measure(CD) ON DELETE RESTRICT,
                FOREIGN KEY (COMBPACKCD) REFERENCES lookup_combination_pack_indicator(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmpp_drug_tariff_info (
                VPPID       INTEGER NOT NULL,
                PAY_CATCD   INTEGER NOT NULL,
                PRICE       INTEGER,
                DT          TEXT,
                PREVPRICE   INTEGER,

                PRIMARY KEY (VPPID, PAY_CATCD),
                FOREIGN KEY (VPPID) REFERENCES vmpp(VPPID) ON DELETE CASCADE,
                FOREIGN KEY (PAY_CATCD) REFERENCES lookup_drug_tariff_payment_category(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE vmpp_combination_content (
                PRNTVPPID   INTEGER NOT NULL,
                CHLDVPPID   INTEGER NOT NULL,

                PRIMARY KEY (PRNTVPPID, CHLDVPPID),
                FOREIGN KEY (PRNTVPPID) REFERENCES vmpp(VPPID) ON DELETE CASCADE,
                FOREIGN KEY (CHLDVPPID) REFERENCES vmpp(VPPID) ON DELETE CASCADE
            )
            """
        ]
        
        for statement in vmpp_tables:
            conn.execute(statement)
        
        # Create AMPP tables
        print("Creating AMPP tables...")
        ampp_tables = [
            """
            CREATE TABLE ampp (
                APPID         INTEGER PRIMARY KEY NOT NULL,
                INVALID       INTEGER,
                NM            TEXT NOT NULL,
                ABBREVNM      TEXT,
                VPPID         INTEGER NOT NULL,
                APID          INTEGER NOT NULL,
                COMBPACKCD    INTEGER,
                LEGAL_CATCD   INTEGER NOT NULL,
                SUBP          TEXT,
                DISCCD        INTEGER,
                DISCDT        TEXT,

                FOREIGN KEY (VPPID) REFERENCES vmpp(VPPID) ON DELETE RESTRICT,
                FOREIGN KEY (APID) REFERENCES amp(APID) ON DELETE RESTRICT,
                FOREIGN KEY (COMBPACKCD) REFERENCES lookup_combination_pack_indicator(CD) ON DELETE RESTRICT,
                FOREIGN KEY (LEGAL_CATCD) REFERENCES lookup_legal_category(CD) ON DELETE RESTRICT,
                FOREIGN KEY (DISCCD) REFERENCES lookup_discontinued_indicator(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE ampp_appliance_pack_info (
                APPID              INTEGER PRIMARY KEY NOT NULL,
                REIMB_STATCD       INTEGER NOT NULL,
                REIMB_STATDT       TEXT,
                REIMB_STATPREVCD   INTEGER,
                PACK_ORDER_NO      TEXT,

                FOREIGN KEY (APPID) REFERENCES ampp(APPID) ON DELETE CASCADE,
                FOREIGN KEY (REIMB_STATCD) REFERENCES lookup_reimbursement_status(CD) ON DELETE RESTRICT,
                FOREIGN KEY (REIMB_STATPREVCD) REFERENCES lookup_reimbursement_status(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE ampp_prescribing_info (
                APPID       INTEGER PRIMARY KEY NOT NULL,
                SCHED_2     INTEGER,
                ACBS        INTEGER,
                PADM        INTEGER,
                FP10_MDA    INTEGER,
                SCHED_1     INTEGER,
                HOSP        INTEGER,
                NURSE_F     INTEGER,
                ENURSE_F    INTEGER,
                DENT_F      INTEGER,

                FOREIGN KEY (APPID) REFERENCES ampp(APPID) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE ampp_price_info (
                APPID           INTEGER PRIMARY KEY NOT NULL,
                PRICE           INTEGER,
                PRICEDT         TEXT,
                PRICE_PREV      INTEGER,
                PRICE_BASISCD   INTEGER NOT NULL,

                FOREIGN KEY (APPID) REFERENCES ampp(APPID) ON DELETE CASCADE,
                FOREIGN KEY (PRICE_BASISCD) REFERENCES lookup_price_basis(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE ampp_reimbursement_info (
                APPID         INTEGER PRIMARY KEY NOT NULL,
                PX_CHRGS      INTEGER,
                DISP_FEES     INTEGER,
                BB            INTEGER,
                LTD_STAB      INTEGER,
                CAL_PACK      INTEGER,
                SPEC_CONTCD   INTEGER,
                DND           INTEGER,
                FP34D         INTEGER,

                FOREIGN KEY (APPID) REFERENCES ampp(APPID) ON DELETE CASCADE,
                FOREIGN KEY (SPEC_CONTCD) REFERENCES lookup_special_container(CD) ON DELETE RESTRICT,
                FOREIGN KEY (DND) REFERENCES lookup_dnd(CD) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE ampp_combination_content (
                PRNTAPPID   INTEGER NOT NULL,
                CHLDAPPID   INTEGER NOT NULL,

                PRIMARY KEY (PRNTAPPID, CHLDAPPID),
                FOREIGN KEY (PRNTAPPID) REFERENCES ampp(APPID) ON DELETE CASCADE,
                FOREIGN KEY (CHLDAPPID) REFERENCES ampp(APPID) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE ampp_gtin (
                AMPPID    INTEGER NOT NULL,
                GTIN      TEXT NOT NULL,
                STARTDT   TEXT NOT NULL,
                ENDDT     TEXT,

                PRIMARY KEY (AMPPID, GTIN, STARTDT),
                FOREIGN KEY (AMPPID) REFERENCES ampp(APPID) ON DELETE CASCADE
            )
            """
        ]
        
        for statement in ampp_tables:
            conn.execute(statement)
        
        # Create indexes (basic ones for now)
        print("Creating indexes...")
        indexes = [
            "CREATE INDEX idx_vmp_vtm_id ON vmp(VTMID)",
            "CREATE INDEX idx_amp_vpid ON amp(VPID)",
            "CREATE INDEX idx_vmpp_vpid ON vmpp(VPID)",
            "CREATE INDEX idx_ampp_vppid ON ampp(VPPID)",
            "CREATE INDEX idx_ampp_apid ON ampp(APID)",
        ]
        
        for index in indexes:
            conn.execute(index)
        
        # Commit and close
        conn.commit()
    
    print(f"Database created successfully at {db_path}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 