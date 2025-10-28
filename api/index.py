from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import httpx
from mangum import Mangum

# RAG system disabled for serverless deployment
RAG_AVAILABLE = False
def ingest_corpus(*args, **kwargs):
    pass
def answer_question(query, **kwargs):
    return {
        "answer": "AI chat is not available in this deployment. The feature requires additional configuration.",
        "sources": []
    }


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


@app.get("/api/item", response_model=ItemDetail)
def get_item_detail() -> ItemDetail:
    return SAMPLE_ITEM


@app.get("/api/reviews", response_model=ReviewsData)
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


# Startup event disabled for serverless - runs on each request instead
# @app.on_event("startup")
# def _bootstrap_vectors() -> None:
#     pass


@app.post("/api/search", response_model=SearchResponse)
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


@app.post("/api/agent/chat")
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


# Vercel handler with Mangum
handler = Mangum(app, lifespan="off")

