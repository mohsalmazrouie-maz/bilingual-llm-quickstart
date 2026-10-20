"""Ask an open LLM a question in Arabic or English.

Works with any OpenAI-compatible endpoint: a local Ollama server (the default),
LM Studio, vLLM, or a hosted provider. Standard library only, nothing to install.

    python chat.py "What is a foundation model?"
    python chat.py "ما هو النموذج التأسيسي؟"
"""
import json
import os
import sys
import time
import urllib.request

BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("LLM_MODEL", "qwen2.5:3b")
API_KEY = os.environ.get("LLM_API_KEY", "not-needed-for-local")

SYSTEM = (
    "You are a helpful assistant for students and developers in the UAE. "
    "Answer in the same language as the question (Arabic or English), "
    "in plain words, in at most five sentences."
)


def chat(question: str, temperature: float = 0.3) -> dict:
    """Send one question and return the raw response plus measured latency."""
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.load(response)
    data["_latency_s"] = round(time.perf_counter() - start, 2)
    return data


def answer_text(data: dict) -> str:
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    question = " ".join(sys.argv[1:]) or (
        "What is a foundation model? Explain it to a high school student."
    )
    data = chat(question)
    print(answer_text(data))
    usage = data.get("usage", {})
    print(
        f"\n[{MODEL} | {data['_latency_s']} s | "
        f"{usage.get('completion_tokens', '?')} output tokens]",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
