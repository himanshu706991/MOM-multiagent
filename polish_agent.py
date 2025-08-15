from typing import Dict, Any
from utils.llm_config import get_final_llm_adapter
def polish_final(text: str) -> str:
    llm = get_final_llm_adapter()
    prompt = f"""You are a senior communications editor. Lightly polish the following Minutes of Meeting (MoM) for clarity, professional tone, grammar, and formatting without changing factual content. Return the final MoM as plain text.

MOM_FINAL_DRAFT:
{text}
"""
    return llm.generate(prompt)
