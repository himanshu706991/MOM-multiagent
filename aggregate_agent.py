from typing import Dict, Any
from utils.llm_config import get_llm_adapter
import json

def aggregate_content(mom_draft: str, critique: Dict[str, Any]) -> str:
    llm = get_llm_adapter()
    prompt = f"""You are a senior editor. Merge the critique into the MoM draft and produce the final detailed, polished MoM with consistent formatting.
Apply suggested edits and fill reasonable gaps if evidence exists in the transcript.
Return final MoM as plain text.

MOM_DRAFT:
{mom_draft}

CRITIQUE_JSON:
{json.dumps(critique, ensure_ascii=False)}
"""
    return llm.generate(prompt)
