import gradio as gr
import json
import requests
from typing import Dict, Any, Optional, List
import time
import os
from datetime import datetime
import uuid
import html

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://langgraph-blog-generator-production.up.railway.app')  # Default to localhost for development
API_ENDPOINT = f"{API_BASE_URL}/blogs"

# Supported languages
SUPPORTED_LANGUAGES = [
    "English",
    "Spanish", 
    "Hindi"
]

# Blog categories - Only tech and wellness
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

def validate_topic(topic: str) -> tuple[bool, str]:
    """Validate if topic is tech or wellness related"""
    topic_lower = topic.lower()
    
    # Tech keywords
    tech_keywords = [
        "technology", "tech", "software", "hardware", "digital", "computer", "ai", "artificial intelligence",
        "machine learning", "ml", "data science", "programming", "coding", "developer", "code", "app",
        "algorithm", "neural", "deep learning", "chatgpt", "gpt", "automation", "robotics", "cybersecurity",
        "cloud", "blockchain", "iot", "virtual reality", "vr", "augmented reality", "ar", "mobile",
        "web", "database", "api", "framework", "startup", "innovation", "digital transformation"
    ]
    
    # Wellness keywords
    wellness_keywords = [
        "health", "wellness", "fitness", "exercise", "workout", "nutrition", "diet", "mental health",
        "meditation", "yoga", "mindfulness", "stress", "anxiety", "depression", "therapy", "counseling",
        "self-care", "lifestyle", "wellbeing", "physical health", "mental wellbeing", "emotional health",
        "sleep", "recovery", "strength training", "cardio", "flexibility", "balance", "energy", "vitality",
        "holistic", "natural", "organic", "supplements", "vitamins", "minerals", "protein", "workout routine"
    ]
    
    # Check if topic contains tech or wellness keywords
    for keyword in tech_keywords:
        if keyword in topic_lower:
            return True, "tech"
    
    for keyword in wellness_keywords:
        if keyword in topic_lower:
            return True, "wellness"
    
    return False, "invalid"

def clean_title(title: str) -> str:
    """Clean up title formatting - remove markdown and quotes"""
    # Remove markdown formatting
    cleaned = title.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
    
    # Remove quotes
    cleaned = cleaned.replace('"', '').replace('"', '').replace('"', '').replace('"', '')
    cleaned = cleaned.replace("'", '').replace("'", '').replace("'", '').replace("'", '')
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned

def clean_content(content: str) -> str:
    """Clean up content formatting - remove markdown and format properly"""
    if not content:
        return ""
    
    # Remove markdown formatting from the beginning
    cleaned = content.strip()
    
    # Remove any markdown headers at the start
    lines = cleaned.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip empty lines at the beginning
        if not cleaned_lines and not line.strip():
            continue
        
        # Clean markdown formatting
        line = line.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        line = line.replace('"', '').replace('"', '').replace('"', '').replace('"', '')
        line = line.replace("'", '').replace("'", '').replace("'", '').replace("'", '')
        
        cleaned_lines.append(line)
    
    # Join lines back together
    cleaned = '\n'.join(cleaned_lines)
    
    return cleaned.strip()

def generate_blog(topic: str, language: str) -> Dict[str, Any]:
    """Generate a blog using the API with enhanced prompts for emojis and better formatting"""
    if not topic.strip():
        return {
            "success": False,
            "error": "Topic cannot be empty",
            "message": "Please provide a topic for the blog"
        }
    
    # Validate topic
    is_valid, category_type = validate_topic(topic.strip())
    if not is_valid:
        return {
            "success": False,
            "error": "Invalid topic",
            "message": "Please provide a topic related to technology or health & wellness only."
        }
    
    try:
        # Enhanced prompt with emojis and better formatting
        enhanced_prompt = f"""
        Create an engaging blog post about: {topic.strip()}
        
        Requirements:
        - Write in {language}
        - Add relevant emojis throughout the content to make it more engaging and fun to read
        - Use proper markdown formatting with headers, bullet points, and emphasis
        - Include a compelling introduction that hooks the reader
        - Structure the content with clear sections and subheadings
        - Add emojis to section headers and key points
        - Make the content informative yet entertaining
        - Include practical examples or tips where relevant
        - End with a thought-provoking conclusion
        - Use emojis strategically to enhance readability and engagement
        - Minimum 1200 words
        - Do NOT include the title - only the content
        
        Make sure the content flows naturally and feels like a high-quality Medium or Substack article!
        """
        
        payload = {
            "topic": enhanced_prompt,
            "language": language
        }
        
        print(f"🌐 Making API request to: {API_ENDPOINT}")
        print(f"📤 Request payload: {payload}")
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300
        )
        
        response.raise_for_status()
        api_response = response.json()
        
        print(f"📥 API Response Status: {response.status_code}")
        print(f"📥 API Response: {api_response}")
        
        return api_response
        
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection failed",
            "message": f"Cannot connect to API at {API_ENDPOINT}. Please check if the API server is running. If you're using Hugging Face Spaces, make sure to set the API_BASE_URL secret to your Railway API endpoint."
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout",
            "message": "The API request timed out. Please try again."
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 502:
            return {
                "success": False,
                "error": "API server error (502)",
                "message": f"The API server is not responding (502 error). Please check if your FastAPI backend is running. Current API endpoint: {API_ENDPOINT}"
            }
        else:
            return {
                "success": False,
                "error": "HTTP error",
                "message": f"API returned error {e.response.status_code}: {e.response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": "Request failed",
            "message": f"Error: {str(e)}"
        }

def check_duplicate_blog(title: str, blogs_storage: List[Dict]) -> bool:
    """Check if a blog with the same title already exists"""
    title_lower = clean_title(title).lower().strip()
    for blog in blogs_storage:
        if clean_title(blog.get('title', '')).lower().strip() == title_lower:
            return True
    return False

