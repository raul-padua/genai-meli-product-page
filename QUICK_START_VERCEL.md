# Quick Start - Deploy to Vercel

Follow these simple steps to deploy your GenAI Product Assistant to Vercel.

## Option 1: Using the Deployment Script (Recommended)

```bash
cd genai-evaluation
./deploy-vercel.sh
```

The script will guide you through deploying both backend and frontend.

## Option 2: Using Vercel CLI Manually

### Deploy Backend
```bash
cd genai-evaluation/backend
vercel login
vercel --prod
# Note the backend URL (e.g., https://genai-product-backend.vercel.app)
```

### Deploy Frontend
```bash
cd ../frontend
vercel --prod
```

### Set Frontend Environment Variable
```bash
# Replace with your actual backend URL
vercel env add NEXT_PUBLIC_API_URL production
# When prompted, enter: https://genai-product-backend.vercel.app
vercel --prod  # Redeploy with env var
```

## Option 3: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository

### Backend Setup
- **Root Directory**: `genai-evaluation/backend`
- **Framework**: Other
- **Build Command**: (leave empty)
- Deploy!

### Frontend Setup
- **Root Directory**: `genai-evaluation/frontend`
- **Framework**: Next.js
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: (your backend URL)
- Deploy!

## Verify Deployment

### Backend
Visit: `https://your-backend.vercel.app/docs`

Should show FastAPI Swagger documentation.

### Frontend
Visit: `https://your-frontend.vercel.app`

Should show the e-commerce product page.

## Common Issues

### CORS Error
**Solution**: Make sure your frontend URL is added to backend CORS settings in `main.py`

### Frontend Can't Connect
**Solution**: Check `NEXT_PUBLIC_API_URL` environment variable is set correctly

### Chat Not Working
**Solution**: Users can provide their own OpenAI API key in the chat interface, or set `OPENAI_API_KEY` in backend environment variables

## Need Help?

See the detailed guide: [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)

---

**That's it!** Your project should now be live on Vercel. 🎉

