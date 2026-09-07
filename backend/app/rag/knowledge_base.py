from pathlib import Path
import json
import urllib.request
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
VECTOR_FILE = BASE_DIR / "vectors.json"

OLLAMA_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"


def ollama_embed(text: str) -> list[float]:
    """
    Generate an embedding using Ollama's local embedding model.
    """

    payload = json.dumps({
        "model": EMBED_MODEL,
        "input": text,
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        embeddings = result.get("embeddings")

        if not embeddings:
            raise RuntimeError("Ollama returned no embeddings.")

        return embeddings[0]

    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate embedding with Ollama: {exc}"
        ) from exc


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100):
    """
    Split knowledge-base text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def build_index():
    """
    Read all Markdown files, create embeddings,
    and save them locally in vectors.json.
    """

    if not KNOWLEDGE_DIR.exists():
        raise RuntimeError(
            f"Knowledge base directory not found: {KNOWLEDGE_DIR}"
        )

    records = []

    files = sorted(KNOWLEDGE_DIR.glob("*.md"))

    if not files:
        raise RuntimeError("No Markdown files found in knowledge_base/")

    print(f"Found {len(files)} knowledge-base files.")

    for file_path in files:
        print(f"\nProcessing: {file_path.name}")

        content = file_path.read_text(encoding="utf-8").strip()
        chunks = chunk_text(content)

        print(f"  Chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks):
            print(f"  Embedding chunk {index + 1}/{len(chunks)}...")

            embedding = ollama_embed(chunk)

            records.append({
                "id": f"{file_path.stem}_{index}",
                "source": file_path.name,
                "category": file_path.stem,
                "content": chunk,
                "embedding": embedding,
            })

    VECTOR_FILE.write_text(
        json.dumps(records, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("RAG INDEX CREATED")
    print("=" * 60)
    print(f"Documents/chunks: {len(records)}")
    print(f"Vector file: {VECTOR_FILE}")
    print("=" * 60)


def cosine_similarity(a, b):
    """
    Calculate cosine similarity between two vectors.
    """

    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def search_knowledge_base(query: str, n_results: int = 3):
    """
    Search the local vector database using cosine similarity.
    """

    if not VECTOR_FILE.exists():
        raise RuntimeError(
            "vectors.json does not exist. Run build_index() first."
        )

    records = json.loads(
        VECTOR_FILE.read_text(encoding="utf-8")
    )

    query_embedding = ollama_embed(query)

    results = []

    for record in records:
        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        results.append({
            "id": record["id"],
            "source": record["source"],
            "category": record["category"],
            "content": record["content"],
            "score": score,
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:n_results]


if __name__ == "__main__":
    build_index()

    print("\nTesting semantic search...\n")

    query = "Wi-Fi is connected but internet is not working"

    results = search_knowledge_base(query, n_results=3)

    print(f"Query: {query}\n")

    for index, result in enumerate(results, start=1):
        print(f"RESULT {index}")
        print("-" * 60)
        print(f"Source: {result['source']}")
        print(f"Category: {result['category']}")
        print(f"Similarity: {result['score']:.4f}")
        print()
        print(result["content"])
        print()
