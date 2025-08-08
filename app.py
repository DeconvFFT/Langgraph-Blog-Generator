import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Blog Generator API",
    description="AI-powered blog generation service",
    version="1.0.0"
)

# Setup LangSmith if needed (optional)
langsmith_key = os.getenv('LANGSMITH_API_KEY')
if langsmith_key: 
    os.environ['LANGSMITH_API_KEY'] = langsmith_key


class BlogRequest(BaseModel):
    """Request model for blog creation"""
    topic: Optional[str] = None
    language: Optional[str] = "English"


class BlogResponse(BaseModel):
    """Response model for blog creation"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    message: Optional[str] = None


@app.post('/blogs', response_model=BlogResponse)
async def create_blogs(blog_request: BlogRequest):
    """
    Create a blog post based on the provided topic
    
    Args:
        blog_request (BlogRequest): Request containing topic and language
        
    Returns:
        BlogResponse: Generated blog content or error message
    """
    try:
        logger.info(f"Received blog creation request for topic: {blog_request.topic}")
        
        # Initialize LLM
        try:
            groqllm = GroqLLM()
            llm = groqllm.get_llm()
            logger.info("✅ LLM initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLM: {str(e)}")
            return BlogResponse(
                success=False,
                error=f"LLM initialization failed: {str(e)}",
                message="Please check your Groq API key configuration"
            )
        
        # Initialize graph
        try:
            graph_builder = GraphBuilder(llm)
            graph = graph_builder.setup_graph(usecase='topic')
            logger.info("✅ Graph initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize graph: {str(e)}")
            return BlogResponse(
                success=False,
                error=f"Graph initialization failed: {str(e)}",
                message="Internal server error during graph setup"
            )
        
        # Prepare initial state
        try:
            initial_state = BlogState(
                topic=blog_request.topic,
                current_language=blog_request.language or "English"
            )
        except Exception as e:
            logger.error(f"❌ Failed to create initial state: {str(e)}")
            return BlogResponse(
                success=False,
                error=f"State initialization failed: {str(e)}",
                message="Internal error during state preparation"
            )
        
        # Execute graph
        try:
            logger.info("🔄 Starting blog generation...")
            result = graph.invoke(initial_state)
            logger.info("✅ Blog generation completed")
            
            # Check if generation was successful
            if result.get('error'):
                return BlogResponse(
                    success=False,
                    error=result['error'],
                    message="Blog generation failed"
                )
            
            # Extract blog content
            blog_content = result.get('blog', {})
            if not blog_content or (not blog_content.get('title') and not blog_content.get('content')):
                return BlogResponse(
                    success=False,
                    error="No content generated",
                    message="The system was unable to generate blog content"
                )
            
            return BlogResponse(
                success=True,
                data={
                    'topic': result.get('topic', blog_request.topic),
                    'language': result.get('current_language', blog_request.language or "English"),
                    'blog': blog_content
                },
                message="Blog generated successfully"
            )
            
        except Exception as e:
            logger.error(f"❌ Graph execution failed: {str(e)}")
            return BlogResponse(
                success=False,
                error=f"Blog generation failed: {str(e)}",
                message="An error occurred during blog generation"
            )
            
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Blog Generator API"}


@app.get('/')
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Blog Generator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /blogs": "Generate a blog post",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }


if __name__ == '__main__':
    uvicorn.run(
        "app:app", 
        host='0.0.0.0', 
        port=8000, 
        reload=True,
        log_level="info"
    )