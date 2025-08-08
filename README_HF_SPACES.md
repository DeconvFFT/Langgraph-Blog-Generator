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

Create the following files in your Space:

### `app.py` (Main Gradio App)
Use the `hf_spaces_app.py` file from this repository as your `app.py`.

**Key Features:**
- Portfolio-style blog cards
- Auto-categorization system
- Category filtering
- Full CRUD operations
- Modern UI with gradients

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

1. **Upload Files**: Upload `hf_spaces_app.py` as `app.py` and `requirements_hf.txt` as `requirements.txt`
2. **Set Secrets**: Add your API endpoint as a secret
3. **Wait for Build**: Hugging Face will automatically build and deploy your app

## 🎯 **UI Features**

### **Blog Cards**
Each blog displays as a beautiful card with:
- **Category Badge**: Color-coded category indicator
- **Blog Image**: Gradient placeholder with emoji
- **Title**: Large, bold blog title
- **Tags**: Topic and language indicators
- **Preview**: First 150 characters of content
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

## 🚀 **Usage**

### **Generate a Blog**
1. Enter topic: "The Future of Artificial Intelligence"
2. Select language: "English"
3. Click "Generate & Save Blog"
4. Blog appears as a card with auto-categorization

### **Filter by Category**
1. Select "Artificial Intelligence" from dropdown
2. Only AI-related blogs are shown
3. Switch to "All" to see everything

### **View Full Blog**
1. Click "👁️ View" button on any card
2. Modal opens with full blog content
3. Click "Close" to return

### **Edit Blog**
1. Click "✏️ Edit" button
2. Modal opens with editable fields
3. Modify title, content, or category
4. Click "Save Changes"

### **Delete Blog**
1. Click "🗑️ Delete" button
2. Confirmation dialog appears
3. Confirm to remove blog

## 🌈 **Category Colors**

Each category has its own color scheme:
- **Technology**: Blue (#3B82F6)
- **Artificial Intelligence**: Purple (#8B5CF6)
- **Machine Learning**: Cyan (#06B6D4)
- **Data Science**: Green (#10B981)
- **Software Development**: Orange (#F59E0B)
- **Business**: Red (#EF4444)
- And more...

## 🔧 **Configuration**

### **API Endpoint**
Make sure your `API_BASE_URL` secret points to your Railway API:
```
https://your-app-name.railway.app
```

### **Customization**
You can customize:
- **Categories**: Modify `BLOG_CATEGORIES` list
- **Colors**: Update `category_colors` dictionary
- **Styling**: Edit the `custom_css` section
- **Languages**: Add more languages to `SUPPORTED_LANGUAGES`

## 📱 **Responsive Design**

The UI is fully responsive and works on:
- **Desktop**: Full portfolio layout
- **Tablet**: Optimized card grid
- **Mobile**: Stacked cards with touch-friendly buttons

## 🎨 **Design Features**

- **Gradient Backgrounds**: Beautiful color transitions
- **Hover Effects**: Cards lift on hover
- **Modal Windows**: For viewing and editing
- **Smooth Animations**: CSS transitions
- **Professional Typography**: Clean, readable fonts

## 🚀 **Deployment Checklist**

- [ ] Created Hugging Face Space
- [ ] Uploaded `hf_spaces_app.py` as `app.py`
- [ ] Uploaded `requirements_hf.txt` as `requirements.txt`
- [ ] Set `API_BASE_URL` secret
- [ ] Verified Railway API is running
- [ ] Tested blog generation
- [ ] Tested category filtering
- [ ] Tested CRUD operations

## 🔗 **Links**

- **Your Space**: `https://huggingface.co/spaces/YOUR_USERNAME/blog-generator`
- **Railway API**: `https://your-app-name.railway.app`
- **Documentation**: This README

## 🎉 **Success!**

Your portfolio-style blog manager is now live on Hugging Face Spaces with:
- ✅ Beautiful card-based UI
- ✅ Auto-categorization
- ✅ Category filtering
- ✅ Full CRUD operations
- ✅ Responsive design
- ✅ Professional styling

**Visit your Space URL to start using the new UI!** 🚀
