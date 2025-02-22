#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: logging.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This script provides logging management. It enhanced it with colorama and read the LOG_LEVEL
    from .env file.

Usage:
    This script is meant to be called from another Python script with the following functions:
        - from XXXXXXX.logging import Config
        - then simply use a variable by calling Config.VARIABLE

Requirements:
    - Python 3.x
    - Required libraries (logging, colorama, llm_tests.config)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""

import logging # Import the logging module
import colorama # Import the colorama library to add colors to terminal output
from llm_tests.config import Config

 
# Initialize colorama
colorama.init(autoreset=True)

# Convert string to logging level
log_level_mapping = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

logging_level = log_level_mapping.get(Config.LOG_LEVEL, logging.CRITICAL)

# Configure logging
logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(levelname)s - %(message)s")
        
logging.debug(colorama.Fore.MAGENTA + "Class Config properly initialised")

class Logger:
    # A class to submit log messages depending on LOG_LEVEL with colors thanks to colorama.
     
    def debug(message:str):
        # Log a DEBUG message with color
        logging.debug(colorama.Fore.MAGENTA + message)
    
    def info(message:str):
        # Log a INFO message with color
        logging.info(colorama.Fore.GREEN + message)

    def warning(message:str):
        # Log a WARNING message with color
        logging.warning(colorama.Fore.RED + message)

    def error(message:str):
        # Log a ERROR message with color
        logging.error(colorama.Fore.RED + message)

    def critical(message:str):
        # Log a CRITICAL message with color
        logging.critical(colorama.Fore.RED + message)