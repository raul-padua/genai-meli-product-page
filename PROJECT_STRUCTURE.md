# 📁 Project Structure Overview

This document provides a detailed breakdown of the GenAI Product Assistant project structure and file organization.

## 🏗️ Root Directory Structure

```
genai-evaluation/
├── 📄 README.md                    # Main project documentation
├── 📄 RUN.md                       # Setup and execution guide
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📁 frontend/                    # Next.js React application
└── 📁 backend/                     # FastAPI Python application
```

## 🎨 Frontend Structure (`frontend/`)

```
frontend/
├── 📄 package.json                 # Node.js dependencies and scripts
├── 📄 next.config.ts               # Next.js configuration
├── 📄 tailwind.config.js           # Tailwind CSS configuration
├── 📄 tsconfig.json                # TypeScript configuration
├── 📁 public/                      # Static assets
│   ├── 🖼️ logo_MELI.png            # E-commerce platform logo
│   ├── 🖼️ hero_1.webp to hero_6.webp  # Product images
│   ├── 🖼️ galaxy_*.webp           # Related product images
│   ├── 🖼️ opinion_photo_*.webp     # Review photos
│   ├── 🖼️ payment_*.png           # Payment method logos
│   └── 🖼️ efectivo.png            # Cash payment logo
└── 📁 src/
    └── 📁 app/
        ├── 📄 page.tsx             # Main product detail page
        ├── 📄 page.module.css      # Component-specific styles
        ├── 📄 globals.css          # Global styles
        ├── 📄 layout.tsx           # Root layout component
        └── 📄 favicon.ico          # Site favicon
```

### Frontend Key Files

- **`src/app/page.tsx`**: Main React component with product display, chat widget, and search functionality
- **`src/app/page.module.css`**: Comprehensive CSS with e-commerce styling
- **`public/`**: Image assets for product gallery, reviews, and payment methods

## ⚙️ Backend Structure (`backend/`)

```
backend/
├── 📄 main.py                      # FastAPI application and endpoints
├── 📄 rag.py                       # RAG system implementation
├── 📄 requirements.txt             # Python dependencies
├── 📄 pytest.ini                  # Test configuration
├── 📄 run_tests.py                # Custom test runner
├── 📁 .venv/                      # Python virtual environment
└── 📁 tests/                      # Unit test suite
    ├── 📄 __init__.py             # Test package initialization
    ├── 📄 test_api.py             # API endpoint tests
    ├── 📄 test_rag.py             # RAG functionality tests
    └── 📄 README.md               # Test documentation
```

### Backend Key Files

- **`main.py`**: FastAPI app with endpoints for items, reviews, chat, and search
- **`rag.py`**: RAG system with OpenAI integration and keyword fallback
- **`tests/`**: Comprehensive test suite with 36 test cases

## 🔌 API Endpoints Structure

### Core Endpoints (`main.py`)

```python
# Data Endpoints
@app.get("/item")                   # Product information
@app.get("/reviews")               # Reviews and ratings

# AI Endpoints  
@app.post("/agent/chat")           # RAG-powered chat
@app.post("/search")               # Tavily search integration

# Health Check
@app.get("/")                      # API health check
```

### Data Models

```python
# Product Data
SAMPLE_ITEM = {
    "title": "Samsung Galaxy A55 5G Celeste",
    "price": 972000,
    "currency": "ARS",
    "seller": {...},
    "payment_methods": [...],
    "images": [...],
    "specifications": [...]
}

# Review Data
REVIEWS_DATA = {
    "overall_rating": 4.5,
    "total_reviews": 464,
    "rating_breakdown": {...},
    "characteristic_ratings": [...],
    "reviews": [...]
}
```

## 🧠 RAG System Structure (`rag.py`)

```python
# Core Functions
def ingest_corpus(docs)            # Document ingestion and embedding
def answer_question(question)      # Question answering with RAG
def _ensure_embedder()             # OpenAI embedder initialization
def _cosine_sim(a, b)             # Cosine similarity calculation

# Global Variables
_EMBEDDINGS = None                 # In-memory vector store
_CORPUS = []                       # Document corpus
_EMBEDDER = None                   # OpenAI embedder instance
```

## 🧪 Test Structure (`tests/`)

