import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from lxml import etree
import sqlite3
from sqlalchemy.orm import Session

from ..config.config import XML_CHUNK_SIZE
from ..database.models import (
    get_session, VMP, VMPP, AMP, AMPP, GTIN, init_db
)

logger = logging.getLogger(__name__)

class XMLParser:
    """Parser for XML files from NHS TRUD service"""
    
    def __init__(self, db_session=None):
        """Initialize the XML parser
        
        Args:
            db_session (Session, optional): SQLAlchemy session. Creates a new one if not provided.
        """
        self.db_session = db_session or get_session()
    
    def parse_file(self, file_path, entity_type):
        """Parse an XML file and load data into the database
        
        Args:
            file_path (str or Path): Path to the XML file
            entity_type (str): Type of entity to parse ('vmp', 'vmpp', 'amp', 'ampp', 'gtin')
            
        Returns:
            int: Number of records processed
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return 0
        
        logger.info(f"Parsing {entity_type} file: {file_path}")
        
        # Map entity type to parsing function
        parser_map = {
            'vmp': self._parse_vmp,
            'vmpp': self._parse_vmpp,
            'amp': self._parse_amp,
            'ampp': self._parse_ampp,
            'gtin': self._parse_gtin
        }
        
        if entity_type not in parser_map:
            logger.error(f"Unknown entity type: {entity_type}")
            return 0
        
        # Get the appropriate parsing function
        parse_func = parser_map[entity_type]
        
        # Use iterparse to process large XML files in chunks
        context = etree.iterparse(file_path, events=('end',), tag=self._get_tag_name(entity_type))
        
        # Process in chunks
        count = 0
        batch = []
        
        for _, elem in context:
            # Process the element
            record = parse_func(elem)
            if record:
                batch.append(record)
                count += 1
            
            # Clear element to free memory
            elem.clear()
            
            # Process batch when it reaches chunk size
            if len(batch) >= XML_CHUNK_SIZE:
                self._commit_batch(batch, entity_type)
                batch = []
                
            # Log progress
            if count % (XML_CHUNK_SIZE * 10) == 0:
                logger.info(f"Processed {count} {entity_type} records")
        
        # Process any remaining records
        if batch:
            self._commit_batch(batch, entity_type)
        
        logger.info(f"Completed parsing {count} {entity_type} records")
        return count
    
    def _commit_batch(self, batch, entity_type):
        """Commit a batch of records to the database
        
        Args:
            batch (list): List of SQLAlchemy model instances
            entity_type (str): Type of entity being committed
        """
        try:
            self.db_session.add_all(batch)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error committing {entity_type} batch: {str(e)}")
    
    def _get_tag_name(self, entity_type):
        """Get the XML tag name for an entity type
        
        Args:
            entity_type (str): Type of entity ('vmp', 'vmpp', 'amp', 'ampp', 'gtin')
            
        Returns:
            str: XML tag name
        """
        tag_map = {
            'vmp': 'VMP',
            'vmpp': 'VMPP',
            'amp': 'AMP',
            'ampp': 'AMPP',
            'gtin': 'AMPP'  # GTIN is nested under AMPP
        }
        return tag_map.get(entity_type, entity_type.upper())
    
    def _parse_vmp(self, elem):
        """Parse a VMP XML element
        
        Args:
            elem (Element): XML element
            
        Returns:
            VMP: SQLAlchemy VMP model instance
        """
        try:
            vpid = int(elem.findtext('VPID'))
            desc = elem.findtext('NM')
            
            return VMP(
                VPID=vpid,
                DESC=desc
            )
        except Exception as e:
            logger.error(f"Error parsing VMP: {str(e)}")
            return None
    
    def _parse_vmpp(self, elem):
        """Parse a VMPP XML element
        
        Args:
            elem (Element): XML element
            
        Returns:
            VMPP: SQLAlchemy VMPP model instance
        """
        try:
            vppid = int(elem.findtext('VPPID'))
            vpid = int(elem.findtext('VPID'))
            desc = elem.findtext('NM')
            
            return VMPP(
                VPPID=vppid,
                VPID=vpid,
                DESC=desc
            )
        except Exception as e:
            logger.error(f"Error parsing VMPP: {str(e)}")
            return None
    
    def _parse_amp(self, elem):
        """Parse an AMP XML element
        
        Args:
            elem (Element): XML element
            
        Returns:
            AMP: SQLAlchemy AMP model instance
        """
        try:
            apid = int(elem.findtext('APID'))
            vpid = int(elem.findtext('VPID'))
            desc = elem.findtext('DESC')
            
            return AMP(
                APID=apid,
                VPID=vpid,
                DESC=desc
            )
        except Exception as e:
            logger.error(f"Error parsing AMP: {str(e)}")
            return None
    
    def _parse_ampp(self, elem):
        """Parse an AMPP XML element
        
        Args:
            elem (Element): XML element
            
        Returns:
            AMPP: SQLAlchemy AMPP model instance
        """
        try:
            apid = int(elem.findtext('APID'))
            vppid = int(elem.findtext('VPPID'))
            desc = elem.findtext('NM')
            
            # Look for price info
            price = None
            price_source = 'initial'
            
            # In a real implementation, you would locate the price info in the XML
            # This is simplified for the example
            price_elem = elem.find('.//PRICE')
            if price_elem is not None and price_elem.text:
                price = float(price_elem.text) / 100.0  # Convert pence to pounds
            
            return AMPP(
                APID=apid,
                VPPID=vppid,
                DESC=desc,
                PRICE=price,
                PRICE_SOURCE=price_source,
                PRICE_METHOD=None
            )
        except Exception as e:
            logger.error(f"Error parsing AMPP: {str(e)}")
            return None
    
    def _parse_gtin(self, elem):
        """Parse a GTIN XML element
        
        Args:
            elem (Element): XML element
            
        Returns:
            list: List of SQLAlchemy GTIN model instances
        """
        try:
            gtins = []
            apid = int(elem.findtext('AMPPID'))
            
            # In the real XML, GTINs would be nested elements
            # This is simplified for the example
            gtin_elems = elem.findall('.//GTIN')
            
            for gtin_elem in gtin_elems:
                gtin_value = gtin_elem.text
                if gtin_value:
                    gtins.append(GTIN(
                        GTIN=gtin_value,
                        APID=apid
                    ))
            
            return gtins
        except Exception as e:
            logger.error(f"Error parsing GTIN: {str(e)}")
            return None
    
    def parse_all_files(self, vmp_path, vmpp_path, amp_path, ampp_path, gtin_path):
        """Parse all XML files
        
        Args:
            vmp_path (str or Path): Path to VMP XML file
            vmpp_path (str or Path): Path to VMPP XML file
            amp_path (str or Path): Path to AMP XML file
            ampp_path (str or Path): Path to AMPP XML file
            gtin_path (str or Path): Path to GTIN XML file
            
        Returns:
            dict: Dictionary with counts of records processed for each entity type
        """
        # Initialize the database
        init_db()
        
        # Process files in the correct order (VMP first, then VMPP, etc.)
        results = {}
        
        results['vmp'] = self.parse_file(vmp_path, 'vmp')
        results['vmpp'] = self.parse_file(vmpp_path, 'vmpp')
        results['amp'] = self.parse_file(amp_path, 'amp')
        results['ampp'] = self.parse_file(ampp_path, 'ampp')
        results['gtin'] = self.parse_file(gtin_path, 'gtin')
        
        return results 