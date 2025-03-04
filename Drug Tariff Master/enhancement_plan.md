# Drug Tariff Master Enhancement Plan

After examining the Drug Tariff Master application and comparing it with the NHS Dictionary of Medicines and Devices (dm+d) Technical Specification, we've identified several areas that need improvement to provide a more complete and accurate representation of the medicinal product data.

## Current Limitations

1. **Missing Lookup Data**: The application doesn't process the LOOKUP XML file, which contains human-readable descriptions for numerous coded values used throughout the dataset.

2. **Incomplete Entity Data**: The current database schema captures only minimal attributes for each entity, omitting many fields that could provide valuable context.

3. **Missing Relationships**: Important relationships such as VMP-ingredient, AMP-ingredient, and combination pack relationships are not currently captured.

4. **Missing Supplementary Files**: The specification mentions several supplementary files (BNF/ATC mappings, historic codes, VTM ingredient file) that aren't currently processed.

5. **Missing VTM Data**: The Virtual Therapeutic Moiety (VTM) data is not currently imported or used.

## Enhancement Plan

### 1. Update Database Schema

#### 1.1 Add Lookup Tables

Create tables to store lookup data for code-based values:

```sql
CREATE TABLE IF NOT EXISTS lookup_control_drug_category (
    CD TEXT PRIMARY KEY,
    DESC TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lookup_legal_category (
    CD TEXT PRIMARY KEY,
    DESC TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lookup_form (
    CD INTEGER PRIMARY KEY,
    DESC TEXT NOT NULL,
    CDDT DATE,
    CDPREV INTEGER
);

CREATE TABLE IF NOT EXISTS lookup_route (
    CD INTEGER PRIMARY KEY,
    DESC TEXT NOT NULL,
    CDDT DATE,
    CDPREV INTEGER
);

CREATE TABLE IF NOT EXISTS lookup_unit_of_measure (
    CD INTEGER PRIMARY KEY,
    DESC TEXT NOT NULL,
    CDDT DATE,
    CDPREV INTEGER
);

CREATE TABLE IF NOT EXISTS lookup_supplier (
    CD INTEGER PRIMARY KEY,
    DESC TEXT NOT NULL,
    CDDT DATE,
    CDPREV INTEGER,
    INVALID INTEGER
);

-- Add more lookup tables as needed
```

#### 1.2 Add VTM Table

```sql
CREATE TABLE IF NOT EXISTS vtm (
    VTMID INTEGER PRIMARY KEY,
    NM TEXT NOT NULL,
    ABBREVNM TEXT,
    VTMIDPREV INTEGER,
    VTMIDDT DATE,
    INVALID INTEGER
);
```

#### 1.3 Enhance Existing Tables

Enhance the VMP table with additional fields:
```sql
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
    FOREIGN KEY (VTMID) REFERENCES vtm(VTMID)
);
```

Enhance the AMP table with additional fields:
```sql
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
);
```

Similar enhancements for VMPP and AMPP tables.

#### 1.4 Add Relationship Tables

Add tables for VMP to ingredient relationships:
```sql
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
);
```

Add tables for VMP to form relationships:
```sql
CREATE TABLE IF NOT EXISTS vmp_form (
    VPID INTEGER NOT NULL,
    FORMCD INTEGER NOT NULL,
    PRIMARY KEY (VPID, FORMCD),
    FOREIGN KEY (VPID) REFERENCES vmp(VPID),
    FOREIGN KEY (FORMCD) REFERENCES lookup_form(CD)
);
```

Add tables for VMP to route relationships:
```sql
CREATE TABLE IF NOT EXISTS vmp_route (
    VPID INTEGER NOT NULL,
    ROUTECD INTEGER NOT NULL,
    PRIMARY KEY (VPID, ROUTECD),
    FOREIGN KEY (VPID) REFERENCES vmp(VPID),
    FOREIGN KEY (ROUTECD) REFERENCES lookup_route(CD)
);
```

Add similar relationship tables for AMP ingredients, routes, etc.

#### 1.5 Add Ingredient Table

```sql
CREATE TABLE IF NOT EXISTS ingredient (
    ISID INTEGER PRIMARY KEY,
    ISIDDT DATE,
    ISIDPREV INTEGER,
    NM TEXT NOT NULL,
    INVALID INTEGER
);
```

### 2. Update Parser Code

#### 2.1 Add Parser for Lookup Data

