import os
from typing import List, Dict, Any, Optional

import numpy as np
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


# Simple in-memory vector store
_DOCS: List[Dict[str, Any]] = []
_EMBEDDINGS: Optional[np.ndarray] = None
_embedder: Optional[OpenAIEmbeddings] = None


def _ensure_embedder() -> Optional[OpenAIEmbeddings]:
    global _embedder
    current_key = os.getenv("OPENAI_API_KEY")
    if current_key and (not _embedder or getattr(_embedder, '_api_key', None) != current_key):
        try:
            _embedder = OpenAIEmbeddings(model="text-embedding-3-small")
        except Exception:
            _embedder = None
    elif not current_key:
        _embedder = None
    return _embedder


def ingest_corpus(docs: List[Dict[str, Any]]) -> None:
    """Ingest documents into an in-memory vector store.

    Each doc should be {id, section, text}.
    """
    global _DOCS, _EMBEDDINGS
    _DOCS = [d for d in docs if d.get("text")]
    if not _DOCS:
        _EMBEDDINGS = None
        return

    embedder = _ensure_embedder()
    if embedder is None:
        # No API key, use simple keyword matching instead
        _EMBEDDINGS = None
        return
        
    texts = [d["text"] for d in _DOCS]
    vectors = embedder.embed_documents(texts)
    _EMBEDDINGS = np.array(vectors, dtype=np.float32)


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    b_norm = b / (np.linalg.norm(b) + 1e-8)
    return np.dot(a_norm, b_norm)


def answer_question(query: str, top_k: int = 3, language: str = "es") -> Dict[str, Any]:
    """Retrieve top-k docs and generate an answer with citations.

    Returns {answer: str, sources: List[{section, snippet}]}.
    """
    global _EMBEDDINGS
    
    if not _DOCS:
        return {
            "answer": "Aún no hay información indexada para responder. Intentalo más tarde.",
            "sources": [],
        }

    # Check if we need to re-embed with new API key
    embedder = _ensure_embedder()
    if embedder is not None and _EMBEDDINGS is None:
        # Re-embed documents with new API key
        texts = [d["text"] for d in _DOCS]
        vectors = embedder.embed_documents(texts)
        _EMBEDDINGS = np.array(vectors, dtype=np.float32)

    # If no embeddings available, use simple keyword matching
    if _EMBEDDINGS is None:
        query_words = set(query.lower().split())
        scored_docs = []
        for i, doc in enumerate(_DOCS):
            doc_words = set(doc["text"].lower().split())
            score = len(query_words.intersection(doc_words))
            if score > 0:
                scored_docs.append((score, i))
        
        scored_docs.sort(reverse=True)
        retrieved = [_DOCS[i] for _, i in scored_docs[:top_k]]
        
        if not retrieved:
            return {
                "answer": "No encontré información específica sobre tu pregunta en los datos del producto.",
                "sources": [],
            }
        
        # Create a clean summary without special characters
        product_info = " ".join([d["text"][:200] for d in retrieved])
        clean_info = product_info.replace("[", "").replace("]", "").replace("*", "").replace("<", "").replace(">", "")
        return {
            "answer": f"Basado en la información disponible: {clean_info[:300]}...",
            "sources": [{"section": d["section"], "snippet": d["text"][:160]} for d in retrieved],
        }

    embedder = _ensure_embedder()
    if embedder is None:
        # Fallback to keyword matching
        return answer_question(query, top_k, language)
        
    q_vec = np.array(embedder.embed_query(query), dtype=np.float32)
    sims = _cosine_sim(_EMBEDDINGS, q_vec)
    idxs = np.argsort(-sims)[: max(1, top_k)]
    retrieved = [_DOCS[i] for i in idxs]

    context = "\n\n".join(
        [f"{d['section']}: {d['text'][:800]}" for d in retrieved]
    )

    # If no API key, return a heuristic extractive answer
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "answer": (
                "(Modo sin LLM) Resumen basado en contexto:\n" + context[:600]
            ),
            "sources": [{"section": d["section"], "snippet": d["text"][:160]} for d in retrieved],
        }

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = (
        "Eres un asistente de compras inteligente. Responde en español de forma natural y conversacional. "
        "Usa la información del contexto para responder de manera útil y precisa. "
        "NO uses corchetes, asteriscos, o caracteres especiales en tu respuesta. "
        "Responde de forma fluida como si fueras un experto en productos.\n\n"
        f"Contexto del producto:\n{context}\n\n"
        f"Pregunta del cliente: {query}\n\n"
        "Responde de forma natural y útil, sin caracteres especiales o formato markdown."
    )
    msg = llm.invoke(prompt)
    answer = msg.content if hasattr(msg, "content") else str(msg)
    return {
        "answer": answer,
        "sources": [{"section": d["section"], "snippet": d["text"][:160]} for d in retrieved],
    }


