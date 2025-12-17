import os
import chromadb
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/docs"
DB_DIR = "rag/chroma_db"

def build_index():
    os.makedirs(DB_DIR, exist_ok=True)
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    db = chromadb.PersistentClient(path=DB_DIR)
    collection = db.get_or_create_collection("loan_docs")

    docs, ids, meta = [], [], []
    chunk = 0

    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_DIR, file), "r") as f:
                text = f.read()
            docs.append(text)
            ids.append(str(chunk))
            meta.append({"source": file})
            chunk += 1

    embeddings = embedder.encode(docs).tolist()

    collection.add(ids=ids, documents=docs, metadatas=meta, embeddings=embeddings)

    print("Index built successfully!")

if __name__ == "__main__":
    build_index()
