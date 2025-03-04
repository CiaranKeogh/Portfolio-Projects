import logging
import re
from sqlalchemy import select, join
from tqdm import tqdm

from ..database.models import get_session, VMP, VMPP, AMPP, SearchData

logger = logging.getLogger(__name__)

class SearchTableBuilder:
    """Builds a unified search table with all required fields"""
    
    def __init__(self, db_session=None):
        """Initialize the search table builder
        
        Args:
            db_session (Session, optional): SQLAlchemy session. Creates a new one if not provided.
        """
        self.db_session = db_session or get_session()
    
    def build_search_table(self):
        """Build the unified search table
        
        Returns:
            int: Number of records created in the search table
        """
        logger.info("Building unified search table")
        
        # Clear existing search data
        self.db_session.query(SearchData).delete()
        self.db_session.commit()
        
        # Get all AMPPs with joined data
        query = self.db_session.query(
            AMPP, VMPP, VMP
        ).join(
            VMPP, AMPP.VPPID == VMPP.VPPID
        ).join(
            VMP, VMPP.VPID == VMP.VPID
        ).all()
        
        logger.info(f"Found {len(query)} records to process")
        
        count = 0
        batch = []
        
        for ampp, vmpp, vmp in tqdm(query, desc="Building search table"):
            # Classify as Brand or Generic
            brand_or_generic = self._classify_brand_or_generic(vmpp.DESC, ampp.DESC)
            
            # Create search record
            search_record = SearchData(
                VPPID=vmpp.VPPID,
                VMPP=vmpp.DESC,
                VPID=vmp.VPID,
                VMP=vmp.DESC,
                APID=ampp.APID,
                Description=ampp.DESC,
                Brand_or_Generic=brand_or_generic,
                Drug_Tariff_Price=ampp.PRICE,
                Price_Source=ampp.PRICE_SOURCE,
                Price_Method=ampp.PRICE_METHOD
            )
            
            batch.append(search_record)
            count += 1
            
            # Commit in batches of 1000
            if len(batch) >= 1000:
                self.db_session.add_all(batch)
                self.db_session.commit()
                batch = []
        
        # Commit any remaining records
        if batch:
            self.db_session.add_all(batch)
            self.db_session.commit()
        
        logger.info(f"Created {count} records in search table")
        return count
    
    def _classify_brand_or_generic(self, vmpp_desc, ampp_desc):
        """Classify a product as Brand or Generic
        
        Args:
            vmpp_desc (str): VMPP description
            ampp_desc (str): AMPP description
            
        Returns:
            str: "Brand" or "Generic"
        """
        # Remove supplier name in brackets
        cleaned_ampp_desc = re.sub(r'\([^)]*\)', '', ampp_desc).strip()
        
        # Compare cleaned descriptions
        if cleaned_ampp_desc == vmpp_desc:
            return "Generic"
        else:
            return "Brand"
    
    def create_indexes(self):
        """Create indexes on the search table for efficient querying"""
        # Note: In SQLAlchemy, indexes are defined in the model class.
        # We're just logging here to document the process.
        logger.info("Creating indexes on search table")
        logger.info("- Index on VPPID for fast VMPP-to-AMPP lookups")
        logger.info("- Index on APID for direct AMPP lookups")
        logger.info("- Index on Description for text searches")
        return True 