def categorize_blog(topic: str, content: str) -> str:
    """Automatically categorize blog based on topic and content"""
    topic_lower = topic.lower()
    content_lower = content.lower()
    
    # Define category keywords - only tech and wellness
    category_keywords = {
        "Technology": ["technology", "tech", "software", "hardware", "digital", "computer", "ai", "artificial intelligence", "automation"],
        "Artificial Intelligence": ["ai", "artificial intelligence", "neural", "deep learning", "chatgpt", "gpt", "machine learning"],
        "Machine Learning": ["machine learning", "ml", "algorithm", "model", "training", "prediction", "neural network"],
        "Data Science": ["data", "analytics", "statistics", "visualization", "big data", "data science"],
        "Software Development": ["programming", "coding", "developer", "code", "software", "app", "framework"],
        "Health & Wellness": ["health", "wellness", "fitness", "medical", "nutrition", "exercise", "lifestyle"],
        "Fitness": ["fitness", "exercise", "workout", "training", "strength", "cardio", "gym"],
        "Nutrition": ["nutrition", "diet", "food", "eating", "supplements", "vitamins", "protein"],
        "Mental Health": ["mental health", "therapy", "counseling", "anxiety", "depression", "stress", "mindfulness"]
    }
    
    # Check topic and content for category matches
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in topic_lower or keyword in content_lower:
                return category
    
    # Default based on validation
    is_valid, category_type = validate_topic(topic)
    if category_type == "tech":
        return "Technology"
    elif category_type == "wellness":
        return "Health & Wellness"
    
    return "Technology"  # Fallback

def create_blog_card(blog: Dict[str, Any]) -> str:
    """Create HTML card for a blog with 4-column grid layout and embedded data"""
    blog_id = blog.get('id', 'unknown')
    title = blog.get('title', 'Untitled')
    content = blog.get('content', 'No content available')
    topic = blog.get('topic', 'Unknown topic')
    category = blog.get('category', 'Technology')
    language = blog.get('language', 'English')
    created_at = blog.get('created_at', 'Unknown date')
    
    # Show first 200 characters as preview (no truncation with ...)
    preview = content[:200] if len(content) > 200 else content
    
    # Get category color
    category_colors = {
        "Technology": "#3B82F6",
        "Artificial Intelligence": "#8B5CF6", 
        "Machine Learning": "#06B6D4",
        "Data Science": "#10B981",
        "Software Development": "#F59E0B",
        "Health & Wellness": "#EC4899",
        "Fitness": "#14B8A6",
        "Nutrition": "#F97316",
        "Mental Health": "#6366F1"
    }
    
    category_color = category_colors.get(category, "#3B82F6")
    
    # Escape content for safe embedding in HTML
    escaped_content = html.escape(content)
    escaped_title = html.escape(title)
    
    card_html = f"""
    <div class="blog-card" data-blog-id="{blog_id}" 
         data-blog-title="{escaped_title}"
         data-blog-content="{escaped_content}"
         data-blog-topic="{html.escape(topic)}"
         data-blog-language="{html.escape(language)}"
         data-blog-category="{html.escape(category)}"
         data-blog-created="{html.escape(created_at)}"
         style="
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 12px 0;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 400px;
        display: flex;
        flex-direction: column;
    ">
        <!-- Category Badge -->
        <div style="
            position: absolute;
            top: 16px;
            right: 16px;
            background: {category_color};
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            z-index: 10;
        ">
            {category}
        </div>
        
        <!-- Blog Image Placeholder -->
        <div style="
            width: 100%;
            height: 120px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
            flex-shrink: 0;
        ">
            📝
        </div>
        
        <!-- Blog Title -->
        <h3 style="
            margin: 0 0 12px 0;
            color: #1f2937;
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.3;
            flex-shrink: 0;
        ">
            {title}
        </h3>
        
        <!-- Topic and Language -->
        <div style="
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 0.8rem;
            color: #6b7280;
            flex-shrink: 0;
        ">
            <span style="
                background: #f3f4f6;
                padding: 3px 6px;
                border-radius: 6px;
            ">
                📌 {topic[:20]}{'...' if len(topic) > 20 else ''}
            </span>
            <span style="
                background: #f3f4f6;
                padding: 3px 6px;
                border-radius: 6px;
            ">
                🌍 {language}
            </span>
        </div>
        
        <!-- Content Preview -->
        <p style="
            color: #4b5563;
            line-height: 1.5;
            margin: 0 0 16px 0;
            font-size: 0.9rem;
            flex-grow: 1;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
        ">
            {preview}
        </p>
        
        <!-- Footer -->
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 12px;
            border-top: 1px solid #e5e7eb;
            flex-shrink: 0;
        ">
            <span style="
                color: #9ca3af;
                font-size: 0.75rem;
            ">
                📅 {created_at}
            </span>
            
            <div style="display: flex; gap: 6px;">
                <button onclick="viewBlogModal('{blog_id}')" style="
                    background: #3b82f6;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 0.8rem;
                    font-weight: 600;
                    transition: background 0.2s ease;
                " onmouseover="this.style.background='#2563eb'" onmouseout="this.style.background='#3b82f6'">
                    👁️ View
                </button>
                <button onclick="editBlogModal('{blog_id}')" style="
                    background: #f59e0b;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 0.8rem;
                    font-weight: 600;
                    transition: background 0.2s ease;
                " onmouseover="this.style.background='#d97706'" onmouseout="this.style.background='#f59e0b'">
                    ✏️ Edit
                </button>
                <button onclick="deleteBlogConfirm('{blog_id}')" style="
                    background: #ef4444;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 0.8rem;
                    font-weight: 600;
                    transition: background 0.2s ease;
                " onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">
                    🗑️
                </button>
            </div>
        </div>
    </div>
    """
    
    return card_html

