import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

from src.rag import get_retriever

load_dotenv()


def get_response(query):
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=300
    )

    retriever = get_retriever()
    search = DuckDuckGoSearchRun()

    # 🔹 Decide tool
    if "latest" in query.lower() or "news" in query.lower():
        return search.run(query)

    # 🔹 RAG
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    context = "\n\n".join([doc.page_content for doc in docs[:3]])

    prompt = f"""
You are a professional financial assistant.

Answer clearly using the context.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content