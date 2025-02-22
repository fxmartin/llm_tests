#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: chatgpt.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This script contains the prompt used to get the results analysis from OpenAI ChatGPT o4.

Usage:
    This script is meant to be called from another Python script.

Requirements:
    - Python 3.x
    - Required libraries (os, dotenv)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""

from llm_tests.logging import Logger # Import the logging module

Logger.debug("chatgpt: Initialising")

# Prompt used to get the results analysis

class Analysis:
    ChatGPT_Start_Prompt = """
    # Prompt: Comparative Analysis of Local LLM Performance (vs. ChatGPT)
    ## Objective:
        Analyze the performance of 15 different locally run LLMs based on response time (duration), token usage,
        and overall efficiency. Additionally, compare each test case result with ChatGPT's responses to evaluate
        differences in quality, coherence, and efficiency.
        When analyzing response quality, do not consider any text enclosed within <think></think> tags.
        The output should include:
	        1. An executive summary summarizing key findings.
	        2. A comparative analysis highlighting performance trends, best/worst performers, and insights.
	        3. A structured array with the following columns:
	            - LLM Name
	            - Test Case Name
	            - Duration (seconds)
	            - Number of Tokens Used
	            - Overall Rating (relative ranking based on efficiency and response quality).
	        4. A comparison with ChatGPT for each test case, assessing:
	            - Response Similarity: How closely the LLM's output matches ChatGPT's in terms of correctness,
                coherence, and completeness.
	            - Efficiency Difference: Speed and token usage compared to ChatGPT.
	        5. A conclusion with final recommendations.
        
        Here are the results to analyse:
    """

    ChatGPT_End_Prompt = """
    
    Evaluation Criteria:
	    - Response Speed: Faster models score higher.
	    - Token Efficiency: Models using fewer tokens for the same result score higher.
	    - Quality vs. ChatGPT: How well the responses compare in clarity, accuracy, and depth.
	    - Overall Rating: A ranking based on a balanced evaluation of speed, token usage, and response quality.

    Expected Output Format:
	    1. Executive Summary - A concise summary of the key findings, including top-performing and underperforming models.
	    2. Comparative Analysis - A deeper breakdown of the differences between LLMs, including trends, anomalies, and
        efficiency insights.
	    3. Structured Array - A table format with LLM performance metrics.
	    4. Comparison with ChatGPT - Evaluation of each model's response quality relative to ChatGPT.
	    5. Conclusion - Recommendations on which models to use based on performance and use case suitability.
    """

    def prompt(self, results: str):
        return (Analysis.ChatGPT_Start_Prompt + "\n" + results + "\n" + Analysis.ChatGPT_End_Prompt)