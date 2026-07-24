import os
from dotenv import load_dotenv

load_dotenv()

class LlamaParserClinet:
    
    BASE_URL="https://api.cloud.llamaindex.ai"
    
    def __init__(self):
        self.api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "LLAMA key not found!"
            )
        
        self.headers = {
            "Authorization" : f"Bearer {self.api_key}"
        }