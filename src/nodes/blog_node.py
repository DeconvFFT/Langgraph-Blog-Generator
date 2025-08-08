from langchain_core.messages import HumanMessage, SystemMessage
from src.states.blogstate import BlogState, Blog
import time

class BlogNode:
    """
    Class representing Blog Node with robust error handling and retry logic
    """
    def __init__(self, llm, max_retries=3):
        self.llm = llm
        self.max_retries = max_retries
        
    def _get_user_input(self, prompt_message: str, error_context: str = "operation") -> str:
        """
        Helper method to get user input with proper error handling
        
        Args:
            prompt_message: Message to display to user
            error_context: Context for error messages
            
        Returns:
            str: User input or raises exception for cancellation
        """
        while True:
            try:
                user_input = input(prompt_message).strip()
                if user_input:
                    return user_input
                print(f"Input cannot be empty. Please try again.")
            except KeyboardInterrupt:
                raise Exception(f"{error_context} cancelled by user")
            except EOFError:
                raise Exception(f"No input provided for {error_context}")
    
    def _handle_llm_error(self, error: Exception, context: str, state: BlogState) -> dict:
        """
        Handle LLM errors with retry logic and user intervention
        
        Args:
            error: The exception that occurred
            context: Context of where the error occurred
            state: Current blog state
            
        Returns:
            dict: Error response or user decision
        """
        print(f"❌ LLM Error in {context}: {str(error)}")
        
        if state.retry_count >= self.max_retries:
            print(f"🔄 Maximum retries ({self.max_retries}) reached for {context}")
            try:
                decision = self._get_user_input(
                    "Options: (r)etry, (s)kip this step, (c)ancel: ",
                    f"{context} error handling"
                ).lower()
                
                if decision == 'r':
                    return {'retry': True}
                elif decision == 's':
                    return {'skip': True}
                else:
                    return {'error': f"{context} cancelled after max retries"}
            except Exception as e:
                return {'error': str(e)}
        else:
            print(f"🔄 Retrying {context} (attempt {state.retry_count + 1}/{self.max_retries})")
            return {'retry': True}
    
    def title_creation(self, state: BlogState):
        """
        Create title for the blog with robust error handling
        
        Args:
            state (BlogState): Current state of the blog generation graph
        """
        try:
            # Reset error state
            state.error = None
            
            # Ensure blog object exists
            if not state.blog:
                state.blog = Blog()
            
            # Check if topic exists and is not empty
            topic = state.topic
            if not topic or not topic.strip():
                print(f'⚠️ Missing or empty topic!')
                try:
                    topic = self._get_user_input(
                        "Please provide a topic for the blog: ",
                        "topic input"
                    )
                    state.topic = topic
                except Exception as e:
                    return {'error': str(e)}
            
            # Generate the title with retry logic
            while state.retry_count < self.max_retries:
                try:
                    prompt = """
                        You are an expert blog content writer. Generate ONLY a creative and SEO-friendly 
                        title for a blog post about: {topic}
                        
                        Requirements:
                        - Return only the title text, no additional formatting
                        - Make it engaging and clickable
                        - Keep it under 60 characters for SEO
                    """
                    system_message = prompt.format(topic=topic.strip())
                    response = self.llm.invoke(system_message)
                    
                    # Validate response
                    if not response or not response.content or not response.content.strip():
                        raise Exception("LLM returned empty response")
                    
                    title = response.content.strip()
                    
                    # Update state
                    state.blog.title = title
                    state.retry_count = 0  # Reset retry count on success
                    
                    print(f"✅ Title generated: {title}")
                    return {'blog': {'title': title}}
                    
                except Exception as e:
                    state.retry_count += 1
                    error_response = self._handle_llm_error(e, "title generation", state)
                    
                    if 'error' in error_response:
                        return error_response
                    elif 'skip' in error_response:
                        print("⏭️ Skipping title generation")
                        state.blog.title = f"Blog about {topic}"  # Fallback title
                        return {'blog': {'title': state.blog.title}}
                    elif 'retry' in error_response:
                        time.sleep(1)  # Brief pause before retry
                        continue
            
            # If we get here, max retries exceeded
            return {'error': 'Title generation failed after maximum retries'}
            
        except Exception as e:
            return {'error': f'Unexpected error in title creation: {str(e)}'}
    
    def content_generation(self, state: BlogState):
        """
        Generate blog content with robust error handling and state validation
        
        Args:
            state (BlogState): Current state of the blog generation graph
        """
        try:
            # Reset error state
            state.error = None
            
            # Validate prerequisites
            if not state.topic or not state.topic.strip():
                try:
                    topic = self._get_user_input(
                        "Please provide a topic for the blog content: ",
                        "topic input for content"
                    )
                    state.topic = topic
                except Exception as e:
                    return {'error': str(e)}
            
            # Ensure blog object and title exist
            if not state.blog:
                state.blog = Blog()
            
            if not state.blog.title:
                print("⚠️ No title found, using topic as fallback")
                state.blog.title = f"Blog about {state.topic}"
            
            # Generate content with retry logic
            while state.retry_count < self.max_retries:
                try:
                    system_prompt = """
                        You are an expert blog writer specializing in creating engaging, emoji-enhanced content. 
                        Create a compelling blog post about: {topic}
                        
                        Requirements:
                        - Write in {language} language
                        - Add relevant emojis throughout the content to make it more engaging and fun to read
                        - Use proper Markdown formatting with headers (##, ###), bullet points, and emphasis
                        - Include a compelling introduction that hooks the reader with emojis
                        - Structure the content with clear sections and subheadings
                        - Add emojis to section headers and key points
                        - Make the content informative yet entertaining
                        - Include practical examples or tips where relevant
                        - Use bullet points and numbered lists with emojis
                        - End with a thought-provoking conclusion
                        - Use emojis strategically to enhance readability and engagement
                        - Minimum 1200 words
                        - Do NOT include the title - only the content
                        
                        Make sure the content flows naturally and feels like a high-quality Medium or Substack article!
                        The goal is to make readers enjoy the content while learning something valuable.
                    """
                    system_message = system_prompt.format(
                        topic=state.topic.strip(),
                        language=state.current_language or "English"
                    )
                    response = self.llm.invoke(system_message)
                    
                    # Validate response
                    if not response or not response.content or not response.content.strip():
                        raise Exception("LLM returned empty response")
                    
                    content = response.content.strip()
                    
                    # Update state
                    state.blog.content = content
                    state.retry_count = 0  # Reset retry count on success
                    
                    print(f"✅ Content generated successfully ({len(content)} characters)")
                    return {
                        'blog': {
                            'title': state.blog.title,
                            'content': content
                        }
                    }
                    
                except Exception as e:
                    state.retry_count += 1
                    error_response = self._handle_llm_error(e, "content generation", state)
                    
                    if 'error' in error_response:
                        return error_response
                    elif 'skip' in error_response:
                        print("⏭️ Skipping content generation")
                        return {
                            'blog': {
                                'title': state.blog.title,
                                'content': f"Content about {state.topic} could not be generated."
                            }
                        }
                    elif 'retry' in error_response:
                        time.sleep(1)  # Brief pause before retry
                        continue
            
            # If we get here, max retries exceeded
            return {'error': 'Content generation failed after maximum retries'}
            
        except Exception as e:
            return {'error': f'Unexpected error in content generation: {str(e)}'}
    
    def should_continue(self, state: BlogState) -> str:
        """
        Conditional edge function to determine if the graph should continue
        
        Args:
            state (BlogState): Current state
            
        Returns:
            str: Next node name or "END"
        """
        if state.error:
            print(f"🛑 Graph stopped due to error: {state.error}")
            return "END"
        
        # Check if we have minimum requirements to continue
        if not state.topic:
            print("🛑 Graph stopped: No topic available")
            return "END"
            
        return "CONTINUE"
        
    def translation(self, state: BlogState):
        """
        Translate the content to specified language

        Args:
            state (BlogState): Current state of the content translation graph
        """
        try:
            # Reset error state
            state.error = None
            
            # Validate prerequisites
            if not state.blog or not state.blog.content:
                return {'error': 'No content available for translation'}
            
            if not state.current_language:
                return {'error': 'No target language specified'}
            
            # Generate translation with retry logic
            while state.retry_count < self.max_retries:
                try:
                    translation_prompt = """
                        Translate the following blog content into {current_language}.
                        
                        Requirements:
                        - Maintain the original tone, style, and formatting
                        - Adapt cultural references and idioms appropriately
                        - Preserve all Markdown formatting
                        - Keep the same structure and flow
                        
                        ORIGINAL CONTENT:
                        {blog_content}
                        
                        TRANSLATED CONTENT:
                    """
                    
                    system_message = translation_prompt.format(
                        current_language=state.current_language,
                        blog_content=state.blog.content
                    )
                    
                    response = self.llm.invoke(system_message)
                    
                    # Validate response
                    if not response or not response.content or not response.content.strip():
                        raise Exception("LLM returned empty translation")
                    
                    translated_content = response.content.strip()
                    
                    # Update state
                    state.blog.content = translated_content
                    state.retry_count = 0  # Reset retry count on success
                    
                    print(f"✅ Content translated to {state.current_language} successfully")
                    return {
                        'blog': {
                            'title': state.blog.title,
                            'content': translated_content
                        },
                        'current_language': state.current_language
                    }
                    
                except Exception as e:
                    state.retry_count += 1
                    error_response = self._handle_llm_error(e, f"translation to {state.current_language}", state)
                    
                    if 'error' in error_response:
                        return error_response
                    elif 'skip' in error_response:
                        print(f"⏭️ Skipping translation to {state.current_language}")
                        return {
                            'blog': {
                                'title': state.blog.title,
                                'content': f"Translation to {state.current_language} could not be completed."
                            },
                            'current_language': state.current_language
                        }
                    elif 'retry' in error_response:
                        time.sleep(1)  # Brief pause before retry
                        continue
            
            # If we get here, max retries exceeded
            return {'error': f'Translation to {state.current_language} failed after maximum retries'}
            
        except Exception as e:
            return {'error': f'Unexpected error in translation: {str(e)}'}

    def route(self, state: BlogState):
        """
        Route function to pass through the current language
        
        Args:
            state (BlogState): Current state
            
        Returns:
            dict: State with current language
        """
        return {'current_language': state.current_language}
    
    def route_decision(self, state: BlogState) -> str:
        """
        Route the content to their respective translation function

        Args:
            state (BlogState): Current state of the content translation graph
            
        Returns:
            str: Target language for translation
        """
        if not state.current_language:
            return "END"
        
        language = state.current_language.lower()
        
        if language in ['hindi', 'spanish']:
            return language
        else:
            # For unsupported languages, end the graph
            print(f"⚠️ Unsupported language: {language}. Ending graph.")
            return "END"