# Resume RAG Chatbot

A chatbot that answers questions about a resume using Retrieval-Augmented Generation (RAG).

Upload a PDF resume → ask questions → get answers grounded in the actual resume content.

**Live demo:** _coming soon_

## How it works

```
PDF → chunks (500 chars) → embeddings (all-MiniLM-L6-v2) → ChromaDB
Question → embed → retrieve top 3 chunks → Claude → Answer
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

# Launch the UI
streamlit run rag-chatbot/app.py
```

Open `http://localhost:8501`, upload a resume PDF, and start asking questions.

## CLI usage (no UI)

```bash
# 1. Ingest your resume
python rag-chatbot/ingestor.py your_resume.pdf

# 2. Chat with it
python rag-chatbot/rag.py
```

## Project structure

```
rag-chatbot/
├── ingestor.py   # PDF → chunks → ChromaDB
├── retriever.py  # query → top 3 chunks
├── rag.py        # chunks + question → Claude → answer
└── app.py        # Streamlit UI
```
