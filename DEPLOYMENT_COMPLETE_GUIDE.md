# Complete Deployment Guide for GenAI Product Assistant

## Current Issue
The Vercel deployment has authentication protection enabled on both the frontend and backend projects. Both need to be disabled for the app to work publicly.

## Solution: Two-Project Deployment

### Step 1: Deploy Backend
1. Go to Vercel dashboard: https://vercel.com/dashboard
2. Find the `backend` project
3. Go to Settings → Deployment Protection → **Disable Protection**
4. The backend should now be accessible at: `https://backend-qhbpubo4p-rauls-projects-2f2cc179.vercel.app`

### Step 2: Configure Frontend Environment Variable
1. Go to your `genai-evaluation` project settings in Vercel
2. Go to Settings → Environment Variables
3. Add a new variable:
   - **Key**: `BACKEND_URL`
   - **Value**: `https://backend-qhbpubo4p-rauls-projects-2f2cc179.vercel.app`
   - **Environment**: Production, Preview, Development (check all)
4. Click Save

### Step 3: Redeploy Frontend
```bash
cd /path/to/genai-evaluation
vercel --prod
```

## How It Works
- The frontend runs as a Next.js app
- The frontend has API routes at `/api/*` that proxy requests to the backend
- The backend runs as a separate FastAPI service
- Both need to have authentication protection disabled for public access

## Alternative: Local Development
If you want to test locally before deploying:
```bash
# Terminal 1 - Run backend
cd genai-evaluation/backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Run frontend (pointing to local backend)
cd genai-evaluation/frontend
export BACKEND_URL=http://localhost:8000
npm run dev
```

## Testing
After both are deployed and protection is disabled:
1. Test backend: `curl https://backend-qhbpubo4p-rauls-projects-2f2cc179.vercel.app/api/item`
2. Test frontend: Open `https://genai-evaluation-YOUR-URL.vercel.app` in browser

## Troubleshooting
- **Still getting "Authentication Required"**: Make sure BOTH projects have deployment protection disabled
- **Frontend shows "Loading..."**: Check that the `BACKEND_URL` environment variable is set correctly
- **500 errors**: Check the Vercel function logs for the backend project

