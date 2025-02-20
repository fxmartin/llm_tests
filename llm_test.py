import logging
import time
import requests
from dotenv import load_dotenv
import os
import ollama
import colorama
import json

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

# Initialize colorama
colorama.init(autoreset=True)

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
    format="%(asctime)s - %(levelname)s - %(message)s")
    
# Retrieve the .env variables
logging.info(colorama.Fore.GREEN + "Loading the .env variables")
logging.info(colorama.Fore.GREEN + "\tLOG_LEVEL = " + log_level)
reasoning_model_id = os.getenv("REASONING_MODEL_ID")
logging.info(colorama.Fore.GREEN + "\tREASONING_MODEL_ID = " + reasoning_model_id)
ollama_call_framework = os.getenv("OLLAMA_CALL_FRAMEWORK")
logging.info(colorama.Fore.GREEN + "\tOLLAMA_CALL_FRAMEWORK = " + ollama_call_framework)
ollama_api_url = os.getenv("OLLAMA_API_URL")
logging.info(colorama.Fore.GREEN + "\tOLLAMA_API_URL = " + ollama_api_url)

def query_ollama_api(model: str, prompt: str, temperature: float = 0.7, api_url: str = "http://localhost:11434/api/generate"):
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
        logging.info(colorama.Fore.GREEN + "Calling Ollama with the following parameters:")
        logging.info(colorama.Fore.GREEN + "\tModel: " + model)
        logging.info(colorama.Fore.GREEN + "\tTemperature: " + temperature)
        logging.info(colorama.Fore.GREEN + "\tPrompt: " + prompt)
        logging.info(colorama.Fore.GREEN + "\tAPI Url: " + api_url)
        response = requests.post(api_url, json=payload)
        
        data = response.json()

        # Extract and convert execution time
        tokens_evaluated = data.get('eval_count', 'N/A')
        total_time_ns = data.get('total_duration', 0)  # Default to 0 if not found
        # total_time_ms = total_time_ns / 1_000_000  # Convert to milliseconds
        total_time_s = total_time_ns / 1_000_000_000  # Convert to seconds

        logging.info(colorama.Fore.GREEN + f"Tokens Evaluated: {tokens_evaluated}")
        logging.info(colorama.Fore.GREEN + f"Total Execution Time: {total_time_s:.2f} s")  # Display 2 decimal places
        
        response.raise_for_status()
        return response.json().get("response", "No response from Ollama").strip()
        
    except requests.exceptions.RequestException as e:
        logging.error(colorama.Fore.RED + "Error connecting to Ollama API")
        return f"Error connecting to Ollama API: {e}"

def list_models():
    try:
        # Fetch the list of available models
        models_data = ollama.list()

        # Extract and display model names
        if "models" in models_data:
            model_names = [model["model"] for model in models_data["models"]]
            return model_names
        else:
            print("No models found.")
            return None

    except Exception as e:
        logging.error(colorama.Fore.RED + "Error retrieving models:" + str(e))

def query_ollama_library(model: str, prompt: str, temperature: float = 0.7):
    # Sends a prompt via ollama python library and returns the response.

    # :param model: The name of the model to use (e.g., 'mistral', 'gemma', etc.).
    # :param prompt: The text prompt to send to the model.
    # :param temperature: Controls randomness (lower = more deterministic).
    # :param api_url: The URL of the Ollama API endpoint (default: localhost).

    # :return: The generated response from the model.

    try:
        logging.info(colorama.Fore.GREEN + "Calling Ollama with the following parameters:")
        logging.info(colorama.Fore.GREEN + "\tModel: " + model)
        logging.info(colorama.Fore.GREEN + "\tTemperature: " + str(temperature))
        logging.info(colorama.Fore.GREEN + "\tPrompt: " + prompt)
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": temperature,  # Controls randomness (0 = deterministic, 1 = max randomness)
                "top_k": 50,         # Limits sampling to top-K most likely tokens
                "top_p": 0.9,        # Nucleus sampling (alternative to top_k)
                "num_predict": 50     # Maximum number of tokens to generate
            },
            stream=False
        )
    
        # Extract and convert execution time
        tokens_evaluated = str(response['eval_count'])
        total_time_ns = response['total_duration']
        total_time_s = total_time_ns / 1_000_000_000  # Convert to seconds

        logging.info(colorama.Fore.GREEN + f"Tokens Evaluated: {tokens_evaluated}")
        logging.info(colorama.Fore.GREEN + f"Total Execution Time: {total_time_s:.2f} s")  # Display 2 decimal places

        return response['response']
    
    except requests.exceptions.RequestException as e:
        logging.error(colorama.Fore.RED + "Error calling Ollama")
        return f"Error calling Ollama: {e}"

if __name__ == "__main__":

    # Display the qestionnaire
    # for capability, questions in questionnaire.items():
    #    print(f"Capability: {capability}")
    #    for question in questions:
    #        print(f"  - {question}")
    #    print()
    
    for model in list_models():
        print(model)
        print(query_ollama_library(
            model=model,
            prompt='What is the capital of France?',
        ))
    
    