import sys
from dotenv import load_dotenv

load_dotenv()

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

COLLECTION_NAME = "resume"
DB_PATH = "./chroma_db"
TOP_K = 3


def retrieve(query: str) -> list[str]:
    client = chromadb.PersistentClient(path=DB_PATH)
    ef = DefaultEmbeddingFunction()
    collection = client.get_collection(COLLECTION_NAME, embedding_function=ef)
    results = collection.query(query_texts=[query], n_results=TOP_K)
    return results["documents"][0]


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "What is your work experience?"
    print(f"Query: {query}\n")
    chunks = retrieve(query)
    for i, chunk in enumerate(chunks):
        print(f"--- Result {i+1} ---\n{chunk}\n")
