from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import httpx

# RAG system - inline implementation (no imports needed)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

# Simple in-memory document store
_DOCS: list = []

def ingest_corpus(docs: list) -> None:
    """Store documents in memory"""
    global _DOCS
    _DOCS = docs
    print(f"✅ Ingested {len(docs)} documents")

def answer_question(query: str, **kwargs) -> dict:
    """Answer a question using the ingested documents and OpenAI"""
    import os
    
    if not OPENAI_AVAILABLE:
        return {
            "answer": "OpenAI SDK not available.",
            "sources": []
        }
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "Por favor, proporciona tu clave de API de OpenAI para usar el chat con IA.",
            "sources": []
        }
    
    try:
        # Simple keyword-based search
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in _DOCS:
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

RAG_AVAILABLE = OPENAI_AVAILABLE


class PaymentMethod(BaseModel):
    type: str
    description: str


class SellerInfo(BaseModel):
    name: str
    reputation: str
    sales: int


class Review(BaseModel):
    id: str
    rating: int
    text: str
    author: str
    date: str
    verified_purchase: bool = False


class RatingBreakdown(BaseModel):
    five_stars: int
    four_stars: int
    three_stars: int
    two_stars: int
    one_star: int


class CharacteristicRating(BaseModel):
    name: str
    rating: float


class ReviewsData(BaseModel):
    overall_rating: float
    total_reviews: int
    rating_breakdown: RatingBreakdown
    characteristic_ratings: List[CharacteristicRating]
    reviews: List[Review]


class ItemDetail(BaseModel):
    id: str
    title: str
    description: str
    price: float
    currency: str
    images: List[str]
    payment_methods: List[PaymentMethod]
    seller: SellerInfo
    stock: int
    ratings: float
    reviews_count: int


app = FastAPI(title="GenAI Product Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_ITEM = ItemDetail(
    id="MLA123456",
    title="Samsung Galaxy A55 5G Dual SIM 256 GB 8 GB RAM (Celeste)",
    description=(
        "Capacidad y eficiencia en un diseño premium. El nuevo Galaxy A55 incorpora el procesador Exynos 1480, 8 GB de RAM y "
        "almacenamiento de 256 GB expandible para que disfrutes de múltiples aplicaciones sin límites. Su pantalla Super AMOLED de 6.6'' "
        "con Vision Booster ofrece colores intensos incluso a plena luz, mientras que la batería de 5000 mAh con carga rápida de 25 W te acompaña todo el día."
    ),
    price=972000,
    currency="ARS",
    images=[
        "/hero_1.webp",
        "/hero_2.webp",
        "/hero_3.webp",
        "/hero_4.webp",
        "/hero_5.webp",
        "/hero_6.webp",
    ],
    payment_methods=[
        PaymentMethod(type="credit_card", description="En 6x $ 162.000 sin interés"),
        PaymentMethod(type="credit_card", description="En 12x $ 81.000 sin interés"),
        PaymentMethod(type="transfer", description="Transferencia bancaria"),
        PaymentMethod(type="mercado_credito", description="Mercado Crédito - Cuotas con interés"),
    ],
    seller=SellerInfo(name="Samsung Official Store", reputation="Platinum", sales=15234),
    stock=18,
    ratings=4.8,
    reviews_count=464,
)

