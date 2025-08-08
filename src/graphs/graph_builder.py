from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        
    def _should_continue_to_content(self, state: BlogState) -> str:
        """
        Conditional edge function to determine if we should proceed to content generation
        
        Args:
            state (BlogState): Current state
            
        Returns:
            str: Next node name or "END"
        """
        if state.error:
            print(f"🛑 Stopping after title generation due to error: {state.error}")
            return "END"
        
        if not state.topic:
            print("🛑 Stopping: No topic available for content generation")
            return "END"
            
        if not state.blog or not state.blog.title:
            print("⚠️ No title generated, but proceeding with content generation")
        
        return "content_generation"
    
    def _should_end_graph(self, state: BlogState) -> str:
        """
        Final conditional edge to determine if graph should end
        
        Args:
            state (BlogState): Current state
            
        Returns:
            str: "END"
        """
        if state.error:
            print(f"🛑 Graph completed with error: {state.error}")
        else:
            print("✅ Blog generation completed successfully!")
            if state.blog and state.blog.title:
                print(f"📝 Title: {state.blog.title}")
            if state.blog and state.blog.content:
                print(f"📄 Content: {len(state.blog.content)} characters generated")
        
        return "END"
        
    def build_topic_graph(self):
        """
        Build a robust graph to generate blogs based on a topic with error handling
        """
        # Initialize blog node with retry configuration
        self.blog_node_obj = BlogNode(self.llm, max_retries=3)
        
        # Add nodes
        self.graph.add_node('title_creation', self.blog_node_obj.title_creation)
        self.graph.add_node('content_generation', self.blog_node_obj.content_generation)
        
        # Add conditional edges for better flow control
        self.graph.add_edge(START, 'title_creation')
        
        # Conditional edge from title_creation
        self.graph.add_conditional_edges(
            'title_creation',
            self._should_continue_to_content,
            {
                'content_generation': 'content_generation',
                'END': END
            }
        )
        
        # Conditional edge from content_generation
        self.graph.add_conditional_edges(
            'content_generation',
            self._should_end_graph,
            {
                'END': END
            }
        )

        return self.graph
    
    def setup_graph(self, usecase: str):
        """
        Setup and compile a graph based on the specified use case
        
        Args:
            usecase (str): The use case for graph setup ('topic', etc.)
            
        Returns:
            Compiled graph instance
            
        Raises:
            ValueError: If invalid use case is provided
        """
        if usecase == 'topic':
            return self.build_topic_graph().compile()
        else:
            raise ValueError(f"❌ Unsupported use case: {usecase}. Supported cases: 'topic'")