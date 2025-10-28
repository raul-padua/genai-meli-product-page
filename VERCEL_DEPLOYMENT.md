# Deploying GenAI Product Assistant to Vercel

This guide will walk you through deploying both the backend (FastAPI) and frontend (Next.js) to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- The Vercel CLI installed: `npm install -g vercel`
- Your GitHub repository (e.g., https://github.com/yourusername/your-repo-name)
- OpenAI API key (optional, for AI features)
- Tavily API key (already in backend code, but you may want to secure it)

## Part 1: Deploy the Backend (FastAPI)

### Step 1: Navigate to Backend Directory
```bash
cd genai-evaluation/backend
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy Backend
```bash
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Select your account
- **Link to existing project?** No
- **What's your project's name?** `genai-product-backend` (or your preferred name)
- **In which directory is your code located?** `.` (current directory)
- **Want to override settings?** No

### Step 4: Set Environment Variables (Optional)

If you want to use OpenAI features with a server-side API key:

```bash
vercel env add OPENAI_API_KEY
```

Then enter your OpenAI API key when prompted. Select all environments (Production, Preview, Development).

### Step 5: Note Your Backend URL

After deployment, Vercel will provide a URL like:
```
https://genai-product-backend.vercel.app
```

**Save this URL** - you'll need it for the frontend configuration.

### Vercel Backend Configuration

The backend includes a `vercel.json` file that configures:
- Python runtime for FastAPI
- Route handling for all endpoints
- CORS settings for Vercel domains

## Part 2: Deploy the Frontend (Next.js)

### Step 1: Navigate to Frontend Directory
```bash
cd ../frontend  # Or: cd genai-evaluation/frontend
```

### Step 2: Deploy Frontend
```bash
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Select your account
- **Link to existing project?** No
- **What's your project's name?** `genai-product-frontend` (or your preferred name)
- **In which directory is your code located?** `.` (current directory)
- **Want to override settings?** No

### Step 3: Configure Environment Variable

Set the backend API URL using your backend URL from Step 5 above:

```bash
vercel env add NEXT_PUBLIC_API_URL
```

When prompted, enter your backend URL:
```
https://genai-product-backend.vercel.app
```

Select all environments (Production, Preview, Development).

### Step 4: Redeploy Frontend

After adding the environment variable, redeploy to apply the changes:

```bash
vercel --prod
```

## Part 3: Alternative - Deploy via Vercel Dashboard

### Backend Deployment via Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset:** Other
   - **Root Directory:** `genai-evaluation/backend`
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
5. Add Environment Variables (optional):
   - `OPENAI_API_KEY`: Your OpenAI API key
6. Click "Deploy"

### Frontend Deployment via Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository (or create a new project)
4. Configure the project:
   - **Framework Preset:** Next.js
   - **Root Directory:** `genai-evaluation/frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
5. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL from above
6. Click "Deploy"

## Part 4: Update Backend CORS (If Needed)

If your frontend URL is different from what's configured, update the backend CORS settings:

Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-frontend-name.vercel.app",  # Add your actual frontend URL
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push changes, then Vercel will automatically redeploy.

## Part 5: Verify Deployment

### Test Backend
Visit your backend URL + `/docs`:
```
https://genai-product-backend.vercel.app/docs
```

You should see the FastAPI Swagger documentation.

Test endpoints:
- `/item` - Should return product details
- `/reviews` - Should return reviews data

### Test Frontend
Visit your frontend URL:
```
https://genai-product-frontend.vercel.app
```

You should see the e-commerce product page.

Test features:
- Product images should load
- Search functionality should work
- Chat assistant should respond (may need OpenAI key)

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
1. Check that the backend URL is correctly set in frontend environment variables
2. Verify that the frontend URL is in the backend's CORS allowed origins
3. Redeploy both services after making changes

### Backend Not Responding
1. Check Vercel function logs in the dashboard
2. Ensure `vercel.json` is in the backend directory
3. Verify Python dependencies in `requirements.txt`

### Frontend Can't Connect to Backend
1. Check the environment variable: `vercel env ls`
2. Ensure the URL doesn't have a trailing slash
3. Check browser network tab for the actual request URL

### OpenAI Features Not Working
1. Users can provide their own OpenAI API key in the chat interface
2. Or set the `OPENAI_API_KEY` environment variable in the backend
3. The app has a fallback keyword matching system when no API key is provided

## Continuous Deployment

Both projects are now set up for continuous deployment:

1. **Push to GitHub**: Any push to your main branch will trigger automatic deployments
2. **Pull Requests**: Preview deployments are created for each PR
3. **Environment Variables**: Managed in the Vercel dashboard or via CLI

## Managing Deployments

### View Deployments
```bash
vercel ls
```

### View Logs
```bash
vercel logs <deployment-url>
```

### Rollback
Go to Vercel dashboard → Select project → Deployments → Click on a previous deployment → "Promote to Production"

## Security Recommendations

1. **API Keys**: Never commit API keys to Git. Use Vercel environment variables.
2. **Tavily API Key**: Currently hardcoded in `main.py` - consider moving to environment variable:
   ```python
   import os
   tavily_api_key = os.getenv("TAVILY_API_KEY", "tvly-dev-...")
   ```
3. **CORS**: Restrict allowed origins to only your domains in production

## Custom Domains (Optional)

To add a custom domain:

1. Go to Vercel dashboard → Project → Settings → Domains
2. Add your domain
3. Configure DNS records as instructed by Vercel
4. Update CORS settings if needed

## Cost Considerations

- **Vercel**: Free tier includes 100GB bandwidth and 6000 build minutes/month
- **OpenAI API**: Users provide their own keys or you set up billing
- **Tavily API**: Check their pricing at https://tavily.com/pricing

## Support

For issues:
- Vercel Documentation: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/docs/frameworks/fastapi
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs

---

**Success!** 🎉 Your GenAI Product Assistant is now deployed to Vercel with both frontend and backend running in the cloud.

