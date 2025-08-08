from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str = Field(description='The title of the blog post')
    content:str = Field(description='The main content of the blog post')
    
class BlogState(BaseModel):
    topic:str = Field('Topic of the blog')
    blog: Blog
    current_language: str = Field('Language in which the blog should be written')