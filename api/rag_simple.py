"""
Simple RAG implementation using only OpenAI SDK - no LangChain
"""
import os
from typing import List, Dict, Any
import json

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


# Simple in-memory document store
_DOCS: List[Dict[str, Any]] = []


def ingest_corpus(docs: List[Dict[str, Any]]) -> None:
    """Store documents in memory"""
    global _DOCS
    _DOCS = docs
    print(f"✅ Ingested {len(docs)} documents")


def answer_question(query: str, **kwargs) -> Dict[str, Any]:
    """
    Answer a question using the ingested documents and OpenAI.
    Simple keyword-based retrieval + GPT completion.
    """
    if not OPENAI_AVAILABLE:
        return {
            "answer": "OpenAI SDK not available. Please check deployment.",
            "sources": []
        }
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "Por favor, proporciona tu clave de API de OpenAI para usar el chat con IA.",
            "sources": []
        }
    
    try:
        # Simple keyword-based search (no embeddings)
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in _DOCS:
            # Simple scoring: count keyword matches
            text_lower = doc.get("text", "").lower()
            score = sum(1 for word in query_lower.split() if word in text_lower)
            if score > 0:
                relevant_docs.append((score, doc))
        
        # Sort by score and take top 3
        relevant_docs.sort(reverse=True, key=lambda x: x[0])
        top_docs = [doc for _, doc in relevant_docs[:3]]
        
        # Build context
        context = "\n\n".join([
            f"Sección: {doc['section']}\n{doc['text']}"
            for doc in top_docs
        ])
        
        # Call OpenAI
        client = OpenAI(api_key=api_key)
        
        system_prompt = """Eres un asistente de compras inteligente. 
Responde preguntas sobre el producto basándote ÚNICAMENTE en la información proporcionada.
Si no tienes información suficiente, dilo claramente.
Responde en español de manera concisa y útil."""
        
        user_prompt = f"""Contexto del producto:
{context}

Pregunta del usuario: {query}

Responde basándote en el contexto proporcionado:"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        answer = response.choices[0].message.content
        sources = [doc['section'] for doc in top_docs]
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        return {
            "answer": f"Error al procesar tu pregunta: {str(e)[:100]}",
            "sources": []
        }

