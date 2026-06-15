import sys
import os
from dotenv import load_dotenv

load_dotenv()

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from pypdf import PdfReader

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
COLLECTION_NAME = "resume"
DB_PATH = "./chroma_db"


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end].strip())
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c]


def ingest(pdf_path: str):
    print(f"[1/3] 读取 PDF: {pdf_path}")
    text = load_pdf(pdf_path)
    print(f"      共 {len(text)} 字符")

    print(f"\n[2/3] 切 chunks（每块 {CHUNK_SIZE} 字符，重叠 {CHUNK_OVERLAP}）")
    chunks = chunk_text(text)
    print(f"      共 {len(chunks)} 个 chunks")
    for i, c in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{c[:200]}{'...' if len(c) > 200 else ''}")

    print("\n[3/3] 存入 ChromaDB（使用内置 embedding，首次会下载小模型）")
    client = chromadb.PersistentClient(path=DB_PATH)
    ef = DefaultEmbeddingFunction()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
    )
    print(f"      ✅ 已存入 {len(chunks)} 条记录")
    print(f"\n完成！现在可以运行 retriever.py 搜索了。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ingestor.py <你的简历.pdf>")
        sys.exit(1)
    ingest(sys.argv[1])