```
tests/
├── 📄 __init__.py                 # Package initialization
├── 📄 test_api.py                 # API endpoint testing
│   ├── TestItemEndpoint          # Product data tests
│   ├── TestReviewsEndpoint       # Review data tests
│   ├── TestSearchEndpoint        # Search functionality tests
│   ├── TestChatEndpoint          # Chat functionality tests
│   ├── TestDataConsistency       # Cross-endpoint validation
│   ├── TestErrorHandling         # Error scenario testing
│   └── TestPriceAndInstallments  # Pricing validation
├── 📄 test_rag.py                # RAG system testing
│   ├── TestRAGIngestion          # Document processing tests
│   ├── TestRAGAnswering          # Question answering tests
│   ├── TestRAGUtilities          # Utility function tests
│   └── TestRAGIntegration        # End-to-end workflow tests
└── 📄 README.md                  # Test documentation
```

## 🎨 Frontend Component Structure

### Main Page Component (`page.tsx`)

```typescript
// State Management
const [item, setItem] = useState<Item | null>(null);
const [selectedImage, setSelectedImage] = useState<string>("");
const [chatOpen, setChatOpen] = useState<boolean>(false);
const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
const [searchQuery, setSearchQuery] = useState<string>("");

// Static Data
const RELATED_PRODUCTS = [...];    // Seller's other products
const ALSO_BOUGHT = [...];         // Recommended products
const SPECIFICATIONS = [...];      // Product specifications

// Functions
const fetchItem = async () => {...};        // API data fetching
const sendChat = async () => {...};         // Chat functionality
const performSearch = async () => {...};    // Search functionality
```

### CSS Module Structure (`page.module.css`)

```css
/* Layout Components */
.page, .banner, .searchBar, .gallery, .productInfo
.mainImage, .thumbnails, .buyBox, .paymentMethods

/* Carousel Components */
.carouselContainer, .carouselTrack, .carouselButton
.sellerCarouselContainer, .sellerCarouselItem

/* Chat Components */
.chatFab, .chatPanel, .chatBody, .chatInputRow
.chatBubbleUser, .chatBubbleBot, .typingIndicator

/* Search Components */
.searchDropdown, .searchResult, .searchLoading

/* Review Components */
.ratingsSection, .ratingBreakdown, .reviewItem
.characteristicRating, .opinionPhoto
```

## 🔧 Configuration Files

### Frontend Configuration

- **`package.json`**: Dependencies, scripts, and metadata
- **`next.config.ts`**: Next.js configuration and image domains
- **`tailwind.config.js`**: Tailwind CSS customization
- **`tsconfig.json`**: TypeScript compiler options

### Backend Configuration

- **`requirements.txt`**: Python package dependencies
- **`pytest.ini`**: Test configuration and markers
- **`run_tests.py`**: Custom test runner with options

## 📊 Data Flow Architecture

```
Frontend (Next.js)          Backend (FastAPI)           External APIs
     │                           │                           │
     ├─ GET /item ──────────────►├─ Return product data      │
     ├─ GET /reviews ───────────►├─ Return review data       │
     ├─ POST /agent/chat ───────►├─ RAG Processing ────────► OpenAI API
     └─ POST /search ───────────►├─ Search Processing ─────► Tavily API
```

## 🎯 Key Integration Points

### Frontend-Backend Communication
- **API Base URL**: `http://127.0.0.1:8000`
- **CORS Configuration**: Enabled for frontend domain
- **Data Validation**: Pydantic models ensure data integrity

### AI System Integration
- **OpenAI Embeddings**: Text-to-vector conversion
- **OpenAI Chat**: GPT-4 for intelligent responses
- **Tavily Search**: Real-time web search integration

### State Management
- **React Hooks**: Local component state
- **API Calls**: Async data fetching
- **Real-time Updates**: Chat and search interactions

## 📈 Performance Considerations

### Frontend Optimization
- **Image Optimization**: Next.js automatic image optimization
- **Code Splitting**: Component-level lazy loading
- **CSS Modules**: Scoped styling for better performance

### Backend Optimization
- **Async Operations**: Non-blocking I/O operations
- **Vector Caching**: In-memory embedding storage
- **Error Handling**: Graceful degradation and fallbacks

## 🔐 Security Structure

### API Security
- **Input Validation**: Pydantic model validation
- **CORS Configuration**: Controlled cross-origin access
- **Error Sanitization**: Safe error message handling

### Data Security
- **API Key Management**: Secure key handling
- **Environment Variables**: Sensitive data protection
- **Request Validation**: Input sanitization and validation

---

This structure provides a solid foundation for the GenAI Product Assistant, with clear separation of concerns and comprehensive testing coverage.
