from pypdf import PdfReader
from pathlib import Path

class PDFLoader:
    """Used only for loading PDF files"""
    def __int__(self, pdf_path: Path):
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")
        self.pdf_path = pdf_path

    def load(self) -> str:
        """Reads the PDF file and returns its content as a string."""
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:  
            text += page.extract_text() + "\n"
        return text