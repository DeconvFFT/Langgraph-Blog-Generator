from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv


class GroqLLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if self.groq_api_key:
            os.environ['GROQ_API_KEY'] = self.groq_api_key
        else:
            self.groq_api_key = input('Please enter your groq API key!!')
        
        ## check validity of groq API KEY
        try:
            llm = ChatGroq(model = 'qwen/qwen3-32b', api_key=self.groq_api_key)
            return llm
        except Exception as e:
            raise ValueError(f'‼️ Error occured with exception: {e}')
        
            
        