def generate_and_save_blog(topic: str, language: str, blogs_storage: List[Dict], current_filter: str) -> tuple:
    """Generate a blog and save it to storage using Gradio State"""
    if not topic.strip():
        return "", "⚠️ Please enter a topic for the blog.", blogs_storage, current_filter
    
    print(f"🚀 Starting blog generation for topic: {topic}")
    print(f"🌍 Language: {language}")
    
    # Generate blog
    result = generate_blog(topic, language)
    
    print(f"📊 Generation result: {result}")
    
    if not result.get('success', False):
        error_message = f"❌ {result.get('message', 'An error occurred')}"
        print(f"❌ Generation failed: {error_message}")
        return "", error_message, blogs_storage, current_filter
    
    # Extract blog data
    data = result.get('data', {})
    blog_content = data.get('blog', {})
    
    print(f"📋 Extracted data: {data}")
    print(f"📝 Blog content: {blog_content}")
    
    if not blog_content:
        print("❌ No blog content found in API response")
        return "", "❌ No blog content was generated.", blogs_storage, current_filter
    
    # Get the generated title and clean it
    generated_title = blog_content.get('title', f'Blog about {topic}')
    cleaned_title = clean_title(generated_title)
    
    print(f"📌 Generated title: {generated_title}")
    print(f"🧹 Cleaned title: {cleaned_title}")
    
    # Check for duplicate blog
    if check_duplicate_blog(cleaned_title, blogs_storage):
        print(f"⚠️ Duplicate blog found: {cleaned_title}")
        return "", "❌ Blog already exists with this title.", blogs_storage, current_filter
    
    # Clean the content
    raw_content = blog_content.get('content', '')
    if not raw_content:
        print("❌ No content found in API response")
        return "", "❌ No content was generated in the API response.", blogs_storage, current_filter
    
    print(f"📄 Raw content length: {len(raw_content)} characters")
    print(f"📄 Raw content preview: {raw_content[:200]}...")
    
    cleaned_content = clean_content(raw_content)
    
    print(f"🧹 Cleaned content length: {len(cleaned_content)} characters")
    print(f"🧹 Cleaned content preview: {cleaned_content[:200]}...")
    
    # Create blog object
    blog = {
        'id': str(uuid.uuid4()),
        'title': cleaned_title,
        'content': cleaned_content,
        'topic': topic,
        'language': language,
        'category': categorize_blog(topic, cleaned_content),
        'created_at': datetime.now().strftime("%B %d, %Y"),
        'api_response': result
    }
    
    print(f"💾 Created blog object: {blog}")
    
    # Add to storage
    updated_blogs = blogs_storage + [blog]
    
    print(f"📦 Added to storage. Total blogs: {len(updated_blogs)}")
    
    # Generate all blog cards
    all_cards = generate_blog_cards(updated_blogs, current_filter)
    
    success_message = f"✅ Blog '{blog['title']}' generated and saved successfully!"
    print(f"✅ {success_message}")
    
    return all_cards, success_message, updated_blogs, current_filter

def generate_blog_cards(blogs: List[Dict], selected_category: str) -> str:
    """Generate HTML for all blog cards in 4-column grid layout"""
    if not blogs:
        return """
        <div style="
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        ">
            <div style="font-size: 4rem; margin-bottom: 20px;">📝</div>
            <h3 style="margin: 0 0 12px 0; color: #374151;">No blogs yet</h3>
            <p style="margin: 0; font-size: 1.1rem;">Generate your first blog to get started!</p>
        </div>
        """
    
    # Filter by category
    if selected_category != "All":
        filtered_blogs = [blog for blog in blogs if blog.get('category') == selected_category]
    else:
        filtered_blogs = blogs
    
    if not filtered_blogs:
        return f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        ">
            <div style="font-size: 4rem; margin-bottom: 20px;">🔍</div>
            <h3 style="margin: 0 0 12px 0; color: #374151;">No blogs in {selected_category}</h3>
            <p style="margin: 0; font-size: 1.1rem;">Try generating a blog or select a different category.</p>
        </div>
        """
    
    # Generate cards HTML with responsive grid
    cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px;">'
    for blog in filtered_blogs:
        cards_html += create_blog_card(blog)
    cards_html += '</div>'
    
    return cards_html

def filter_blogs_by_category(selected_category: str, blogs_storage: List[Dict]) -> tuple:
    """Filter blogs by category using Gradio State"""
    # Get fresh data and filter
    if selected_category != "All":
        filtered_blogs = [blog for blog in blogs_storage if blog.get('category') == selected_category]
    else:
        filtered_blogs = blogs_storage
    
    cards_html = generate_blog_cards(filtered_blogs, selected_category)
    return cards_html, blogs_storage, selected_category

def handle_category_change(selected_category: str, blogs_storage: List[Dict], current_filter: str) -> tuple:
    """Handle category change and update state properly"""
    print(f"🔄 Category changed from '{current_filter}' to '{selected_category}'")
    print(f"📦 Total blogs in storage: {len(blogs_storage)}")
    
    # Update the current filter
    new_filter = selected_category
    
    # Filter blogs based on new category
    if new_filter != "All":
        filtered_blogs = [blog for blog in blogs_storage if blog.get('category') == new_filter]
    else:
        filtered_blogs = blogs_storage
    
    print(f"📋 Filtered blogs for '{new_filter}': {len(filtered_blogs)}")
    
    # Generate cards for the filtered blogs
    cards_html = generate_blog_cards(filtered_blogs, new_filter)
    
    return cards_html, blogs_storage, new_filter

def delete_blog_from_storage(blog_id: str, blogs_storage: List[Dict], current_filter: str) -> tuple:
    """Delete a blog from storage using Gradio State"""
    # Delete blog
    updated_blogs = [blog for blog in blogs_storage if blog.get('id') != blog_id]
    
    if len(updated_blogs) < len(blogs_storage):
        print(f"🗑️ Blog deleted successfully. Remaining blogs: {len(updated_blogs)}")
    else:
        print(f"⚠️ Blog deletion failed for ID: {blog_id}")
    
    # Generate updated cards
    cards_html = generate_blog_cards(updated_blogs, current_filter)
    return cards_html, updated_blogs, current_filter

def get_blog_by_id(blog_id: str, blogs_storage: List[Dict]) -> Optional[Dict]:
    """Get a blog by its ID"""
    for blog in blogs_storage:
        if blog.get('id') == blog_id:
            return blog
    return None

def update_blog(blog_id: str, title: str, content: str, category: str, blogs_storage: List[Dict], current_filter: str) -> tuple:
    """Update a blog using Gradio State"""
    # Update blog
    updated_blogs = []
    success = False
    
    for blog in blogs_storage:
        if blog.get('id') == blog_id:
            updated_blog = blog.copy()
            updated_blog.update({
                'title': clean_title(title), 
                'content': clean_content(content), 
                'category': category,
                'updated_at': datetime.now().strftime("%B %d, %Y")
            })
            updated_blogs.append(updated_blog)
            success = True
            print(f"✏️ Blog updated successfully: {updated_blog.get('title', 'Untitled')}")
        else:
            updated_blogs.append(blog)
    
    if success:
        print(f"✏️ Blog updated successfully. Total blogs: {len(updated_blogs)}")
    else:
        print(f"⚠️ Blog update failed for ID: {blog_id}")
    
    # Generate updated cards
    cards_html = generate_blog_cards(updated_blogs, current_filter)
    return cards_html, updated_blogs, current_filter

def check_api_status() -> str:
    """Check if the API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return "✅ API is available"
        else:
            return "⚠️ API is responding but may have issues"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to API. Please check if the server is running."
    except requests.exceptions.Timeout:
        return "⚠️ API connection timeout"
    except Exception as e:
        return f"❌ API check failed: {str(e)}"