REVIEWS_DATA = ReviewsData(
    overall_rating=4.8,
    total_reviews=464,
    rating_breakdown=RatingBreakdown(
        five_stars=420,
        four_stars=42,
        three_stars=2,
        two_stars=0,
        one_star=0,
    ),
    characteristic_ratings=[
        CharacteristicRating(name="Relación precio-calidad", rating=4.5),
        CharacteristicRating(name="Calidad de la cámara", rating=4.5),
        CharacteristicRating(name="Duración de la batería", rating=4.5),
        CharacteristicRating(name="Durabilidad", rating=4.5),
    ],
    reviews=[
        Review(
            id="1",
            rating=5,
            text="Destaca por su cámara espectacular que captura fotos de alta calidad. Su rendimiento es excelente, con un procesador veloz y una batería duradera que cumple con las expectativas de los usuarios. Además, su diseño es atractivo y el teléfono es intuitivo y fácil de usar, lo que lo convierte en una opción muy recomendable.",
            author="Usuario verificado",
            date="Hace 2 días",
            verified_purchase=True,
        ),
        Review(
            id="2",
            rating=5,
            text="Es hermoso la cámara un espectáculo,y dura un montón la bacteria.",
            author="Usuario verificado",
            date="Hace 5 días",
            verified_purchase=True,
        ),
        Review(
            id="3",
            rating=5,
            text="Venía de un a54 y se nota mucho la diferencia con el nuevo procesador, si bien es un exynos, está versión cuenta con un gpu de tecnología amd. Se nota un mejor rendimiento y administración de energía. Además, no tiene tanto calentamiento como la versión anterior. Si bien no es un snapdragon, se notan mucho los cambios de una versión a la otra.",
            author="Usuario verificado",
            date="Hace 1 semana",
            verified_purchase=True,
        ),
        Review(
            id="4",
            rating=5,
            text="Yo tenia el samsung galaxy a30s, la verdad fue un cambio que se noto, y me gusta muchísimo.",
            author="Usuario verificado",
            date="Hace 1 semana",
            verified_purchase=True,
        ),
        Review(
            id="5",
            rating=5,
            text="Muy lindo es celular y muy buen precio me encantó 💕",
            author="Usuario verificado",
            date="Hace 2 semanas",
            verified_purchase=True,
        ),
        Review(
            id="6",
            rating=5,
            text="Mi celu es una preciosura!!!. Lo amo 💕. Super rápido e intuitivo. Las fotos que toma tienen una calidad magnífica y los videos son la gloria👌. Compren sin dudarlo. No se van a arrepentir. Gracias a los chicos por enviarlo super rápido y en un packaging hermoso!!. Son unos genios!! 😍. Compren sin dudar!. Mi experiencia fue un 10 🤩.",
            author="Usuario verificado",
            date="Hace 2 semanas",
            verified_purchase=True,
        ),
    ],
)


@app.get("/py-api/item", response_model=ItemDetail)
@app.get("/item", response_model=ItemDetail)  # Keep both for compatibility
def get_item_detail() -> ItemDetail:
    return SAMPLE_ITEM


@app.get("/py-api/reviews", response_model=ReviewsData)
@app.get("/reviews", response_model=ReviewsData)  # Keep both for compatibility
def get_reviews() -> ReviewsData:
    return REVIEWS_DATA


class ChatRequest(BaseModel):
    question: str
    openai_key: str = None


class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: Optional[float] = None


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    results: List[SearchResult]


@app.on_event("startup")
def _bootstrap_vectors() -> None:
    # Build a tiny in-memory corpus from existing sections
    if RAG_AVAILABLE:
        docs = [
            {"id": "title", "section": "Título", "text": SAMPLE_ITEM.title},
            {"id": "desc", "section": "Descripción", "text": SAMPLE_ITEM.description},
            {
                "id": "specs",
                "section": "Características del producto",
                "text": "\n".join([f"{c.name}: {c.rating}★" for c in REVIEWS_DATA.characteristic_ratings]),
            },
            {
                "id": "seller",
                "section": "Vendedor",
                "text": f"{SAMPLE_ITEM.seller.name} reputación {SAMPLE_ITEM.seller.reputation} ventas {SAMPLE_ITEM.seller.sales}",
            },
            {
                "id": "payments",
                "section": "Medios de pago",
                "text": ", ".join([m.description for m in SAMPLE_ITEM.payment_methods]),
            },
            {
                "id": "reviews",
                "section": "Opiniones destacadas",
                "text": "\n\n".join([r.text for r in REVIEWS_DATA.reviews]),
            },
        ]
        ingest_corpus(docs)


@app.post("/py-api/search", response_model=SearchResponse)
@app.post("/search", response_model=SearchResponse)  # Keep both for compatibility
async def search_endpoint(payload: SearchRequest):
    """Search MercadoLibre Argentina using Tavily API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": "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",
                    "query": f"{payload.query} -wikipedia -wikimedia mercadolibre.com.ar",
                    "search_depth": "basic",
                    "include_answer": False,
                    "include_images": False,
                    "include_raw_content": False,
                    "max_results": 7
                },
                headers={"Content-Type": "application/json"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("results", [])[:7]:
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        content=item.get("content", ""),
                        score=item.get("score")
                    ))
                
                return SearchResponse(results=results)
            else:
                return SearchResponse(results=[])
                
    except Exception as e:
        print(f"Search error: {e}")
        return SearchResponse(results=[])


@app.post("/py-api/agent/chat")
@app.post("/agent/chat")  # Keep both for compatibility
def chat_endpoint(payload: ChatRequest):
    # Temporarily set the API key if provided
    import os
    original_key = os.environ.get("OPENAI_API_KEY")
    if payload.openai_key:
        os.environ["OPENAI_API_KEY"] = payload.openai_key
    
    try:
        result = answer_question(payload.question, top_k=4, language="es")
        return result
    finally:
        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key
        elif "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]


# No special handler needed - Vercel handles FastAPI directly

