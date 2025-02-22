#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: tests_cases.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This script contains the prompts to be used for the various tests cases.

Usage:
    This script is meant to be called from another Python script to initialise the tests cases

Requirements:
    - Python 3.x
    - Required libraries (logging)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""

from llm_tests.logging import Logger # Import the logging module

Logger.debug("tests_cases: Initialising")

# Structured list of prompts tailored for a comprehensive evaluation of LLMs
# Where each capability has a list of related questions

class TestCases:
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

    testcases = {
        "Test case 1 - Easy question": [
            "What is the capital of France?"
        ],
        "Test case 2 - Simple rewrite:": [
            """
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
            """
        ],
        "Test case 3 - Slightly more complex rewrite": [
            """
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
            """
        ],
        "Test case 4 - Document summarising": [
            """
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
        ]
    }

    Logger.debug("TestCases: Class TestCases properly initialised")

    # A classs to display the questionnaires
    @staticmethod 
    def print_questionnaire():
        for capability, questions in TestCases.questionnaire.items():
            print(f"Capability: {capability}")
            for question in questions:
                print(f"  - {question}")
                print()

    def print_testcases():
        for testcase, prompts in TestCases.testcases.items():
            print(f"Test case: {testcase}")
            for prompt in prompts:
                print(f"  - {prompt}")
                print()