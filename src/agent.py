import os
from dotenv import load_dotenv
from groq import Groq

from src.rag import get_context

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _chat(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful finance assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=350,
    )
    return response.choices[0].message.content.strip()


def get_response(query: str) -> dict:
    query_lower = query.lower().strip()

    if any(word in query_lower for word in ["latest", "news", "today", "current"]):
        prompt = (
            "Answer briefly and clearly about this finance query. "
            "If you are unsure about the latest facts, say that you need a live source.\n\n"
            f"Question: {query}"
        )
        answer = _chat(prompt)
        return {"answer": answer, "sources": []}

    context, sources = get_context(query)

    if context:
        prompt = (
            "Answer the question using only the context below. "
            "If the context does not contain the answer, say that the information is not in the knowledge base.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )
    else:
        prompt = (
            "Answer the question clearly and concisely. "
            "No document context was found.\n\n"
            f"Question: {query}"
        )

    answer = _chat(prompt)
    return {"answer": answer, "sources": sources}