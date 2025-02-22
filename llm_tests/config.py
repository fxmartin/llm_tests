#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: config.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This script provides environement variable management. It provides functionalities to get
    environment variables and check if they are set.
    The script includes robust error handling.

Usage:
    This script is meant to be called from another Python script with the following functions:
        - from XXXXXXX.config import Config
        - then simply use a variable by calling Config.VARIABLE

Requirements:
    - Python 3.x
    - Required libraries (os, dotenv)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""

import os # Import the os module to interact with the operating system
from dotenv import load_dotenv # Import the load_dotenv function from the python-dotenv library

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    A class to manage environment variables. It provides functionalities to get environment variables
    and check if they are set.
    The class includes robust error handling.

    Attributes:
        LOG_LEVEL (str): The logging level ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG').
        REASONING_MODEL_ID (str): The ID of the reasoning model to be used.
        OLLAMA_CALL_FRAMEWORK (str): The ollama calling method (API, OLLAMA)
        OLLAMA_API_URL (str): The Ollama local url
        MODEL_TEMPERATURE (float): Controls the randomness of the generated text.
	        Lower values (e.g., 0.2) produce more deterministic and focused responses, ideal for factual
            or precise tasks. Higher values (e.g., 0.8) encourage creativity and variability, suitable for
            storytelling or brainstorming.
            Recommended value: 0.7 (balanced between creativity and reliability).
        MODEL_TOP_K (int): Limits the model's choices to the top k most likely tokens.
	        A lower value (e.g., 10) results in more conservative outputs, while a higher value (e.g., 50-100)
            produces diverse responses.
            Recommended value: 40-50 (moderate diversity).
        MODEL_TOP_P (float): Considers tokens within a cumulative probability mass of p (e.g., 0.9 includes
            tokens until their combined probability reaches 90%). Balances diversity and focus; lower values
            (e.g., 0.5) generate more focused outputs, while higher values (e.g., 0.9) allow for more variety.
            Recommended value: 0.8-0.9 (good balance of focus and variety).
        NUM_PREDICT (int): Defines the maximum number of tokens the model can generate in its response.
	        A smaller value (e.g., 50-100) limits verbosity, while larger values allow for extended text
            generation. Setting it to `-1` enables infinite generation within the context window.
            Recommended value: Num_predict: 128-256 (sufficient for most conversational or content generation tasks).
    """

    @staticmethod
    def get_env_variable(name, default=None, var_type=str):
        """
        Retrieve an environment variable and cast it to the specified type.

        :param name: Name of the environment variable.
        :param default: Default value if the variable is not found.
        :param var_type: Type to cast the variable to (e.g., str, int, bool).
        :return: The value of the environment variable or the default value.
        """
        value = os.getenv(name, default)

        # Convert value to the specified type
        try:
            if var_type == bool:
                return value.lower() in ["true", "1", "yes"] if isinstance(value, str) else bool(value)
            return var_type(value)
        except ValueError:
            raise ValueError(f"Invalid value for environment variable {name}: {value}")

    def _validate_attribute(attribute, valid_options):
        if attribute not in valid_options:
            raise ValueError(
                f"Invalid {attribute}. Must be one of {valid_options}"
            )
    
    # Define the environment variables with default values
    LOG_LEVEL = get_env_variable("LOG_LEVEL", default="CRITICAL")
    _validate_attribute(LOG_LEVEL, ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])
    REASONING_MODEL_ID = get_env_variable("REASONING_MODEL_ID", default="llama3.1:8b")
    OLLAMA_CALL_FRAMEWORK = get_env_variable("OLLAMA_CALL_FRAMEWORK", default="OLLAMA")
    OLLAMA_API_URL = get_env_variable("OLLAMA_API_URL", default="http://localhost:11434/api/generate")
    MODEL_TEMPERATURE = get_env_variable("MODEL_TEMPERATURE", default=0.7, var_type=float)
    MODEL_TOP_K = get_env_variable("MODEL_TOP_K", default=50, var_type=int)
    MODEL_TOP_P = get_env_variable("MODEL_TOP_P", default=0.8, var_type=float)
    NUM_PREDICT = get_env_variable("NUM_PREDICT", default=512, var_type=int)