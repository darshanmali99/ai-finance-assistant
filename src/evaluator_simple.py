from src.rag import get_retriever
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def run_evaluation():
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    retriever = get_retriever()

    test_cases = [
        {
            "question": "What is RBI?",
            "expected": "central bank of India"
        },
        {
            "question": "What is repo rate?",
            "expected": "rate at which RBI lends"
        },
        {
            "question": "What is SEBI?",
            "expected": "regulates securities market"
        },
        {
            "question": "What is inflation?",
            "expected": "increase in prices"
        },
        {
            "question": "What is monetary policy?",
            "expected": "controls money supply"
        }
    ]

    score = 0

    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)

    for case in test_cases:
        q = case["question"]
        expected = case["expected"]

        docs = retriever.invoke(q)
        context = "\n".join([d.page_content for d in docs])

        response = llm.invoke(f"Context:\n{context}\n\nQuestion: {q}")
        answer = response.content.lower()

        match = expected in answer

        if match:
            score += 1

        print(f"\nQ: {q}")
        print(f"A: {answer}")
        print(f"Expected keyword: {expected}")
        print(f"Match: {'✅' if match else '❌'}")

    accuracy = (score / len(test_cases)) * 100

    print("\n" + "="*50)
    print(f"FINAL ACCURACY: {accuracy:.2f}%")
    print("="*50)


if __name__ == "__main__":
    run_evaluation()