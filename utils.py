#This handles the "dirty work": file parsing, web scraping, and database persistence.
import os
import requests
import shelve
import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime

HISTORY_DB = "chat_history.db"

# --- File Handling ---
try:
    from docx import Document
except ImportError:
    Document = None 

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None 

def get_llm_response(client, model, prompt, system_instruction=None, is_json_output=False):
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            response_format={"type": "json_object"} if is_json_output else None,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"

def extract_url_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]): script.decompose()
        content = soup.get_text(separator=' ')
        return f"\n--- URL CONTENT ({url}) ---\n{content[:2500]}...\n---"
    except Exception as e:
        return f"\nError extracting URL: {url}\n"

def extract_file_content(uploaded_file):
    if uploaded_file is None: return ""
    file_type = uploaded_file.name.split('.')[-1].lower()
    content = ""
    try:
        if file_type in ['txt', 'md']:
            content = uploaded_file.read().decode('utf-8')
        elif file_type == 'pdf' and PdfReader:
            reader = PdfReader(uploaded_file)
            content = "\n".join([p.extract_text() for p in reader.pages])
        elif file_type == 'docx' and Document:
            doc = Document(uploaded_file)
            content = "\n".join([p.text for p in doc.paragraphs])
        return f"\n--- FILE CONTEXT ({uploaded_file.name}) ---\n{content[:2000]}...\n---"
    except Exception as e:
        return f"File reading error: {e}"

def save_current_chat(session_id, title, messages):
    with shelve.open(HISTORY_DB) as db:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db[session_id] = {"timestamp": ts, "title": title, "messages": messages}

def get_history_entries():
    with shelve.open(HISTORY_DB) as db:
        return sorted(db.items(), key=lambda x: x[1]['timestamp'], reverse=True)

def delete_history_entry(key):
    with shelve.open(HISTORY_DB) as db:
        if key in db:
            del db[key]