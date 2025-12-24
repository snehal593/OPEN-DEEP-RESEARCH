OpenDeepResearcher: An Agentic Multi-Agent Research Framework
________________________________________
1. Project Overview
OpenDeepResearcher is an autonomous AI-driven research assistant designed to bridge the gap between static Large Language Models (LLMs) and the dynamic nature of the live web. Traditional LLMs are limited by knowledge cutoffs; this project solves that by utilizing an Agentic Workflow to autonomously plan, browse, and synthesize information into high-quality research reports.
Core Objective: To simulate a human researcher’s cognitive process—breaking down complex queries into logical sub-tasks, retrieving verified data from credible sources, and producing a grounded, hallucination-free summary.
________________________________________
2. Software and Hardware Dependencies
Software Dependencies
•	Programming Language: Python 3.10+

•	Orchestration Framework: LangGraph (for state machine management)

•	LLM Integration: LangChain & Groq (Llama-3.1-8b-instant)

•	Web Search Engine: Tavily AI (optimized for AI agents)

•	Frontend UI: Streamlit

•	Data Parsing: BeautifulSoup4, PyPDF, python-docx

•	Validation: Pydantic (for structured JSON outputs)

Hardware Dependencies
•	Minimum: 8GB RAM | Dual-core CPU.

•	Optimal: 16GB RAM (for concurrent agent processing).

•	Internet: High-speed connection required for real-time API-based web crawling.
________________________________________
3. Architecture Diagram

________________________________________
4. Workflow
The system utilizes a Directed Acyclic Graph (DAG) to manage the logic flow:
a.	Entry Point: The user submits a research topic or a file.

b.	Routing: A Router Node determines if the query requires a Full Research path or a Follow-up Analysis path based on chat history.
	
c.	Planning: The Planner Agent generates a multi-step roadmap.

d.	Searching: The Searcher Agent executes parallel web queries via Tavily.

e.	Writing: The Writer Agent synthesizes raw findings into a structured report.

f.	Persistence: The state is saved to a local database for continuity.
________________________________________
5. Agent Roles
•	Planner Agent: Decomposes a vague research prompt into 3-5 distinct sub-questions using Structured Output (Pydantic). This ensures the research is comprehensive and targeted.

•	Searcher Agent: Acting as the "eyes" of the system, it crawls the web. It is programmed to filter results based on the user's preference (e.g., Scholarly vs. General News).

•	Writer Agent: The "synthesizer." It performs Information Fusion, taking fragmented snippets and converting them into a professional Markdown report with chronological flow and citations.

•	Execution Graph: Managed via LangGraph, it ensures that data flows seamlessly from one agent to the next using a shared TypedDict state.
________________________________________
6. Sample Working Demo
Example Prompt: "Analyze the impact of Quantum Computing on current Cybersecurity encryption."
•	Planner Output: Generates questions on RSA vulnerability, Post-Quantum Cryptography (PQC), and NIST standards.

•	Searcher Output: Retrieves snippets from recent research papers and tech journals.

•	Final Report: A structured 700-word report with dedicated sections on "Current Risks" and "Mitigation Strategies."
________________________________________
7. Outputs / Results
The system generates:
•	Structured Research Reports: Comprehensive Markdown documents with auto-generated titles.

•	Follow-up Insights: Short-form answers based on the context of previous reports.

•	Context-Aware Analysis: Summaries that combine uploaded PDF/Docx content with live web data.
________________________________________
8. Future Enhancements
•	Vector DB Integration: Implementing ChromaDB for long-term memory of all researched topics.

•	Multi-Modality: Enabling the agent to "see" and describe charts/graphs within uploaded PDFs.

•	Asynchronous Processing: Speeding up the search agent by 300% using asyncio for parallel web requests.
________________________________________
9. Deployed Project Link
•	Live App:"https://open-deep-research-a4pbbsas6ssq5szmn5ou4k.streamlit.app/"
