#!/bin/bash

# 🚀 GenAI Product Assistant - Quick Start Script
# This script automates the setup and startup of the entire application

set -e  # Exit on any error

echo "🚀 Starting GenAI Product Assistant Setup..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js v18+ from https://nodejs.org/"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "Python is not installed. Please install Python 3.9+ from https://www.python.org/"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Backend setup completed"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    print_success "Frontend setup completed"
    cd ..
}

# Kill existing processes
cleanup_processes() {
    print_status "Cleaning up existing processes..."
    
    # Kill processes on ports 3000 and 8000
    if lsof -ti:3000 > /dev/null 2>&1; then
        print_warning "Killing existing process on port 3000..."
        lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    fi
    
    if lsof -ti:8000 > /dev/null 2>&1; then
        print_warning "Killing existing process on port 8000..."
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    fi
    
    # Kill any existing uvicorn or npm processes
    pkill -f "uvicorn main:app" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    sleep 2
    print_success "Process cleanup completed"
}

# Start backend
start_backend() {
    print_status "Starting backend server..."
    
    cd backend
    source .venv/bin/activate
    
    # Start backend in background
    nohup uvicorn main:app --reload --host 127.0.0.1 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to start
    print_status "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
            print_success "Backend started successfully on http://127.0.0.1:8000"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Backend failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
    done
}

# Start frontend
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Start frontend in background
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait for frontend to start
    print_status "Waiting for frontend to start..."
    for i in {1..60}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend started successfully on http://localhost:3000"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Frontend failed to start within 60 seconds"
            exit 1
        fi
        sleep 1
    done
}

# Main execution
main() {
    echo "🎯 GenAI Product Assistant"
    echo "========================================"
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
        print_error "Please run this script from the genai-evaluation directory"
        exit 1
    fi
    
    # Run setup steps
    check_prerequisites
    cleanup_processes
    setup_backend
    setup_frontend
    
    # Start services
    start_backend
    start_frontend
    
    # Display success message
    echo ""
    echo "🎉 Application started successfully!"
    echo "=================================="
    echo ""
    echo "📡 Backend API:    http://127.0.0.1:8000"
    echo "📚 API Docs:       http://127.0.0.1:8000/docs"
    echo "🎨 Frontend:       http://localhost:3000"
    echo ""
    echo "📋 Available Features:"
    echo "   • Product detail page with MercadoLibre-inspired design"
    echo "   • AI-powered chat assistant (add your OpenAI API key in chat)"
    echo "   • Real-time search with Tavily integration"
    echo "   • Interactive product gallery and carousels"
    echo "   • Reviews and ratings display"
    echo ""
    echo "🛠️  Management Commands:"
    echo "   • View logs:     tail -f backend.log frontend.log"
    echo "   • Stop servers:  pkill -f 'uvicorn\\|npm'"
    echo "   • Restart:       ./start.sh"
    echo ""
    echo "📖 For detailed documentation, see:"
    echo "   • README.md - Complete project overview"
    echo "   • RUN.md - Detailed setup instructions"
    echo "   • PROJECT_STRUCTURE.md - File organization"
    echo ""
    echo "Press Ctrl+C to stop both servers"
    echo ""
    
    # Wait for interrupt
    trap 'echo ""; print_warning "Stopping servers..."; pkill -f "uvicorn\\|npm" 2>/dev/null || true; print_success "Servers stopped. Goodbye!"; exit 0' INT
    
    # Keep script running
    while true; do
        sleep 1
    done
}

# Run main function
main "$@"
