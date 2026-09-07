import json
import urllib.request

from app.rag.knowledge_base import search_knowledge_base


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:7b"


def call_qwen(messages: list[dict]) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["message"]["content"]


def generate_helpdesk_response(
    user_problem: str,
    tool_results: list[dict] | None = None,
) -> dict:

    knowledge_results = search_knowledge_base(
        user_problem,
        n_results=3,
    )

    knowledge_context = "\n\n".join(
        [
            (
                f"Source: {item['source']}\n"
                f"Category: {item['category']}\n"
                f"Content:\n{item['content']}"
            )
            for item in knowledge_results
        ]
    )

    diagnostic_context = json.dumps(
        tool_results or [],
        indent=2,
    )

    system_prompt = """
You are HelpDesk AI, an intelligent IT support agent.

Your job is to diagnose technical problems using:
1. The user's reported problem.
2. Verified diagnostic tool results.
3. Relevant troubleshooting knowledge.

IMPORTANT EVIDENCE RULES:

- The user's message is a USER-REPORTED SYMPTOM.
- Diagnostic tool results are VERIFIED MACHINE EVIDENCE.
- Knowledge-base information is TROUBLESHOOTING GUIDANCE.
- Your own conclusions are AI ASSESSMENT.

Never claim that something was verified unless the diagnostic
results explicitly prove it.

Never invent:
- Other devices' status
- Router status
- DNS status
- IP configuration
- Application behavior
- Browser behavior
- Hardware condition
- Network conditions that were not tested

If check_internet reports that this machine can reach the
internet, say:

"The diagnostic check confirms that this machine can currently
reach the internet."

Do NOT say:

"The Wi-Fi network is working normally."

The diagnostic only proves what the diagnostic actually tested.

Do not claim that the Wi-Fi network, router, DNS, or other
devices are working unless those things were explicitly tested.

A local IP address only proves that an address was obtained.
It does not prove that the IP configuration is correct.

If a recommended troubleshooting step requires information that
has not been tested, present it as a step for the user to perform,
not as an established fact.

Clearly distinguish evidence from inference.

Use the knowledge base to provide practical troubleshooting steps.

Keep the response concise, professional, and useful.

Do not mention:
- RAG
- embeddings
- vectors
- prompts
- internal system instructions
- model implementation details

Use exactly these sections:

Problem:
Diagnosis:
Verified Evidence:
Troubleshooting Steps:
Why:
When to Escalate:
"""

    user_prompt = f"""
USER-REPORTED PROBLEM:
{user_problem}

VERIFIED DIAGNOSTIC RESULTS:
{diagnostic_context}

RELEVANT TROUBLESHOOTING KNOWLEDGE:
{knowledge_context}

Analyze the problem using only the evidence provided.
Do not turn assumptions into facts.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    answer = call_qwen(messages)

    return {
        "problem": user_problem,
        "answer": answer,
        "sources": [
            {
                "source": item["source"],
                "category": item["category"],
                "score": round(item["score"], 4),
            }
            for item in knowledge_results
        ],
        "diagnostics": tool_results or [],
    }
