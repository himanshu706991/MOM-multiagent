import fitz
from docx import Document

def extract_text_from_pdf(path: str) -> str:
    text = []
    with fitz.open(path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text).strip()

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def ingest_any(path: str) -> str:
    p = path.lower()
    if p.endswith('.pdf'):
        return extract_text_from_pdf(path)
    elif p.endswith('.docx'):
        return extract_text_from_docx(path)
    elif p.endswith('.txt'):
        return extract_text_from_txt(path)
    else:
        raise ValueError('Unsupported file type. Use PDF, DOCX, or TXT.')
