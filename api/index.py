from fastapi import FastAPI, Query
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

def answer_question(query: str, language: str = "es", **kwargs) -> dict:
    """Answer a question using the ingested documents and OpenAI"""
    import os
    
    # Get translations for the specified language
    t = TRANSLATIONS.get(language, TRANSLATIONS["es"])
    
    if not OPENAI_AVAILABLE:
        return {
            "answer": "OpenAI SDK not available.",
            "sources": []
        }
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": t["no_api_key"],
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
        
        system_prompt = t["system_prompt"]
        
        user_prompt = f"""{t["context_prefix"]}
{context}

{t["question_prefix"]} {query}

{t["answer_instruction"]}"""
        
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
        error_msg = {
            "es": f"Error al procesar tu pregunta: {str(e)[:100]}",
            "pt": f"Erro ao processar sua pergunta: {str(e)[:100]}",
            "en": f"Error processing your question: {str(e)[:100]}"
        }
        return {
            "answer": error_msg.get(language, error_msg["es"]),
            "sources": []
        }

RAG_AVAILABLE = OPENAI_AVAILABLE


# Translation dictionaries
TRANSLATIONS = {
    "es": {
        "title": "Samsung Galaxy A55 5G Dual SIM 256 GB 8 GB RAM (Celeste)",
        "description": "Capacidad y eficiencia en un diseño premium. El nuevo Galaxy A55 incorpora el procesador Exynos 1480, 8 GB de RAM y almacenamiento de 256 GB expandible para que disfrutes de múltiples aplicaciones sin límites. Su pantalla Super AMOLED de 6.6'' con Vision Booster ofrece colores intensos incluso a plena luz, mientras que la batería de 5000 mAh con carga rápida de 25 W te acompaña todo el día.",
        "payment1": "En 6x $71.50 sin interés",
        "payment2": "En 12x $35.75 sin interés",
        "payment3": "Transferencia bancaria",
        "payment4": "Cuotas con interés",
        "char1": "Relación precio-calidad",
        "char2": "Calidad de la cámara",
        "char3": "Duración de la batería",
        "char4": "Durabilidad",
        "system_prompt": "Eres un asistente de compras inteligente. Responde preguntas sobre el producto basándote ÚNICAMENTE en la información proporcionada. Si no tienes información suficiente, dilo claramente. Responde en español de manera concisa y útil.",
        "no_api_key": "Por favor, proporciona tu clave de API de OpenAI para usar el chat con IA.",
        "context_prefix": "Contexto del producto:",
        "question_prefix": "Pregunta del usuario:",
        "answer_instruction": "Responde basándote en el contexto proporcionado:",
        "verified_user": "Usuario verificado",
        "days_ago": "Hace {} días",
        "weeks_ago": "Hace {} semana" if 1 else "Hace {} semanas",
        "review1": "Destaca por su cámara espectacular que captura fotos de alta calidad. Su rendimiento es excelente, con un procesador veloz y una batería duradera que cumple con las expectativas de los usuarios. Además, su diseño es atractivo y el teléfono es intuitivo y fácil de usar, lo que lo convierte en una opción muy recomendable.",
        "review2": "Es hermoso la cámara un espectáculo,y dura un montón la bacteria.",
        "review3": "Venía de un a54 y se nota mucho la diferencia con el nuevo procesador, si bien es un exynos, está versión cuenta con un gpu de tecnología amd. Se nota un mejor rendimiento y administración de energía. Además, no tiene tanto calentamiento como la versión anterior. Si bien no es un snapdragon, se notan mucho los cambios de una versión a la otra.",
        "review4": "Yo tenia el samsung galaxy a30s, la verdad fue un cambio que se noto, y me gusta muchísimo.",
        "review5": "Muy lindo es celular y muy buen precio me encantó 💕",
        "review6": "Mi celu es una preciosura!!!. Lo amo 💕. Super rápido e intuitivo. Las fotos que toma tienen una calidad magnífica y los videos son la gloria👌. Compren sin dudarlo. No se van a arrepentir. Gracias a los chicos por enviarlo super rápido y en un packaging hermoso!!. Son unos genios!! 😍. Compren sin dudar!. Mi experiencia fue un 10 🤩.",
        "date1": "Hace 2 días",
        "date2": "Hace 5 días",
        "date3": "Hace 1 semana",
        "date4": "Hace 1 semana",
        "date5": "Hace 2 semanas",
        "date6": "Hace 2 semanas",
    },
    "pt": {
        "title": "Samsung Galaxy A55 5G Dual SIM 256 GB 8 GB RAM (Azul Claro)",
        "description": "Capacidade e eficiência em um design premium. O novo Galaxy A55 incorpora o processador Exynos 1480, 8 GB de RAM e armazenamento de 256 GB expansível para que você aproveite vários aplicativos sem limites. Sua tela Super AMOLED de 6,6'' com Vision Booster oferece cores intensas mesmo sob luz solar direta, enquanto a bateria de 5000 mAh com carga rápida de 25 W acompanha você o dia todo.",
        "payment1": "Em 6x $71.50 sem juros",
        "payment2": "Em 12x $35.75 sem juros",
        "payment3": "Transferência bancária",
        "payment4": "Parcelas com juros",
        "char1": "Relação preço-qualidade",
        "char2": "Qualidade da câmera",
        "char3": "Duração da bateria",
        "char4": "Durabilidade",
        "system_prompt": "Você é um assistente de compras inteligente. Responda perguntas sobre o produto baseando-se APENAS nas informações fornecidas. Se não tiver informações suficientes, diga claramente. Responda em português de forma concisa e útil.",
        "no_api_key": "Por favor, forneça sua chave da API OpenAI para usar o chat com IA.",
        "context_prefix": "Contexto do produto:",
        "question_prefix": "Pergunta do usuário:",
        "answer_instruction": "Responda com base no contexto fornecido:",
        "verified_user": "Usuário verificado",
        "days_ago": "Há {} dias",
        "weeks_ago": "Há {} semana" if 1 else "Há {} semanas",
        "review1": "Destaca-se pela sua câmera espetacular que captura fotos de alta qualidade. Seu desempenho é excelente, com um processador rápido e uma bateria durável que atende às expectativas dos usuários. Além disso, seu design é atraente e o telefone é intuitivo e fácil de usar, tornando-o uma opção muito recomendável.",
        "review2": "É lindo, a câmera é um espetáculo e a bateria dura muito.",
        "review3": "Vinha de um A54 e nota-se muito a diferença com o novo processador, embora seja um Exynos, esta versão tem uma GPU de tecnologia AMD. Nota-se melhor desempenho e gestão de energia. Além disso, não aquece tanto quanto a versão anterior. Embora não seja um Snapdragon, as mudanças de uma versão para outra são muito notáveis.",
        "review4": "Eu tinha o Samsung Galaxy A30s, a verdade foi uma mudança notável e eu gosto muito.",
        "review5": "Muito lindo é o celular e muito bom preço, adorei 💕",
        "review6": "Meu celular é uma preciosidade!!!. Eu amo 💕. Super rápido e intuitivo. As fotos que tira têm qualidade magnífica e os vídeos são a glória👌. Comprem sem duvidar. Não vão se arrepender. Obrigado aos rapazes por enviá-lo super rápido e em uma embalagem linda!!. São uns gênios!! 😍. Comprem sem duvidar!. Minha experiência foi um 10 🤩.",
        "date1": "Há 2 dias",
        "date2": "Há 5 dias",
        "date3": "Há 1 semana",
        "date4": "Há 1 semana",
        "date5": "Há 2 semanas",
        "date6": "Há 2 semanas",
    },
    "en": {
        "title": "Samsung Galaxy A55 5G Dual SIM 256 GB 8 GB RAM (Light Blue)",
        "description": "Capacity and efficiency in a premium design. The new Galaxy A55 features the Exynos 1480 processor, 8 GB of RAM, and 256 GB of expandable storage so you can enjoy multiple apps without limits. Its 6.6'' Super AMOLED display with Vision Booster offers intense colors even in bright sunlight, while the 5000 mAh battery with 25W fast charging keeps you going all day.",
        "payment1": "In 6x $71.50 interest-free",
        "payment2": "In 12x $35.75 interest-free",
        "payment3": "Bank transfer",
        "payment4": "Installments with interest",
        "char1": "Price-quality ratio",
        "char2": "Camera quality",
        "char3": "Battery life",
        "char4": "Durability",
        "system_prompt": "You are an intelligent shopping assistant. Answer questions about the product based ONLY on the information provided. If you don't have enough information, say so clearly. Respond in English concisely and helpfully.",
        "no_api_key": "Please provide your OpenAI API key to use the AI chat.",
        "context_prefix": "Product context:",
        "question_prefix": "User question:",
        "answer_instruction": "Answer based on the provided context:",
        "verified_user": "Verified user",
        "days_ago": "{} days ago",
        "weeks_ago": "{} week ago" if 1 else "{} weeks ago",
        "review1": "It stands out for its spectacular camera that captures high-quality photos. Its performance is excellent, with a fast processor and long-lasting battery that meets user expectations. Additionally, its design is attractive and the phone is intuitive and easy to use, making it a highly recommended option.",
        "review2": "It's beautiful, the camera is spectacular, and the battery lasts a long time.",
        "review3": "I came from an A54 and the difference with the new processor is very noticeable. Although it's an Exynos, this version has an AMD technology GPU. You can notice better performance and power management. Also, it doesn't heat up as much as the previous version. While it's not a Snapdragon, the changes from one version to another are very noticeable.",
        "review4": "I had the Samsung Galaxy A30s, it was truly a noticeable change and I love it.",
        "review5": "Very beautiful phone and great price, I loved it 💕",
        "review6": "My phone is gorgeous!!!. I love it 💕. Super fast and intuitive. The photos it takes have magnificent quality and the videos are glorious👌. Buy without hesitation. You won't regret it. Thanks to the guys for sending it super fast and in beautiful packaging!!. They're geniuses!! 😍. Buy without hesitation!. My experience was a 10 🤩.",
        "date1": "2 days ago",
        "date2": "5 days ago",
        "date3": "1 week ago",
        "date4": "1 week ago",
        "date5": "2 weeks ago",
        "date6": "2 weeks ago",
    },
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
    title="Samsung Galaxy A55 5G Dual SIM 256 GB 8 GB RAM (Light Blue)",
    description=(
        "Capacity and efficiency in a premium design. The new Galaxy A55 features the Exynos 1480 processor, 8 GB of RAM, and "
        "256 GB of expandable storage so you can enjoy multiple apps without limits. Its 6.6'' Super AMOLED display "
        "with Vision Booster offers intense colors even in bright sunlight, while the 5000 mAh battery with 25W fast charging keeps you going all day."
    ),
    price=429.00,
    currency="USD",
    images=[
        "/hero_1.webp",
        "/hero_2.webp",
        "/hero_3.webp",
        "/hero_4.webp",
        "/hero_5.webp",
        "/hero_6.webp",
    ],
    payment_methods=[
        PaymentMethod(type="credit_card", description="In 6x $71.50 interest-free"),
        PaymentMethod(type="credit_card", description="In 12x $35.75 interest-free"),
        PaymentMethod(type="transfer", description="Bank transfer"),
        PaymentMethod(type="installments", description="Installments with interest"),
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
def get_item_detail(lang: str = Query("es", regex="^(es|pt|en)$")) -> ItemDetail:
    """Get item details in the specified language"""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["es"])
    
    return ItemDetail(
        id=SAMPLE_ITEM.id,
        title=t["title"],
        description=t["description"],
        price=SAMPLE_ITEM.price,
        currency=SAMPLE_ITEM.currency,
        images=SAMPLE_ITEM.images,
        payment_methods=[
            PaymentMethod(type="credit_card", description=t["payment1"]),
            PaymentMethod(type="credit_card", description=t["payment2"]),
            PaymentMethod(type="transfer", description=t["payment3"]),
            PaymentMethod(type="mercado_credito", description=t["payment4"]),
        ],
        seller=SAMPLE_ITEM.seller,
        stock=SAMPLE_ITEM.stock,
        ratings=SAMPLE_ITEM.ratings,
        reviews_count=SAMPLE_ITEM.reviews_count,
    )


@app.get("/py-api/reviews", response_model=ReviewsData)
@app.get("/reviews", response_model=ReviewsData)  # Keep both for compatibility
def get_reviews(lang: str = Query("es", regex="^(es|pt|en)$")) -> ReviewsData:
    """Get reviews in the specified language"""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["es"])
    
    # Translate reviews
    translated_reviews = [
        Review(
            id="1",
            rating=5,
            text=t["review1"],
            author=t["verified_user"],
            date=t["date1"],
            verified_purchase=True,
        ),
        Review(
            id="2",
            rating=5,
            text=t["review2"],
            author=t["verified_user"],
            date=t["date2"],
            verified_purchase=True,
        ),
        Review(
            id="3",
            rating=5,
            text=t["review3"],
            author=t["verified_user"],
            date=t["date3"],
            verified_purchase=True,
        ),
        Review(
            id="4",
            rating=5,
            text=t["review4"],
            author=t["verified_user"],
            date=t["date4"],
            verified_purchase=True,
        ),
        Review(
            id="5",
            rating=5,
            text=t["review5"],
            author=t["verified_user"],
            date=t["date5"],
            verified_purchase=True,
        ),
        Review(
            id="6",
            rating=5,
            text=t["review6"],
            author=t["verified_user"],
            date=t["date6"],
            verified_purchase=True,
        ),
    ]
    
    return ReviewsData(
        overall_rating=REVIEWS_DATA.overall_rating,
        total_reviews=REVIEWS_DATA.total_reviews,
        rating_breakdown=REVIEWS_DATA.rating_breakdown,
        characteristic_ratings=[
            CharacteristicRating(name=t["char1"], rating=4.5),
            CharacteristicRating(name=t["char2"], rating=4.5),
            CharacteristicRating(name=t["char3"], rating=4.5),
            CharacteristicRating(name=t["char4"], rating=4.5),
        ],
        reviews=translated_reviews,
    )


class ChatRequest(BaseModel):
    question: str
    openai_key: str = None
    language: str = "es"


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
    """Search Amazon using Tavily API - defaults to amazon.com"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": "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",
                    "query": f"{payload.query} site:amazon.com -wikipedia -wikimedia",
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
    # Ensure documents are ingested (serverless might not preserve state)
    if len(_DOCS) == 0:
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
        print(f"✅ Documents ingested on-demand: {len(docs)} docs")
    
    # Temporarily set the API key if provided
    import os
    original_key = os.environ.get("OPENAI_API_KEY")
    if payload.openai_key:
        os.environ["OPENAI_API_KEY"] = payload.openai_key
    
    try:
        result = answer_question(payload.question, language=payload.language, top_k=4)
        return result
    finally:
        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key
        elif "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]


# No special handler needed - Vercel handles FastAPI directly

