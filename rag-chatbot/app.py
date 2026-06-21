import os
import sys
import tempfile
import streamlit as st

# resolve imports and chroma_db path relative to this file, not cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from ingestor import ingest
from rag import rag_query
from jd_analyzer import analyze_jd
from fit_scorer import score_fit
from rag import clear_debug_log, get_debug_log

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
                        st.session_state.jd_report = None
                    finally:
                        os.unlink(tmp_path)
                st.rerun()

    if st.session_state.get("file_ingested"):
        st.success("✅ Resume loaded")
        if st.button("Replace with new resume"):
            st.session_state.file_ingested = False
            st.session_state.messages = []
            st.session_state.jd_report = None
            st.rerun()

    st.divider()
    st.header("JD Analysis")
    if not st.session_state.get("file_ingested"):
        st.caption("Load a resume first.")
    else:
        jd_text = st.text_area("Paste Job Description", height=200,
                               placeholder="Paste the full JD here...")
        if jd_text.strip():
            if st.button("Analyze Fit →", type="primary"):
                with st.spinner("Analyzing... (~30s)"):
                    clear_debug_log()
                    jd_analysis = analyze_jd(jd_text)
                    result = score_fit(jd_analysis)
                    st.session_state.jd_report = result
                    st.session_state.debug_log = get_debug_log()
                st.rerun()

# --- Init session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Main chat area ---
if not st.session_state.get("file_ingested"):
    st.info("Upload a resume PDF in the sidebar and click **Load Resume** to start.")
else:
    if st.session_state.get("jd_report"):
        r = st.session_state.jd_report
        st.subheader("JD Fit Report")
        st.metric("Fit Score", f"{r['score']} / 100")
        st.markdown(r["report"])

        if st.session_state.get("debug_log"):
            with st.expander("🔍 Debug View — Full Pipeline Trace"):
                for i, entry in enumerate(st.session_state.debug_log):
                    st.markdown(f"### {entry['label']}")
                    st.markdown("**Prompt sent to Claude:**")
                    st.code(entry["prompt"], language="text")
                    st.markdown("**Raw response:**")
                    st.code(entry["response"], language="text")
                    if i < len(st.session_state.debug_log) - 1:
                        st.divider()

        st.divider()

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
