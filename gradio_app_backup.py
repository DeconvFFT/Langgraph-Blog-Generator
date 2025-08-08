import gradio as gr
import json
import requests
from typing import Dict, Any, Optional
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_ENDPOINT = f"{API_BASE_URL}/blogs"

# Supported languages
SUPPORTED_LANGUAGES = [
    "English",
    "Spanish", 
    "Hindi"
]

def generate_blog(topic: str, language: str) -> Dict[str, Any]:
    """
    Generate a blog using the API
    
    Args:
        topic (str): Blog topic
        language (str): Target language
        
    Returns:
        Dict[str, Any]: API response
    """
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
            timeout=300  # 5 minutes timeout
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection failed",
            "message": "Could not connect to the blog generation service. Please check if the server is running."
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout",
            "message": "Blog generation took too long. Please try again."
        }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": "HTTP Error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "message": f"An unexpected error occurred: {str(e)}"
        }

def create_blog_card(blog_data: Dict[str, Any], index: int) -> str:
    """
    Create HTML card for a blog
    
    Args:
        blog_data (Dict[str, Any]): Blog data
        index (int): Card index
        
    Returns:
        str: HTML card
    """
    title = blog_data.get('title', 'Untitled')
    content = blog_data.get('content', 'No content available')
    topic = blog_data.get('topic', 'Unknown topic')
    language = blog_data.get('language', 'Unknown language')
    
    # Truncate content for preview
    preview = content[:200] + "..." if len(content) > 200 else content
    
    # Create modal ID
    modal_id = f"modal-{index}"
    
    card_html = f"""
    <div class="blog-card" style="
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #007bff;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    " onclick="openModal('{modal_id}')">
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
        <p style="color: #555; line-height: 1.5; margin: 10px 0;">
            {preview}
        </p>
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        ">
            <span style="color: #888; font-size: 0.8em;">
                {len(content)} characters
            </span>
            <button style="
                background: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.9em;
            " onclick="event.stopPropagation(); openModal('{modal_id}')">
                Read Full Blog
            </button>
        </div>
    </div>
    
    <!-- Modal -->
    <div id="{modal_id}" class="modal" style="
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
    ">
        <div class="modal-content" style="
            background-color: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 12px;
            width: 80%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        ">
            <span class="close" onclick="closeModal('{modal_id}')" style="
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                position: absolute;
                right: 20px;
                top: 15px;
            ">&times;</span>
            
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h2 style="margin: 0; color: #333;">{title}</h2>
                    <span style="
                        background: #007bff;
                        color: white;
                        padding: 6px 12px;
                        border-radius: 16px;
                        font-size: 0.9em;
                    ">{language}</span>
                </div>
                <p style="color: #666; margin: 5px 0;">
                    <strong>Topic:</strong> {topic}
                </p>
            </div>
            
            <div style="
                line-height: 1.6;
                color: #333;
                white-space: pre-wrap;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            ">
                {content}
            </div>
            
            <div style="
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                text-align: center;
            ">
                <button onclick="closeModal('{modal_id}')" style="
                    background: #6c757d;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 1em;
                ">
                    Close
                </button>
            </div>
        </div>
    </div>
    """
    
    return card_html

def blog_generation_interface(topic: str, language: str) -> tuple:
    """
    Main interface function for blog generation
    
    Args:
        topic (str): Blog topic
        language (str): Target language
        
    Returns:
        tuple: (HTML output, status message)
    """
    if not topic.strip():
        return "", "⚠️ Please enter a topic for the blog."
    
    # Show loading message
    loading_html = """
    <div style="
        text-align: center;
        padding: 40px;
        color: #666;
    ">
        <div style="
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        "></div>
        <h3>Generating your blog...</h3>
        <p>This may take a few moments. Please wait.</p>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """
    
    # Generate blog
    result = generate_blog(topic, language)
    
    if not result.get('success', False):
        error_message = f"❌ {result.get('message', 'An error occurred')}"
        return "", error_message
    
    # Extract blog data
    data = result.get('data', {})
    blog_content = data.get('blog', {})
    
    if not blog_content:
        return "", "❌ No blog content was generated."
    
    # Create blog card
    blog_card = create_blog_card(blog_content, 0)
    
    success_message = f"✅ Blog generated successfully in {language}!"
    
    return blog_card, success_message

# Custom CSS for better styling
custom_css = """
<style>
.blog-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.modal-content {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.gradio-container {
    max-width: 1200px;
    margin: 0 auto;
}

.gradio-interface {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.gradio-main {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.gradio-input {
    border-radius: 10px;
    border: 2px solid #e1e5e9;
    transition: border-color 0.3s ease;
}

.gradio-input:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.gradio-button {
    background: linear-gradient(45deg, #007bff, #0056b3);
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    transition: transform 0.2s ease;
}

.gradio-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.gradio-output {
    border-radius: 10px;
    border: 2px solid #e1e5e9;
    background: white;
}
</style>
"""

# Create Gradio interface
with gr.Blocks(css=custom_css, title="AI Blog Generator") as demo:
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #007bff, #0056b3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            🤖 AI Blog Generator
        </h1>
        <p style="
            color: #666;
            font-size: 1.1em;
            margin: 0;
        ">
            Generate engaging blog content in multiple languages with AI
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label="📝 Blog Topic",
                placeholder="Enter your blog topic here... (e.g., 'The Future of Artificial Intelligence')",
                lines=2,
                max_lines=3
            )
            
            language_dropdown = gr.Dropdown(
                choices=SUPPORTED_LANGUAGES,
                value="English",
                label="🌍 Language",
                info="Select the language for your blog"
            )
            
            generate_btn = gr.Button(
                "🚀 Generate Blog",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                padding: 20px;
                border-radius: 12px;
                border-left: 4px solid #007bff;
            ">
                <h3 style="margin-top: 0; color: #333;">💡 Tips</h3>
                <ul style="color: #666; line-height: 1.6;">
                    <li>Be specific with your topic</li>
                    <li>Use clear, descriptive language</li>
                    <li>Consider your target audience</li>
                    <li>Blogs are generated in 30-60 seconds</li>
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
    
    # Event handlers
    generate_btn.click(
        fn=blog_generation_interface,
        inputs=[topic_input, language_dropdown],
        outputs=[output_html, status_output]
    )
    
    # Add JavaScript for modal functionality
    gr.HTML("""
    <script>
    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
        document.body.style.overflow = "hidden";
    }
    
    function closeModal(modalId) {
        document.getElementById(modalId).style.display = "none";
        document.body.style.overflow = "auto";
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
            document.body.style.overflow = "auto";
        }
    }
    </script>
    """)

if __name__ == "__main__":
    # Get port from environment or default to 7860
    port = int(os.getenv('PORT', 7860))
    host = os.getenv('HOST', '0.0.0.0')
    
    demo.launch(
        server_name=host,
        server_port=port,
        share=False,
        debug=False  # Disable debug in production
    )
