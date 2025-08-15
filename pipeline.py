from agents.extract_agent import extract_content
from agents.summarize_agent import summarize_content
from agents.critique_agent import critique_summary
from agents.aggregate_agent import aggregate_content
from agents.polish_agent import polish_final
from utils.export_docs import export_to_docx_pdf
import os

def run_pipeline(file_path: str, session_id: str):
    # session-specific output
    output_dir = os.path.join(os.getenv('OUTPUT_DIR','/mnt/data/output'), session_id)
    os.makedirs(output_dir, exist_ok=True)

    extracted = extract_content(file_path)
    mom_draft = summarize_content(extracted) if isinstance(extracted, dict) else summarize_content({'raw': extracted})
    critique = critique_summary(mom_draft)
    aggregated = aggregate_content(mom_draft, critique)
    polished = polish_final(aggregated)

    docx_path, pdf_path = export_to_docx_pdf(polished, output_dir)
    return docx_path, pdf_path
