import os
from dotenv import load_dotenv
from groq import Groq

from src.rag import get_context

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_response(query):
    query_lower = query.lower()

    # =========================
    # 🔹 SIMPLE SEARCH FALLBACK
    # =========================
    if "latest" in query_lower or "news" in query_lower:
        prompt = f"Give latest financial news about: {query}"
    else:
        context = get_context(query)

        if not context:
            return "No relevant information found."

        prompt = f"""
You are a financial assistant.

Context:
{context}

Question:
{query}

Answer clearly:
"""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return completion.choices[0].message.content