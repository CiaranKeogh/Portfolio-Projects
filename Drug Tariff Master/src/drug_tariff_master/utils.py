"""
Utility functions for the Drug Tariff Master application.
"""
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Any, Union

from drug_tariff_master.config import LOGS_DIR


def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up and return a logger with the given name.
    
    Args:
        name: The name of the logger.
        log_file: Optional log file name. If not provided, will use name.log.
    
    Returns:
        A configured logger instance.
    """
    if log_file is None:
        log_file = f"{name}.log"
    
    log_path = LOGS_DIR / log_file
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create handlers
    file_handler = logging.FileHandler(log_path)
    console_handler = logging.StreamHandler()
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatters to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 

# XML Data Extraction and Conversion Helper Functions
logger = setup_logger("drug_tariff_master.utils")

def find_text_safe(element: Any, tag: str, default: Any = None) -> Optional[str]:
    """
    Safely get the text content of a direct child element with a specific tag name.
    Avoids AttributeError if the tag or its text is missing.
    
    Args:
        element: The parent lxml.etree._Element object to search within.
        tag: A string representing the tag name of the child element (e.g., "NM", "VTMID").
        default: The value to return if the tag is not found or has no text (defaults to None).
    
    Returns:
        A string (the element's text) or the default value.
    """
    child = element.find(tag)
    if child is not None and child.text is not None:
        return child.text.strip()
    return default

def safe_int(value: Any, default: Any = None) -> Optional[int]:
    """
    Safely convert a value into an integer.
    Avoids ValueError if the conversion fails.
    
    Args:
        value: The input value (potentially a string like "123", "abc", None, or "").
        default: The value to return if the input is None, empty, or cannot be
                 converted to an int (defaults to None).
    
    Returns:
        An integer or the default value.
    """
    if value is None or value == "":
        return default
    
    try:
        return int(value)
    except ValueError:
        logger.warning(f"Could not convert '{value}' to int.")
        return default

def safe_float(value: Any, default: Any = None) -> Optional[float]:
    """
    Safely convert a value into a float.
    Avoids ValueError if the conversion fails.
    
    Args:
        value: The input value (potentially a string like "123.45", "abc", None, or "").
        default: The value to return on failure (defaults to None).
    
    Returns:
        A float or the default value.
    """
    if value is None or value == "":
        return default
    
    try:
        return float(value)
    except ValueError:
        logger.warning(f"Could not convert '{value}' to float.")
        return default

def safe_int_bool(value: Any, default: Any = None) -> Optional[int]:
    """
    Safely convert a value representing a boolean (typically "0" or "1" in dm+d XML)
    into an integer (0 or 1).
    Avoids ValueError if the conversion fails.
    
    Args:
        value: The input value (potentially "0", "1", None, "", or other text).
        default: The value to return on failure (defaults to None).
    
    Returns:
        An integer (0 or 1) or the default value.
    """
    if value is None or value == "":
        return default
    
    try:
        result = int(value)
        if result in (0, 1):
            return result
        else:
            logger.warning(f"Unexpected boolean integer value: {result}")
            return default
    except ValueError:
        logger.warning(f"Could not convert '{value}' to boolean int.")
        return default 