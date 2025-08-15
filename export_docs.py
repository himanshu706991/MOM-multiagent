import os
from docx import Document
from docx.shared import Pt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUTPUT_DIR_BASE = os.getenv('OUTPUT_DIR','/mnt/data/output')

def export_to_docx_pdf(text: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    docx_path = os.path.join(output_dir, 'Minutes_of_Meeting_FINAL.docx')
    pdf_path = os.path.join(output_dir, 'Minutes_of_Meeting_FINAL.pdf')

    # DOCX
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(docx_path)

    # PDF (simple)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin
    for line in text.splitlines():
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line[:110])
        y -= 14
    c.save()

    return docx_path, pdf_path
