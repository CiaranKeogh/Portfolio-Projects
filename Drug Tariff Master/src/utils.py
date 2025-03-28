"""
Utility functions for the Drug Tariff Master application.
"""
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import LOGS_DIR


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