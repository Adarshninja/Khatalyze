from pathlib import Path
from llama_cloud import LlamaCloud 
# from llama_cloud import AsyncLlamaCloud
from dotenv import load_dotenv
import os

load_dotenv()

class StatementParser:
    
    def __init__(self):
        self.client = LlamaCloud(
            api_key=os.getenv("LLAMA_CLOUD_API_KEY")
        )
        
    def parse(self, pdf_path):
        
        file_obj = self.client.files.create(
            file=str(pdf_path),
            purpose='parse'
        )
        
        result = self.client.parsing.parse(
            file_id=file_obj.id,
            tier='agentic',
            version='latest',
            expand=['markdown_full', 'text_full']
        )
        
        output_dir = Path("data/parsed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        md_file = output_dir / f"{Path(pdf_path).stem}.md"
        txt_file = output_dir / f"{Path(pdf_path).stem}.txt"
        
        md_file.write_text(
            result.markdown_full or "",
            encoding='utf-8'
            )
        txt_file.write_text(
            result.text_full or "",
            encoding='utf-8'
            )
        
        return {
            "markdown" : md_file,
            "text" : txt_file
        }
        
