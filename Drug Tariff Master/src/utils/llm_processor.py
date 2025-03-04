import logging
import json
import time
import google.generativeai as genai
from tqdm import tqdm

from ..config.config import GEMINI_API_KEY, LLM_BATCH_SIZE

logger = logging.getLogger(__name__)

class GeminiProcessor:
    """Processor for NLP tasks using Google Gemini"""
    
    def __init__(self, api_key=None):
        """Initialize the Gemini processor
        
        Args:
            api_key (str, optional): The API key for Google Gemini. Defaults to the one in config.
        """
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Google Gemini API key is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Create a Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def extract_strength_and_pack_size(self, descriptions, batch_size=None):
        """Extract strength and pack size from product descriptions
        
        Args:
            descriptions (list): List of tuples (id, description)
            batch_size (int, optional): Size of batches to process. Defaults to LLM_BATCH_SIZE.
            
        Returns:
            dict: Dictionary mapping IDs to extracted data (strength and pack size)
        """
        batch_size = batch_size or LLM_BATCH_SIZE
        
        # Process in batches
        batches = [descriptions[i:i+batch_size] for i in range(0, len(descriptions), batch_size)]
        
        results = {}
        
        for batch in batches:
            # Create prompt
            prompt = self._create_extraction_prompt(batch)
            
            # Try to get a response with retries
            response_text = self._get_llm_response(prompt)
            
            if not response_text:
                logger.error("Failed to get a valid response from Gemini")
                continue
            
            # Parse the response
            try:
                # The response should be a JSON string
                parsed_data = json.loads(response_text)
                
                # Add to results
                for item_id, data in parsed_data.items():
                    # Convert string IDs (from JSON) to integers
                    item_id = int(item_id)
                    results[item_id] = data
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response_text}")
                
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        return results
    
    def match_ampp_to_vmpp(self, ampp_descriptions, vmpp_descriptions, batch_size=None):
        """Match AMPP descriptions to VMPP descriptions
        
        Args:
            ampp_descriptions (list): List of tuples (APID, description)
            vmpp_descriptions (list): List of tuples (VPPID, description)
            batch_size (int, optional): Size of batches to process. Defaults to LLM_BATCH_SIZE.
            
        Returns:
            dict: Dictionary mapping APIDs to VPPIDs
        """
        batch_size = batch_size or LLM_BATCH_SIZE
        
        # Process in batches
        batches = [ampp_descriptions[i:i+batch_size] for i in range(0, len(ampp_descriptions), batch_size)]
        
        results = {}
        
        for batch in batches:
            # Create prompt
            prompt = self._create_matching_prompt(batch, vmpp_descriptions)
            
            # Try to get a response with retries
            response_text = self._get_llm_response(prompt)
            
            if not response_text:
                logger.error("Failed to get a valid response from Gemini")
                continue
            
            # Parse the response
            try:
                # The response should be a JSON string
                parsed_data = json.loads(response_text)
                
                # Add to results
                for apid_str, vppid in parsed_data.items():
                    # Convert string IDs (from JSON) to integers
                    apid = int(apid_str)
                    if vppid:  # vppid could be null for no match
                        vppid = int(vppid)
                    results[apid] = vppid
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response_text}")
                
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        return results
    
    def match_gtin_to_ampp(self, gtin_values, ampp_details, batch_size=None):
        """Match GTIN values to AMPP details
        
        Args:
            gtin_values (list): List of tuples (GTIN ID, GTIN value)
            ampp_details (list): List of tuples (APID, description)
            batch_size (int, optional): Size of batches to process. Defaults to LLM_BATCH_SIZE.
            
        Returns:
            dict: Dictionary mapping GTIN IDs to APIDs
        """
        batch_size = batch_size or LLM_BATCH_SIZE
        
        # Process in batches
        batches = [gtin_values[i:i+batch_size] for i in range(0, len(gtin_values), batch_size)]
        
        results = {}
        
        for batch in batches:
            # Create prompt
            prompt = self._create_gtin_matching_prompt(batch, ampp_details)
            
            # Try to get a response with retries
            response_text = self._get_llm_response(prompt)
            
            if not response_text:
                logger.error("Failed to get a valid response from Gemini")
                continue
            
            # Parse the response
            try:
                # The response should be a JSON string
                parsed_data = json.loads(response_text)
                
                # Add to results
                for gtin_id_str, apid in parsed_data.items():
                    # Convert string IDs (from JSON) to integers
                    gtin_id = int(gtin_id_str)
                    if apid:  # apid could be null for no match
                        apid = int(apid)
                    results[gtin_id] = apid
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response_text}")
                
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        return results
    
    def _get_llm_response(self, prompt, max_retries=3):
        """Get a response from the LLM with retries
        
        Args:
            prompt (str): The prompt to send to the LLM
            max_retries (int, optional): Maximum number of retries. Defaults to 3.
            
        Returns:
            str: The response text, or None if failed
        """
        for attempt in range(max_retries):
            try:
                # Generate response
                response = self.model.generate_content(prompt)
                
                # Return the text
                return response.text
                
            except Exception as e:
                logger.error(f"Error calling Gemini API (attempt {attempt+1}/{max_retries}): {str(e)}")
                
                if attempt < max_retries - 1:
                    # Exponential backoff (1s, 2s, 4s, ...)
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        
        return None
    
    def _create_extraction_prompt(self, descriptions):
        """Create a prompt for extracting strength and pack size
        
        Args:
            descriptions (list): List of tuples (id, description)
            
        Returns:
            str: The prompt text
        """
        # Format the descriptions for the prompt
        items = []
        for id_val, desc in descriptions:
            items.append(f"{id_val}: {desc}")
        
        items_text = "\n".join(items)
        
        # Create the prompt
        prompt = f"""
        Extract the strength (e.g., "500mg") and pack size (e.g., "32") from each medication description.
        
        For each description, return the strength and pack size as numbers.
        If strength or pack size can't be determined, leave it null.
        
        Descriptions:
        {items_text}
        
        Return a JSON object where each key is the ID and each value is an object with "strength" and "pack_size" properties.
        Example output format:
        {{
            "12345": {{"strength": "500", "pack_size": "32"}},
            "67890": {{"strength": "250", "pack_size": "100"}}
        }}
        
        Only provide the JSON response with no additional explanation.
        """
        
        return prompt
    
    def _create_matching_prompt(self, ampp_descriptions, vmpp_descriptions):
        """Create a prompt for matching AMPP to VMPP
        
        Args:
            ampp_descriptions (list): List of tuples (APID, description)
            vmpp_descriptions (list): List of tuples (VPPID, description)
            
        Returns:
            str: The prompt text
        """
        # Format the AMPP descriptions
        ampp_items = []
        for apid, desc in ampp_descriptions:
            ampp_items.append(f"{apid}: {desc}")
        
        ampp_text = "\n".join(ampp_items)
        
        # Format the VMPP descriptions (limit to 100 for token constraints)
        vmpp_items = []
        for vppid, desc in vmpp_descriptions[:100]:
            vmpp_items.append(f"{vppid}: {desc}")
        
        vmpp_text = "\n".join(vmpp_items)
        
        # Create the prompt
        prompt = f"""
        Match each AMPP (Actual Medicinal Product Pack) to the most appropriate VMPP (Virtual Medicinal Product Pack).
        
        AMPPs to match:
        {ampp_text}
        
        Available VMPPs:
        {vmpp_text}
        
        For each AMPP, return the VPPID of the matching VMPP. If no match is found, return null.
        
        Return a JSON object where each key is the APID and each value is the matching VPPID or null.
        Example output format:
        {{
            "12345": 67890,
            "54321": null
        }}
        
        Only provide the JSON response with no additional explanation.
        """
        
        return prompt
    
    def _create_gtin_matching_prompt(self, gtin_values, ampp_details):
        """Create a prompt for matching GTIN to AMPP
        
        Args:
            gtin_values (list): List of tuples (GTIN ID, GTIN value)
            ampp_details (list): List of tuples (APID, description)
            
        Returns:
            str: The prompt text
        """
        # Format the GTIN values
        gtin_items = []
        for gtin_id, gtin_value in gtin_values:
            gtin_items.append(f"{gtin_id}: {gtin_value}")
        
        gtin_text = "\n".join(gtin_items)
        
        # Format the AMPP details (limit to 100 for token constraints)
        ampp_items = []
        for apid, desc in ampp_details[:100]:
            ampp_items.append(f"{apid}: {desc}")
        
        ampp_text = "\n".join(ampp_items)
        
        # Create the prompt
        prompt = f"""
        Match each GTIN (Global Trade Item Number) to the most appropriate AMPP (Actual Medicinal Product Pack).
        
        GTINs to match:
        {gtin_text}
        
        Available AMPPs:
        {ampp_text}
        
        For each GTIN, return the APID of the matching AMPP. If no match is found, return null.
        
        Return a JSON object where each key is the GTIN ID and each value is the matching APID or null.
        Example output format:
        {{
            "12345": 67890,
            "54321": null
        }}
        
        Only provide the JSON response with no additional explanation.
        """
        
        return prompt 