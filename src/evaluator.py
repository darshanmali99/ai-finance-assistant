from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

from src.rag import get_retriever
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()


def run_evaluation():
    # =========================
    # LLM SETUP
    # =========================
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    # =========================
    # RETRIEVER
    # =========================
    retriever = get_retriever()

    # =========================
    # TEST QUESTIONS
    # =========================
    questions = [
        "What is RBI?",
        "What is repo rate?",
        "What is SEBI?",
        "What is inflation?",
        "What is monetary policy?"
    ]

    # Ground truth (simple for now — improve later)
    ground_truths = [
        "RBI is the central bank of India",
        "Repo rate is the rate at which RBI lends money to banks",
        "SEBI regulates the securities market in India",
        "Inflation is the increase in prices over time",
        "Monetary policy is how RBI controls money supply"
    ]

    # =========================
    # BUILD DATASET
    # =========================
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }

    for q, gt in zip(questions, ground_truths):
        # Retrieve docs
        docs = retriever.invoke(q)

        # Extract text contexts
        contexts = [doc.page_content for doc in docs]

        # Combine context for LLM
        context_text = "\n".join(contexts)

        # Generate answer
        response = llm.invoke(f"Context:\n{context_text}\n\nQuestion: {q}")
        answer = response.content

        # Append (FIXED FORMAT)
        data["question"].append(q)
        data["answer"].append(answer)
        data["contexts"].append([str(c) for c in contexts])
        data["ground_truth"].append(gt)

    # =========================
    # CREATE DATASET
    # =========================
    dataset = Dataset.from_dict(data)

    # =========================
    # RUN EVALUATION
    # =========================
    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy]
    )

    # =========================
    # PRINT RESULTS
    # =========================
    print("\n" + "=" * 50)
    print("RAGAS EVALUATION RESULTS")
    print("=" * 50)

    print(f"Faithfulness: {result['faithfulness']:.4f}")
    print(f"Answer Relevancy: {result['answer_relevancy']:.4f}")

    print("\nTarget:")
    print("Faithfulness > 0.85")
    print("Answer Relevancy > 0.80")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    run_evaluation()