```python
def parse_lookup_data(xml_path):
    """
    Parse lookup data from the XML file.
    
    Args:
        xml_path (Path): Path to the lookup XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing lookup data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # Process each lookup category
        lookup_categories = [
            "CONTROL_DRUG_CATEGORY",
            "LEGAL_CATEGORY",
            "FORM",
            "ROUTE",
            "UNIT_OF_MEASURE",
            "SUPPLIER",
            # Add more as needed
        ]
        
        for category in lookup_categories:
            logger.info(f"Processing lookup category: {category}")
            
            # Find all info elements for this category
            elements = root.xpath(f"//{category}/INFO")
            
            if not elements:
                logger.warning(f"No elements found for lookup category: {category}")
                continue
                
            # Prepare table name
            table_name = f"lookup_{category.lower()}"
            
            # Extract and insert data
            data_list = []
            
            for elem in elements:
                cd = elem.find("CD").text
                desc = elem.find("DESC").text
                
                record = {
                    "CD": cd,
                    "DESC": desc
                }
                
                # Handle additional fields for some categories
                cddt_elem = elem.find("CDDT")
                if cddt_elem is not None:
                    record["CDDT"] = cddt_elem.text
                    
                cdprev_elem = elem.find("CDPREV")
                if cdprev_elem is not None:
                    record["CDPREV"] = cdprev_elem.text
                    
                invalid_elem = elem.find("INVALID")
                if invalid_elem is not None:
                    record["INVALID"] = invalid_elem.text
                
                data_list.append(record)
                
                # Insert in chunks
                if len(data_list) >= config.CHUNK_SIZE:
                    database.insert_data(table_name, data_list)
                    data_list = []
            
            # Insert any remaining data
            if data_list:
                database.insert_data(table_name, data_list)
                
        logger.info(f"Lookup parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing lookup data: {e}")
        return False
```

#### 2.2 Add Parser for VTM Data

```python
def parse_vtm_data(xml_path):
    """
    Parse VTM data from the XML file.
    
    Args:
        xml_path (Path): Path to the VTM XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing VTM data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        vtm_data = []
        vtm_elements = root.xpath("//VTM")
        
        for i in range(0, len(vtm_elements), config.CHUNK_SIZE):
            chunk = vtm_elements[i:i+config.CHUNK_SIZE]
            
            for vtm_elem in chunk:
                vtmid = vtm_elem.find("VTMID").text
                nm = vtm_elem.find("NM").text
                
                vtm_record = {
                    "VTMID": int(vtmid),
                    "NM": nm
                }
                
                # Add optional fields if present
                abbrevnm_elem = vtm_elem.find("ABBREVNM")
                if abbrevnm_elem is not None:
                    vtm_record["ABBREVNM"] = abbrevnm_elem.text
                    
                vtmidprev_elem = vtm_elem.find("VTMIDPREV")
                if vtmidprev_elem is not None:
                    vtm_record["VTMIDPREV"] = int(vtmidprev_elem.text)
                    
                vtmiddt_elem = vtm_elem.find("VTMIDDT")
                if vtmiddt_elem is not None:
                    vtm_record["VTMIDDT"] = vtmiddt_elem.text
                    
                invalid_elem = vtm_elem.find("INVALID")
                if invalid_elem is not None:
                    vtm_record["INVALID"] = int(invalid_elem.text)
                
                vtm_data.append(vtm_record)
                
            # Insert this chunk
            database.insert_data("vtm", vtm_data)
            vtm_data = []
            
        logger.info(f"VTM parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing VTM data: {e}")
        return False
```

#### 2.3 Enhance Existing Parsers

Update the existing parsers (`parse_vmp_data`, `parse_amp_data`, etc.) to extract and store the additional fields and relationships as outlined in the database schema changes.

#### 2.4 Add Parsers for Relationship Data

Create new parser functions to extract and store relationship data:

```python
def parse_vmp_ingredient_data(xml_path):
    """
    Parse VMP ingredient data from the XML file.
    
    Args:
        xml_path (Path): Path to the VMP XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing VMP ingredient data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # Extract VPI elements
        vpi_elements = root.xpath("//VIRTUAL_PRODUCT_INGREDIENT/VPI")
        
        vpi_data = []
        for i in range(0, len(vpi_elements), config.CHUNK_SIZE):
            chunk = vpi_elements[i:i+config.CHUNK_SIZE]
            
            for vpi_elem in chunk:
                vpid = vpi_elem.find("VPID").text
                isid = vpi_elem.find("ISID").text
                
                vpi_record = {
                    "VPID": int(vpid),
                    "ISID": int(isid)
                }
                
                # Add optional fields if present
                basis_strntcd_elem = vpi_elem.find("BASIS_STRNTCD")
                if basis_strntcd_elem is not None:
                    vpi_record["BASIS_STRNTCD"] = basis_strntcd_elem.text
                
                # Add more optional fields similarly
                
                vpi_data.append(vpi_record)
            
            # Insert this chunk
            database.insert_data("vmp_ingredient", vpi_data)
            vpi_data = []
            
        logger.info(f"VMP ingredient parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing VMP ingredient data: {e}")
        return False
```

