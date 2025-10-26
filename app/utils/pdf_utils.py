from io import BytesIO
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        return extract_text(BytesIO(file_bytes))
    except Exception:
        return ""
