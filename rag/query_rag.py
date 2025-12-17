import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

DB_DIR = "rag/chroma_db"
db = chromadb.PersistentClient(path=DB_DIR)
collection = db.get_or_create_collection("loan_docs")

def rag_answer(query):
    q_emb = embedder.encode([query]).tolist()[0]

    result = collection.query(query_embeddings=[q_emb], n_results=3)

    if not result["documents"]:
        return "Policy does not specify."

    context = "\n\n".join(result["documents"][0])

    prompt = f"""
You are a professional bank loan support assistant.
Only use the details from context below.
If answer not found, reply: Policy does not specify.

Context:
{context}

Question: {query}

Answer in bullet points:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {e}"
