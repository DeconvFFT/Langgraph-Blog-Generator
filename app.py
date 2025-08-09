#!/usr/bin/env python3

import gradio as gr
import requests
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://langgraph-blog-generator-production.up.railway.app")
SUPPORTED_LANGUAGES = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Chinese", "Japanese"]

# Blog categories for tech and wellness topics
BLOG_CATEGORIES = [
    "All",
    "Technology", 
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Software Development",
    "Health & Wellness",
    "Fitness",
    "Nutrition",
    "Mental Health"
]

def clean_title(title: str) -> str:
    """Clean title by removing markdown formatting"""
    if not title:
        return "Untitled"
    # Remove ** and quotes
    title = title.replace('**', '').replace('"', '').replace("'", "")
    return title.strip()

def clean_content(content: str) -> str:
    """Clean and format content for better display"""
    if not content:
        return "No content available."
    
    # Basic content cleaning
    content = content.replace('**', '')
    return content.strip()

def validate_topic(topic: str) -> bool:
    """Validate if topic is tech or wellness related"""
    if not topic:
        return False
    
    topic_lower = topic.lower()
    tech_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'data science', 
        'technology', 'tech', 'software', 'programming', 'coding', 'computer',
        'digital', 'internet', 'web', 'app', 'algorithm', 'automation', 'robot'
    ]
    
    wellness_keywords = [
        'health', 'wellness', 'fitness', 'exercise', 'nutrition', 'diet',
        'mental health', 'meditation', 'yoga', 'workout', 'wellbeing',
        'medical', 'healthcare', 'therapy', 'mindfulness', 'sleep'
    ]
    
    all_keywords = tech_keywords + wellness_keywords
    return any(keyword in topic_lower for keyword in all_keywords)

