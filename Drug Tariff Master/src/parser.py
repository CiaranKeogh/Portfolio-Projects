"""
Parser module for Drug Tariff Master.
This module handles XML parsing, validation against XSD schemas,
and extraction of data for database insertion.
"""
import os
import logging
import xmlschema
from pathlib import Path
from lxml import etree
from datetime import datetime

import config
import database

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('parser')


def validate_xml_against_xsd(xml_path, xsd_path):
    """
    Validate an XML file against an XSD schema.
    
    Args:
        xml_path (Path): Path to the XML file.
        xsd_path (Path): Path to the XSD schema.
        
    Returns:
        bool: True if validation passed, False otherwise.
    """
    logger.info(f"Validating {xml_path} against {xsd_path}")
    
    try:
        schema = xmlschema.XMLSchema(str(xsd_path))
        is_valid = schema.is_valid(str(xml_path))
        
        if is_valid:
            logger.info(f"Validation successful for {xml_path}")
        else:
            logger.error(f"Validation failed for {xml_path}")
            
        return is_valid
        
    except Exception as e:
        logger.error(f"Error during XML validation: {e}")
        return False


def parse_vmp_data(xml_path):
    """
    Parse VMP data from the XML file.
    
    Args:
        xml_path (Path): Path to the VMP XML file.
        
    Returns:
        list: List of dictionaries containing VMP data.
    """
    logger.info(f"Parsing VMP data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # VMP data list
        vmp_data = []
        
        # Find all VMP elements in chunks of CHUNK_SIZE
        vmp_elements = root.xpath("//VMPS/VMP")
        
        for i in range(0, len(vmp_elements), config.CHUNK_SIZE):
            chunk = vmp_elements[i:i+config.CHUNK_SIZE]
            
            for vmp_elem in chunk:
                vpid = vmp_elem.find("VPID").text
                nm = vmp_elem.find("NM").text
                
                vmp_data.append({
                    "VPID": int(vpid),
                    "NM": nm
                })
                
            # Insert this chunk into the database
            database.insert_data("vmp", vmp_data)
            vmp_data = []  # Clear for next chunk
            
        logger.info(f"VMP parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing VMP data: {e}")
        return False


def parse_vmpp_data(xml_path):
    """
    Parse VMPP data from the XML file.
    
    Args:
        xml_path (Path): Path to the VMPP XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing VMPP data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # VMPP data list
        vmpp_data = []
        
        # Find all VMPP elements in chunks of CHUNK_SIZE
        vmpp_elements = root.xpath("//VMPPS/VMPP")
        dtinfo_elements = root.xpath("//DRUG_TARIFF_INFO/DTINFO")
        
        # Create a dictionary to look up DTINFO by VPPID
        dt_info_dict = {}
        for dt_elem in dtinfo_elements:
            vppid = dt_elem.find("VPPID").text
            price_elem = dt_elem.find("PRICE")
            dt_elem = dt_elem.find("DT")
            
            if price_elem is not None and dt_elem is not None:
                # If multiple DT entries exist for the same VPPID, use the most recent one
                if vppid in dt_info_dict:
                    current_dt = datetime.strptime(dt_info_dict[vppid]["DT"], "%Y-%m-%d")
                    new_dt = datetime.strptime(dt_elem.text, "%Y-%m-%d")
                    
                    if new_dt > current_dt:
                        dt_info_dict[vppid] = {
                            "PRICE": int(price_elem.text),
                            "DT": dt_elem.text
                        }
                else:
                    dt_info_dict[vppid] = {
                        "PRICE": int(price_elem.text),
                        "DT": dt_elem.text
                    }
        
        for i in range(0, len(vmpp_elements), config.CHUNK_SIZE):
            chunk = vmpp_elements[i:i+config.CHUNK_SIZE]
            
            for vmpp_elem in chunk:
                vppid = vmpp_elem.find("VPPID").text
                vpid = vmpp_elem.find("VPID").text
                nm = vmpp_elem.find("NM").text
                qtyval = vmpp_elem.find("QTYVAL").text
                qty_uomcd = vmpp_elem.find("QTY_UOMCD").text
                
                vmpp_record = {
                    "VPPID": int(vppid),
                    "VPID": int(vpid),
                    "NM": nm,
                    "QTYVAL": float(qtyval),
                    "QTY_UOMCD": int(qty_uomcd)
                }
                
                # Add drug tariff price information if available
                if vppid in dt_info_dict:
                    vmpp_record["PRICE"] = dt_info_dict[vppid]["PRICE"]
                    vmpp_record["DT"] = dt_info_dict[vppid]["DT"]
                
                vmpp_data.append(vmpp_record)
                
            # Insert this chunk into the database
            database.insert_data("vmpp", vmpp_data)
            vmpp_data = []  # Clear for next chunk
            
        logger.info(f"VMPP parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing VMPP data: {e}")
        return False


def parse_amp_data(xml_path):
    """
    Parse AMP data from the XML file.
    
    Args:
        xml_path (Path): Path to the AMP XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing AMP data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # AMP data list
        amp_data = []
        
        # Find all AMP elements in chunks of CHUNK_SIZE
        amp_elements = root.xpath("//AMPS/AMP")
        
        for i in range(0, len(amp_elements), config.CHUNK_SIZE):
            chunk = amp_elements[i:i+config.CHUNK_SIZE]
            
            for amp_elem in chunk:
                apid = amp_elem.find("APID").text
                vpid = amp_elem.find("VPID").text
                desc = amp_elem.find("DESC").text
                suppcd = amp_elem.find("SUPPCD").text
                
                amp_data.append({
                    "APID": int(apid),
                    "VPID": int(vpid),
                    "DESC": desc,
                    "SUPPCD": int(suppcd)
                })
                
            # Insert this chunk into the database
            database.insert_data("amp", amp_data)
            amp_data = []  # Clear for next chunk
            
        logger.info(f"AMP parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing AMP data: {e}")
        return False


def parse_ampp_data(xml_path):
    """
    Parse AMPP data from the XML file.
    
    Args:
        xml_path (Path): Path to the AMPP XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing AMPP data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # AMPP data list
        ampp_data = []
        
        # Find all AMPP elements in chunks of CHUNK_SIZE
        ampp_elements = root.xpath("//AMPPS/AMPP")
        price_info_elements = root.xpath("//MEDICINAL_PRODUCT_PRICE/PRICE_INFO")
        
        # Create a dictionary to look up PRICE_INFO by APPID
        price_info_dict = {}
        for price_elem in price_info_elements:
            appid = price_elem.find("APPID").text
            price_value_elem = price_elem.find("PRICE")
            
            if price_value_elem is not None:
                price_info_dict[appid] = int(price_value_elem.text)
        
        for i in range(0, len(ampp_elements), config.CHUNK_SIZE):
            chunk = ampp_elements[i:i+config.CHUNK_SIZE]
            
            for ampp_elem in chunk:
                appid = ampp_elem.find("APPID").text
                vppid = ampp_elem.find("VPPID").text
                apid = ampp_elem.find("APID").text
                nm = ampp_elem.find("NM").text
                
                ampp_record = {
                    "APPID": int(appid),
                    "VPPID": int(vppid),
                    "APID": int(apid),
                    "NM": nm,
                    "PRICE_SOURCE": "initial",  # Default value
                    "PRICE_METHOD": None
                }
                
                # Add price information if available
                if appid in price_info_dict:
                    ampp_record["PRICE"] = price_info_dict[appid]
                
                ampp_data.append(ampp_record)
                
            # Insert this chunk into the database
            database.insert_data("ampp", ampp_data)
            ampp_data = []  # Clear for next chunk
            
        logger.info(f"AMPP parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing AMPP data: {e}")
        return False


def parse_gtin_data(xml_path):
    """
    Parse GTIN data from the XML file.
    
    Args:
        xml_path (Path): Path to the GTIN XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing GTIN data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        # GTIN data list
        gtin_data = []
        
        # Find all AMPP elements in chunks of CHUNK_SIZE
        ampp_elements = root.xpath("//AMPPS/AMPP")
        
        for i in range(0, len(ampp_elements), config.CHUNK_SIZE):
            chunk = ampp_elements[i:i+config.CHUNK_SIZE]
            
            for ampp_elem in chunk:
                amppid = ampp_elem.find("AMPPID").text
                gtin_data_elements = ampp_elem.findall("GTINDATA")
                
                for gtin_data_elem in gtin_data_elements:
                    gtin = gtin_data_elem.find("GTIN").text
                    startdt = gtin_data_elem.find("STARTDT").text
                    enddt_elem = gtin_data_elem.find("ENDDT")
                    
                    gtin_record = {
                        "AMPPID": int(amppid),
                        "GTIN": gtin,
                        "STARTDT": startdt
                    }
                    
                    if enddt_elem is not None:
                        gtin_record["ENDDT"] = enddt_elem.text
                    
                    gtin_data.append(gtin_record)
                
            # Insert this chunk into the database
            database.insert_data("gtin", gtin_data)
            gtin_data = []  # Clear for next chunk
            
        logger.info(f"GTIN parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing GTIN data: {e}")
        return False


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


def parse_ingredient_data(xml_path):
    """
    Parse ingredient data from the XML file.
    
    Args:
        xml_path (Path): Path to the ingredient XML file.
        
    Returns:
        bool: True if parsing was successful, False otherwise.
    """
    logger.info(f"Parsing ingredient data from {xml_path}")
    
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()
        
        ingredient_data = []
        ingredient_elements = root.xpath("//INGREDIENT")
        
        for i in range(0, len(ingredient_elements), config.CHUNK_SIZE):
            chunk = ingredient_elements[i:i+config.CHUNK_SIZE]
            
            for ingredient_elem in chunk:
                isid = ingredient_elem.find("ISID").text
                nm = ingredient_elem.find("NM").text
                
                ingredient_record = {
                    "ISID": int(isid),
                    "NM": nm
                }
                
                # Add optional fields if present
                isiddt_elem = ingredient_elem.find("ISIDDT")
                if isiddt_elem is not None:
                    ingredient_record["ISIDDT"] = isiddt_elem.text
                    
                isidprev_elem = ingredient_elem.find("ISIDPREV")
                if isidprev_elem is not None:
                    ingredient_record["ISIDPREV"] = int(isidprev_elem.text)
                    
                invalid_elem = ingredient_elem.find("INVALID")
                if invalid_elem is not None:
                    ingredient_record["INVALID"] = int(invalid_elem.text)
                
                ingredient_data.append(ingredient_record)
                
            # Insert this chunk
            database.insert_data("ingredient", ingredient_data)
            ingredient_data = []
            
        logger.info(f"Ingredient parsing completed")
        return True
        
    except Exception as e:
        logger.error(f"Error parsing ingredient data: {e}")
        return False


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


def find_xml_files():
    """
    Find all the relevant XML files in the data directory.
    
    Returns:
        dict: Dictionary mapping file type to file path.
    """
    logger.info(f"Searching for XML files in {config.DATA_DIR}")
    
    xml_files = {}
    
    for file_type, pattern_info in config.FILE_PATTERNS.items():
        pattern = pattern_info['pattern']
        schema = pattern_info['schema']
        
        # Search for files matching the pattern in the extracted directory
        for file_path in Path(config.DATA_DIR).glob(f"**/{pattern}"):
            logger.info(f"Found {file_type} file: {file_path}")
            
            # Validate the file against its schema
            if validate_xml_against_xsd(file_path, schema):
                xml_files[file_type] = file_path
                break
    
    return xml_files


def process_all_files():
    """
    Process all XML files: validate, parse, and insert into the database.
    
    Returns:
        bool: True if all processing was successful, False otherwise.
    """
    logger.info("Starting to process all XML files")
    
    # Initialize the database
    if not database.initialize_database():
        logger.error("Database initialization failed")
        return False
    
    # Find and validate XML files
    xml_files = find_xml_files()
    
    if len(xml_files) != len(config.FILE_PATTERNS):
        logger.warning(f"Some XML files were not found or did not validate. Found {len(xml_files)} of {len(config.FILE_PATTERNS)}")
    
    # Process each file type in the correct order for foreign key constraints
    
    # First VTM (Virtual Therapeutic Moiety)
    if 'vtm' in xml_files:
        if not parse_vtm_data(xml_files['vtm']):
            logger.error("VTM parsing failed")
            return False
    else:
        logger.error("VTM file not found or invalid")
        return False
    
    # Then VMP (Virtual Medicinal Product)
    if 'vmp' in xml_files:
        if not parse_vmp_data(xml_files['vmp']):
            logger.error("VMP parsing failed")
            return False
    else:
        logger.error("VMP file not found or invalid")
        return False
    
    # Then VMPP (Virtual Medicinal Product Pack)
    if 'vmpp' in xml_files:
        if not parse_vmpp_data(xml_files['vmpp']):
            logger.error("VMPP parsing failed")
            return False
    else:
        logger.error("VMPP file not found or invalid")
        return False
    
    # Then AMP (Actual Medicinal Product)
    if 'amp' in xml_files:
        if not parse_amp_data(xml_files['amp']):
            logger.error("AMP parsing failed")
            return False
    else:
        logger.error("AMP file not found or invalid")
        return False
    
    # Then AMPP (Actual Medicinal Product Pack)
    if 'ampp' in xml_files:
        if not parse_ampp_data(xml_files['ampp']):
            logger.error("AMPP parsing failed")
            return False
    else:
        logger.error("AMPP file not found or invalid")
        return False
    
    # Then GTIN mapping
    if 'gtin' in xml_files:
        if not parse_gtin_data(xml_files['gtin']):
            logger.error("GTIN parsing failed")
            return False
    else:
        logger.error("GTIN file not found or invalid")
        return False
    
    # Then Ingredient
    if 'ingredient' in xml_files:
        if not parse_ingredient_data(xml_files['ingredient']):
            logger.error("Ingredient parsing failed")
            return False
    else:
        logger.error("Ingredient file not found or invalid")
        return False
    
    # Then Lookup
    if 'lookup' in xml_files:
        if not parse_lookup_data(xml_files['lookup']):
            logger.error("Lookup parsing failed")
            return False
    else:
        logger.error("Lookup file not found or invalid")
        return False
    
    # Finally VMP Ingredient
    if 'vmp_ingredient' in xml_files:
        if not parse_vmp_ingredient_data(xml_files['vmp_ingredient']):
            logger.error("VMP Ingredient parsing failed")
            return False
    else:
        logger.error("VMP Ingredient file not found or invalid")
        return False
    
    logger.info("All XML files processed successfully")
    return True


if __name__ == "__main__":
    # Test processing
    process_all_files() 