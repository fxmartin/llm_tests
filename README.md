# Local LLM Testing with Ollama

## Introduction

This repository contains a set of Python scripts designed to test locally hosted large language models (LLMs) using Ollama. The experiment was conducted on a MacBook Pro M3 Max with 48 GB of RAM as part of an exploration into the feasibility of running LLMs locally, their capabilities, and their limitations compared to cloud-based models like ChatGPT.

## Objective

The primary goal of this experiment is to assess the performance, accuracy, and responsiveness of local LLMs running on consumer-grade hardware. Once test results are collected, they are submitted to **ChatGPT-4o** for further analysis and comparison with **ChatGPT** to evaluate:

- **Inference speed** on local hardware vs. cloud-based models.
- **Response accuracy** and coherence.
- **Handling of complex queries** in different domains.
- **Resource consumption** (CPU, GPU, and memory usage).
- **Use cases and practical feasibility** for local deployments.

## Repository Contents

- `llm_test.py` – Core script for running test prompts on a locally hosted LLM via Ollama.
- `.env` – Configuration file for specifying model parameters and test cases.
- For each test case, we provide a structured set of results stored in the **results/** directory. This includes a markdown file containing the collected outputs from the locally hosted LLM, along with key performance metrics such as response time, CPU/GPU utilization, and memory consumption. Additionally, we document the exact prompt submitted to OpenAI’s ChatGPT-4o, along with the locally generated response, to ensure consistency in analysis. Finally, the directory contains the analysis provided by ChatGPT-4o, offering insights into the accuracy, coherence, and overall quality of the local model’s responses in comparison to cloud-based alternatives. This structured approach facilitates a detailed evaluation of local LLM capabilities and helps identify strengths, weaknesses, and potential optimization strategies.

## Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed and configured with a local LLM model
- Required Python dependencies

### Running the Tests

1. Ensure that Ollama is running and the local model is loaded.
2. Modify `.env` to define test cases and parameters.
3. Execute the test script:

   ```
   python llm_test.py
   ````

## Insights and Findings

After running multiple test scenarios, key insights were obtained regarding the feasibility of using local LLMs. These results, documented in `/results`, highlight the trade-offs between performance, accuracy, and resource consumption.

## Future Work

- Expanding test cases with different domains (coding, finance, general knowledge, creative writing).
- Exploring optimization techniques for local model efficiency.
- Investigating hybrid approaches combining local LLMs with cloud-based models.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the MIT License.