from pathlib import Path
from pypdf import PdfReader, PdfWriter

class PDFHandler:
    @staticmethod 
    def prepare_pdf(pdf_path : str | Path, password: str | None = None):
        
        pdf_path = Path(pdf_path)
        
        reader = PdfReader(pdf_path)
        
        if not reader.is_encrypted:
            return pdf_path
        
        if password is None:
            raise ValueError("Password required")
        
        if reader.decrypt(password) == 0:
            raise ValueError("Incorrect Password.")
        
        output = Path("data/decrypted") / pdf_path.name
        
        output.parent.mkdir(parents=True, exist_ok=True)
        
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output, 'wb') as f:
            writer.write(f)
            
        return output
    
