from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState

class GraphBuilder:
    def _init__(self, llm):
        self.llm = llm
        self.graph = StateGraph()