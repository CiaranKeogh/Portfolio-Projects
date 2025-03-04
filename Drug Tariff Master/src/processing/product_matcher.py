import logging
import re
from sqlalchemy import and_, or_, func
from tqdm import tqdm

from ..database.models import get_session, AMPP, VMPP, GTIN
from ..utils.llm_processor import GeminiProcessor
from ..config.config import LLM_BATCH_SIZE

logger = logging.getLogger(__name__)

class ProductMatcher:
    """Matches products (AMPP to VMPP, GTIN to AMPP) based on database relationships or LLM"""
    
    def __init__(self, db_session=None, llm_processor=None):
        """Initialize the product matcher
        
        Args:
            db_session (Session, optional): SQLAlchemy session. Creates a new one if not provided.
            llm_processor (GeminiProcessor, optional): LLM processor for matching. Creates a new one if not provided.
        """
        self.db_session = db_session or get_session()
        self.llm_processor = llm_processor or GeminiProcessor()
    
    def match_ampp_to_vmpp(self):
        """Match AMPPs to VMPPs
        
        This function:
        1. Identifies AMPPs with missing VPPID
        2. Uses LLM to match descriptions and find the correct VMPP
        
        Returns:
            int: Number of AMPPs matched
        """
        logger.info("Starting AMPP to VMPP matching")
        
        # Find AMPPs with missing VPPID
        ampp_missing_vmpp = self.db_session.query(AMPP).filter(
            AMPP.VPPID.is_(None)
        ).all()
        
        if not ampp_missing_vmpp:
            logger.info("No AMPPs with missing VMPP found")
            return 0
        
        logger.info(f"Found {len(ampp_missing_vmpp)} AMPPs with missing VMPP")
        
        # Process in batches
        batch_size = LLM_BATCH_SIZE
        batches = [ampp_missing_vmpp[i:i+batch_size] for i in range(0, len(ampp_missing_vmpp), batch_size)]
        
        matched_count = 0
        
        for batch in tqdm(batches, desc="Matching AMPPs to VMPPs"):
            # Get AMPP descriptions
            ampp_descriptions = [(ampp.APID, ampp.DESC) for ampp in batch]
            
            # Query all VMPPs for matching
            vmpp_records = self.db_session.query(VMPP).all()
            vmpp_descriptions = [(vmpp.VPPID, vmpp.DESC) for vmpp in vmpp_records]
            
            # Use LLM to match descriptions
            matches = self.llm_processor.match_ampp_to_vmpp(ampp_descriptions, vmpp_descriptions)
            
            # Update the database with matches
            for apid, vppid in matches.items():
                if vppid:
                    try:
                        ampp = self.db_session.query(AMPP).filter(AMPP.APID == apid).first()
                        if ampp:
                            ampp.VPPID = vppid
                            matched_count += 1
                    except Exception as e:
                        logger.error(f"Error updating AMPP {apid}: {str(e)}")
            
            # Commit the batch
            try:
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
                logger.error(f"Error committing AMPP-VMPP matches: {str(e)}")
        
        logger.info(f"Matched {matched_count} AMPPs to VMPPs")
        return matched_count
    
    def match_gtin_to_ampp(self):
        """Match GTINs to AMPPs
        
        This function:
        1. Identifies GTINs with missing APID
        2. Uses LLM to match product details and find the correct AMPP
        
        Returns:
            int: Number of GTINs matched
        """
        logger.info("Starting GTIN to AMPP matching")
        
        # Find GTINs with missing APID
        gtin_missing_ampp = self.db_session.query(GTIN).filter(
            GTIN.APID.is_(None)
        ).all()
        
        if not gtin_missing_ampp:
            logger.info("No GTINs with missing AMPP found")
            return 0
        
        logger.info(f"Found {len(gtin_missing_ampp)} GTINs with missing AMPP")
        
        # Process in batches
        batch_size = LLM_BATCH_SIZE
        batches = [gtin_missing_ampp[i:i+batch_size] for i in range(0, len(gtin_missing_ampp), batch_size)]
        
        matched_count = 0
        
        for batch in tqdm(batches, desc="Matching GTINs to AMPPs"):
            # Get GTIN values
            gtin_values = [(gtin.id, gtin.GTIN) for gtin in batch]
            
            # Query all AMPPs for matching
            ampp_records = self.db_session.query(AMPP).all()
            ampp_details = [(ampp.APID, ampp.DESC) for ampp in ampp_records]
            
            # Use LLM to match GTINs to AMPPs
            matches = self.llm_processor.match_gtin_to_ampp(gtin_values, ampp_details)
            
            # Update the database with matches
            for gtin_id, apid in matches.items():
                if apid:
                    try:
                        gtin = self.db_session.query(GTIN).filter(GTIN.id == gtin_id).first()
                        if gtin:
                            gtin.APID = apid
                            matched_count += 1
                    except Exception as e:
                        logger.error(f"Error updating GTIN {gtin_id}: {str(e)}")
            
            # Commit the batch
            try:
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
                logger.error(f"Error committing GTIN-AMPP matches: {str(e)}")
        
        logger.info(f"Matched {matched_count} GTINs to AMPPs")
        return matched_count
    
    def run_all_matching(self):
        """Run all matching operations
        
        Returns:
            dict: Dictionary with counts of matches for each type
        """
        results = {}
        
        # Match AMPPs to VMPPs
        results['ampp_to_vmpp'] = self.match_ampp_to_vmpp()
        
        # Match GTINs to AMPPs
        results['gtin_to_ampp'] = self.match_gtin_to_ampp()
        
        return results 