from typing import Dict, Any
from utils.llm_config import get_llm_adapter
import json

def critique_summary(mom_draft: str) -> Dict[str, Any]:
    llm = get_llm_adapter()
    prompt = f"""You are a critical reviewer. Read the MoM draft and identify missing details, ambiguities, tone/style issues, and any inconsistencies.
Return JSON with keys:
- missing_info: [string]
- suggested_edits: [string]
- tone_issues: [string]
- formatting_changes: [string]
Return only JSON.

MOM_DRAFT:
{mom_draft}
"""
    raw = llm.generate(prompt)
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}
