#This is the "Brain." It contains the LangGraph workflow and the agent logic.
import re
from typing import TypedDict, List, Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import utils

MODEL = 'llama-3.1-8b-instant'

class ResearchPlan(BaseModel):
    research_strategy: str
    sub_questions: List[str]
    expected_output_format: str

class ResearchState(TypedDict):
    topic: str 
    structured_plan: ResearchPlan | None
    sub_questions: List[str]
    research_results: List[str]
    final_report: str
    summary_preference: str 
    source_focus: str 
    run_time: str 
    messages: Annotated[List[tuple], add_messages]

def router_node(state: ResearchState) -> str:
    query = state["topic"].lower()
    messages = state.get("messages", [])
    has_report = any("## Research Report" in (m[1] if isinstance(m, tuple) else str(m)) for m in messages)
    is_detail_query = any(w in query for w in ["drawback", "limit", "why", "how", "detail", "compare", "paper"])
    if has_report and (len(query.split()) < 20 or is_detail_query):
        return "follow_up"
    return "full_research"

def planner_agent(state: ResearchState, client):
    topic = state["topic"]
    sys_msg = "You are an expert research planner. Decompose the topic into 3-5 sub-questions. Output JSON."
    prompt = f"Topic: {topic}\nReturn JSON matching ResearchPlan schema."
    try:
        res = utils.get_llm_response(client, MODEL, prompt, sys_msg, is_json_output=True)
        plan = ResearchPlan.model_validate_json(res)
        return {"structured_plan": plan, "sub_questions": plan.sub_questions}
    except:
        return {"sub_questions": [f"Analysis of {topic}"]}

def searcher_agent(state: ResearchState, tavily):
    sub_questions = state["sub_questions"]
    focus = state["source_focus"]
    results = []
    urls = re.findall(r'https?://\S+', state["topic"])
    for url in urls: results.append(utils.extract_url_content(url))
    keyword = " scholarly papers" if focus == "Scholarly/Academic" else " latest news"
    if tavily:
        for q in sub_questions:
            try:
                res = tavily.search(query=f"{q}{keyword}", search_depth="advanced", max_results=2)
                formatted = f"**Findings for: {q}**\n"
                for r in res['results']:
                    formatted += f"- URL: {r['url']}\n- Snippet: {r['content'][:400]}\n"
                results.append(formatted)
            except: pass
    return {"research_results": results}

def writer_agent(state: ResearchState, client):
    pref = state["summary_preference"]
    len_instr = "150-200 words" if pref == "Short" else "max 700 words"
    sys_prompt = f"Synthesize findings into a {len_instr} report. Focus: {state['source_focus']}."
    prompt = f"Topic: {state['topic']}\nFindings: {' '.join(state['research_results'])}"
    report = utils.get_llm_response(client, MODEL, prompt, sys_prompt)
    return {"final_report": f"## Research Report\n*Generated: {state['run_time']}*\n\n{report}"}

def follow_up_agent(state: ResearchState, client, tavily) -> ResearchState:
    query = state["topic"]
    prev_context = ""
    for m in reversed(state.get("messages", [])):
        content = m[1] if isinstance(m, tuple) else str(m)
        if "## Research Report" in content:
            prev_context = content
            break
    mini_findings = ""
    if tavily:
        try:
            response = tavily.search(query=f"{query} details", max_results=2)
            for res in response['results']: mini_findings += f"\n- {res['content'][:400]}"
        except: pass
    prompt = f"QUERY: {query}\nCONTEXT: {prev_context[:2000]}\nNEW: {mini_findings}"
    res = utils.get_llm_response(client, MODEL, prompt, "Answer the follow-up briefly (max 250 words).")
    return {"final_report": f"### 💬 Follow-up Analysis\n\n{res}"}

def create_workflow(client, tavily):
    workflow = StateGraph(ResearchState)
    workflow.add_node("entry", lambda x: {})
    workflow.add_node("planner", lambda x: planner_agent(x, client))
    workflow.add_node("searcher", lambda x: searcher_agent(x, tavily))
    workflow.add_node("writer", lambda x: writer_agent(x, client))
    workflow.add_node("follow_up", lambda x: follow_up_agent(x, client, tavily))
    
    workflow.set_entry_point("entry")
    workflow.add_conditional_edges("entry", router_node, {"full_research": "planner", "follow_up": "follow_up"})
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "writer")
    workflow.add_edge("writer", END)
    workflow.add_edge("follow_up", END)
    return workflow.compile()