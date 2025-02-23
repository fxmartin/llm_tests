#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: llm_tests.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This python program is designed to automate the execution of tests cases with locally run LLMs.

Usage:
    Launched the script without any parameters.
    Environment variables can be changed in the .env file.
    test cases are defined in the file llm_tests\test_cases.py where you can find the various prompts used.
    The script use ollama list to test the locally pulled models.
    The final results is printed in the terminal and copied into the clipboard for easy pasting into a markdown document.
    There are two copy/paste done:
        1. the first with only the results
        2. the second with the prompt used to ask ChatGPT for analysis of the results.

Requirements:
    - Python 3.x
    - Required libraries (time, requests, ollama, json, pyperclip, re)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""
import time
import requests
import ollama
import json
from llm_tests.config import Config
from llm_tests.logging import Logger
from llm_tests.test_cases import TestCases
from llm_tests.display import ColoramaWrapper
from llm_tests.chatgpt import Analysis
import pyperclip
import re

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
#       str: The initial text without formatting
def colorPrint(text: str, color: str = None, background: str = None, style: str = None):
    print(display.color_text(text, color, background, style) + display.reset())
    return(text)

# Write a string to a file.
#   Args:
#       filepath (str): The file.
#       content (str): The string to write into the file.
def write_to_file(file_path, content):
    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as f:
            # Write the content to the file
            f.write(content)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")

    except PermissionError:
        print(f"Error: You do not have permission to write to the file '{file_path}'.")

    except Exception as e:
        # Catch any other exceptions that may occur
        print(f"An unexpected error occurred while writing to file '{file_path}': {str(e)}")

if __name__ == "__main__":
    
    # Instanciate the ColoramaWrapper class
    display = ColoramaWrapper()
    clipboard = ""
    clipboard += colorPrint( "# Tests to compare various LLMs running locally with Ollama", color="blue", style="bright")
    clipboard += "\n" + colorPrint("## Large Language Models (LLM) tested", color="blue", style="bright")
    models = list_models()
    clipboard += "\n" + colorPrint("There are " + str(len(models)) + " models installed locally, which will be tested.")
    models.sort()
    for model in models:
        clipboard += "\n" + colorPrint("- Model: " + model)
    clipboard += "\n" + colorPrint("")
    clipboard += "\n" + colorPrint("For each model, the various test cases will be executed and the result, duration and number of tokens collected.")
    clipboard += "\n" + colorPrint("The consolidated results will then be submitted to OpenAI ChatGPT 4o for analysis and comparison.")
    clipboard += "\n" + colorPrint("")
    
    header = clipboard

    # Start of tests
    for testcase, prompts in TestCases.testcases.items():
            start_time = time.time()
            clipboard += "\n" + colorPrint("## Test case: " + testcase + "\n")
            for prompt in prompts:
                clipboard += "\n" + colorPrint("- Prompt: " + prompt+ "\n")
                for model in models:
                    clipboard += "\n\n" + colorPrint("### Model: " + model)
                    response = query_ollama_library(
                        model=model,
                        prompt=prompt,
                        temperature=0.7,
                        num_predict=1000
                    )
                    cleaned_response = re.sub(r"<think>.*?</think>", "", response[0])
                    cleaned_response = cleaned_response.strip()
                    clipboard += "\n" + colorPrint("\t- Response: " + cleaned_response)
                    clipboard += "\n" + colorPrint("\t- Duration: " + str(response[1])+" s")
                    clipboard += "\n" + colorPrint("\t- Number of tokens: " + str(response[2]) + "\n")

            # Instanciation of ChatGPT class
            chatgpt = Analysis()

            results = chatgpt.prompt(clipboard)

            end_time = time.time()
            elapsed_time = end_time - start_time
            clipboard += "\n\n" + colorPrint("Total time taken for executing these tests on a Macbook M3 Max with 48 Gb of RAM: " + str(round(elapsed_time,0)) + " seconds.\n")
    
            # Write the results to file
            write_to_file('./results/' + testcase + '_results.md', clipboard)
    
            # Write the results and ChatGPT prompt to file
            write_to_file('./results/' + testcase + '_prompt_for_ChatGPT_4o.md', results)