def get_api_status_message() -> str:
    """Get a user-friendly API status message"""
    status = check_api_status()
    if "✅" in status:
        return "Ready to generate blogs"
    elif "⚠️" in status:
        return "API may have issues - try generating a blog"
    else:
        return "API unavailable - please check server connection"

def refresh_status() -> str:
    """Refresh the API status"""
    return get_api_status_message()

def debug_state(blogs_storage: List[Dict], current_filter: str) -> str:
    """Debug function to log current state"""
    print(f"🔍 DEBUG STATE:")
    print(f"   📦 Total blogs: {len(blogs_storage)}")
    print(f"   🏷️ Current filter: {current_filter}")
    print(f"   📋 Blog categories: {list(set(blog.get('category', 'Unknown') for blog in blogs_storage))}")
    
    if blogs_storage:
        print(f"   📝 Sample blog: {blogs_storage[0].get('title', 'No title')} - {blogs_storage[0].get('category', 'No category')}")
    
    return f"Debug: {len(blogs_storage)} blogs, filter: {current_filter}"

def get_state_summary(blogs_storage: List[Dict]) -> str:
    """Get a summary of current state for display"""
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        font-size: 0.9rem;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <strong>💾 State Management:</strong> 
                <span style="opacity: 0.9;">{len(blogs_storage)} blogs saved</span>
            </div>
            <div style="opacity: 0.8; font-size: 0.8rem;">
                Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
            </div>
        </div>
    </div>
    """

# Custom CSS for better styling
custom_css = """
<style>
.blog-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
.gradio-container {
    max-width: 1600px;
    margin: 0 auto;
}
.gradio-interface {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    min-height: 100vh;
    padding: 20px;
}
.gradio-main {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
.gradio-input {
    border-radius: 12px;
    border: 2px solid #e1e5e9;
    transition: border-color 0.3s ease;
}
.gradio-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.gradio-button {
    background: linear-gradient(45deg, #3b82f6, #1d4ed8);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    transition: transform 0.2s ease;
}
.gradio-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}
.gradio-output {
    border-radius: 12px;
    border: 2px solid #e1e5e9;
    background: white;
}
/* Modal styles */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}
.modal-content {
    background-color: white;
    margin: 2% auto;
    padding: 0;
    border-radius: 16px;
    width: 95%;
    max-width: 900px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    position: absolute;
    right: 20px;
    top: 15px;
    z-index: 1001;
}
.close:hover {
    color: #000;
}
/* Medium/Substack article styling */
.article-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px 30px;
    border-radius: 16px 16px 0 0;
    position: relative;
}
.article-title {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 20px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.article-meta {
    display: flex;
    gap: 20px;
    font-size: 1rem;
    opacity: 0.9;
}
.article-content {
    padding: 40px 30px;
    line-height: 1.8;
    font-size: 1.1rem;
    color: #374151;
    font-family: 'Georgia', serif;
    min-height: 400px;
    overflow-y: auto;
    max-height: 60vh;
}
.article-content h1, .article-content h2, .article-content h3 {
    color: #1f2937;
    margin-top: 40px;
    margin-bottom: 20px;
    font-weight: 700;
}
.article-content h1 {
    font-size: 2rem;
}
.article-content h2 {
    font-size: 1.5rem;
}
.article-content h3 {
    font-size: 1.25rem;
}
.article-content p {
    margin-bottom: 20px;
}
.article-content ul, .article-content ol {
    margin-bottom: 20px;
    padding-left: 30px;
}
.article-content li {
    margin-bottom: 8px;
}
.article-content blockquote {
    border-left: 4px solid #3b82f6;
    padding-left: 20px;
    margin: 30px 0;
    font-style: italic;
    color: #6b7280;
    background: #f9fafb;
    padding: 20px;
    border-radius: 8px;
}
.article-content strong {
    font-weight: 700;
    color: #1f2937;
}
.article-content em {
    font-style: italic;
}
/* Edit modal specific styles */
#editModal .modal-content {
    max-height: 95vh;
    overflow-y: auto;
}
#editModal textarea {
    min-height: 400px;
    max-height: 60vh;
    overflow-y: auto;
    resize: vertical;
}
/* Responsive grid */
@media (max-width: 1200px) {
    .blog-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
@media (max-width: 900px) {
    .blog-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 600px) {
    .blog-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

# Create Gradio interface with State management
with gr.Blocks(css=custom_css, title="Blog Portfolio Manager") as demo:
    # Gradio State components for persistent state management
    blogs_storage_state = gr.State(value=[])  # Store blogs data
    current_filter_state = gr.State(value="All")  # Store current filter
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="
            color: #1f2937;
            font-size: 3rem;
            margin-bottom: 16px;
            font-weight: 800;
            background: linear-gradient(45deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            📝 Blog Portfolio Manager
        </h1>
        <p style="
            color: #6b7280;
            font-size: 1.2rem;
            margin: 0;
            max-width: 600px;
            margin: 0 auto;
        ">
            Generate, organize, and manage your AI-powered blog collection
        </p>
        <p style="
            color: #9ca3af;
            font-size: 1rem;
            margin-top: 8px;
        ">
            💡 Only technology and health & wellness topics are supported
        </p>
    </div>
    """)
    
    # Blog Generation Section
    with gr.Row():
        with gr.Column(scale=3):
            topic_input = gr.Textbox(
                label="📝 Blog Topic",
                placeholder="Enter your blog topic here... (e.g., 'The Future of Artificial Intelligence' or 'Benefits of Morning Exercise')",
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
                "🚀 Generate & Save Blog",
                variant="primary",
                size="lg"
            )
    
    # Status Section
    with gr.Row():
        status_output = gr.Textbox(
            label="📊 Status",
            value=get_api_status_message(),
            interactive=False,
            lines=1
        )
    
    # State Management Status Section
    with gr.Row():
        state_status = gr.HTML(
            value=get_state_summary([]),
            label="💾 State Status"
        )
        
        debug_btn = gr.Button(
            "🔍 Debug State",
            size="sm",
            variant="secondary"
        )
    
    # Debug output
    debug_output = gr.Textbox(
        label="🔍 Debug Info",
        interactive=False,
        visible=False
    )
    
    # Category Filter Section
    with gr.Row():
        category_dropdown = gr.Dropdown(
            choices=BLOG_CATEGORIES,
            value="All",
            label="🏷️ Filter by Category",
            info="Select a category to filter blogs"
        )
    
    # Blog Cards Display Section
    with gr.Row():
        blog_cards_output = gr.HTML(
            label="📄 Your Blog Portfolio",
            value=generate_blog_cards([], "All")
        )

    # Hidden components for blog operations
    blog_id_input = gr.Textbox(visible=False, elem_id="blog_id_input")
    delete_btn = gr.Button("Delete", visible=False, elem_id="delete_btn")
    
    # Hidden components for blog updates
    update_blog_id_input = gr.Textbox(visible=False, elem_id="update_blog_id_input")
    update_title_input = gr.Textbox(visible=False, elem_id="update_title_input")
    update_content_input = gr.Textbox(visible=False, elem_id="update_content_input")
    update_category_input = gr.Textbox(visible=False, elem_id="update_category_input")
    update_btn = gr.Button("Update", visible=False, elem_id="update_btn")
    
    # Hidden component to get latest blog data
    get_blogs_trigger = gr.Button("Get Blogs", visible=False, elem_id="get_blogs_trigger")
    blogs_data_output = gr.JSON(visible=False, elem_id="blogs_data_output")
    
    def get_current_blogs_data(blogs_storage):
        """Get current blogs data for JavaScript"""
        return blogs_storage
    
    # Event handlers with State management
    generate_btn.click(
        fn=generate_and_save_blog,
        inputs=[topic_input, language_dropdown, blogs_storage_state, current_filter_state],
        outputs=[blog_cards_output, status_output, blogs_storage_state, current_filter_state]
    )
    
    category_dropdown.change(
        fn=handle_category_change,
        inputs=[category_dropdown, blogs_storage_state, current_filter_state],
        outputs=[blog_cards_output, blogs_storage_state, current_filter_state]
    )
    
    delete_btn.click(
        fn=delete_blog_from_storage,
        inputs=[blog_id_input, blogs_storage_state, current_filter_state],
        outputs=[blog_cards_output, blogs_storage_state, current_filter_state]
    )
    
    # Add update event handler
    update_btn.click(
        fn=update_blog,
        inputs=[update_blog_id_input, update_title_input, update_content_input, update_category_input, blogs_storage_state, current_filter_state],
        outputs=[blog_cards_output, blogs_storage_state, current_filter_state]
    )
    
    # Add debug event handler
    debug_btn.click(
        fn=debug_state,
        inputs=[blogs_storage_state, current_filter_state],
        outputs=[debug_output]
    )
    
    # State management refresh
    def refresh_state_status(blogs_storage):
        """Refresh the state management status display"""
        return get_state_summary(blogs_storage)
    
    # Update state status when blogs change
    blogs_storage_state.change(
        fn=refresh_state_status,
        inputs=[blogs_storage_state],
        outputs=[state_status]
    )
    
    get_blogs_trigger.click(
        fn=get_current_blogs_data,
        inputs=[blogs_storage_state],
        outputs=[blogs_data_output]
    )
    
    # Add JavaScript for advanced blog management with proper data synchronization
    gr.HTML(f"""
    <script>
    // Global variables for blog data - synchronized with Python backend
    let blogsData = [];
    
    // Function to update blogs data from Python backend
    function updateBlogsData(newData) {{
        blogsData = newData;
    }}
    
    // Function to get the latest Python data
    function getLatestPythonData() {{
        // This function will be called to get the most recent data from Python
        // For now, we'll use the initial data, but in a real implementation,
        // this would make an AJAX call to get the latest data
        return [];
    }}
    
    // Function to sync JavaScript data with Python data
    function syncJavaScriptData() {{
        console.log('Syncing JavaScript data with Python data...');
        const latestData = getLatestPythonData();
        blogsData = latestData;
        console.log('JavaScript data synced:', blogsData);
    }}
    
    // Function to debug available blogs
    function debugAvailableBlogs() {{
        console.log('=== DEBUG: Available Blogs ===');
        console.log('Current JavaScript data:', blogsData);
        
        const latestData = getLatestPythonData();
        console.log('Latest Python data:', latestData);
        
        console.log('Blogs in current data:');
        blogsData.forEach((blog, index) => {{
            console.log(`  ${{index}}: ID=${{blog.id}}, Title="${{blog.title}}"`);
        }});
        
        console.log('Blogs in latest data:');
        latestData.forEach((blog, index) => {{
            console.log(`  ${{index}}: ID=${{blog.id}}, Title="${{blog.title}}"`);
        }});
        console.log('=== END DEBUG ===');
    }}
    
    // Function to find blog by ID - simplified using embedded data
    function findBlogById(blogId) {{
        console.log('🔍 Finding blog with ID:', blogId);
        
        // Find the blog card in the DOM
        const blogCard = document.querySelector(`[data-blog-id="${{blogId}}"]`);
        if (blogCard) {{
            console.log('✅ Found blog card in DOM:', blogCard);
            
            // Extract data from the card's data attributes
            const blog = {{
                id: blogCard.getAttribute('data-blog-id'),
                title: blogCard.getAttribute('data-blog-title'),
                content: blogCard.getAttribute('data-blog-content'),
                topic: blogCard.getAttribute('data-blog-topic'),
                language: blogCard.getAttribute('data-blog-language'),
                category: blogCard.getAttribute('data-blog-category'),
                created_at: blogCard.getAttribute('data-blog-created')
            }};
            
            console.log('📋 Extracted blog data from DOM:', blog);
            console.log('📄 Content length from DOM:', blog.content ? blog.content.length : 0);
            console.log('📄 Content preview from DOM:', blog.content ? blog.content.substring(0, 200) : 'null');
            
            return blog;
        }}
        
        console.log('❌ Blog card not found in DOM');
        console.log('🔍 Available blog cards:', document.querySelectorAll('.blog-card').length);
        console.log('🔍 Available blog IDs:', Array.from(document.querySelectorAll('.blog-card')).map(card => card.getAttribute('data-blog-id')));
        return null;
    }}
    
    // Function to get full blog content - simplified using embedded data
    function getFullBlogContent(blogId) {{
        console.log('📄 Getting full content for blog ID:', blogId);
        
        // Get the blog card from DOM
        const blogCard = document.querySelector(`[data-blog-id="${{blogId}}"]`);
        if (blogCard) {{
            const content = blogCard.getAttribute('data-blog-content');
            console.log('✅ Content found in DOM, length:', content ? content.length : 0);
            console.log('📄 Content preview from DOM:', content ? content.substring(0, 200) : 'null');
            return content;
        }}
        
        console.log('❌ Blog card not found in DOM');
        return '';
    }}
    
    function viewBlogModal(blogId) {{
        console.log('Opening view modal for blog ID:', blogId);
        
        // Get blog data from DOM
        const targetBlog = findBlogById(blogId);
        if (!targetBlog) {{
            console.log('Blog not found in DOM');
            alert('Blog not found. This might be a temporary issue. Please try refreshing the page.');
            return;
        }}
        
        console.log('Target blog found:', targetBlog);
        
        // Get the full content from DOM
        const fullContent = getFullBlogContent(blogId);
        console.log('Full content retrieved, length:', fullContent ? fullContent.length : 0);
        
        // Use the content we have
        const contentToDisplay = fullContent || targetBlog.content || '';
        console.log('Content to display, length:', contentToDisplay.length);
        
        // Format content for Medium/Substack style
        const formattedContent = formatContentForArticle(contentToDisplay);
        
        // Create modal content with mobile-friendly design
        const modalContent = `
            <div id="viewModal" class="modal" style="display: block;">
                <div class="modal-content" style="
                    width: 95%;
                    max-width: 900px;
                    max-height: 90vh;
                    margin: 2% auto;
                    border-radius: 16px;
                    overflow-y: auto;
                ">
                    <span class="close" onclick="closeModal('viewModal')" style="
                        position: absolute;
                        right: 20px;
                        top: 15px;
                        font-size: 28px;
                        font-weight: bold;
                        cursor: pointer;
                        z-index: 1001;
                        color: #aaa;
                    ">&times;</span>
                    
                    <!-- Article Header -->
                    <div class="article-header" style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px 20px;
                        border-radius: 16px 16px 0 0;
                        position: relative;
                    ">
                        <h1 class="article-title" style="
                            font-size: clamp(1.5rem, 4vw, 2.5rem);
                            font-weight: 800;
                            line-height: 1.2;
                            margin-bottom: 20px;
                            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        ">${{targetBlog.title}}</h1>
                        <div class="article-meta" style="
                            display: flex;
                            flex-wrap: wrap;
                            gap: 10px;
                            font-size: 0.9rem;
                            opacity: 0.9;
                        ">
                            <span>📌 ${{targetBlog.topic}}</span>
                            <span>🌍 ${{targetBlog.language}}</span>
                            <span>🏷️ ${{targetBlog.category}}</span>
                            <span>📅 ${{targetBlog.created_at}}</span>
                        </div>
                    </div>
                    
                    <!-- Article Content -->
                    <div class="article-content" style="
                        padding: 30px 20px;
                        line-height: 1.8;
                        font-size: 1.1rem;
                        color: #374151;
                        font-family: 'Georgia', serif;
                        min-height: 400px;
                        overflow-y: auto;
                        max-height: 60vh;
                    ">
                        ${{formattedContent}}
                    </div>
                    
                    <!-- Action Buttons -->
                    <div style="
                        padding: 20px;
                        border-top: 1px solid #e5e7eb;
                        text-align: center;
                        background: #f9fafb;
                        display: flex;
                        flex-wrap: wrap;
                        gap: 10px;
                        justify-content: center;
                    ">
                        <button onclick="editBlogModal('${{blogId}}')" style="
                            background: #f59e0b;
                            color: white;
                            border: none;
                            padding: 12px 20px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 0.9rem;
                            font-weight: 600;
                            min-width: 120px;
                        ">
                            ✏️ Edit Article
                        </button>
                        <button onclick="closeModal('viewModal')" style="
                            background: #6b7280;
                            color: white;
                            border: none;
                            padding: 12px 20px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 0.9rem;
                            font-weight: 600;
                            min-width: 120px;
                        ">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalContent);
    }}
    
    function editBlogModal(blogId) {{
        console.log('Opening edit modal for blog ID:', blogId);
        
        // Get blog data from DOM
        const targetBlog = findBlogById(blogId);
        if (!targetBlog) {{
            console.log('Blog not found in DOM');
            alert('Blog not found. This might be a temporary issue. Please try refreshing the page.');
            return;
        }}
        
        console.log('Target blog for edit found:', targetBlog);
        
        // Get the full content from DOM
        const fullContent = getFullBlogContent(blogId);
        console.log('Full content for edit, length:', fullContent ? fullContent.length : 0);
        
        const modalContent = `
            <div id="editModal" class="modal" style="display: block;">
                <div class="modal-content" style="
                    width: 95%;
                    max-width: 800px;
                    max-height: 95vh;
                    margin: 2% auto;
                    border-radius: 16px;
                    overflow-y: auto;
                ">
                    <span class="close" onclick="closeModal('editModal')" style="
                        position: absolute;
                        right: 20px;
                        top: 15px;
                        font-size: 28px;
                        font-weight: bold;
                        cursor: pointer;
                        z-index: 1001;
                        color: #aaa;
                    ">&times;</span>
                    <div style="padding: 30px 20px;">
                        <h2 style="color: #1f2937; margin-bottom: 20px; font-size: clamp(1.2rem, 3vw, 1.5rem);">Edit Blog</h2>
                        <form id="editForm">
                            <div style="margin-bottom: 16px;">
                                <label style="display: block; margin-bottom: 8px; font-weight: 600;">Title:</label>
                                <input type="text" id="editTitle" value="${{targetBlog.title}}" style="
                                    width: 100%;
                                    padding: 12px;
                                    border: 2px solid #e5e7eb;
                                    border-radius: 8px;
                                    font-size: 1rem;
                                    box-sizing: border-box;
                                ">
                            </div>
                            <div style="margin-bottom: 16px;">
                                <label style="display: block; margin-bottom: 8px; font-weight: 600;">Content:</label>
                                <textarea id="editContent" rows="20" style="
                                    width: 100%;
                                    padding: 12px;
                                    border: 2px solid #e5e7eb;
                                    border-radius: 8px;
                                    font-size: 1rem;
                                    resize: vertical;
                                    font-family: 'Georgia', serif;
                                    min-height: 400px;
                                    max-height: 50vh;
                                    overflow-y: auto;
                                    box-sizing: border-box;
                                ">${{fullContent || targetBlog.content || ''}}</textarea>
                            </div>
                            <div style="margin-bottom: 20px;">
                                <label style="display: block; margin-bottom: 8px; font-weight: 600;">Category:</label>
                                <select id="editCategory" style="
                                    width: 100%;
                                    padding: 12px;
                                    border: 2px solid #e5e7eb;
                                    border-radius: 8px;
                                    font-size: 1rem;
                                    box-sizing: border-box;
                                ">
                                    <option value="Technology" ${{targetBlog.category === 'Technology' ? 'selected' : ''}}>Technology</option>
                                    <option value="Artificial Intelligence" ${{targetBlog.category === 'Artificial Intelligence' ? 'selected' : ''}}>Artificial Intelligence</option>
                                    <option value="Machine Learning" ${{targetBlog.category === 'Machine Learning' ? 'selected' : ''}}>Machine Learning</option>
                                    <option value="Data Science" ${{targetBlog.category === 'Data Science' ? 'selected' : ''}}>Data Science</option>
                                    <option value="Software Development" ${{targetBlog.category === 'Software Development' ? 'selected' : ''}}>Software Development</option>
                                    <option value="Health & Wellness" ${{targetBlog.category === 'Health & Wellness' ? 'selected' : ''}}>Health & Wellness</option>
                                    <option value="Fitness" ${{targetBlog.category === 'Fitness' ? 'selected' : ''}}>Fitness</option>
                                    <option value="Nutrition" ${{targetBlog.category === 'Nutrition' ? 'selected' : ''}}>Nutrition</option>
                                    <option value="Mental Health" ${{targetBlog.category === 'Mental Health' ? 'selected' : ''}}>Mental Health</option>
                                </select>
                            </div>
                            <div style="text-align: center; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                                <button type="button" onclick="saveBlogEdit('${{blogId}}')" style="
                                    background: #10b981;
                                    color: white;
                                    border: none;
                                    padding: 12px 20px;
                                    border-radius: 8px;
                                    cursor: pointer;
                                    font-size: 0.9rem;
                                    font-weight: 600;
                                    min-width: 120px;
                                ">
                                    💾 Save Changes
                                </button>
                                <button type="button" onclick="closeModal('editModal')" style="
                                    background: #6b7280;
                                    color: white;
                                    border: none;
                                    padding: 12px 20px;
                                    border-radius: 8px;
                                    cursor: pointer;
                                    font-size: 0.9rem;
                                    font-weight: 600;
                                    min-width: 120px;
                                ">
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalContent);
    }}
    
    function deleteBlogConfirm(blogId) {{
        if (confirm('Are you sure you want to delete this blog? This action cannot be undone.')) {{
            // Remove from JavaScript data
            blogsData = blogsData.filter(blog => blog.id !== blogId);
            
            // Remove the card from the DOM
            const card = document.querySelector(`[data-blog-id="${{blogId}}"]`);
            if (card) {{
                card.remove();
            }}
            
            // Trigger Gradio delete function to update backend
            const deleteBtn = document.querySelector('#delete_btn');
            if (deleteBtn) {{
                // Set the blog ID and trigger delete
                const blogIdInput = document.querySelector('#blog_id_input');
                if (blogIdInput) {{
                    blogIdInput.value = blogId;
                }}
                deleteBtn.click();
            }}
            
            // Show success message
            alert('Blog deleted successfully!');
        }}
    }}
    
    function closeModal(modalId) {{
        const modal = document.getElementById(modalId);
        if (modal) {{
            modal.remove();
        }}
    }}
    
    function saveBlogEdit(blogId) {{
        const title = document.getElementById('editTitle').value;
        const content = document.getElementById('editContent').value;
        const category = document.getElementById('editCategory').value;
        
        // Close modal first
        closeModal('editModal');
        
                 // Update the blog card in the DOM immediately
         const blogCard = document.querySelector(`[data-blog-id="${{blogId}}"]`);
         if (blogCard) {{
             // Update the title in the card
             const titleElement = blogCard.querySelector('h3');
             if (titleElement) {{
                 titleElement.textContent = title;
             }}
             
             // Update the category badge
             const categoryBadge = blogCard.querySelector('div[style*="position: absolute"][style*="top: 16px"][style*="right: 16px"]');
             if (categoryBadge) {{
                 categoryBadge.textContent = category;
                 
                 // Update category badge color
                 const categoryColors = {{
                     "Technology": "#3B82F6",
                     "Artificial Intelligence": "#8B5CF6", 
                     "Machine Learning": "#06B6D4",
                     "Data Science": "#10B981",
                     "Software Development": "#F59E0B",
                     "Health & Wellness": "#EC4899",
                     "Fitness": "#14B8A6",
                     "Nutrition": "#F97316",
                     "Mental Health": "#6366F1"
                 }};
                 
                 const newColor = categoryColors[category] || "#3B82F6";
                 categoryBadge.style.background = newColor;
             }}
             
             // Update the content preview
             const contentPreview = blogCard.querySelector('p[style*="color: #4b5563"]');
             if (contentPreview) {{
                 const preview = content.length > 200 ? content.substring(0, 200) : content;
                 contentPreview.textContent = preview;
             }}
             
             // Update the data attributes for future reference
             blogCard.setAttribute('data-blog-title', title);
             blogCard.setAttribute('data-blog-content', content);
             blogCard.setAttribute('data-blog-category', category);
             
             // Update the JavaScript data array to reflect the changes
             const blogIndex = blogsData.findIndex(blog => blog.id === blogId);
             if (blogIndex !== -1) {{
                 blogsData[blogIndex].title = title;
                 blogsData[blogIndex].content = content;
                 blogsData[blogIndex].category = category;
             }}
             
             // Check if the current category filter should hide this blog
             const currentCategoryDropdown = document.querySelector('#category_dropdown select');
             if (currentCategoryDropdown) {{
                 const selectedCategory = currentCategoryDropdown.value;
                 
                 // If we're filtering by a specific category and the blog no longer matches, hide it
                 if (selectedCategory !== 'All' && selectedCategory !== category) {{
                     blogCard.style.display = 'none';
                     console.log(`🔄 Blog hidden from ${selectedCategory} filter (now categorized as ${category})`);
                 }} else if (selectedCategory === 'All' || selectedCategory === category) {{
                     blogCard.style.display = 'block';
                     console.log(`✅ Blog visible in ${selectedCategory} filter`);
                 }}
             }}
             
             console.log('✅ Blog card updated in DOM and category filtering applied');
         }}
         
         // Trigger Gradio update function to update backend state
         const updateBlogIdInput = document.querySelector('#update_blog_id_input input');
         const updateTitleInput = document.querySelector('#update_title_input input');
         const updateContentInput = document.querySelector('#update_content_input input');
         const updateCategoryInput = document.querySelector('#update_category_input input');
         const updateBtn = document.querySelector('#update_btn');
         
         if (updateBlogIdInput && updateTitleInput && updateContentInput && updateCategoryInput && updateBtn) {{
             // Set the values
             updateBlogIdInput.value = blogId;
             updateTitleInput.value = title;
             updateContentInput.value = content;
             updateCategoryInput.value = category;
             
             // Trigger change events
             [updateBlogIdInput, updateTitleInput, updateContentInput, updateCategoryInput].forEach(input => {{
                 input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                 input.dispatchEvent(new Event('change', {{ bubbles: true }}));
             }});
             
             // Trigger the update
             updateBtn.click();
             
             console.log('✅ Gradio update triggered');
             
             // Show success message
             alert('Blog updated successfully!');
         }} else {{
             console.error('Update components not found');
             alert('Update failed. Please try refreshing the page.');
         }}
    }}
    
    // Function to format content for Medium/Substack style
    function formatContentForArticle(content) {{
        console.log('Formatting content, length:', content ? content.length : 0);
        console.log('Content preview:', content ? content.substring(0, 100) : 'null');
        
        if (!content || content.trim() === '') {{
            console.log('No content provided, showing error message');
            return '<p style="color: #ef4444; font-style: italic;">⚠️ Content not available. Please try refreshing the page or contact support if the issue persists.</p>';
        }}
        
        // Convert markdown-like formatting to HTML
        let formatted = content
            // Headers
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            // Bold
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Italic
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Lists
            .replace(/^\\* (.*$)/gim, '<li>$1</li>')
            .replace(/^- (.*$)/gim, '<li>$1</li>')
            // Line breaks
            .replace(/\\n\\n/g, '</p><p>')
            .replace(/\\n/g, '<br>');
        
        // Wrap in paragraphs
        formatted = '<p>' + formatted + '</p>';
        
        // Fix list formatting
        formatted = formatted.replace(/<p><li>/g, '<ul><li>');
        formatted = formatted.replace(/<\\/li><\\/p>/g, '</li></ul>');
        
        console.log('Formatted content length:', formatted.length);
        return formatted;
    }}
    
    // Close modal when clicking outside
    window.onclick = function(event) {{
        if (event.target.classList.contains('modal')) {{
            event.target.remove();
        }}
    }}
    
    // Auto-refresh blogs data after page loads
    window.addEventListener('load', function() {{
        setTimeout(() => {{
            syncJavaScriptData();
            debugAvailableBlogs();
        }}, 1000);
    }});
    
    // Refresh blogs data when new blogs are generated
    function refreshBlogsData() {{
        setTimeout(() => {{
            syncJavaScriptData();
            debugAvailableBlogs();
        }}, 500);
    }}
    </script>
    """)

# Launch the app
demo.launch()