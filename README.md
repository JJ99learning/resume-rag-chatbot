# Resume RAG Chatbot

An AI-powered job application assistant. Upload your resume, paste a job description, and get an instant fit analysis — plus a chatbot to query the resume directly.

**Live demo:** _coming soon_

## Features

- **Resume Q&A** — ask anything about the resume, answers grounded in actual content
- **JD Fit Analysis** — paste any job description → get a 0-100 fit score, matched skills, missing skills, and top improvement suggestions
- **Debug View** — full pipeline trace showing every prompt sent to Claude and the raw response

## How it works

```
PDF → chunks (500 chars) → embeddings (all-MiniLM-L6-v2) → ChromaDB

Chat:       question → retrieve top 3 chunks → Claude → answer

JD Analysis:
  Step 1:   JD text → Claude → { required_skills, nice_to_have, keywords }
  Step 2:   skills → retrieve resume chunks → Claude → score + report
```

## Stack

- **LLM:** Claude (via Claude Code CLI)
- **Embeddings:** `all-MiniLM-L6-v2` via ChromaDB default embedding
- **Vector DB:** ChromaDB (local)
- **PDF parsing:** pypdf
- **UI:** Streamlit

## Quickstart

```bash
pip install -r requirements.txt
streamlit run rag-chatbot/app.py
```

Open `http://localhost:8501`, upload a resume PDF, and start chatting — or paste a JD in the sidebar for fit analysis.

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
├── ingestor.py      # PDF → chunks → ChromaDB
├── retriever.py     # query → top-k chunks
├── rag.py           # RAG pipeline + Claude call + debug logging
├── jd_analyzer.py   # JD text → structured requirements (JSON)
├── fit_scorer.py    # JD requirements + resume → fit score + report
└── app.py           # Streamlit UI
```
