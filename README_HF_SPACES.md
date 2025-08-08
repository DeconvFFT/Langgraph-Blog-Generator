# Deploying to Hugging Face Spaces

This guide will help you deploy the Blog Generator to Hugging Face Spaces.

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
```python
import gradio as gr
import requests
import os
from typing import Dict, Any

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://your-api-endpoint.com')
API_ENDPOINT = f"{API_BASE_URL}/blogs"

# Supported languages
SUPPORTED_LANGUAGES = ["English", "Spanish", "Hindi"]

def generate_blog(topic: str, language: str) -> Dict[str, Any]:
    """Generate a blog using the API"""
    if not topic.strip():
        return {
            "success": False,
            "error": "Topic cannot be empty",
            "message": "Please provide a topic for the blog"
        }
    
    try:
        payload = {
            "topic": topic.strip(),
            "language": language
        }
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300
        )
        
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {
            "success": False,
            "error": "Request failed",
            "message": f"Error: {str(e)}"
        }

def create_blog_card(blog_data: Dict[str, Any]) -> str:
    """Create HTML card for a blog"""
    title = blog_data.get('title', 'Untitled')
    content = blog_data.get('content', 'No content available')
    topic = blog_data.get('topic', 'Unknown topic')
    language = blog_data.get('language', 'Unknown language')
    
    # Truncate content for preview
    preview = content[:200] + "..." if len(content) > 200 else content
    
    return f"""
    <div style="
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #007bff;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
            <h3 style="margin: 0; color: #333; font-size: 1.2em;">{title}</h3>
            <span style="
                background: #007bff;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
            ">{language}</span>
        </div>
        <p style="color: #666; margin: 5px 0; font-size: 0.9em;">
            <strong>Topic:</strong> {topic}
        </p>
        <div style="
            color: #555;
            line-height: 1.6;
            white-space: pre-wrap;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            {content}
        </div>
    </div>
    """

def blog_generation_interface(topic: str, language: str) -> tuple:
    """Main interface function for blog generation"""
    if not topic.strip():
        return "", "⚠️ Please enter a topic for the blog."
    
    result = generate_blog(topic, language)
    
    if not result.get('success', False):
        error_message = f"❌ {result.get('message', 'An error occurred')}"
        return "", error_message
    
    data = result.get('data', {})
    blog_content = data.get('blog', {})
    
    if not blog_content:
        return "", "❌ No blog content was generated."
    
    blog_card = create_blog_card(blog_content)
    success_message = f"✅ Blog generated successfully in {language}!"
    
    return blog_card, success_message

# Create Gradio interface
with gr.Blocks(title="AI Blog Generator") as demo:
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #333; font-size: 2.5em; margin-bottom: 10px;">
            🤖 AI Blog Generator
        </h1>
        <p style="color: #666; font-size: 1.1em; margin: 0;">
            Generate engaging blog content in multiple languages with AI
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label="📝 Blog Topic",
                placeholder="Enter your blog topic here...",
                lines=2
            )
            
            language_dropdown = gr.Dropdown(
                choices=SUPPORTED_LANGUAGES,
                value="English",
                label="🌍 Language"
            )
            
            generate_btn = gr.Button(
                "🚀 Generate Blog",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: #f8f9fa; padding: 20px; border-radius: 12px;">
                <h3 style="margin-top: 0;">💡 Tips</h3>
                <ul style="color: #666;">
                    <li>Be specific with your topic</li>
                    <li>Use clear, descriptive language</li>
                    <li>Consider your target audience</li>
                </ul>
            </div>
            """)
    
    with gr.Row():
        status_output = gr.Textbox(
            label="📊 Status",
            interactive=False,
            lines=1
        )
    
    with gr.Row():
        output_html = gr.HTML(
            label="📄 Generated Blog",
            value=""
        )
    
    generate_btn.click(
        fn=blog_generation_interface,
        inputs=[topic_input, language_dropdown],
        outputs=[output_html, status_output]
    )

demo.launch()
```

### `requirements.txt`
```
gradio>=4.0.0
requests>=2.31.0
```

### `.gitignore`
```
__pycache__/
*.pyc
.env
.DS_Store
```

## Step 3: Set Environment Variables

1. Go to your Space settings
2. Click on "Repository secrets"
3. Add the following secrets:
   - `GROQ_API_KEY`: Your Groq API key
   - `API_BASE_URL`: Your API endpoint URL

## Step 4: Deploy the API Separately

Since Hugging Face Spaces is for the frontend, you need to deploy the API separately:

### Option A: Deploy API to Hugging Face Spaces (Separate Space)
1. Create another Space for the API
2. Use **FastAPI** SDK instead of Gradio
3. Upload the API code (`app.py`, `src/` folder, etc.)

### Option B: Deploy API to Other Platforms
- **Railway**: Easy deployment with environment variables
- **Render**: Free tier available
- **Heroku**: Paid service
- **DigitalOcean App Platform**: Good for production

## Step 5: Update API URL

Once your API is deployed, update the `API_BASE_URL` in your Space's environment variables to point to your deployed API.

## Step 6: Test Your Deployment

1. Go to your Space URL
2. Enter a topic and select a language
3. Click "Generate Blog"
4. Verify that the blog is generated successfully

## Troubleshooting

### Common Issues:

1. **API Connection Failed**
   - Check if your API is running
   - Verify the API_BASE_URL is correct
   - Ensure CORS is configured on your API

2. **Environment Variables Not Working**
   - Make sure secrets are set in Space settings
   - Check that variable names match exactly

3. **Timeout Errors**
   - Increase timeout in the requests
   - Consider using async requests for better performance

### Getting Help:

- Check Space logs in the "Logs" tab
- Review API logs from your deployment platform
- Test API endpoints directly using curl or Postman

## Advanced Configuration

### Custom Domain (Optional)
1. Go to Space settings
2. Click "Custom domain"
3. Add your domain and configure DNS

### Monitoring
- Use Hugging Face's built-in monitoring
- Set up external monitoring for your API
- Configure alerts for downtime

## Security Considerations

1. **API Keys**: Never commit API keys to Git
2. **Rate Limiting**: Implement rate limiting on your API
3. **Input Validation**: Validate all user inputs
4. **HTTPS**: Always use HTTPS in production

## Cost Optimization

1. **Free Tier**: Hugging Face Spaces offers free hosting
2. **API Costs**: Monitor your Groq API usage
3. **Scaling**: Start with free tiers and scale as needed

Your Blog Generator is now ready for deployment to Hugging Face Spaces! 🚀
