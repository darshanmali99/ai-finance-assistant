from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"


def _extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)
    return "\n".join(pages)


def _read_text_files() -> List[dict]:
    docs: List[dict] = []

    if PDF_DIR.exists():
        for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
            text = _extract_text_from_pdf(pdf_path)
            if text.strip():
                docs.append(
                    {
                        "source": pdf_path.name,
                        "text": text,
                    }
                )

    if DATA_DIR.exists():
        for txt_path in sorted(DATA_DIR.glob("*.txt")):
            text = txt_path.read_text(encoding="utf-8", errors="ignore")
            if text.strip():
                docs.append(
                    {
                        "source": txt_path.name,
                        "text": text,
                    }
                )

    return docs


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if len(chunk) >= 120:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(end - overlap, start + 1)

    return chunks


@lru_cache(maxsize=1)
def _build_index():
    raw_docs = _read_text_files()

    chunks: List[dict] = []
    for doc in raw_docs:
        parts = _chunk_text(doc["text"])
        for i, part in enumerate(parts):
            chunks.append(
                {
                    "text": part,
                    "source": doc["source"],
                    "chunk_id": f'{doc["source"]}_{i}',
                }
            )

    if not chunks:
        return {
            "chunks": [],
            "vectorizer": None,
            "matrix": None,
        }

    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000)
    matrix = vectorizer.fit_transform([c["text"] for c in chunks])

    return {
        "chunks": chunks,
        "vectorizer": vectorizer,
        "matrix": matrix,
    }


def get_context(query: str, top_k: int = 3) -> Tuple[str, List[str]]:
    index = _build_index()
    chunks = index["chunks"]
    vectorizer = index["vectorizer"]
    matrix = index["matrix"]

    if not chunks or vectorizer is None or matrix is None:
        return "", []

    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, matrix).flatten()

    ranked = scores.argsort()[::-1][:top_k]
    selected = [i for i in ranked if scores[i] > 0]

    if not selected:
        return "", []

    context_parts: List[str] = []
    sources: List[str] = []

    for i in selected:
        item = chunks[i]
        context_parts.append(f"[Source: {item['source']}]\n{item['text']}")
        if item["source"] not in sources:
            sources.append(item["source"])

    return "\n\n---\n\n".join(context_parts), sources