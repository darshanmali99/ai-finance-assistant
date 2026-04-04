import os
from dotenv import load_dotenv
from groq import Groq

from src.rag import get_context

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_response(query):
    context = get_context(query)

    if context:
        prompt = f"""
Use the context to answer.

Context:
{context}

Question:
{query}
"""
    else:
        prompt = f"Answer this finance question:\n{query}"

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return {
        "answer": response.choices[0].message.content
    }