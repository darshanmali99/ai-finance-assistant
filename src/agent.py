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

    query_lower = query.lower()

    # =========================
    # 🔹 SEARCH (WITH FALLBACK)
    # =========================
    if "latest" in query_lower or "news" in query_lower:
        try:
            result = search.run(query)

            if not result or "No good" in result:
                # fallback to LLM knowledge
                return llm.invoke(
                    f"Give latest general financial update about: {query}"
                ).content

            return result

        except Exception:
            return llm.invoke(
                f"Give latest general financial update about: {query}"
            ).content

    # =========================
    # 🔹 RAG (DOCUMENT BASED)
    # =========================
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in knowledge base."

    context = "\n\n".join([doc.page_content for doc in docs[:3]])

    prompt = f"""
You are a professional financial assistant.

Answer clearly and in simple terms.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content