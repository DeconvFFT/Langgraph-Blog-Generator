# Deploying to Hugging Face Spaces

This guide will help you deploy the Blog Generator with the new **Portfolio-Style UI** to Hugging Face Spaces.

## 🎨 **New Features**

The updated UI includes:
- **📋 Card-Based Layout**: Beautiful blog cards with gradients and hover effects
- **🏷️ Auto-Categorization**: Blogs are automatically categorized based on content
- **🔍 Category Filtering**: Filter blogs by 15 different categories
- **⚡ CRUD Operations**: Create, Read, Update, Delete blogs
- **📱 Responsive Design**: Works perfectly on all devices
- **🎯 Portfolio-Style**: Professional layout like modern portfolio websites
- **💾 State Persistence**: Blogs persist across refreshes and deployments

## Prerequisites

1. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
2. **Groq API Key**: Get your API key from [console.groq.com](https://console.groq.com)
3. **Git**: Make sure you have Git installed

## Step 1: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose settings:
   - **Owner**: Your username
   - **Space name**: `blog-generator` (or your preferred name)
   - **License**: MIT
   - **SDK**: **Gradio** (important!)
   - **Python version**: 3.10
   - **Hardware**: CPU (free) or GPU if needed

## Step 2: Configure the Space

The repository now has the correct file structure:

### `app.py` (Main Gradio App)
This is the Gradio frontend with state management and portfolio-style UI.

**Key Features:**
- Portfolio-style blog cards
- Auto-categorization system
- Category filtering
- Full CRUD operations
- Modern UI with gradients
- **State persistence** with pickle-based storage
- Mobile-friendly responsive design

### `app_fastapi.py` (Backend API)
This is the FastAPI backend for blog generation (deploy separately to Railway/Render/etc.)

### `requirements.txt`
```
gradio>=4.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## Step 3: Set Up Environment Variables

In your Hugging Face Space settings, add these secrets:

1. Go to your Space → Settings → Repository secrets
2. Add the following secrets:

```
API_BASE_URL=https://your-railway-api-endpoint.com
```

**Note**: Replace `your-railway-api-endpoint.com` with your actual Railway API endpoint.

## Step 4: Deploy

1. **Push to Repository**: The `app.py` file is now correctly set up for Gradio deployment
2. **Set Secrets**: Add your API endpoint as a secret
3. **Wait for Build**: Hugging Face will automatically build and deploy your app

## 🎯 **UI Features**

### **Blog Cards**
Each blog displays as a beautiful card with:
- **Category Badge**: Color-coded category indicator
- **Blog Image**: Gradient placeholder with emoji
- **Title**: Large, bold blog title
- **Tags**: Topic and language indicators
- **Preview**: First 200 characters of content
- **Actions**: View, Edit, Delete buttons

### **Category System**
- **15 Categories**: Technology, AI, ML, Data Science, Business, etc.
- **Auto-Categorization**: Based on topic and content keywords
- **Color-Coded**: Each category has its own color scheme
- **Filtering**: Show only blogs in selected category

### **CRUD Operations**
- **Create**: Generate new blogs with AI
- **Read**: View full blog content in modal
- **Update**: Edit blog title, content, and category
- **Delete**: Remove blogs with confirmation

### **State Management**
- **💾 Persistent Storage**: Blogs saved to `blog_state.pkl`
- **🔄 Auto-Save**: Every operation automatically saves state
- **📊 Status Display**: Shows total blogs and last save time
- **🛡️ Backup System**: Automatic backup before each save

## 🚀 **Usage**

### **Generate a Blog**
1. Enter topic: "The Future of Artificial Intelligence"
2. Select language: "English"
