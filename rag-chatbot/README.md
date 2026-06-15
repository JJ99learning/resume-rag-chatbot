# Resume RAG Chatbot

A chatbot that answers questions about a resume using Retrieval-Augmented Generation (RAG).

Upload a PDF resume → ask questions → get answers grounded in the actual resume content.

## How it works

```
PDF → chunks (500 chars) → embeddings (all-MiniLM-L6-v2) → ChromaDB
Question → embed → retrieve top 3 chunks → Claude → Answer
```

## Stack

- **LLM:** Claude (via Claude Code CLI)
- **Embeddings:** `all-MiniLM-L6-v2` via ChromaDB
- **Vector DB:** ChromaDB (local)
- **PDF parsing:** pypdf

## Usage

```bash
# 1. Ingest your resume
python ingestor.py your_resume.pdf

# 2. Chat with it
python rag.py
```

## Setup

```bash
pip install chromadb pypdf sentence-transformers python-dotenv
```
