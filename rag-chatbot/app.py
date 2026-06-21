import os
import sys
import tempfile
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from ingestor import ingest
from rag import rag_query, clear_debug_log, get_debug_log
from jd_analyzer import analyze_jd
from fit_scorer import score_fit
from interview_prep import generate_interview_prep
from cover_letter import generate_cover_letter
from resume_enhancer import enhance_bullet, keyword_coverage

st.set_page_config(page_title="Resume RAG Chatbot", page_icon="📄", layout="wide")
st.title("📄 Resume RAG Chatbot")

# --- Sidebar ---
with st.sidebar:
    st.header("1. Upload Resume")
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
                        st.session_state.jd_analysis = None
                        st.session_state.jd_report = None
                        st.session_state.interview_result = None
                        st.session_state.cover_letter_result = None
                    finally:
                        os.unlink(tmp_path)
                st.rerun()

    if st.session_state.get("file_ingested"):
        st.success("✅ Resume loaded")
        if st.button("Replace resume"):
            for key in ["file_ingested", "jd_analysis", "jd_report",
                        "interview_result", "cover_letter_result", "messages", "debug_log"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.divider()
    st.header("2. Paste Job Description")

    if not st.session_state.get("file_ingested"):
        st.caption("Load a resume first.")
    else:
        jd_text = st.text_area("Job Description", height=220,
                               placeholder="Paste the full JD here...")
        if jd_text.strip():
            if st.button("Analyze Fit →", type="primary"):
                with st.spinner("Analyzing... (~30s)"):
                    clear_debug_log()
                    jd_analysis = analyze_jd(jd_text)
                    result = score_fit(jd_analysis)
                    st.session_state.jd_analysis = jd_analysis
                    st.session_state.jd_report = result
                    st.session_state.debug_log = get_debug_log()
                    # clear downstream results when JD changes
                    st.session_state.interview_result = None
                    st.session_state.cover_letter_result = None
                st.rerun()

        if st.session_state.get("jd_analysis"):
            st.caption("✅ JD analyzed — use tabs above to explore results.")

# --- Init session state ---
for key in ["messages", "jd_analysis", "jd_report", "interview_result",
            "cover_letter_result", "debug_log"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "messages" else []

# --- Main area ---
if not st.session_state.get("file_ingested"):
    st.info("Upload a resume PDF in the sidebar and click **Load Resume** to start.")
else:
    tab_chat, tab_jd, tab_interview, tab_cover, tab_resume = st.tabs([
        "💬 Chat", "📊 JD 分析", "🎯 面试准备", "✉️ Cover Letter", "✨ 简历优化"
    ])

    # ── Tab 1: Chat ──────────────────────────────────────────
    with tab_chat:
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

    # ── Tab 2: JD 分析 ────────────────────────────────────────
    with tab_jd:
        if not st.session_state.get("jd_report"):
            st.info("Paste a Job Description in the sidebar and click **Analyze Fit →**.")
        else:
            r = st.session_state.jd_report
            jd = st.session_state.jd_analysis

            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Fit Score", f"{r['score']} / 100")
            with col2:
                st.markdown(f"**Role:** {jd.get('role_summary', '')}")
                st.markdown(f"**Required:** {', '.join(jd.get('required_skills', []))}")
                st.markdown(f"**Nice to Have:** {', '.join(jd.get('nice_to_have', []))}")

            st.divider()
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

    # ── Tab 3: 面试准备 ───────────────────────────────────────
    with tab_interview:
        if not st.session_state.get("jd_analysis"):
            st.info("Run **Analyze Fit →** first to unlock this tab.")
        else:
            if not st.session_state.get("interview_result"):
                if st.button("Generate Interview Questions", type="primary", key="btn_interview_gen"):
                    with st.spinner("Generating 10 questions + answers... (~30s)"):
                        result = generate_interview_prep(st.session_state.jd_analysis)
                        st.session_state.interview_result = result
                    st.rerun()
            else:
                st.markdown(st.session_state.interview_result)
                if st.button("Regenerate", key="btn_interview_regen"):
                    st.session_state.interview_result = None
                    st.rerun()

    # ── Tab 4: Cover Letter ───────────────────────────────────
    with tab_cover:
        if not st.session_state.get("jd_analysis"):
            st.info("Run **Analyze Fit →** first to unlock this tab.")
        else:
            if not st.session_state.get("cover_letter_result"):
                if st.button("Generate Cover Letter", type="primary", key="btn_cover_gen"):
                    with st.spinner("Writing cover letter... (~30s)"):
                        result = generate_cover_letter(st.session_state.jd_analysis)
                        st.session_state.cover_letter_result = result
                    st.rerun()
            else:
                st.markdown(st.session_state.cover_letter_result)
                st.divider()
                st.text_area("Copy-friendly plain text", value=st.session_state.cover_letter_result,
                             height=300, label_visibility="collapsed", key="cover_letter_text")
                if st.button("Regenerate", key="btn_cover_regen"):
                    st.session_state.cover_letter_result = None
                    st.rerun()

    # ── Tab 5: 简历优化 ───────────────────────────────────────
    with tab_resume:
        if not st.session_state.get("jd_analysis"):
            st.info("Run **Analyze Fit →** first to unlock this tab.")
        else:
            # Keyword coverage (no Claude call, instant)
            st.subheader("Keyword Coverage")
            with st.spinner("Checking keywords..."):
                coverage = keyword_coverage(st.session_state.jd_analysis)

            col_covered, col_missing = st.columns(2)
            with col_covered:
                st.markdown("**✅ Covered**")
                for k in coverage["covered"]:
                    st.markdown(f"- {k}")
            with col_missing:
                st.markdown("**❌ Missing**")
                for k in coverage["missing"]:
                    st.markdown(f"- {k}")

            st.divider()
            st.subheader("Bullet Point Enhancer")
            bullet = st.text_area("Paste a weak bullet point from your resume",
                                  placeholder="e.g. worked on backend services using java",
                                  height=80)
            if bullet.strip():
                if st.button("Enhance Bullet →", type="primary", key="btn_enhance"):
                    with st.spinner("Rewriting... (~20s)"):
                        enhanced = enhance_bullet(bullet, st.session_state.jd_analysis)
                    st.markdown(enhanced)
