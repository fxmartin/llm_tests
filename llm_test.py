import time
import requests
import ollama
import json
from llm_tests.config import Config
from llm_tests.logging import Logger
from llm_tests.test_cases import TestCases
from llm_tests.display import ColoramaWrapper
import pyperclip

# Retrieve the .env variables
Logger.debug("Environment Variables retrieved from .env file")
Logger.debug("\tLOG_LEVEL = " + Config.LOG_LEVEL)
Logger.debug("\tREASONING_MODEL_ID = " + Config.REASONING_MODEL_ID)
Logger.debug("\tOLLAMA_CALL_FRAMEWORK = " + Config.OLLAMA_CALL_FRAMEWORK)
Logger.debug("\tOLLAMA_API_URL = " + Config.OLLAMA_API_URL)
Logger.debug("\tMODEL_TEMPERATURE = " + str(Config.MODEL_TEMPERATURE))
Logger.debug("\tMODEL_TOP_K = " + str(Config.MODEL_TOP_K))
Logger.debug("\tMODEL_TOP_P = " + str(Config.MODEL_TOP_P))
Logger.debug("\tNUM_PREDICT = " + str(Config.NUM_PREDICT))

def query_ollama_api(model: str, prompt: str, temperature: float = Config.MODEL_TEMPERATURE, api_url: str = Config.OLLAMA_API_URL):
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
        Logger.info("Calling Ollama with the following parameters:")
        Logger.info("\tModel: " + model)
        Logger.info("\tTemperature: " + temperature)
        Logger.info("\tPrompt: " + prompt)
        Logger.info("\tAPI Url: " + api_url)
        response = requests.post(api_url, json=payload)
        
        data = response.json()

        # Extract and convert execution time
        tokens_evaluated = data.get('eval_count', 'N/A')
        total_time_ns = data.get('total_duration', 0)  # Default to 0 if not found
        # total_time_ms = total_time_ns / 1_000_000  # Convert to milliseconds
        total_time_s = total_time_ns / 1_000_000_000  # Convert to seconds

        Logger.info(f"Tokens Evaluated: {tokens_evaluated}")
        Logger.info(f"Total Execution Time: {total_time_s:.2f} s")  # Display 2 decimal places
        
        response.raise_for_status()
        return response.json().get("response", "No response from Ollama").strip()
        
    except requests.exceptions.RequestException as e:
        Logger.error("Error connecting to Ollama API")
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
        Logger.error("Error retrieving models:" + str(e))

def query_ollama_library(model: str, prompt: str, temperature: float = Config.MODEL_TEMPERATURE, num_predict: float = Config.NUM_PREDICT):
    # Sends a prompt via ollama python library and returns the response.

    # :param model: The name of the model to use (e.g., 'mistral', 'gemma', etc.).
    # :param prompt: The text prompt to send to the model.
    # :param temperature: Controls randomness (lower = more deterministic).
    # :param num_predict: # Maximum number of tokens to generate

    # :return: The generated response from the model.

    try:
        Logger.info("Calling Ollama with the following parameters:")
        Logger.info("\tModel: " + model)
        Logger.info("\tTemperature: " + str(temperature))
        Logger.info("\tPrompt: " + prompt)
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": temperature,  # Controls randomness (0 = deterministic, 1 = max randomness)
                "top_k": 50,         # Limits sampling to top-K most likely tokens
                "top_p": 0.9,        # Nucleus sampling (alternative to top_k)
                "num_predict": num_predict     # Maximum number of tokens to generate
            },
            stream=False
        )
    
        # Extract and convert execution time
        tokens_evaluated = str(response['eval_count'])
        total_time_ns = response['total_duration']
        total_time_s = total_time_ns / 1_000_000_000  # Convert to seconds

        Logger.info(f"Tokens Evaluated: {tokens_evaluated}")
        Logger.info(f"Total Execution Time: {total_time_s:.2f} s")  # Display 2 decimal places

        return [response['response'], round(total_time_s,2), tokens_evaluated]
    
    except requests.exceptions.RequestException as e:
        Logger.error("Error calling Ollama")
        return f"Error calling Ollama: {e}"

# Display the text with the colorama codes and return the text without any formatting.
#   Args:
#       text (str): The text to style.
#       color (str): The foreground color (e.g., "RED", "GREEN").
#       background (str): The background color (e.g., "BLACK", "YELLOW").
#       style (str): The text style (e.g., "BRIGHT", "DIM").
#
#   Returns:
#   str: The initial text without formatting
def colorPrint(text: str, color: str = None, background: str = None, style: str = None):
    print(display.color_text(text, color, background, style) + display.reset())
    return(text)

if __name__ == "__main__":
    # Instanciate the ColoramaWrapper class
    display = ColoramaWrapper()
    clipboard = ""
    clipboard += colorPrint( "# Tests to compare various LLMs running locally with Ollama", color="blue", style="bright")
    clipboard += "\n" + colorPrint("## 1. Models tests", color="blue", style="bright")
    models = list_models()
    clipboard += "\n" + colorPrint("There are " + str(len(models)) + " models install locally, which will be tested.")
    models.sort()
    for model in models:
        clipboard += "\n" + colorPrint("- Model: " + model)
    clipboard += "\n" + colorPrint("")
    clipboard += "\n" + colorPrint("For each model, the various test cases will be executed and the result, duration and number of tokens collected.")
    clipboard += "\n" + colorPrint("The consolidated results will then be submitted to OpenAI ChatGPT 4o for analysis and comparison.")
    pyperclip.copy (clipboard)

    """
    print("Prompt used for the test: " + prompt)
    for model in list_models():
        print("Model: " + model)
        response = query_ollama_library(
            model=model,
            prompt=prompt,
            temperature=0.7,
            num_predict=1000
        )
        print("Response: " + response[0])
        print("Duration: " + str(response[1]) + " s")
        print("Number of tokens: " + str(response[2]))
"""