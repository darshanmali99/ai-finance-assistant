from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_retriever():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="vectordb",
        embedding_function=embedding
    )

    return vectordb.as_retriever(search_kwargs={"k": 3})