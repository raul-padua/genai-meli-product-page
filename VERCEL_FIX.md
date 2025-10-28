# Fix: Disable Vercel Deployment Protection

## Problem
The deployment is protected with Vercel authentication, preventing the frontend from accessing the API.

## Solution: Disable Deployment Protection

### Via Vercel Dashboard:

1. **Go to your project:**
   https://vercel.com/rauls-projects-2f2cc179/genai-evaluation

2. **Navigate to Settings:**
   - Click on "Settings" tab
   
3. **Go to Deployment Protection:**
   - In the left sidebar, find "Deployment Protection"
   
4. **Disable Protection:**
   - Turn OFF "Vercel Authentication"
   - Or select "Standard Protection" > "No Protection"
   
5. **Save Changes**

### Alternative: Make Production Public

If you want to keep protection on preview deployments but make production public:

1. Go to Settings → Deployment Protection
2. Under "Production Deployment Protection", select **"No Protection"**
3. Keep preview protection if desired
4. Save

### After Changing Settings:

The existing deployment will become accessible without authentication.

Test: `curl https://genai-evaluation-poxrpg4pf-rauls-projects-2f2cc179.vercel.app/api/item`

Should return JSON instead of authentication page.

