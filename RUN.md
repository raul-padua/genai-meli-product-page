# 🚀 How to Run the GenAI Evaluation Project

This guide provides step-by-step instructions to set up and run the MercadoLibre GenAI evaluation project on your local machine.

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Optional (for enhanced AI features):
- **OpenAI API Key** - [Get yours here](https://platform.openai.com/api-keys)
- **Tavily API Key** - [Sign up here](https://tavily.com/)

## 🛠️ Setup Instructions

### 1. Clone and Navigate to Project

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd technical_challenge_DS_GenAI/genai-evaluation
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from genai-evaluation root)
cd frontend

# Install Node.js dependencies
npm install
```

## 🏃‍♂️ Running the Application

### Option 1: Manual Startup (Recommended for Development)

#### Terminal 1 - Start Backend
```bash
cd genai-evaluation/backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### Terminal 2 - Start Frontend
```bash
cd genai-evaluation/frontend
npm run dev
```

### Option 2: Automated Startup Script

Create a startup script for easier execution:

```bash
# Create startup script (macOS/Linux)
cat > start_app.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting MercadoLibre GenAI Evaluation Project..."

# Start backend in background
echo "📡 Starting backend server..."
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers are starting..."
echo "📡 Backend: http://127.0.0.1:8000"
echo "🎨 Frontend: http://localhost:3000"
echo "📚 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x start_app.sh
./start_app.sh
```

## 🌐 Accessing the Application

Once both servers are running, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory for API keys:

```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### API Keys Integration

The application works without API keys but provides enhanced functionality with them:

#### OpenAI API Key
- **Without Key**: Uses keyword matching for chat responses
- **With Key**: Uses GPT-4 for intelligent, context-aware responses
- **How to Add**: Enter your key in the chat widget's input field

#### Tavily API Key
- **Current Setup**: Uses provided key for MercadoLibre search
- **Custom Key**: Update `main.py` line 248 with your key

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_api.py -v
python -m pytest tests/test_rag.py -v

# Run with coverage
python -m pytest tests/ --cov=main --cov=rag --cov-report=html

# Using the custom test runner
python run_tests.py --verbose --coverage
```

### Test Results
- **Total Tests**: 36
- **Passing**: 33 (91.7%)
- **Coverage**: API endpoints, RAG functionality, data validation

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or use specific commands
pkill -f "npm run dev"
pkill -f "uvicorn main:app"
```

#### Python Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf backend/.venv
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Node.js Dependencies Issues
```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### CORS Issues
- Ensure backend is running on `127.0.0.1:8000`
- Check that frontend is making requests to correct backend URL
- Verify CORS middleware is properly configured in `main.py`

### Backend Not Starting
```bash
# Check Python version
python --version  # Should be 3.9+

# Verify virtual environment
which python  # Should point to .venv/bin/python

# Check dependencies
pip list | grep -E "(fastapi|uvicorn|pydantic)"
```

### Frontend Not Loading
```bash
# Check Node.js version
node --version  # Should be 18+

# Verify dependencies
cd frontend
npm list --depth=0

# Check for build errors
npm run build
```

## 📊 Performance Monitoring

### Backend Performance
```bash
# Monitor backend logs
tail -f backend/logs/app.log  # If logging is configured

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://127.0.0.1:8000/item
```

### Frontend Performance
- Open browser DevTools (F12)
- Check Network tab for API response times
- Monitor Console for any JavaScript errors

## 🚀 Production Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment
```bash
# Build for production
cd frontend
npm run build

# Serve static files
npm run start
```

## 📱 Mobile Testing

### Responsive Design Testing
- Use browser DevTools device emulation
- Test on actual mobile devices
- Verify touch interactions and carousel functionality

### Performance on Mobile
- Check image loading times
- Verify chat widget accessibility
- Test search functionality on mobile keyboards

## 🔐 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly

### CORS Configuration
- Restrict CORS origins in production
- Use HTTPS in production environments
- Validate all incoming requests

## 📈 Monitoring and Logging

### Application Logs
```bash
# Backend logs (if configured)
tail -f backend/logs/*.log

# Frontend logs
# Check browser console and Network tab
```

### Health Checks
```bash
# Backend health
curl http://127.0.0.1:8000/item

# Frontend health
curl http://localhost:3000
```

## 🆘 Getting Help

### Debug Mode
```bash
# Backend with debug logging
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000 --log-level debug

# Frontend with verbose output
cd frontend
npm run dev -- --verbose
```

### Common Commands Reference

```bash
# Quick restart (both services)
pkill -f "uvicorn\|npm" && sleep 2 && ./start_app.sh

# Check running processes
ps aux | grep -E "(uvicorn|npm)"

# Check port usage
netstat -tulpn | grep -E "(3000|8000)"
```

## ✅ Verification Checklist

Before considering the setup complete, verify:

- [ ] Backend starts without errors on port 8000
- [ ] Frontend loads on port 3000
- [ ] API documentation is accessible at `/docs`
- [ ] Product page displays correctly
- [ ] Chat widget opens and accepts input
- [ ] Search functionality works
- [ ] All tests pass (optional)
- [ ] No console errors in browser
- [ ] Images load correctly
- [ ] Responsive design works on mobile

---

**🎉 You're all set! The MercadoLibre GenAI Evaluation Project should now be running successfully.**

For questions or issues, refer to the troubleshooting section above or check the comprehensive README.md for detailed project information.
