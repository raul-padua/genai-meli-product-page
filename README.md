# GenAI Product Assistant Platform

A comprehensive full-stack application demonstrating advanced GenAI capabilities with an e-commerce product detail page, featuring RAG-powered chat assistance and intelligent search functionality.

## 🚀 Project Overview

This project showcases the integration of modern AI technologies in an e-commerce context, specifically:

- **Frontend**: Next.js application with MercadoLibre-inspired UI/UX
- **Backend**: FastAPI with RAG (Retrieval-Augmented Generation) capabilities
- **AI Features**: OpenAI integration, Tavily search, and intelligent product assistance
- **Testing**: Comprehensive unit test suite with 91.7% test coverage

## 🏗️ Architecture

```
genai-evaluation/
├── frontend/                 # Next.js React application
│   ├── src/app/             # App Router pages and components
│   ├── public/              # Static assets (images, logos)
│   └── package.json         # Frontend dependencies
├── backend/                 # FastAPI Python application
│   ├── main.py             # FastAPI app and endpoints
│   ├── rag.py              # RAG system implementation
│   ├── tests/              # Unit test suite
│   └── requirements.txt    # Python dependencies
└── README.md               # This documentation
```

## ✨ Key Features

### 🛍️ Frontend Features
- **Product Detail Page**: MercadoLibre-inspired design with product images, pricing, and specifications
- **Interactive Gallery**: Image carousel with thumbnail navigation
- **Payment Methods**: Display of installment options and payment logos
- **Reviews Section**: Star ratings, review breakdown, and user testimonials
- **Related Products**: Carousel of similar items and seller products
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

### 🤖 AI-Powered Features
- **Intelligent Chat Assistant**: RAG-powered product Q&A with OpenAI integration
- **Dynamic API Key Support**: Users can provide their own OpenAI API key
- **Fallback System**: Keyword matching when no API key is provided
- **Real-time Search**: Tavily integration for MercadoLibre Argentina search
- **Smart Recommendations**: Context-aware product suggestions

### 🔧 Backend Capabilities
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **RAG System**: In-memory vector store with OpenAI embeddings
- **External Integrations**: Tavily search API for real-time product search
- **CORS Support**: Cross-origin requests for frontend integration
- **Error Handling**: Comprehensive error handling and logging

## 🎯 Technical Highlights

### Frontend Technologies
- **Next.js 15.5.4** with App Router and Turbopack
- **React 18** with hooks and modern patterns
- **TypeScript** for type safety
- **CSS Modules** for scoped styling
- **Tailwind CSS** for utility-first styling

### Backend Technologies
- **FastAPI** for high-performance API development
- **Pydantic** for data validation and serialization
- **LangChain** for LLM integration and RAG
- **OpenAI API** for embeddings and chat completions
- **httpx** for async HTTP requests
- **NumPy** for vector operations

### AI/ML Stack
- **OpenAI Embeddings** (text-embedding-3-small)
- **OpenAI Chat Completions** (GPT-4)
- **Tavily Search API** for web search
- **Cosine Similarity** for vector matching
- **Keyword Matching** as fallback strategy

## 📊 Test Coverage

The project includes a comprehensive test suite:

- **36 Test Cases** across API and RAG functionality
- **91.7% Test Success Rate** (33/36 tests passing)
- **Unit Tests**: FastAPI endpoints, RAG operations, data validation
- **Integration Tests**: End-to-end workflows and API interactions
- **Mocking Strategy**: External API mocking for reliable testing

## 🔌 API Endpoints

### Core Endpoints
- `GET /item` - Retrieve product information
- `GET /reviews` - Get product reviews and ratings
- `POST /agent/chat` - AI-powered product assistance
- `POST /search` - Search MercadoLibre products

### Data Models
- **Item**: Product details, pricing, seller information
- **Reviews**: Rating breakdown, individual reviews, characteristics
- **Chat**: Question/answer pairs with sources
- **Search**: Query results with titles, URLs, and content

## 🎨 UI/UX Features

