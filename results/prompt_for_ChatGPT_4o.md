
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
    
# Tests to compare various LLMs running locally with Ollama
## Large Language Models (LLM) tested
There are 17 models installed locally, which will be tested.
- Model: codestral:22b
- Model: deepscaler:latest
- Model: deepseek-r1:14b
- Model: deepseek-r1:32b
- Model: deepseek-r1:7b
- Model: dolphin3:latest
- Model: gemma2:latest
- Model: llama3.1:8b
- Model: llama3:latest
- Model: llava:latest
- Model: mistral-small:24b
- Model: o639/Dolphin3.0-Mistral-24B-Q6_K_L:latest
- Model: openthinker:32b
- Model: openthinker:7b
- Model: phi4:14b
- Model: qwen2.5-coder:latest
- Model: qwen2.5:14b

For each model, the various test cases will be executed and the result, duration and number of tokens collected.
The consolidated results will then be submitted to OpenAI ChatGPT 4o for analysis and comparison.

## Test case: Test case 1 - Easy question

- Prompt: What is the capital of France?

## Test case: Test case 2 - Simple rewrite:

- Prompt: 
            Rewrite the following message into a professional and well-structured email
            suitable for communication with C-level executives or senior leadership.
            Ensure the tone is clear, concise, and appropriately formal while maintaining
            the original intent. The email should reflect a structured approach, including
            a subject line, a clear introduction, body, and a polite closing.

            If the original text is very brief (only a couple of lines), refine it without
            overcomplicating—keep it succinct while ensuring it remains polished and professional.
            Text to rewrite:
            Hey, I saw the document you sent, but I think we need to change a few
            things. Some parts are unclear, and we should probably add more details
            in section 3. Let me know when you can update it. Thanks.
            

## Test case: Test case 3 - Slightly more complex rewrite

- Prompt: 
            Rewrite the following message into a professional and well-structured email
            suitable for communication with C-level executives or senior leadership.
            Ensure the tone is clear, concise, and appropriately formal while maintaining
            the original intent. The email should reflect a structured approach, including
            a subject line, a clear introduction, body, and a polite closing.

            If the original text is very brief (only a couple of lines), refine it without
            overcomplicating—keep it succinct while ensuring it remains polished and professional.
            Text to rewrite:
            Hey, we've been reviewing the project timeline, and I don't think we can meet the
            original deadline. The integration is taking longer than expected, and we've run
            into some unforeseen technical issues. I know this isn't ideal, but we might need
            more time. Maybe we can extend the deadline by two weeks? Let me know if that's
            possible. Thanks.
            

## Test case: Test case 4 - Document summarising

- Prompt: 
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
    