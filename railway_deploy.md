# Deploy FastAPI Backend to Railway

## Step 1: Prepare for Railway Deployment

1. **Create a new Railway project** at [railway.app](https://railway.app)
2. **Connect your GitHub repository**
3. **Set the source directory** to your repository root

## Step 2: Configure Railway

### **Environment Variables**
Add these to your Railway project:
```
GROQ_API_KEY=your_groq_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here (optional)
```

### **Railway Configuration**
Railway will automatically detect and run your FastAPI app.

## Step 3: Deploy

1. **Push your code** to GitHub
2. **Railway will auto-deploy** your FastAPI backend
3. **Get your Railway URL** (e.g., `https://your-app-name.railway.app`)

## Step 4: Update Hugging Face Spaces

1. **Go to your Hugging Face Space**
2. **Settings → Repository secrets**
3. **Add/Update the secret**:
   ```
   API_BASE_URL=https://your-app-name.railway.app
   ```

## Step 5: Test

Your Gradio app should now connect to your Railway API successfully!