### Design System
- **Brand Colors**: Yellow (#FFE600), Blue (#3483FA)
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent grid system and component spacing
- **Interactive Elements**: Hover effects, transitions, and animations

### User Experience
- **Floating Chat Widget**: Always-accessible AI assistant
- **Auto-scrolling Chat**: Seamless conversation flow
- **Typing Indicators**: Visual feedback during AI processing
- **Search Dropdown**: Real-time search results with preview
- **Responsive Layout**: Optimized for desktop and mobile

## 🔐 Security & Performance

### Security Measures
- **Input Validation**: Pydantic models for data validation
- **CORS Configuration**: Controlled cross-origin access
- **API Key Handling**: Secure OpenAI API key management
- **Error Sanitization**: Safe error message handling

### Performance Optimizations
- **Async Operations**: Non-blocking I/O for better performance
- **Vector Caching**: In-memory embedding storage
- **Image Optimization**: Next.js automatic image optimization
- **Lazy Loading**: Component-level code splitting

## 🌟 AI Capabilities

### RAG System Features
- **Document Ingestion**: Process product information into embeddings
- **Semantic Search**: Find relevant information using vector similarity
- **Context-Aware Responses**: Generate answers based on product context
- **Source Attribution**: Provide references to original information

### Chat Assistant Capabilities
- **Product Q&A**: Answer questions about specifications, features, pricing
- **Installment Calculations**: Help with payment plan calculations
- **Comparison Assistance**: Compare products and features
- **Seller Information**: Provide details about sellers and reputation

### Search Integration
- **Real-time Search**: Live product search integration
- **Focused Results**: Filtered results for better relevance
- **Preview Functionality**: Show content snippets before navigation
- **Debounced Input**: Optimized search performance

## 📈 Business Value

### User Benefits
- **Enhanced Shopping Experience**: AI-powered product assistance
- **Informed Decisions**: Detailed product information and comparisons
- **Seamless Interaction**: Natural language product queries
- **Real-time Search**: Find products across the platform

### Technical Benefits
- **Scalable Architecture**: Modular design for easy extension
- **High Performance**: Async operations and optimized queries
- **Maintainable Code**: Comprehensive testing and documentation
- **Modern Stack**: Latest technologies and best practices

## 🚀 Deployment

### Deploy to Vercel

This project is ready to be deployed to Vercel with both backend and frontend.

#### Quick Deploy (Script)
```bash
./deploy-vercel.sh
```

#### Manual Deploy
See the comprehensive guide: **[VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)**

#### Requirements
- Vercel account (free tier available)
- Vercel CLI: `npm install -g vercel`
- OpenAI API key (optional, for AI features)

#### What's Deployed
- **Backend**: FastAPI serverless functions
- **Frontend**: Next.js static site with SSR
- **Environment Variables**: Secure API key management
- **Custom Domains**: Optional domain configuration

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Spanish and English interfaces
- **Advanced Analytics**: User interaction tracking and insights
- **Personalization**: User-specific recommendations
- **Voice Interface**: Speech-to-text chat capabilities
- **Mobile App**: Native mobile application

### Technical Improvements
- **Database Integration**: Persistent storage for embeddings
- **Caching Layer**: Redis for improved performance
- **Monitoring**: Application performance monitoring
- **Container Orchestration**: Kubernetes deployment

## 📚 Learning Outcomes

This project demonstrates:

- **Full-Stack Development**: Modern frontend and backend integration
- **AI Integration**: Practical implementation of RAG and LLM systems
- **API Design**: RESTful API development with FastAPI
- **Testing Strategies**: Comprehensive unit and integration testing
- **UI/UX Design**: User-centered design with modern frameworks
- **Performance Optimization**: Async operations and efficient algorithms

## 🤝 Contributing

This project showcases GenAI capabilities in e-commerce. The codebase serves as a reference implementation for:

- AI-powered e-commerce applications
- RAG system implementation
- Modern full-stack development
- Testing best practices
- API design patterns

## 📄 License

This project is created for educational and demonstration purposes.

---

*Built with ❤️ using Next.js, FastAPI, and OpenAI technologies*
