#This is the entry point for Streamlit. Run it using streamlit run main.py.
import os

import streamlit as st

# Custom CSS to hide the icons and clean up the footer
hide_st_style = """
            <style>
            /* 1. Hide GitHub Icon (Top Right) */
            #GithubIcon {visibility: hidden;}
            
            /* 2. Hide the Red Crown and Globe Icons (Bottom Right) */
            div[data-testid="stStatusWidget"] {visibility: hidden;}
            .stAppDeployButton {display: none !important;}
            
            /* 3. Style your custom name to be centered and clear */
            .custom-footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #0e1117; /* Matches Streamlit Dark Theme */
                color: #FAFAFA;
                text-align: center;
                padding: 10px 0;
                font-size: 14px;
                font-weight: 500;
                z-index: 9999;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# The actual text that will appear
st.markdown('<div class="custom-footer">Designed with ❤️ by Snehal Sonkamble</div>', unsafe_allow_html=True)

from datetime import datetime
from groq import Groq
from tavily import TavilyClient

import utils
import engine

def generate_chat_title(client, messages):
    context = ""
    for m in messages[:4]:
        role = "User" if m["role"] == "user" else "Assistant"
        context += f"{role}: {m['content'][:200]}\n"
    
    prompt = f"Provide a short 3-4 word descriptive title for this chat. No quotes.\n\n{context}"
    title = utils.get_llm_response(client, engine.MODEL, prompt, "Concise titling assistant.")
    return title.strip() if "LLM_ERROR" not in title else "New Chat"

def run_research_app():
    st.set_page_config(page_title="Deep Research Assistant", layout="wide")
    st.title("🧠 Deep Research Assistant")

    # API Keys
    groq_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")

    if not groq_key:
        st.error("Missing GROQ_API_KEY")
        return
    
    client = Groq(api_key=groq_key)
    tavily = TavilyClient(api_key=tavily_key) if tavily_key else None

    # Init Session State
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! I'm your research assistant. What topic should I research for you today?."}]
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"sid_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if "current_title" not in st.session_state:
        st.session_state.current_title = "New Chat"
    if "app" not in st.session_state:
        st.session_state.app = engine.create_workflow(client, tavily)

    # Sidebar
    with st.sidebar:
        st.header("New Chat Control")
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Started a new session."}]
            st.session_state.session_id = f"sid_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.current_title = "New Chat"
            st.rerun()
            
        sum_pref = st.radio("Summary Style:", ("Short Summary", "Long Summary"))
        src_focus = st.radio("Search Scope:", ("Scholarly/Academic", "General Web/News"))
        uploaded_file = st.file_uploader("Upload Context", type=['pdf', 'docx', 'txt'])
        
        st.markdown("---")
        st.header("History")
        for sid, data in utils.get_history_entries():
            col1, col2 = st.columns([0.8, 0.2])
            if col1.button(f"📄 {data['title']}", key=f"load_{sid}", use_container_width=True):
                st.session_state.messages, st.session_state.session_id, st.session_state.current_title = data["messages"], sid, data["title"]
                st.rerun()
            if col2.button("🗑️", key=f"del_{sid}"):
                utils.delete_history_entry(sid)
                st.rerun()

    # Chat UI
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Researching..."):
                file_text = utils.extract_file_content(uploaded_file)
                inputs = engine.ResearchState(
                    topic=prompt + file_text,
                    structured_plan=None, sub_questions=[], research_results=[],
                    final_report="", summary_preference=sum_pref.split()[0],
                    source_focus=src_focus, run_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    messages=[(m["role"], m["content"]) for m in st.session_state.messages]
                )
                result = st.session_state.app.invoke(inputs)
                final_output = result["final_report"]
                st.markdown(final_output)
                st.session_state.messages.append({"role": "assistant", "content": final_output})
                
                if st.session_state.current_title == "New Chat":
                    st.session_state.current_title = generate_chat_title(client, st.session_state.messages)
                
                utils.save_current_chat(st.session_state.session_id, st.session_state.current_title, st.session_state.messages)
                st.rerun()

if __name__ == "__main__":
    run_research_app()