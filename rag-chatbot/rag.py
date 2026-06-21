import subprocess
from retriever import retrieve

_debug_log: list[dict] = []


def ask_claude(prompt: str, label: str = "") -> str:
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    output = result.stdout.strip()
    _debug_log.append({"label": label, "prompt": prompt, "response": output})
    return output


def get_debug_log() -> list[dict]:
    return list(_debug_log)


def clear_debug_log() -> None:
    _debug_log.clear()


def rag_query(question: str) -> str:
    chunks = retrieve(question)
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful assistant analyzing a resume. Answer the question based ONLY on the resume content provided below.

Resume content:
{context}

Question: {question}

Answer:"""
    return ask_claude(prompt, label="Chat")


if __name__ == "__main__":
    print("=== Resume RAG Chatbot ===")
    print("问简历相关问题，输入 quit 退出\n")
    while True:
        q = input("你: ").strip()
        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue
        print("Claude: ", end="", flush=True)
        print(rag_query(q))
        print()
