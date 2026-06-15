import subprocess


def ask_claude(prompt: str) -> str:
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed:\n{result.stderr}")
    return result.stdout.strip()


def chat():
    print("=== Claude 多轮对话 (输入 'quit' 退出) ===\n")
    history = []

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        history.append(f"User: {user_input}")

        prompt = "\n".join(history) + "\nAssistant:"
        print("Claude: ", end="", flush=True)

        response = ask_claude(prompt)
        print(response)

        history.append(f"Assistant: {response}")
        print()


if __name__ == "__main__":
    chat()
