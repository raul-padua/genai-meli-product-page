#!/bin/bash

# Vercel Deployment Script for GenAI Product Assistant
# This script helps deploy both backend and frontend to Vercel

set -e

echo "🚀 GenAI Product Assistant - Vercel Deployment Script"
echo "======================================================"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is ready"
echo ""

# Deploy Backend
echo "📦 Step 1: Deploying Backend (FastAPI)"
echo "---------------------------------------"
cd backend
echo "Current directory: $(pwd)"
echo ""

read -p "Deploy backend to Vercel? (y/n): " deploy_backend

if [ "$deploy_backend" = "y" ]; then
    echo "Deploying backend..."
    vercel --prod
    echo ""
    echo "✅ Backend deployed!"
    echo ""
    read -p "Enter your backend URL (e.g., https://genai-product-backend.vercel.app): " BACKEND_URL
    echo ""
    
    # Ask about environment variables
    read -p "Do you want to add OPENAI_API_KEY environment variable? (y/n): " add_openai
    if [ "$add_openai" = "y" ]; then
        echo "Adding OPENAI_API_KEY..."
        vercel env add OPENAI_API_KEY
        echo "✅ Environment variable added. Redeploying..."
        vercel --prod
    fi
else
    read -p "Enter your existing backend URL: " BACKEND_URL
fi

cd ..
echo ""

# Deploy Frontend
echo "📦 Step 2: Deploying Frontend (Next.js)"
echo "----------------------------------------"
cd frontend
echo "Current directory: $(pwd)"
echo ""

read -p "Deploy frontend to Vercel? (y/n): " deploy_frontend

if [ "$deploy_frontend" = "y" ]; then
    echo "Deploying frontend..."
    vercel --prod
    echo ""
    echo "✅ Frontend deployed!"
    echo ""
    
    # Set backend URL
    echo "Setting NEXT_PUBLIC_API_URL environment variable..."
    echo "Value: $BACKEND_URL"
    vercel env add NEXT_PUBLIC_API_URL production <<EOF
$BACKEND_URL
EOF
    
    echo "✅ Environment variable set. Redeploying..."
    vercel --prod
fi

cd ..
echo ""
echo "================================================"
echo "🎉 Deployment Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Test your backend at: $BACKEND_URL/docs"
echo "2. Test your frontend at the URL provided above"
echo "3. If you encounter CORS issues, check VERCEL_DEPLOYMENT.md"
echo ""
echo "For detailed instructions, see: VERCEL_DEPLOYMENT.md"
echo ""

