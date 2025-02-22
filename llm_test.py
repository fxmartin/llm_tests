import time
import requests
import ollama
import json
from llm_tests.config import Config
from llm_tests.logging import Logger

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

if __name__ == "__main__":

    # Display the qestionnaire
    # for capability, questions in questionnaire.items():
    #    print(f"Capability: {capability}")
    #    for question in questions:
    #        print(f"  - {question}")
    #    print()
    
    # Test 1
    # prompt = "What is the capital of France?"

    # Test 2
    # prompt = """
    #    Rewrite the following message into a professional and well-structured email
    #    suitable for communication with C-level executives or senior leadership.
    #    Ensure the tone is clear, concise, and appropriately formal while maintaining
    #    the original intent. The email should reflect a structured approach, including
    #    a subject line, a clear introduction, body, and a polite closing.
    #
    #    If the original text is very brief (only a couple of lines), refine it without
    #    overcomplicating—keep it succinct while ensuring it remains polished and professional.
    #    Text to rewrite:
    #    Hey, I saw the document you sent, but I think we need to change a few
    #    things. Some parts are unclear, and we should probably add more details
    #    in section 3. Let me know when you can update it. Thanks.
    #    """

    # Test 3
    # prompt = """
    #    Rewrite the following message into a professional and well-structured email
    #    suitable for communication with C-level executives or senior leadership.
    #    Ensure the tone is clear, concise, and appropriately formal while maintaining
    #    the original intent. The email should reflect a structured approach, including
    #    a subject line, a clear introduction, body, and a polite closing.
    #
    #    If the original text is very brief (only a couple of lines), refine it without
    #    overcomplicating—keep it succinct while ensuring it remains polished and professional.
    #    Text to rewrite:
    #    Hey, we've been reviewing the project timeline, and I don't think we can meet the
    #    original deadline. The integration is taking longer than expected, and we've run
    #    into some unforeseen technical issues. I know this isn't ideal, but we might need
    #    more time. Maybe we can extend the deadline by two weeks? Let me know if that's
    #    possible. Thanks.
    #"""
    
    # Test 4 - Summarising a long text
    prompt = """
        Summarize the following long business document into a structured, concise, and
        professional executive summary. Ensure that the summary highlights key takeaways,
        strategic implications, and any critical action points. Maintain clarity while
        reducing complexity, and focus on the most relevant information for senior
        leadership decision-making.
        Text to summarise:
        Title: Strategic Review of Core Banking Transformation – 2024 Insights
        The global banking landscape is undergoing a significant transformation driven by digitalization,
        regulatory shifts, and evolving customer expectations. Financial institutions are accelerating their
        core banking modernization efforts to remain competitive. This report examines key trends, challenges,
        and opportunities shaping core banking transformation strategies in 2024.
	    1.	Market Trends & Industry Drivers
        1.1 Acceleration of Cloud Adoption
        Banks are increasingly migrating to cloud-native core banking platforms to enhance scalability,
        security, and operational efficiency. Hybrid and multi-cloud strategies are gaining traction,
        reducing dependency on legacy infrastructure.
        1.2 Embedded Finance & Open Banking
        The rise of API-driven ecosystems is enabling greater collaboration between banks, fintechs,
        and third-party providers. Regulatory mandates such as PSD2 and Open Banking initiatives continue
        to push banks toward open financial ecosystems.
        1.3 AI and Automation in Core Banking
        AI-driven fraud detection, predictive analytics for risk management, and automated workflows are
        becoming central to banking operations. Banks leveraging AI for personalized banking experiences
        are seeing increased customer retention.
	    2.	Challenges in Core Banking Transformation
        2.1 Legacy System Limitations
        Many banks still operate on monolithic core banking architectures, leading to high maintenance
        costs and slow innovation cycles. Migration complexity remains a key barrier to cloud adoption.
        2.2 Regulatory Compliance & Security Risks
        New data privacy laws, including GDPR, CCPA, and emerging AI regulations, require continuous
        adaptation in banking operations. Cybersecurity threats are intensifying, demanding robust identity
        verification and threat intelligence solutions.
        2.3 Cost & ROI Concerns
        Core banking modernization is capital-intensive, requiring long-term cost-benefit justifications
        to gain executive buy-in. Banks face pressure to balance innovation investments with operational
        cost optimization.
	    3.	Strategic Recommendations for Banks in 2024
        3.1 Phased Approach to Cloud Migration
        Banks should adopt a progressive migration strategy to reduce risks associated with core system
        overhauls. Composable banking architectures can provide flexibility while integrating with existing
        systems.
        3.2 Strengthening AI & Automation in Operations
        Financial institutions should prioritize AI governance frameworks to ensure ethical AI usage in
        customer interactions. Automated regulatory reporting can reduce compliance burdens while improving
        accuracy.
        3.3 Enhancing Cybersecurity & Regulatory Preparedness
        Proactive investments in zero-trust security models and AI-driven fraud detection can mitigate
        emerging cyber threats. Regular compliance audits should be embedded into digital transformation
        roadmaps.
	    4.	Conclusion: The Path Forward for Banking Leaders
        As banks navigate core banking transformation, balancing innovation with risk management remains
        critical. Cloud adoption, AI-driven automation, and regulatory agility will be the key differentiators
        for banks seeking long-term growth. Financial institutions that embrace modular core banking, API
        ecosystems, and security-first strategies will outpace competitors and drive sustainable transformation
        in 2024 and beyond.
    """

    print("There are " + str(len(list_models())) + " models to test")
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