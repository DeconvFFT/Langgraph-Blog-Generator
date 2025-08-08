# Hugging Face Spaces Deployment Guide

## Files for Deployment

The following files are ready for Hugging Face Spaces deployment:

- `app.py` - Main Gradio application (copied from hf_spaces_app_native.py)
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Deployment Steps

### 1. Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/new-space)
2. Choose **Gradio** as the framework
3. Set your Space name (e.g., "blog-portfolio-manager")
4. Choose visibility (Public/Private)

### 2. Upload Files

Upload these files to your new Space:
- `app.py`
- `requirements.txt` 
- `README.md`

### 3. Configure Environment Variables

In your Space settings, add this environment variable:
- **Name**: `API_BASE_URL`
- **Value**: `https://your-api-domain.railway.app` (replace with your actual Railway API URL)

### 4. API URL Configuration

**IMPORTANT**: Update the API_BASE_URL in `app.py` line 12:

```python
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-actual-railway-domain.railway.app")
```

Replace `https://your-actual-railway-domain.railway.app` with your actual Railway deployment URL.

### 5. Deploy

Once files are uploaded and environment variables are set, your Space will automatically build and deploy.

## Expected Behavior

- ✅ Beautiful gradient header with floating animations
- ✅ Blog generation with topic validation
- ✅ Auto-loading of first blog in viewer
- ✅ Category-based filtering
- ✅ Edit/Delete functionality with gray edit button and red delete button
- ✅ Popup notifications for success/error messages
- ✅ Mobile-responsive design
- ✅ Native Gradio components only (no custom JavaScript)

## Troubleshooting

If the app doesn't work:
1. Check that `API_BASE_URL` environment variable is set correctly
2. Verify your Railway API is running and accessible
3. Check the Space logs for any errors
4. Ensure all required dependencies are in `requirements.txt`

## Space Settings

- Framework: **Gradio**
- Python Version: **3.11** (default)
- Hardware: **CPU Basic** (free tier)

Your app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
