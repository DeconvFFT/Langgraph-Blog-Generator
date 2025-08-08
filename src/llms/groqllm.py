from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv


class GroqLLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        """
        Initialize and return a ChatGroq LLM instance
        
        Returns:
            ChatGroq: Configured LLM instance
            
        Raises:
            ValueError: If API key is invalid or LLM initialization fails
        """
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            self.groq_api_key = input('Please enter your groq API key: ')
            if not self.groq_api_key.strip():
                raise ValueError("❌ Groq API key cannot be empty")
        
        # Set environment variable for the API key
        os.environ['GROQ_API_KEY'] = self.groq_api_key
        
        # Initialize and validate the LLM
        try:
            llm = ChatGroq(
                model='llama3-8b-8192',  # Using a more reliable model
                temperature=0.7,
                max_tokens=2048
            )
            # Test the LLM with a simple call to validate the API key
            test_response = llm.invoke("Hello")
            if not test_response:
                raise ValueError("LLM test call failed")
            return llm
        except Exception as e:
            raise ValueError(f'❌ Error initializing Groq LLM: {str(e)}')
            
        