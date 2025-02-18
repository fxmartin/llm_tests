import requests
import logging
from dotenv import load_dotenv
import os
import ollama

# Structured list of prompts tailored for a comprehensive evaluation of LLMs
# Where each capability has a list of related questions
questionnaire = {
    "1. General Knowledge & Fact-Checking": [
        "What are the key economic implications of central bank digital currencies (CBDCs)?",
	    "Summarize the causes and effects of the 2008 global financial crisis.",
	    "Who were the last five CEOs of Goldman Sachs?",
	    "Provide a brief history of artificial intelligence, including key milestones."
    ],
    "2. Reasoning & Problem-Solving": [
        "If a train leaves New York at 8 AM traveling at 80 mph and another leaves Chicago at 9 AM traveling at 100 mph, when and where will they meet?",
	    "A company is experiencing declining profit margins despite increasing revenues. What could be potential reasons?",
	    "You have two jugs: one holds 3 liters, and the other holds 5 liters. How can you measure exactly 4 liters using only these two jugs?"
    ],
    "3. Business & Strategy Analysis": [
        "A major bank is losing customers to digital-first competitors. Outline a strategy to improve customer retention.",
	    "Compare the advantages and disadvantages of a centralized vs. decentralized IT infrastructure for a multinational bank.",
	    "How would you structure a digital transformation roadmap for a 100-year-old financial institution?"
    ]
}

def query_ollama(model: str, prompt: str, temperature: float = 0.7, api_url: str = "http://localhost:11434/api/generate"):
    # Sends a prompt to Ollama's API and returns the response.

    # :param model: The name of the model to use (e.g., 'mistral', 'gemma', etc.).
    # :param prompt: The text prompt to send to the model.
    # :param temperature: Controls randomness (lower = more deterministic).
    # :param api_url: The URL of the Ollama API endpoint (default: localhost).

    # :return: The generated response from the model.

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False  # Change to True for streaming responses
    }

    try:
        logging.info("Calling Ollama with the following parameters:")
        logging.info("\tModel: " + model)
        logging.info("\tTemperature: " + temperature)
        logging.info("\tPrompt: " + prompt)
        logging.info("\tAPI Url: " + api_url)
        response = requests.post(api_url, json=payload)
        
        data = response.json()

        # Extract and convert execution time
        tokens_evaluated = data.get('eval_count', 'N/A')
        total_time_ns = data.get('total_duration', 0)  # Default to 0 if not found
        # total_time_ms = total_time_ns / 1_000_000  # Convert to milliseconds
        total_time_s = total_time_ns / 1_000_000_000  # Convert to seconds

        logging.info(f"Tokens Evaluated: {tokens_evaluated}")
        logging.info(f"Total Execution Time: {total_time_s:.2f} s")  # Display 2 decimal places
        
        response.raise_for_status()
        return response.json().get("response", "No response from Ollama").strip()
        
    except requests.exceptions.RequestException as e:
        logging.error("Error connecting to Ollama API")
        return f"Error connecting to Ollama API: {e}"
    
if __name__ == "__main__":
    load_dotenv() # Load environment variables from .env file

    # Get logging level from .env, default to WARNING if not set
    log_level = os.getenv("LOG_LEVEL", "WARNING").upper()

    # Convert string to logging level
    log_level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    logging_level = log_level_mapping.get(log_level, logging.WARNING)

    # Configure logging
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Retrieve the .env variables
    logging.debug("Loading the .env variables")
    reasoning_model_id = os.getenv("REASONING_MODEL_ID")
    logging.debug("REASONING_MODEL_ID = " + reasoning_model_id)
    ollama_api_url = os.getenv("OLLAMA_API_URL")
    logging.debug("OLLAMA_API_URL = " + ollama_api_url)
    
    # Display the qestionnaire
    for capability, questions in questionnaire.items():
        print(f"Capability: {capability}")
        for question in questions:
            print(f"  - {question}")
        print()
    
    # Fetch the list of available models
    models = ollama.list()
    
    # Extract model names
    models_list = [model['model'] for model in models['models']]

    # Print the list of models
    print("Available Local Models in Ollama:")
    for model in models_list:
        print(f"- {model}")