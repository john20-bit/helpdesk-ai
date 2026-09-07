import json
import urllib.request

from app.rag.knowledge_base import search_knowledge_base


OLLAMA_URL = "http://127.0.0.1:11434"
CHAT_MODEL = "qwen2.5:7b"


def ask_qwen(prompt: str) -> str:
    """
    Send a prompt to Qwen through the local Ollama API.
    """

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are HelpDesk AI, a professional IT helpdesk assistant. "
                    "Give clear, practical and safe troubleshooting guidance. "
                    "Use the provided knowledge base as your primary source. "
                    "Do not invent technical facts that are not supported by the "
                    "knowledge base unless they are necessary for a basic safe "
                    "explanation. "
                    "Keep answers concise and easy for a normal computer user to follow."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        return result["message"]["content"].strip()

    except Exception as exc:
        raise RuntimeError(
            f"Failed to communicate with Ollama: {exc}"
        ) from exc


def generate_helpdesk_response(user_problem: str) -> dict:
    """
    Perform RAG retrieval and generate a grounded response using Qwen.
    """

    results = search_knowledge_base(
        user_problem,
        n_results=3,
    )

    knowledge_context = "\n\n".join(
        [
            (
                f"Source: {result['source']}\n"
                f"Category: {result['category']}\n"
                f"Similarity: {result['score']:.4f}\n"
                f"Content:\n{result['content']}"
            )
            for result in results
        ]
    )

    prompt = f"""
User's IT problem:

{user_problem}

Relevant knowledge-base information:

{knowledge_context}

Based on the knowledge base, provide a helpful troubleshooting response.

Use this structure:

Problem:
Briefly identify the likely problem.

Troubleshooting Steps:
Give numbered steps in the best order.

Why:
Briefly explain what is likely causing the issue.

When to Escalate:
Explain when the user should contact IT support or their ISP.

Do not mention embeddings, vector databases, similarity scores,
RAG, or internal system details.
"""

    answer = ask_qwen(prompt)

    return {
        "problem": user_problem,
        "answer": answer,
        "sources": [
            {
                "source": result["source"],
                "category": result["category"],
                "score": round(result["score"], 4),
            }
            for result in results
        ],
    }


if __name__ == "__main__":
    problem = "My Wi-Fi is connected but I cannot access the internet."

    print("\nGenerating HelpDesk AI response...\n")

    result = generate_helpdesk_response(problem)

    print("=" * 70)
    print("HELPDESK AI")
    print("=" * 70)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("KNOWLEDGE SOURCES")
    print("=" * 70)

    for source in result["sources"]:
        print(
            f"{source['source']} "
            f"(similarity: {source['score']})"
        )
