import logging
import re
from sqlalchemy import func, and_, or_
from tqdm import tqdm

from ..database.models import get_session, AMPP, VMPP, VMP, AMP
from ..utils.llm_processor import GeminiProcessor
from ..config.config import LLM_BATCH_SIZE

logger = logging.getLogger(__name__)

class PriceCalculator:
    """Calculates missing drug tariff prices based on similar products"""
    
    def __init__(self, db_session=None, llm_processor=None):
        """Initialize the price calculator
        
        Args:
            db_session (Session, optional): SQLAlchemy session. Creates a new one if not provided.
            llm_processor (GeminiProcessor, optional): LLM processor for strength/pack size extraction. Creates a new one if not provided.
        """
        self.db_session = db_session or get_session()
        self.llm_processor = llm_processor or GeminiProcessor()
    
    def apply_same_vmpp_rule(self):
        """Apply the Same VMPP rule to calculate missing prices
        
        For each AMPP with a null PRICE, calculate the average PRICE of other AMPPs 
        with the same VPPID that have a non-null PRICE.
        
        Returns:
            int: Number of prices calculated
        """
        logger.info("Applying Same VMPP rule")
        
        # Find AMPPs with null prices
        ampps_null_price = self.db_session.query(AMPP).filter(
            AMPP.PRICE.is_(None)
        ).all()
        
        if not ampps_null_price:
            logger.info("No AMPPs with null prices found")
            return 0
        
        logger.info(f"Found {len(ampps_null_price)} AMPPs with null prices")
        
        # Group AMPPs by VPPID
        vppid_groups = {}
        for ampp in ampps_null_price:
            if ampp.VPPID:
                if ampp.VPPID not in vppid_groups:
                    vppid_groups[ampp.VPPID] = []
                vppid_groups[ampp.VPPID].append(ampp)
        
        # For each VPPID group, calculate the average price of other AMPPs with the same VPPID
        count = 0
        
        for vppid, ampps in tqdm(vppid_groups.items(), desc="Applying Same VMPP rule"):
            # Get average price of other AMPPs with the same VPPID
            avg_price = self.db_session.query(func.avg(AMPP.PRICE)).filter(
                and_(
                    AMPP.VPPID == vppid,
                    AMPP.PRICE.isnot(None)
                )
            ).scalar()
            
            if avg_price:
                # Update all AMPPs in this group
                for ampp in ampps:
                    ampp.PRICE = avg_price
                    ampp.PRICE_SOURCE = 'calculated'
                    ampp.PRICE_METHOD = 'Same VMPP'
                    count += 1
        
        # Commit changes
        try:
            self.db_session.commit()
            logger.info(f"Updated {count} AMPPs with Same VMPP rule")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error committing price updates: {str(e)}")
        
        return count
    
    def apply_same_vmp_rule(self):
        """Apply the Same VMP rule to calculate missing prices
        
        For AMPPs that still have null prices after the Same VMPP rule:
        1. Use LLM to extract strength and pack size
        2. Calculate price per unit from similar products
        3. Estimate price based on pack size
        
        Returns:
            int: Number of prices calculated
        """
        logger.info("Applying Same VMP rule")
        
        # Find AMPPs with null prices
        ampps_null_price = self.db_session.query(AMPP).filter(
            AMPP.PRICE.is_(None)
        ).all()
        
        if not ampps_null_price:
            logger.info("No remaining AMPPs with null prices found")
            return 0
        
        logger.info(f"Found {len(ampps_null_price)} remaining AMPPs with null prices")
        
        # Process in batches
        batch_size = LLM_BATCH_SIZE
        batches = [ampps_null_price[i:i+batch_size] for i in range(0, len(ampps_null_price), batch_size)]
        
        count = 0
        
        for batch in tqdm(batches, desc="Applying Same VMP rule"):
            # Get descriptions for LLM processing
            descriptions = [(ampp.APID, ampp.DESC) for ampp in batch]
            
            # Use LLM to extract strength and pack size
            extracted_data = self.llm_processor.extract_strength_and_pack_size(descriptions)
            
            # For each AMPP in the batch
            for ampp in batch:
                # Skip if no extracted data
                if ampp.APID not in extracted_data:
                    continue
                
                # Get VPID from VPPID
                vmpp = self.db_session.query(VMPP).filter(VMPP.VPPID == ampp.VPPID).first()
                if not vmpp:
                    continue
                
                vpid = vmpp.VPID
                
                # Get strength and pack size
                strength = extracted_data[ampp.APID].get('strength')
                pack_size = extracted_data[ampp.APID].get('pack_size')
                
                if not strength or not pack_size:
                    continue
                
                # Find similar products with the same VMP and known prices
                similar_ampps = self.db_session.query(AMPP).join(
                    VMPP, AMPP.VPPID == VMPP.VPPID
                ).filter(
                    and_(
                        VMPP.VPID == vpid,
                        AMPP.PRICE.isnot(None)
                    )
                ).all()
                
                if not similar_ampps:
                    continue
                
                # Calculate price per unit for similar products
                price_per_unit_data = []
                
                for similar_ampp in similar_ampps:
                    # Extract strength and pack size for the similar product
                    similar_data = self.llm_processor.extract_strength_and_pack_size(
                        [(similar_ampp.APID, similar_ampp.DESC)]
                    )
                    
                    if similar_ampp.APID in similar_data:
                        similar_strength = similar_data[similar_ampp.APID].get('strength')
                        similar_pack_size = similar_data[similar_ampp.APID].get('pack_size')
                        
                        if similar_strength and similar_pack_size and float(similar_pack_size) > 0:
                            # Calculate price per unit
                            price_per_unit = similar_ampp.PRICE / float(similar_pack_size)
                            price_per_unit_data.append(price_per_unit)
                
                if price_per_unit_data:
                    # Calculate average price per unit
                    avg_price_per_unit = sum(price_per_unit_data) / len(price_per_unit_data)
                    
                    # Estimate price
                    estimated_price = avg_price_per_unit * float(pack_size)
                    
                    # Update AMPP
                    ampp.PRICE = estimated_price
                    ampp.PRICE_SOURCE = 'calculated'
                    ampp.PRICE_METHOD = 'Same VMP'
                    count += 1
        
        # Commit changes
        try:
            self.db_session.commit()
            logger.info(f"Updated {count} AMPPs with Same VMP rule")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error committing price updates: {str(e)}")
        
        return count
    
    def apply_default_rule(self):
        """Apply the Default rule to any remaining AMPPs with null prices
        
        Set PRICE to 0, set PRICE_SOURCE to 'calculated', and set PRICE_METHOD to 'None'
        
        Returns:
            int: Number of prices set to 0
        """
        logger.info("Applying Default rule")
        
        # Find remaining AMPPs with null prices
        ampps_null_price = self.db_session.query(AMPP).filter(
            AMPP.PRICE.is_(None)
        ).all()
        
        if not ampps_null_price:
            logger.info("No remaining AMPPs with null prices found")
            return 0
        
        logger.info(f"Found {len(ampps_null_price)} remaining AMPPs with null prices")
        
        # Update all remaining AMPPs
        for ampp in tqdm(ampps_null_price, desc="Applying Default rule"):
            ampp.PRICE = 0
            ampp.PRICE_SOURCE = 'calculated'
            ampp.PRICE_METHOD = 'None'
        
        # Commit changes
        try:
            self.db_session.commit()
            logger.info(f"Set {len(ampps_null_price)} AMPPs to price 0 with Default rule")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error committing price updates: {str(e)}")
        
        return len(ampps_null_price)
    
    def calculate_all_prices(self):
        """Apply all price calculation rules in order
        
        Returns:
            dict: Dictionary with counts of prices calculated for each rule
        """
        results = {}
        
        # Apply Same VMPP rule (primary)
        results['same_vmpp'] = self.apply_same_vmpp_rule()
        
        # Apply Same VMP rule (fallback)
        results['same_vmp'] = self.apply_same_vmp_rule()
        
        # Apply Default rule (last resort)
        results['default'] = self.apply_default_rule()
        
        return results 