Create similar functions for other relationships.

#### 2.5 Add Parsers for Supplementary Files

Add parser functions for BNF/ATC mappings, historic codes, and VTM ingredient files.

### 3. Update Config and Other Supporting Code

Update `config.py` to include file patterns for the additional XML files:

```python
FILE_PATTERNS = {
    'vtm': {'pattern': 'f_vtm2_*.xml', 'schema': SCHEMAS_DIR / 'vtm_v2_3.xsd'},
    'vmp': {'pattern': 'f_vmp2_*.xml', 'schema': SCHEMAS_DIR / 'vmp_v2_3.xsd'},
    'vmpp': {'pattern': 'f_vmpp2_*.xml', 'schema': SCHEMAS_DIR / 'vmpp_v2_3.xsd'},
    'amp': {'pattern': 'f_amp2_*.xml', 'schema': SCHEMAS_DIR / 'amp_v2_3.xsd'},
    'ampp': {'pattern': 'f_ampp2_*.xml', 'schema': SCHEMAS_DIR / 'ampp_v2_3.xsd'},
    'gtin': {'pattern': 'f_gtin2_*.xml', 'schema': SCHEMAS_DIR / 'gtin_v2_0.xsd'},
    'lookup': {'pattern': 'f_lookup2_*.xml', 'schema': SCHEMAS_DIR / 'lookup_v2_3.xsd'},
    'ingredient': {'pattern': 'f_ingredient*.xml', 'schema': SCHEMAS_DIR / 'ingredient_v2_3.xsd'},
    'bnf': {'pattern': 'f_bnf_*.xml', 'schema': SCHEMAS_DIR / 'bnf_v2_3.xsd'},
    'hist': {'pattern': 'f_history_*.xml', 'schema': SCHEMAS_DIR / 'history_v2_3.xsd'},
    'vtming': {'pattern': 'f_vtming_*.xml', 'schema': SCHEMAS_DIR / 'vtming_v2_3.xsd'},
}
```

Update `process_all_files()` function to include processing of the new files in the correct order.

### 4. Update Search Functionality

Enhance the search functionality to include lookup data in search results:

```python
def enhance_search_results(search_results):
    """
    Enhance search results with lookup data.
    
    Args:
        search_results (list): The search results to enhance.
        
    Returns:
        list: Enhanced search results.
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    for result in search_results:
        # Add human-readable form descriptions
        if 'FORMCD' in result and result['FORMCD']:
            cursor.execute(
                "SELECT DESC FROM lookup_form WHERE CD = ?", 
                (result['FORMCD'],)
            )
            form_desc = cursor.fetchone()
            if form_desc:
                result['FORM_DESC'] = form_desc['DESC']
                
        # Add human-readable route descriptions
        if 'ROUTECD' in result and result['ROUTECD']:
            cursor.execute(
                "SELECT DESC FROM lookup_route WHERE CD = ?", 
                (result['ROUTECD'],)
            )
            route_desc = cursor.fetchone()
            if route_desc:
                result['ROUTE_DESC'] = route_desc['DESC']
                
        # Add human-readable supplier descriptions
        if 'SUPPCD' in result and result['SUPPCD']:
            cursor.execute(
                "SELECT DESC FROM lookup_supplier WHERE CD = ?", 
                (result['SUPPCD'],)
            )
            supp_desc = cursor.fetchone()
            if supp_desc:
                result['SUPPLIER_DESC'] = supp_desc['DESC']
                
        # Add more lookup-based enhancements as needed
                
    conn.close()
    return search_results
```

### 5. Update Web Interface

Update the web interface to display the additional data:

1. Add new columns to search results table for human-readable descriptions
2. Add tabs for viewing relationship data (ingredients, routes, etc.)
3. Add visualization of product hierarchies (VTM -> VMP -> AMP -> AMPP)

## Implementation Plan

1. **Phase 1: Schema Updates**
   - Update database schema to include lookup tables and enhanced entity tables
   - Add indexes for performance

2. **Phase 2: Parser Updates**
   - Add parsers for lookup data, VTM, and relationship data
   - Enhance existing parsers to extract additional fields

3. **Phase 3: Search and API Updates**
   - Update search functionality to include lookup data
   - Enhance API to expose the additional data and relationships

4. **Phase 4: Web Interface Updates**
   - Update web interface to display the additional data
   - Add visualizations and navigation for relationships

## Notes for Implementation

- The `LOOKUP` XML file is structurally complex with many nested categories
- Care must be taken to preserve the correct ordering when loading data to maintain foreign key relationships
- Some lookup tables (e.g., FORM, ROUTE, SUPPLIER) have historic code tracking, requiring special handling
- The enhanced data model will significantly increase the size of the database but provide much richer information 