# Minutes of Meeting (MoM) Generator - mom_app

This project provides a multi-agent MoM generator with a Streamlit UI and configurable LLM backends (Ollama, HuggingFace, OpenAI).

## Structure
- agents/: agents for extract, summarize, critique, aggregate, polish
- utils/: file handling, LLM config, export helpers
- pipeline.py: orchestrates the 5-step flow
- app.py: Streamlit UI (multi-user via session-id)
- requirements.txt, Dockerfile, .env

## How to run (local)
1. Set environment variables in `.env` or export in shell.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Streamlit UI:
   ```bash
   streamlit run app.py
   ```
4. Upload a PDF/DOCX/TXT in the UI. Output files are saved at `/mnt/data/output/<session_id>/`.

## Docker
Build and run container:
```bash
docker build -t mom_app .
docker run -p 8501:8501 -v $(pwd)/output:/mnt/data/output --env-file .env mom_app
```

## Notes
- This code includes simple LLM adapter wrappers. You may need to configure and install model runtimes (Ollama server, HF models) before use.
- For production multi-user handling, run pipeline tasks in background workers (Celery/RQ) and avoid long blocking requests in Streamlit.
