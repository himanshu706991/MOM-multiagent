from typing import Dict, Any
from utils.file_handler import ingest_any
from utils.llm_config import get_llm_adapter

def extract_content(file_path: str) -> Dict[str, Any]:
    """Extract raw text and structured info using the configured LLM adapter."""
    text = ingest_any(file_path)
    llm = get_llm_adapter()
    prompt = f"""You are an information extraction agent for meeting transcripts.
From the text below, return strict JSON with keys:
- participants: [ {{ \"name\": \"...\", \"role\": \"...\" }} ]
- meeting_title: string
- meeting_datetime: string
- agenda: [string]
- key_points: [string]
- decisions: [string]
- risks: [string]
- action_items: [ {{ \"description\": \"...\", \"owner\": \"...\", \"due_date\": \"...\" }} ]

Return only JSON.
TEXT:
{text}
""".format(text=text[:150000])
    try:
        raw = llm.generate(prompt)
    except Exception as e:
        # Fallback: return simple fields
        return {"raw_text": text, "error": str(e)}
    # Best-effort parse
    try:
        import json, re
        s = re.sub(r"```json|```", "", raw)
        data = json.loads(s)
    except Exception:
        data = {"raw_text": text, "llm_response": raw}
    return data
