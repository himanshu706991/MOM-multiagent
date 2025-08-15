import os
from typing import Dict, Any

class LLMAdapter:
    def __init__(self, backend: str, model_overrides: Dict[str,str]|None=None):
        self.backend = backend
        self.model_overrides = model_overrides or {}

    def generate(self, prompt: str) -> str:
        # This is a thin adapter. Replace with actual client calls in your env.
        if self.backend == 'openai':
            try:
                import openai
                model = self.model_overrides.get('openai', os.getenv('OPENAI_MODEL'))
                res = openai.ChatCompletion.create(model=model, messages=[{'role':'user','content':prompt}], temperature=0.2)
                return res.choices[0].message.content
            except Exception as e:
                return f'OPENAI_ERROR: {e}'
        elif self.backend == 'ollama':
            try:
                from ollama import Client as OllamaClient
                client = OllamaClient(host=os.getenv('OLLAMA_HOST','http://localhost:11434'))
                model = self.model_overrides.get('ollama', os.getenv('OLLAMA_MODEL'))
                out = client.generate(model=model, prompt=prompt, stream=False)
                return out.get('response','')
            except Exception as e:
                return f'OLLAMA_ERROR: {e}'
        elif self.backend == 'hf':
            try:
                from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
                model_name = self.model_overrides.get('hf', os.getenv('HF_MODEL'))
                tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
                model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')
                pipe = pipeline('text-generation', model=model, tokenizer=tok, max_new_tokens=512)
                out = pipe(prompt)[0]['generated_text']
                return out[len(prompt):] if out.startswith(prompt) else out
            except Exception as e:
                return f'HF_ERROR: {e}'
        else:
            return 'NO_LLM_CONFIGURED'

def get_llm_adapter() -> LLMAdapter:
    backend = os.getenv('LLM_BACKEND','ollama')
    return LLMAdapter(backend)

def get_final_llm_adapter() -> LLMAdapter:
    backend = os.getenv('LLM_FINAL_BACKEND', 'same')
    if backend == 'same':
        backend = os.getenv('LLM_BACKEND','ollama')
    return LLMAdapter(backend)
