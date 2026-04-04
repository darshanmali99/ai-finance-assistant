import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

from src.rag import get_retriever

load_dotenv()


def get_agent():
    # 🔹 LLM (FIXED)
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=300
    )

    # 🔹 Memory
    memory = ConversationBufferMemory(memory_key="chat_history")

    # 🔹 Tools
    search = DuckDuckGoSearchRun()
    retriever = get_retriever()

    def rag_tool(query):
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant information found."

        context = "\n\n".join([doc.page_content for doc in docs[:3]])

        prompt = f"""
You are a professional financial assistant.

Use the context below to answer clearly.

Context:
{context}

Question:
{query}

Answer:
"""

        response = llm.invoke(prompt)
        return response.content

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Use for latest news and current information"
        ),
        Tool(
            name="RAG",
            func=rag_tool,
            description="Use for finance concepts and internal documents"
        )
    ]

    # 🔹 Agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    return agent