def categorize_blog(topic: str, content: str) -> str:
    """Auto-categorize blog based on topic and content"""
    text = f"{topic} {content}".lower()
    
    if any(keyword in text for keyword in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
        return "Artificial Intelligence"
    elif any(keyword in text for keyword in ['data science', 'data analysis', 'analytics']):
        return "Data Science"
    elif any(keyword in text for keyword in ['software', 'programming', 'coding', 'development']):
        return "Software Development"
    elif any(keyword in text for keyword in ['fitness', 'exercise', 'workout', 'training']):
        return "Fitness"
    elif any(keyword in text for keyword in ['nutrition', 'diet', 'food', 'eating']):
        return "Nutrition"
    elif any(keyword in text for keyword in ['mental health', 'therapy', 'meditation', 'mindfulness']):
        return "Mental Health"
    elif any(keyword in text for keyword in ['health', 'wellness', 'medical', 'healthcare']):
        return "Health & Wellness"
    else:
        return "Technology"

def check_duplicate_blog(title: str, blogs_storage: List[Dict]) -> bool:
    """Check if a blog with the same title already exists"""
    clean_new_title = clean_title(title).lower()
    for blog in blogs_storage:
        if clean_title(blog.get('title', '')).lower() == clean_new_title:
            return True
    return False

def generate_blog_api(topic: str, language: str) -> Dict:
    """Call the API to generate a blog - with fallback to mock data"""
    try:
        # Validate topic first
        if not validate_topic(topic):
            return {
                "success": False,
                "error": "❌ Invalid topic. Please enter a technology or health & wellness related topic."
            }
        
        # Try to call the real API first
        url = f"{API_BASE_URL}/blogs"
        payload = {
            "topic": topic.strip(),
            "language": language,
            "usecase": "blog"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                # Extract blog data from nested response
                data = result.get('data', {})
                blog_data = data.get('blog', {})
                
                if blog_data:
                    return {
                        "success": True,
                        "blog": blog_data,
                        "topic": data.get('topic', topic),
                        "language": data.get('language', language)
                    }
            
            # If API returns error, fall back to mock
            return _generate_mock_blog(topic, language)
            
        except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            # If API is down, use mock data
            return _generate_mock_blog(topic, language)
        
    except Exception as e:
        # If anything fails, use mock data
        return _generate_mock_blog(topic, language)

def _generate_mock_blog(topic: str, language: str) -> Dict:
    """Generate mock blog data when API is unavailable"""
    import random
    
    # Mock blog templates based on topic
    topic_lower = topic.lower()
    
    if any(keyword in topic_lower for keyword in ['ai', 'artificial intelligence', 'machine learning']):
        title = f"🤖 The Future of AI: Exploring {topic}"
        content = f"""# {title}

🚀 **Welcome to the exciting world of Artificial Intelligence!**

In today's rapidly evolving technological landscape, {topic} represents one of the most fascinating developments of our time. As we dive deeper into this revolutionary field, we discover endless possibilities that are reshaping our world.

## 🌟 Key Insights

✨ **Innovation at its Peak**: The current state of AI technology is nothing short of remarkable. From natural language processing to computer vision, we're witnessing breakthroughs that seemed impossible just a few years ago.

🔬 **Research and Development**: Scientists and engineers worldwide are pushing the boundaries of what's possible with {topic}. Every day brings new discoveries and applications that benefit humanity.

## 💡 Practical Applications

Here are some exciting ways {topic} is being used today:

- **Healthcare**: Revolutionizing diagnosis and treatment
- **Education**: Personalizing learning experiences
- **Business**: Optimizing operations and decision-making
- **Entertainment**: Creating immersive experiences

## 🚀 Looking Forward

The future of {topic} holds immense promise. As we continue to innovate and explore, we can expect even more groundbreaking developments that will transform how we live, work, and interact with technology.

*Stay curious, stay informed, and embrace the AI revolution!* 🌟

---
*This is a demo blog generated for the Blog Portfolio Manager. Connect your API for full AI-powered content generation.*"""
    
    elif any(keyword in topic_lower for keyword in ['health', 'wellness', 'fitness', 'nutrition']):
        title = f"🌱 Wellness Journey: {topic} for Better Living"
        content = f"""# {title}

💪 **Your path to better health starts here!**

Embarking on a wellness journey with focus on {topic} is one of the best decisions you can make for your overall well-being. Let's explore how this can transform your life.

## 🎯 Health Benefits

🌟 **Physical Wellness**: Understanding {topic} helps you make informed decisions about your body and health. Every step you take towards better health is an investment in your future.

🧠 **Mental Clarity**: When we focus on wellness, our mental health improves dramatically. The connection between physical and mental well-being cannot be overstated.

## 🥗 Practical Tips

Here are some actionable steps you can take today:

- **Start Small**: Begin with manageable changes to your routine
- **Stay Consistent**: Consistency is key to long-term success
- **Listen to Your Body**: Pay attention to how you feel
- **Seek Support**: Don't hesitate to ask for help when needed

## 🌈 Lifestyle Integration

Incorporating {topic} into your daily life doesn't have to be overwhelming. Here's how to make it sustainable:

1. **Morning Routine**: Start your day with intention
2. **Mindful Choices**: Make conscious decisions throughout the day
3. **Evening Reflection**: Take time to reflect on your progress

## 🚀 Moving Forward

Remember, wellness is a journey, not a destination. Every small step you take towards better health matters. Be patient with yourself and celebrate your progress.

*Your health is your wealth - invest in it wisely!* 💎

---
*This is a demo blog generated for the Blog Portfolio Manager. Connect your API for full AI-powered content generation.*"""
    
    else:
        title = f"🔧 Technology Deep Dive: {topic}"
        content = f"""# {title}

⚡ **Exploring the cutting edge of technology!**

In the ever-evolving world of technology, {topic} stands out as a significant development that's shaping our digital future. Let's dive deep into what makes this so important.

## 🚀 Innovation Overview

🔬 **Technical Excellence**: The advancement in {topic} represents years of research, development, and innovation. It's fascinating to see how far we've come and where we're heading.

💻 **Practical Impact**: This technology isn't just theoretical - it has real-world applications that are making a difference in people's lives every day.

## 🛠️ Key Features

Here's what makes {topic} special:

- **Scalability**: Designed to grow with your needs
- **Efficiency**: Optimized for performance and resource usage
- **Reliability**: Built with stability and consistency in mind
- **User-Friendly**: Accessible to both beginners and experts

## 🌍 Real-World Applications

The applications of {topic} are diverse and impactful:

1. **Enterprise Solutions**: Helping businesses operate more efficiently
2. **Personal Use**: Making everyday tasks easier and more enjoyable
3. **Research**: Enabling new discoveries and innovations
4. **Education**: Enhancing learning experiences

## 📈 Future Prospects

Looking ahead, {topic} promises even more exciting developments. The potential for growth and innovation in this space is tremendous.

*Technology is best when it brings people together and makes life better!* 🌟

---
*This is a demo blog generated for the Blog Portfolio Manager. Connect your API for full AI-powered content generation.*"""
    
    return {
        "success": True,
        "blog": {
            "title": title,
            "content": content
        },
        "topic": topic,
        "language": language
    }

def generate_and_save_blog(topic: str, language: str, blogs_storage: List[Dict]) -> Tuple[str, List[Dict], List[str]]:
    """Generate a new blog and save it to storage"""
    if not topic.strip():
        return "❌ Please enter a topic", blogs_storage, get_blog_choices(blogs_storage)
    
    # Check for duplicates
    if check_duplicate_blog(topic, blogs_storage):
        return "❌ Blog already exists with this title", blogs_storage, get_blog_choices(blogs_storage)
    
    # Generate blog via API
    result = generate_blog_api(topic, language)
    
    if not result.get("success"):
        return result.get("error", "❌ Failed to generate blog"), blogs_storage, get_blog_choices(blogs_storage)
    
    # Extract blog data
    blog_data = result.get("blog", {})
    title = clean_title(blog_data.get('title', topic))
    content = clean_content(blog_data.get('content', ''))
    api_topic = result.get('topic', topic)
    api_language = result.get('language', language)
    
    # Create blog entry
    new_blog = {
        'id': str(uuid.uuid4()),
        'title': title,
        'content': content,
        'topic': api_topic,
        'language': api_language,
        'category': categorize_blog(api_topic, content),
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Add to storage
    updated_blogs = blogs_storage + [new_blog]
    blog_choices = get_blog_choices(updated_blogs)
    
    return f"✅ Blog '{title}' generated successfully!", updated_blogs, blog_choices

def get_blog_choices(blogs_storage: List[Dict]) -> List[str]:
    """Get list of blog choices for dropdown"""
    if not blogs_storage:
        return ["No blogs available"]
    return [f"{blog.get('title', 'Untitled')} ({blog.get('category', 'No Category')})" for blog in blogs_storage]

def filter_blogs_by_category(blogs_storage: List[Dict], category: str) -> List[Dict]:
    """Filter blogs by category"""
    if category == "All":
        return blogs_storage
    return [blog for blog in blogs_storage if blog.get('category') == category]

def get_filtered_blog_choices(blogs_storage: List[Dict], category_filter: str) -> List[str]:
    """Get filtered blog choices based on category"""
    filtered_blogs = filter_blogs_by_category(blogs_storage, category_filter)
    return get_blog_choices(filtered_blogs)

def find_blog_by_display_text(display_text: str, blogs_storage: List[Dict]) -> Optional[Dict]:
    """Find blog by display text from dropdown"""
    if display_text == "No blogs available":
        return None
    
    # Extract title from display text (remove category part)
    if " (" in display_text:
        title_part = display_text.split(" (")[0]
    else:
        title_part = display_text
    
    for blog in blogs_storage:
        if blog.get('title', 'Untitled') == title_part:
            return blog
    return None

def load_blog_for_viewing(selected_blog: str, blogs_storage: List[Dict], category_filter: str):
    """Load selected blog for viewing"""
    if selected_blog == "No blogs available" or not selected_blog:
        return "", "", "", gr.update(visible=False), gr.update(visible=False)
    
    # Filter blogs first
    filtered_blogs = filter_blogs_by_category(blogs_storage, category_filter)
    blog = find_blog_by_display_text(selected_blog, filtered_blogs)
    
    if not blog:
        return "", "", "", gr.update(visible=False), gr.update(visible=False)
    
    title = blog.get('title', 'Untitled')
    content = blog.get('content', 'No content available')
    category = blog.get('category', 'No Category')
    created_at = blog.get('created_at', 'Unknown')
    
    # Format metadata
    meta_info = f"📂 Category: {category} | 📅 Created: {created_at}"
    
    return title, content, meta_info, gr.update(visible=True), gr.update(visible=True)

def load_blog_for_editing(selected_blog: str, blogs_storage: List[Dict], category_filter: str):
    """Load selected blog for editing"""
    if selected_blog == "No blogs available" or not selected_blog:
        return "", "", "No Category", gr.update(visible=False)
    
    # Filter blogs first
    filtered_blogs = filter_blogs_by_category(blogs_storage, category_filter)
    blog = find_blog_by_display_text(selected_blog, filtered_blogs)
    
    if not blog:
        return "", "", "No Category", gr.update(visible=False)
    
    title = blog.get('title', 'Untitled')
    content = blog.get('content', 'No content available')
    category = blog.get('category', 'No Category')
    
    return title, content, category, gr.update(visible=True)

def save_blog_edit(selected_blog: str, new_title: str, new_content: str, new_category: str, 
                   blogs_storage: List[Dict], category_filter: str) -> Tuple[str, List[Dict], List[str]]:
    """Save edited blog"""
    if selected_blog == "No blogs available" or not selected_blog:
        return "❌ No blog selected", blogs_storage, get_filtered_blog_choices(blogs_storage, category_filter)
    
    if not new_title.strip():
        return "❌ Title cannot be empty", blogs_storage, get_filtered_blog_choices(blogs_storage, category_filter)
    
    # Find the blog to edit
    blog_to_edit = None
    blog_index = -1
    
    for i, blog in enumerate(blogs_storage):
        if f"{blog.get('title', 'Untitled')} ({blog.get('category', 'No Category')})" == selected_blog:
            blog_to_edit = blog
            blog_index = i
            break
    
    if blog_to_edit is None:
        return "❌ Blog not found", blogs_storage, get_filtered_blog_choices(blogs_storage, category_filter)
    
    # Update the blog
    updated_blog = blog_to_edit.copy()
    updated_blog['title'] = clean_title(new_title)
    updated_blog['content'] = clean_content(new_content)
    updated_blog['category'] = new_category
    updated_blog['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")  # Update timestamp
    
    # Replace in storage
    updated_blogs = blogs_storage.copy()
    updated_blogs[blog_index] = updated_blog
    
    blog_choices = get_filtered_blog_choices(updated_blogs, category_filter)
    
    return f"✅ Blog '{updated_blog['title']}' updated successfully!", updated_blogs, blog_choices

def load_first_blog_automatically(blogs_storage: List[Dict], category_filter: str):
    """Load the first blog automatically when blogs are available"""
    filtered_blogs = filter_blogs_by_category(blogs_storage, category_filter)
    blog_choices = get_blog_choices(filtered_blogs)
    
    if blog_choices and blog_choices[0] != "No blogs available":
        first_blog_choice = blog_choices[0]
        # Load the first blog for viewing - load_blog_for_viewing returns (title, content, meta, viewer_visible, edit_btn_visible)
        view_results = load_blog_for_viewing(first_blog_choice, blogs_storage, category_filter)
        return view_results + (gr.update(choices=blog_choices, value=first_blog_choice),)
    else:
        return ("", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(choices=["No blogs available"], value=None))

def delete_selected_blog(selected_blog: str, blogs_storage: List[Dict], category_filter: str) -> Tuple[str, List[Dict], List[str]]:
    """Delete the selected blog"""
    if selected_blog == "No blogs available" or not selected_blog:
        return "❌ No blog selected", blogs_storage, get_filtered_blog_choices(blogs_storage, category_filter)
    
    # Find and remove the blog
    updated_blogs = []
    deleted_title = ""
    
    for blog in blogs_storage:
        if f"{blog.get('title', 'Untitled')} ({blog.get('category', 'No Category')})" == selected_blog:
            deleted_title = blog.get('title', 'Untitled')
        else:
            updated_blogs.append(blog)
    
    if deleted_title:
        blog_choices = get_filtered_blog_choices(updated_blogs, category_filter)
        return f"✅ Blog '{deleted_title}' deleted successfully!", updated_blogs, blog_choices
    else:
        return "❌ Blog not found", blogs_storage, get_filtered_blog_choices(blogs_storage, category_filter)

# Create the Gradio interface
with gr.Blocks(
    title="Blog Portfolio Manager - Native Gradio",
    css="""
    .main-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
    .blog-viewer { 
        background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%); 
        border: 1px solid #bfdbfe; 
        border-radius: 16px; 
        padding: 32px; 
        margin: 16px 0; 
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        backdrop-filter: blur(10px);
    }
    .blog-title { 
        color: #1e293b; 
        font-size: 2.25rem; 
        font-weight: 800; 
        margin-bottom: 16px; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .blog-meta { 
        color: #1e40af; 
        font-size: 1.05rem; 
        margin-bottom: 24px; 
        padding: 16px 24px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.05));
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    .blog-content { 
        color: #1f2937; 
        line-height: 1.8; 
        font-size: 1.1rem; 
        background: transparent;
        padding: 24px 0;
        border-radius: 0;
        box-shadow: none;
        border: none;
        font-weight: 400;
    }
    .blog-content h1, .blog-content h2, .blog-content h3 {
        color: #1e40af;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    .blog-content p {
        margin-bottom: 16px;
    }
    .blog-content strong {
        color: #3730a3;
        font-weight: 600;
    }
    /* Override any white text in Gradio components */
    .gradio-container * {
        color: inherit !important;
    }
    /* Ensure all text in blog viewer is visible */
    .blog-viewer * {
        color: #1f2937 !important;
    }
    .blog-viewer .blog-title {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .blog-viewer .blog-meta {
        color: #1e40af !important;
    }
    /* Fix any markdown content styling */
    .blog-content h1, .blog-content h2, .blog-content h3, 
    .blog-content h4, .blog-content h5, .blog-content h6 {
        color: #1e40af !important;
    }
    .blog-content p, .blog-content div, .blog-content span {
        color: #1f2937 !important;
    }
    /* Enhanced button styling for better visibility */
    .blog-viewer .gr-button {
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border: 2px solid transparent !important;
    }
    .blog-viewer .gr-button[variant="secondary"] {
        background: linear-gradient(135deg, #6b7280, #4b5563) !important;
        color: white !important;
        border: 2px solid #6b7280 !important;
    }
    .blog-viewer .gr-button[variant="secondary"]:hover {
        background: linear-gradient(135deg, #4b5563, #374151) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(107, 114, 128, 0.3) !important;
        color: white !important;
    }
    .blog-viewer .gr-button[variant="secondary"] span {
        color: white !important;
    }
    .blog-viewer .gr-button[variant="secondary"]:hover span {
        color: white !important;
    }
    .blog-viewer .gr-button[variant="stop"] {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        color: white !important;
        border: 2px solid #dc2626 !important;
    }
    .blog-viewer .gr-button[variant="stop"]:hover {
        background: linear-gradient(135deg, #b91c1c, #991b1b) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3) !important;
    }
    /* Add spacing between content and buttons */
    .blog-viewer .gr-row {
        margin-top: 32px !important;
        padding-top: 24px !important;
        border-top: 2px solid rgba(59, 130, 246, 0.1) !important;
    }
    /* Remove any unwanted card backgrounds */
    .blog-viewer .gr-group {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    """
) as demo:
    
    # State management
    blogs_storage_state = gr.State(value=[])
    
    # Header
    gr.HTML("""
    <div style="
        text-align: center; 
        padding: 40px 20px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
        border-radius: 24px; 
        margin-bottom: 32px;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        "></div>
        <h1 style="
            margin: 0; 
            font-size: 3rem; 
            font-weight: 900; 
            background: linear-gradient(45deg, #ffffff, #f1f5f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        ">📝 Blog Portfolio Manager</h1>
        <p style="
            margin: 16px 0 0 0; 
            font-size: 1.3rem; 
            opacity: 0.95;
            font-weight: 500;
            position: relative;
            z-index: 1;
        ">
            Generate, View & Edit Your Tech and Wellness Blogs
        </p>
        <p style="
            color: rgba(255,255,255,0.8); 
            font-size: 1.1rem; 
            margin-top: 12px;
            background: rgba(255,255,255,0.1);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            position: relative;
            z-index: 1;
        ">
            💡 Only technology and health & wellness topics are supported
        </p>
    </div>
    <style>
        @keyframes float {
            0%, 100% { transform: translate(0%, 0%) rotate(0deg); }
            50% { transform: translate(-20px, -20px) rotate(180deg); }
        }
    </style>
    """)
    
    # Main interface using Tabs
    with gr.Tabs():
        
        # Tab 1: Blog Generation
        with gr.Tab("📝 Generate Blog"):
            with gr.Row():
                with gr.Column(scale=2):
                    topic_input = gr.Textbox(
                        label="📝 Blog Topic",
                        placeholder="Enter your blog topic here... (e.g., 'The Future of Artificial Intelligence' or 'Benefits of Morning Exercise')",
                        lines=2,
                        max_lines=3
                    )
                with gr.Column(scale=1):
                    language_dropdown = gr.Dropdown(
                        choices=SUPPORTED_LANGUAGES,
                        value="English",
                        label="🌍 Language",
                        info="Select the language for your blog"
                    )
            
            generate_btn = gr.Button(
                "🚀 Generate & Save Blog",
                variant="primary",
                size="lg"
            )
            
            generation_status = gr.Textbox(
                label="📊 Status",
                value="Ready to generate blogs",
                interactive=False
            )
        
        # Tab 2: View & Edit Blogs
        with gr.Tab("👁️ View & Edit Blogs"):
            with gr.Row():
                with gr.Column(scale=2):
                    category_filter = gr.Dropdown(
                        choices=BLOG_CATEGORIES,
                        value="All",
                        label="📂 Filter by Category",
                        info="Filter blogs by category"
                    )
                with gr.Column(scale=3):
                    blog_selector = gr.Dropdown(
                        choices=["No blogs available"],
                        label="📖 Select Blog",
                        info="Choose a blog to view or edit"
                    )
            
            # Blog Viewer Section
            with gr.Group():
                gr.HTML("<h3>👁️ Blog Viewer</h3>")
                
                blog_viewer_container = gr.Column(visible=False, elem_classes=["blog-viewer"])
                with blog_viewer_container:
                    view_title = gr.HTML(elem_classes=["blog-title"])
                    view_meta = gr.HTML(elem_classes=["blog-meta"])
                    view_content = gr.Markdown(elem_classes=["blog-content"])
                    
                    with gr.Row():
                        edit_btn = gr.Button("✏️ Edit This Blog", variant="secondary", size="lg")
                        delete_btn = gr.Button("🗑️ Delete This Blog", variant="stop", size="lg")
            
            # Blog Editor Section (completely hidden by default)
            blog_editor_container = gr.Group(visible=False)
            with blog_editor_container:
                gr.HTML("<h3>✏️ Blog Editor</h3>")
                
                edit_title = gr.Textbox(
                    label="📝 Title",
                    placeholder="Enter blog title...",
                    lines=1
                )
                edit_category = gr.Dropdown(
                    choices=[cat for cat in BLOG_CATEGORIES if cat != "All"],
                    label="📂 Category"
                )
                edit_content = gr.Textbox(
                    label="📄 Content",
                    placeholder="Enter blog content...",
                    lines=10,
                    max_lines=20
                )
                
                with gr.Row():
                    save_btn = gr.Button("💾 Save Changes", variant="primary")
                    cancel_btn = gr.Button("❌ Cancel Edit", variant="secondary")
            
            # Hidden status for popups
            edit_status = gr.Textbox(visible=False)
    
    # Add event listeners for popups
    generation_status.change(
        fn=lambda msg: gr.Info(msg) if msg and ("✅" in msg or "❌" in msg) else None,
        inputs=[generation_status],
        outputs=[]
    )
    
    edit_status.change(
        fn=lambda msg: gr.Info(msg) if msg and ("✅" in msg or "❌" in msg) else None,
        inputs=[edit_status],
        outputs=[]
    )
    
    # Event handlers
    
    # Blog generation
    def handle_blog_generation(topic: str, language: str, blogs_storage: List[Dict], current_category: str):
        """Handle blog generation and update all necessary components"""
        status, updated_blogs, all_blog_choices = generate_and_save_blog(topic, language, blogs_storage)
        
        # Load first blog automatically and show popup
        auto_load_results = load_first_blog_automatically(updated_blogs, current_category)
        
        return (
            status,  # generation_status (will show as popup)
            updated_blogs,  # blogs_storage_state
            auto_load_results[0],  # view_title
            auto_load_results[1],  # view_content  
            auto_load_results[2],  # view_meta
            auto_load_results[3],  # blog_viewer_container
            auto_load_results[5],  # blog_selector
            gr.update(visible=False)  # blog_editor_container (hidden by default)
        )
    
    generate_btn.click(
        fn=handle_blog_generation,
        inputs=[topic_input, language_dropdown, blogs_storage_state, category_filter],
        outputs=[generation_status, blogs_storage_state, view_title, view_content, view_meta, blog_viewer_container, blog_selector, blog_editor_container]
    )
    
    # Category filtering
    def handle_category_filter(blogs_storage: List[Dict], category: str):
        """Handle category filtering and update blog selector"""
        # Load first blog automatically for new category
        auto_load_results = load_first_blog_automatically(blogs_storage, category)
        
        return (
            auto_load_results[5],  # blog_selector with choices and value
            auto_load_results[0],  # view_title
            auto_load_results[1],  # view_content
            auto_load_results[2],  # view_meta
            auto_load_results[3],  # blog_viewer_container
            gr.update(visible=False)   # hide blog_editor_container
        )
    
    category_filter.change(
        fn=handle_category_filter,
        inputs=[blogs_storage_state, category_filter],
        outputs=[blog_selector, view_title, view_content, view_meta, blog_viewer_container, blog_editor_container]
    )
    
    # Blog selection for viewing
    blog_selector.change(
        fn=load_blog_for_viewing,
        inputs=[blog_selector, blogs_storage_state, category_filter],
        outputs=[view_title, view_content, view_meta, blog_viewer_container, edit_btn]
    )
    
    # Edit button click
    def handle_edit_click(selected_blog: str, blogs_storage: List[Dict], category_filter: str):
        """Handle edit button click and show editor"""
        title, content, category, _ = load_blog_for_editing(selected_blog, blogs_storage, category_filter)
        return title, content, category, gr.update(visible=True)
    
    edit_btn.click(
        fn=handle_edit_click,
        inputs=[blog_selector, blogs_storage_state, category_filter],
        outputs=[edit_title, edit_content, edit_category, blog_editor_container]
    )
    
    # Save edit
    def handle_save_edit(selected_blog: str, new_title: str, new_content: str, new_category: str, 
                        blogs_storage: List[Dict], category_filter: str):
        """Handle save edit and update blog selector"""
        status, updated_blogs, blog_choices = save_blog_edit(selected_blog, new_title, new_content, new_category, blogs_storage, category_filter)
        
        # Load first blog automatically after save
        auto_load_results = load_first_blog_automatically(updated_blogs, category_filter)
        
        return (
            status,  # edit_status (will show as popup)
            updated_blogs,  # blogs_storage_state
            auto_load_results[5],  # blog_selector
            gr.update(visible=False),  # hide editor
            auto_load_results[0],  # view_title
            auto_load_results[1],  # view_content
            auto_load_results[2],  # view_meta
            auto_load_results[3]   # blog_viewer_container
        )
    
    save_btn.click(
        fn=handle_save_edit,
        inputs=[blog_selector, edit_title, edit_content, edit_category, blogs_storage_state, category_filter],
        outputs=[edit_status, blogs_storage_state, blog_selector, blog_editor_container, view_title, view_content, view_meta, blog_viewer_container]
    )
    
    # Cancel edit
    cancel_btn.click(
        fn=lambda: gr.update(visible=False),
        outputs=[blog_editor_container]
    )
    
    # Delete blog
    def handle_delete_blog(selected_blog: str, blogs_storage: List[Dict], category_filter: str):
        """Handle delete blog and update blog selector"""
        status, updated_blogs, blog_choices = delete_selected_blog(selected_blog, blogs_storage, category_filter)
        
        # Load first blog automatically after delete
        auto_load_results = load_first_blog_automatically(updated_blogs, category_filter)
        
        return (
            status,  # edit_status (will show as popup)
            updated_blogs,  # blogs_storage_state
            auto_load_results[5],  # blog_selector
            auto_load_results[0],  # view_title
            auto_load_results[1],  # view_content
            auto_load_results[2],  # view_meta
            auto_load_results[3],  # blog_viewer_container
            gr.update(visible=False)   # hide editor
        )
    
    delete_btn.click(
        fn=handle_delete_blog,
        inputs=[blog_selector, blogs_storage_state, category_filter],
        outputs=[edit_status, blogs_storage_state, blog_selector, view_title, view_content, view_meta, blog_viewer_container, blog_editor_container]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
