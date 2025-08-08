from typing import TypedDict, Optional
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: Optional[str] = Field(default=None, description='The title of the blog post')
    content: Optional[str] = Field(default=None, description='The main content of the blog post')
    
class BlogState(BaseModel):
    topic: Optional[str] = Field(default=None, description='Topic of the blog')
    blog: Optional[Blog] = Field(default_factory=Blog, description='Blog content structure')
    current_language: str = Field(default='English', description='Language in which the blog should be written')
    error: Optional[str] = Field(default=None, description='Error message if any step fails')
    retry_count: int = Field(default=0, description='Number of retry attempts')