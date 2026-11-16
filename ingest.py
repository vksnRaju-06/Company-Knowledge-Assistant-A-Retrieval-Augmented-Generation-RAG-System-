import os
import glob
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
import pypdf

load_dotenv()

# ── local embedding model (runs on your machine, free) ────────
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

# ── chromadb (no embedding_function — we embed manually) ──────
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="company_knowledge")

# ── chunking ──────────────────────────────────────────────────
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
        if i >= len(words):
            break
    return chunks

# ── document readers ──────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    reader = pypdf.PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_document(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext in (".txt", ".md"):
        return read_txt(path)
    else:
        print(f"  Skipping unsupported format: {path}")
        return None

# ── main ingestion ─────────────────────────────────────────────
def ingest_documents(folder="./documents"):
    files = glob.glob(f"{folder}/**/*.*", recursive=True)
    if not files:
        print("No files found in ./documents — add .txt or .pdf files there.")
        return

    total_chunks = 0

    for path in files:
        doc_name = os.path.basename(path)
        print(f"\nProcessing: {doc_name}")

        text = read_document(path)
        if not text or not text.strip():
            print("  Empty or unreadable — skipping.")
            continue

        chunks = chunk_text(text)
        print(f"  {len(chunks)} chunks created")

        # Generate embeddings locally
        print("  Generating embeddings...")
        embeddings = embedder.encode(chunks, show_progress_bar=False).tolist()

        ids       = [f"{doc_name}::chunk{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_name, "chunk_index": i}
                     for i in range(len(chunks))]

        # Store in ChromaDB with our own embeddings
        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
            embeddings=embeddings
        )
        total_chunks += len(chunks)
        print(f"  Stored in ChromaDB ✓")

    print(f"\nDone! {total_chunks} total chunks indexed across {len(files)} file(s).")

if __name__ == "__main__":
    ingest_documents()