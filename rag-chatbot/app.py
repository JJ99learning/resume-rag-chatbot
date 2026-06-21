import os
import sys
import tempfile
import streamlit as st

# resolve imports and chroma_db path relative to this file, not cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from ingestor import ingest
from rag import rag_query

st.set_page_config(page_title="Resume RAG Chatbot", page_icon="📄")
st.title("📄 Resume RAG Chatbot")
st.caption("Upload a resume PDF, then ask anything about it.")

# --- Sidebar: upload & ingest ---
with st.sidebar:
    st.header("Resume")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file:
        if not st.session_state.get("file_ingested"):
            if st.button("Load Resume", type="primary"):
                with st.spinner("Processing PDF..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name
                    try:
                        ingest(tmp_path)
                        st.session_state.file_ingested = True
                        st.session_state.messages = []
                    finally:
                        os.unlink(tmp_path)
                st.rerun()

    if st.session_state.get("file_ingested"):
        st.success("✅ Resume loaded")
        if st.button("Replace with new resume"):
            st.session_state.file_ingested = False
            st.session_state.messages = []
            st.rerun()

# --- Init session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Main chat area ---
if not st.session_state.get("file_ingested"):
    st.info("Upload a resume PDF in the sidebar and click **Load Resume** to start.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if question := st.chat_input("Ask about the resume..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = rag_query(question)
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
