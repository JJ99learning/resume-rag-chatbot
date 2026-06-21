# Resume RAG Chatbot

An AI-powered job application assistant. Upload your resume, paste a job description, and get a complete application package — fit score, interview prep, cover letter, and resume optimization — all grounded in your actual resume content.

**Live demo:** _coming soon_

## Features

| Tab | What it does |
|-----|-------------|
| **💬 Chat** | Ask anything about the resume; answers grounded in actual content |
| **📊 JD 分析** | Paste any JD → 0–100 fit score, matched skills, missing skills, top improvement suggestions |
| **🎯 面试准备** | 10 most likely interview questions + reference answers based on your resume |
| **✉️ Cover Letter** | One-click cover letter tailored to the JD, keywords aligned |
| **✨ 简历优化** | Keyword coverage report (covered vs. missing) + STAR-format bullet rewriter |

## How it works

```
PDF → chunks (500 chars) → embeddings (all-MiniLM-L6-v2) → ChromaDB

Chat:         question → retrieve top 3 chunks → Claude → answer

JD Pipeline:
  Step 1:     JD text → Claude → { role_summary, required_skills, nice_to_have, keywords }
  Step 2:     skills → retrieve resume chunks → Claude → fit score + report
  Step 3:     JD analysis + resume chunks → Claude → 10 interview Q&As
  Step 4:     JD analysis + resume chunks → Claude → cover letter
  Step 5:     bullet + JD context → Claude → STAR-format rewrite
  Step 5b:    JD keywords × full resume → string match → covered / missing list (no LLM)
```

## Stack

- **LLM:** Claude (via Claude Code CLI — no API key needed, uses Pro plan)
- **Embeddings:** `all-MiniLM-L6-v2` via ChromaDB default embedding
- **Vector DB:** ChromaDB (local, zero config)
- **PDF parsing:** pypdf
- **UI:** Streamlit

## Quickstart

```bash
pip install -r requirements.txt
streamlit run rag-chatbot/app.py
```

Open `http://localhost:8501`, upload a resume PDF, paste a JD in the sidebar, and click **Analyze Fit →** to unlock all tabs.

## CLI usage (no UI)

```bash
# Ingest a resume
python rag-chatbot/ingestor.py your_resume.pdf

# Chat in terminal
python rag-chatbot/rag.py
```

## Project structure

```
rag-chatbot/
├── ingestor.py        # PDF → chunks → ChromaDB
├── retriever.py       # query → top-k chunks; retrieve_all → full resume
├── rag.py             # RAG pipeline + Claude call + debug logging
├── jd_analyzer.py     # JD text → structured requirements (JSON)
├── fit_scorer.py      # JD requirements + resume chunks → fit score + report
├── interview_prep.py  # JD + resume → 10 interview questions + answers
├── cover_letter.py    # JD + resume → tailored cover letter
├── resume_enhancer.py # bullet rewriter + keyword coverage checker
└── app.py             # Streamlit UI (5 tabs)
```
