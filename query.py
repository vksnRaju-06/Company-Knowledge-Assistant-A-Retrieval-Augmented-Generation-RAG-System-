import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# ── clients ───────────────────────────────────────────────────
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")   # local, free, turns text into vectors

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # generates the actual answer

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="company_knowledge")

# ── retrieval ─────────────────────────────────────────────────
def retrieve(question, top_k=5):
    query_embedding = embedder.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    chunks    = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return list(zip(chunks, metadatas, distances))

# ── generation ────────────────────────────────────────────────
def build_prompt(question, retrieved):
    context_parts = []
    for i, (chunk, meta, _) in enumerate(retrieved, 1):
        context_parts.append(f"[{i}] Source: {meta['source']}\n{chunk}")
    context = "\n\n---\n\n".join(context_parts)

    system = """You are a helpful company knowledge assistant.
Answer the user's question using ONLY the document excerpts provided.
- Be clear and concise
- Cite sources inline using [1], [2], [3] etc.
- If the answer is not in the documents, say: "I couldn't find this in the knowledge base."
- Never make up information."""

    user = f"""Document excerpts:
{context}

Question: {question}"""

    return system, user

def ask(question, top_k=5):
    retrieved = retrieve(question, top_k)
    if not retrieved:
        return "No documents found. Run ingest.py first.", []

    system, user = build_prompt(question, retrieved)

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",   # ← Groq's hosted model, called via API (not downloaded)
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    return answer, retrieved

# ── CLI test ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("RAG Query Engine ready. Type 'quit' to exit.\n")
    while True:
        q = input("Your question: ").strip()
        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue

        answer, sources = ask(q)
        print(f"\nAnswer:\n{answer}\n")
        print("Sources used:")
        for i, (chunk, meta, dist) in enumerate(sources, 1):
            score = round(1 - dist, 3)
            print(f"  [{i}] {meta['source']} (relevance: {score})")
            print(f"       \"{chunk[:80]}...\"")
        print("\n" + "─"*60 + "\n")