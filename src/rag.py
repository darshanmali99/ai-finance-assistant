import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection("finance")


def get_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    docs = results.get("documents", [])

    if not docs:
        return ""

    return "\n\n".join(docs[0])