**OpenDeepResearcher: Agentic LLM Research Framework**
________________________________________
**1. Project Overview**

The OpenDeepResearcher is an autonomous AI system designed to conduct comprehensive web-based research.Unlike traditinal RAG(Retrieval-Augmented Generation) systems that perform simple keyword lookups,this project implements a **Multi_Agent WorkFlow**. It mimics a human research process by planning a strategy, searching multiple sources and synthesizing a structed report with citations.

**Core Objective:** The goal was to solve the "hallucination" and "recency" problem of LLMs. By integrating Tavily’s Search API with a multi-agent state machine, the system ensures every claim in a research report is backed by real-time data and filtered through a multi-step verification process.
________________________________________
**2. Software and Hardware Dependencies**

**Software Dependencies**

**•**	Programming Language: Python 3.10+

**•**	Orchestration Framework: LangGraph (for state machine management)

**•**	LLM Integration: LangChain & Groq (Llama-3.1-8b-instant)

**•**	Web Search Engine: Tavily AI (optimized for AI agents)

**•**	Frontend UI: Streamlit

**•**	Data Parsing: BeautifulSoup4, PyPDF, python-docx

**•**	Validation: Pydantic (for structured JSON outputs)

**Hardware Dependencies**

**•**	Minimum: 8GB RAM | Dual-core CPU.

**•**	Optimal: 16GB RAM (for concurrent agent processing).

**•**	Internet: High-speed connection required for real-time API-based web crawling.
________________________________________
**3. Installation & Setup**

|**1. Clone the repository:**|
|--- |
|git clone https://github.com/your-username/OpenDeepResearcher.git|
|cd OpenDeepResearcher|


|2. Create a Virtual environment:|
|---  |
|python -m venv venv|
|source venv/bin/activate  | # On Windows: venv\Scripts\activate|


|**3. Install Dependencies:**|
|---  |
|pip install -r requirements.txt|


|**4. Environment Variables: Create a .env file or export your keys:**|
|---  |
|export GROQ_API_KEY='your_key_here'|
|export TAVILY_API_KEY='your_key_here'|


|**5. Run the Application:**|
|---  |
|streamlit run main.py|
________________________________________
**4. Architecture Diagram**
   
 <img width="800" height="400" alt="Screenshot 2025-12-25 164810" src="https://github.com/user-attachments/assets/c6c7ba9d-2a72-493e-876b-0c7187ff2d9a" />

________________________________________
**5. Agent Roles**

•	**Planner Agent:** Decomposes a vague research prompt into 3-5 distinct sub-questions using Structured Output (Pydantic). This ensures the research is comprehensive and targeted.

•	**Searcher Agent:** Acting as the "eyes" of the system, it crawls the web. It is programmed to filter results based on the user's preference (e.g., Scholarly vs. General News).

•	**Writer Agent:** The "synthesizer." It performs Information Fusion, taking fragmented snippets and converting them into a professional Markdown report with chronological flow and citations.

•	**Execution Graph:** Managed via LangGraph, it ensures that data flows seamlessly from one agent to the next using a shared TypedDict state.
________________________________________
**6.Technical Implementaion Pillars**

•**State Management:** LangGraph TypedDict for cross-agent memory.

•**Structured Outputs:** Pydantic validation for JSON realiability.

•**Real-Time Retrieval:** Tavily API integration for live web grounding.

•**Persistence:** shelve database for seesion history
________________________________________
**7. Workflow**

The system utilizes a Directed Acyclic Graph (DAG) to manage the logic flow: 

1.	**Entry Point:** The user submits a research topic or a file.
   
3.	**Routing:** A Router Node determines if the query requires a Full Research path or a Follow-up Analysis path based on chat history.
   
5.	**Planning:** The Planner Agent generates a multi-step roadmap.
   
7.	**Searching:** The Searcher Agent executes parallel web queries via Tavily.
   
9.	**Writing:** The Writer Agent synthesizes raw findings into a structured report.

6.	**Persistence:** The state is saved to a local database for continuity.
________________________________________
**8. Sample Working Demo**

**Example Prompt: "Analyze the impact of Quantum Computing on current Cybersecurity encryption."**

•	Planner Output: Generates questions on RSA vulnerability, Post-Quantum Cryptography (PQC), and NIST standards.

•	Searcher Output: Retrieves snippets from recent research papers and tech journals.

•	Final Report: A structured 700-word report with dedicated sections on "Current Risks" and "Mitigation Strategies."
________________________________________
**9. Outputs / Results**

<img width="800" height="400" alt="Screenshot 2025-12-25 162058" src="https://github.com/user-attachments/assets/0951980b-17f2-4e53-9169-1e121b8bb2fb" />

<img width="800" height="400" alt="Screenshot 2025-12-25 162233" src="https://github.com/user-attachments/assets/64638388-4bf5-4dc3-bd6d-f28f5778bc06" />

<img width="800" height="400" alt="Screenshot 2025-12-25 162344" src="https://github.com/user-attachments/assets/38f4c166-9adc-488e-80a0-caa9e7a50c10" />

<img width="800" height="400" alt="Screenshot 2025-12-25 162553" src="https://github.com/user-attachments/assets/eae931fb-e9a5-4595-88e5-87b211926ec0" />

<img width="800" height="400" alt="Screenshot 2025-12-25 162712" src="https://github.com/user-attachments/assets/4bb82f8c-3029-4616-8cc3-045750a5a8a5" />

________________________________________
**10. Future Enhancements**

• Vector DB Integration: Implementing ChromaDB for long-term memory of all researched topics.

• Multi-Modality: Enabling the agent to "see" and describe charts/graphs within uploaded PDFs.

• Parallelization: Moving from sequentical search to asynchronous parallel search for faster results.
________________________________________
**11. Deployed Project Link**

•	Live App: https://open-deep-research-a4pbbsas6ssq5szmn5ou4k.streamlit.app/
