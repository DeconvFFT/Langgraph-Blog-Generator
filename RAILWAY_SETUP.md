# Railway Setup Guide

## Quick Fix for 502 Error

### 1. Set Environment Variables in Railway
Go to your Railway project → Variables → Add:
```
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### 2. Check Railway Logs
Go to Railway project → Deployments → Click on latest deployment → View logs

### 3. Test Your API
Once deployed, test these endpoints:
- **Health**: `https://your-app.railway.app/health`
- **Test**: `https://your-app.railway.app/test`
- **Docs**: `https://your-app.railway.app/docs`

### 4. Update Hugging Face Spaces
In your Hugging Face Space → Settings → Repository secrets:
```
API_BASE_URL=https://your-app.railway.app
```

## Common Issues

### ❌ 502 Error
- **Missing GROQ_API_KEY**: Set in Railway environment variables
- **Build failed**: Check Railway build logs
- **Service paused**: Resume in Railway dashboard

### ✅ Success Indicators
- Health check returns: `{"status": "healthy", "groq_key_set": true}`
- Test endpoint shows: `{"message": "API is working!", "groq_key_set": true}`
- No errors in Railway logs
