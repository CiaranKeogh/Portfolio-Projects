#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Database Script for Drug Tariff Master

This script creates the SQLite database schema for storing dm+d (Dictionary of Medicines and Devices) data.
It defines tables according to the dm+d data model, including all relationships between tables.

Usage:
    python -m drug_tariff_master.setup_database

"""

import os
import sqlite3
import logging
from pathlib import Path

from drug_tariff_master.config import DATA_DIR, LOGS_DIR
from drug_tariff_master.utils import setup_logging

# Setup logging
logger = logging.getLogger(__name__)
setup_logging(LOGS_DIR / "database.log")


class DatabaseSetup:
    """Class to handle database setup for the dm+d data."""

    def __init__(self, db_path=None):
        """Initialize with the path to the SQLite database."""
        self.db_path = db_path or DATA_DIR / "dmd.db"
        self._ensure_directory()
        print(f"Database path: {self.db_path}")
        print(f"Does parent directory exist? {self.db_path.parent.exists()}")

    def _ensure_directory(self):
        """Ensure the database directory exists."""
        print(f"Creating directory: {self.db_path.parent}")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {self.db_path.parent.exists()}")

    def setup_database(self):
        """
        Set up the SQLite database with all required tables.
        This method drops existing tables and creates new ones.
        """
        print(f"Setting up database at {self.db_path}")
        logger.info(f"Setting up database at {self.db_path}")
        
        try:
            print("Connecting to database...")
            with sqlite3.connect(self.db_path) as conn:
                print("Connected to database")
                # Enable foreign keys
                conn.execute("PRAGMA foreign_keys = ON")
                
                # Drop existing tables
                print("Dropping existing tables...")
                self._drop_tables(conn)
                
                # Create tables
                print("Creating lookup tables...")
                self._create_lookup_tables(conn)
                print("Creating ingredient tables...")
                self._create_ingredient_tables(conn)
                print("Creating VTM tables...")
                self._create_vtm_tables(conn)
                print("Creating VMP tables...")
                self._create_vmp_tables(conn)
                print("Creating AMP tables...")
                self._create_amp_tables(conn)
                print("Creating VMPP tables...")
                self._create_vmpp_tables(conn)
                print("Creating AMPP tables...")
                self._create_ampp_tables(conn)
                
                # Create indexes
                print("Creating indexes...")
                self._create_indexes(conn)
                
                print("Database setup completed successfully")
                logger.info("Database setup completed successfully")
                
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            logger.error(f"SQLite error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}")
            raise

    def _drop_tables(self, conn):
        """Drop existing tables in the reverse order of dependencies."""
        logger.info("Dropping existing tables")
        
        cursor = conn.cursor()
        
        # AMPP tables
        tables_to_drop = [
            # AMPP detail/linking tables
            "ampp_gtin",
            "ampp_combination_content",
            "ampp_reimbursement_info",
            "ampp_price_info",
            "ampp_prescribing_info",
            "ampp_appliance_pack_info",
            "ampp",
            
            # VMPP detail/linking tables
            "vmpp_combination_content",
            "vmpp_drug_tariff_info",
            "vmpp",
            
            # AMP detail/linking tables
            "amp_information",
            "amp_licensed_route",
            "amp_ingredient",
            "amp",
            
            # VMP detail/linking tables
            "vmp_control_drug_info",
            "vmp_drug_route",
            "vmp_drug_form",
            "vmp_ontology_form_route",
            "vmp_ingredient",
            "vmp",
            
            # VTM tables
            "vtm",
            
            # Ingredient tables
            "ingredient",
            
            # Lookup tables
            "lookup_licensing_authority_change_reason",
            "lookup_availability_restriction",
            "lookup_legal_category",
            "lookup_price_basis",
            "lookup_df_indicator",
            "lookup_discontinued_indicator",
            "lookup_virtual_product_non_avail",
            "lookup_dnd",
            "lookup_special_container",
            "lookup_reimbursement_status",
            "lookup_basis_of_strength",
            "lookup_colour",
            "lookup_flavour",
            "lookup_supplier",
            "lookup_drug_tariff_payment_category",
            "lookup_route",
            "lookup_ontology_form_route",
            "lookup_form",
            "lookup_unit_of_measure",
            "lookup_licensing_authority",
            "lookup_control_drug_category",
            "lookup_virtual_product_pres_status",
            "lookup_name_change_reason",
            "lookup_basis_of_name",
            "lookup_combination_product_indicator",
            "lookup_combination_pack_indicator"
        ]
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                logger.debug(f"Dropped table {table}")
            except sqlite3.Error as e:
                logger.error(f"Error dropping table {table}: {e}")
        
        conn.commit()
        print("Tables dropped successfully")

    def _create_lookup_tables(self, conn):
        """Create all lookup tables."""
        logger.info("Creating lookup tables")
        
        cursor = conn.cursor()
        
        # Lookup tables with no dependencies
        statements = [
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
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                logger.error(f"Error creating lookup table: {e}")
                logger.error(f"Statement: {statement}")
                raise
        
        conn.commit()

    def _create_ingredient_tables(self, conn):
        """Create the ingredient table."""
        logger.info("Creating ingredient table")
        
        cursor = conn.cursor()
        
        statement = """
        CREATE TABLE ingredient (
            ISID      INTEGER PRIMARY KEY NOT NULL,
            ISIDDT    TEXT,
            ISIDPREV  INTEGER,
            INVALID   INTEGER,
            NM        TEXT NOT NULL
        )
        """
        
        try:
            cursor.execute(statement)
        except sqlite3.Error as e:
            logger.error(f"Error creating ingredient table: {e}")
            raise
        
        conn.commit()

    def _create_vtm_tables(self, conn):
        """Create the vtm table."""
        logger.info("Creating VTM table")
        
        cursor = conn.cursor()
        
        statement = """
        CREATE TABLE vtm (
            VTMID       INTEGER PRIMARY KEY NOT NULL,
            INVALID     INTEGER,
            NM          TEXT NOT NULL,
            ABBREVNM    TEXT,
            VTMIDPREV   TEXT,
            VTMIDDT     TEXT
        )
        """
        
        try:
            cursor.execute(statement)
        except sqlite3.Error as e:
            logger.error(f"Error creating VTM table: {e}")
            raise
        
        conn.commit()

    def _create_vmp_tables(self, conn):
        """Create the VMP and related tables."""
        logger.info("Creating VMP tables")
        
        cursor = conn.cursor()
        
        # Core VMP table
        statements = [
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
            
            # VMP linking tables
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
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                logger.error(f"Error creating VMP tables: {e}")
                logger.error(f"Statement: {statement}")
                raise
        
        conn.commit()

    def _create_amp_tables(self, conn):
        """Create the AMP and related tables."""
        logger.info("Creating AMP tables")
        
        cursor = conn.cursor()
        
        statements = [
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
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                logger.error(f"Error creating AMP tables: {e}")
                logger.error(f"Statement: {statement}")
                raise
        
        conn.commit()

    def _create_vmpp_tables(self, conn):
        """Create the VMPP and related tables."""
        logger.info("Creating VMPP tables")
        
        cursor = conn.cursor()
        
        statements = [
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
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                logger.error(f"Error creating VMPP tables: {e}")
                logger.error(f"Statement: {statement}")
                raise
        
        conn.commit()

    def _create_ampp_tables(self, conn):
        """Create the AMPP and related tables."""
        logger.info("Creating AMPP tables")
        
        cursor = conn.cursor()
        
        statements = [
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
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                logger.error(f"Error creating AMPP tables: {e}")
                logger.error(f"Statement: {statement}")
                raise
        
        conn.commit()

    def _create_indexes(self, conn):
        """Create indexes for foreign keys and commonly queried fields."""
        logger.info("Creating indexes")
        
        cursor = conn.cursor()
        
        indexes = [
            # VMP Indexes
            "CREATE INDEX idx_vmp_vtm_id ON vmp(VTMID)",
            "CREATE INDEX idx_vmp_basiscd ON vmp(BASISCD)",
            "CREATE INDEX idx_vmp_basis_prevcd ON vmp(BASIS_PREVCD)",
            "CREATE INDEX idx_vmp_nmchangecd ON vmp(NMCHANGECD)",
            "CREATE INDEX idx_vmp_combprodcd ON vmp(COMBPRODCD)",
            "CREATE INDEX idx_vmp_pres_statcd ON vmp(PRES_STATCD)",
            "CREATE INDEX idx_vmp_non_availcd ON vmp(NON_AVAILCD)",
            "CREATE INDEX idx_vmp_df_indcd ON vmp(DF_INDCD)",
            "CREATE INDEX idx_vmp_udfs_uomcd ON vmp(UDFS_UOMCD)",
            "CREATE INDEX idx_vmp_unit_dose_uomcd ON vmp(UNIT_DOSE_UOMCD)",
            "CREATE INDEX idx_vmp_nm ON vmp(NM)",
            "CREATE INDEX idx_vmp_abbrevnm ON vmp(ABBREVNM)",

            # VMP Linking Tables Indexes
            "CREATE INDEX idx_vmp_ingredient_isid ON vmp_ingredient(ISID)",
            "CREATE INDEX idx_vmp_ingredient_basis_strntcd ON vmp_ingredient(BASIS_STRNTCD)",
            "CREATE INDEX idx_vmp_ingredient_bs_subid ON vmp_ingredient(BS_SUBID)",
            "CREATE INDEX idx_vmp_ingredient_strnt_nmrtr_uomcd ON vmp_ingredient(STRNT_NMRTR_UOMCD)",
            "CREATE INDEX idx_vmp_ingredient_strnt_dnmtr_uomcd ON vmp_ingredient(STRNT_DNMTR_UOMCD)",
            "CREATE INDEX idx_vmp_ont_form_route_formcd ON vmp_ontology_form_route(FORMCD)",
            "CREATE INDEX idx_vmp_drug_form_formcd ON vmp_drug_form(FORMCD)",
            "CREATE INDEX idx_vmp_drug_route_routecd ON vmp_drug_route(ROUTECD)",
            "CREATE INDEX idx_vmp_control_drug_info_catcd ON vmp_control_drug_info(CATCD)",
            "CREATE INDEX idx_vmp_control_drug_info_cat_prevcd ON vmp_control_drug_info(CAT_PREVCD)",

            # AMP Indexes
            "CREATE INDEX idx_amp_vpid ON amp(VPID)",
            "CREATE INDEX idx_amp_suppcd ON amp(SUPPCD)",
            "CREATE INDEX idx_amp_lic_authcd ON amp(LIC_AUTHCD)",
            "CREATE INDEX idx_amp_lic_auth_prevcd ON amp(LIC_AUTH_PREVCD)",
            "CREATE INDEX idx_amp_lic_authchangecd ON amp(LIC_AUTHCHANGECD)",
            "CREATE INDEX idx_amp_combprodcd ON amp(COMBPRODCD)",
            "CREATE INDEX idx_amp_flavourcd ON amp(FLAVOURCD)",
            "CREATE INDEX idx_amp_avail_restrictcd ON amp(AVAIL_RESTRICTCD)",
            "CREATE INDEX idx_amp_nm ON amp(NM)",
            "CREATE INDEX idx_amp_abbrevnm ON amp(ABBREVNM)",
            "CREATE INDEX idx_amp_desc ON amp(DESC)",

            # AMP Linking/Detail Tables Indexes
            "CREATE INDEX idx_amp_ingredient_isid ON amp_ingredient(ISID)",
            "CREATE INDEX idx_amp_ingredient_uomcd ON amp_ingredient(UOMCD)",
            "CREATE INDEX idx_amp_licensed_route_routecd ON amp_licensed_route(ROUTECD)",
            "CREATE INDEX idx_amp_information_colourcd ON amp_information(COLOURCD)",

            # VMPP Indexes
            "CREATE INDEX idx_vmpp_vpid ON vmpp(VPID)",
            "CREATE INDEX idx_vmpp_qty_uomcd ON vmpp(QTY_UOMCD)",
            "CREATE INDEX idx_vmpp_combpackcd ON vmpp(COMBPACKCD)",
            "CREATE INDEX idx_vmpp_nm ON vmpp(NM)",

            # VMPP Linking Tables Indexes
            "CREATE INDEX idx_vmpp_drug_tariff_info_pay_catcd ON vmpp_drug_tariff_info(PAY_CATCD)",
            "CREATE INDEX idx_vmpp_comb_content_chldvppid ON vmpp_combination_content(CHLDVPPID)",

            # AMPP Indexes
            "CREATE INDEX idx_ampp_vppid ON ampp(VPPID)",
            "CREATE INDEX idx_ampp_apid ON ampp(APID)",
            "CREATE INDEX idx_ampp_combpackcd ON ampp(COMBPACKCD)",
            "CREATE INDEX idx_ampp_legal_catcd ON ampp(LEGAL_CATCD)",
            "CREATE INDEX idx_ampp_disccd ON ampp(DISCCD)",
            "CREATE INDEX idx_ampp_nm ON ampp(NM)",
            "CREATE INDEX idx_ampp_abbrevnm ON ampp(ABBREVNM)",

            # AMPP Detail/Linking Tables Indexes
            "CREATE INDEX idx_ampp_appl_pack_info_reimb_statcd ON ampp_appliance_pack_info(REIMB_STATCD)",
            "CREATE INDEX idx_ampp_appl_pack_info_reimb_statprevcd ON ampp_appliance_pack_info(REIMB_STATPREVCD)",
            "CREATE INDEX idx_ampp_price_info_price_basiscd ON ampp_price_info(PRICE_BASISCD)",
            "CREATE INDEX idx_ampp_reimb_info_spec_contcd ON ampp_reimbursement_info(SPEC_CONTCD)",
            "CREATE INDEX idx_ampp_reimb_info_dnd ON ampp_reimbursement_info(DND)",
            "CREATE INDEX idx_ampp_comb_content_chldappid ON ampp_combination_content(CHLDAPPID)",
            "CREATE INDEX idx_ampp_gtin_gtin ON ampp_gtin(GTIN)",
            "CREATE INDEX idx_ampp_gtin_startdt ON ampp_gtin(STARTDT)",
            "CREATE INDEX idx_ampp_gtin_enddt ON ampp_gtin(ENDDT)",

            # Lookup Descriptions Indexes
            "CREATE INDEX idx_lookup_supplier_desc ON lookup_supplier(DESC)",
            "CREATE INDEX idx_lookup_form_desc ON lookup_form(DESC)",
            "CREATE INDEX idx_lookup_route_desc ON lookup_route(DESC)",
            "CREATE INDEX idx_ingredient_nm ON ingredient(NM)",
        ]
        
        for index in indexes:
            try:
                cursor.execute(index)
            except sqlite3.Error as e:
                logger.error(f"Error creating index: {e}")
                logger.error(f"Statement: {index}")
        
        conn.commit()


def main():
    """Main function to set up the database."""
    try:
        print("Starting database setup")
        db_setup = DatabaseSetup()
        db_setup.setup_database()
        print("Database setup completed successfully.")
        
        # Verify database file exists
        if os.path.exists(db_setup.db_path):
            print(f"Database file created successfully at {db_setup.db_path}")
            print(f"File size: {os.path.getsize(db_setup.db_path)} bytes")
        else:
            print(f"Database file was not created at {db_setup.db_path}")
        
        return 0
    except Exception as e:
        print(f"Error setting up database: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 