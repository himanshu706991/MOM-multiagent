from typing import Dict, Any
from utils.llm_config import get_llm_adapter
import json

def summarize_content(extracted: Dict[str, Any]) -> str:
    llm = get_llm_adapter()
    prompt = f"""You are a summarization agent. Convert this extracted JSON into a clear, detailed Minutes of Meeting (MoM) with sections:
- Meeting Title
- Date/Time
- Participants (Name - Role)
- Agenda
- Summary (bulleted, but rich and specific)
- Decisions
- Action Items (Owner - Description - Due Date)
- Risks / Open Questions
Return a client-ready MoM as plain text.

EXTRACTED_JSON:
{json.dumps(extracted, ensure_ascii=False)}
"""
    return llm.generate(prompt)
