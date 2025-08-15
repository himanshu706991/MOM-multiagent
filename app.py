import streamlit as st
import uuid, os
from pipeline import run_pipeline

st.set_page_config(page_title='Minutes of Meeting Generator', layout='centered')
st.title('Minutes of Meeting Generator (Multi-user)')

with st.sidebar:
    st.header('Settings')
    st.write('LLM backend (set via .env)')
    st.text('LLM_BACKEND='+os.getenv('LLM_BACKEND','ollama'))

uploaded = st.file_uploader('Upload transcript (PDF/DOCX/TXT)', type=['pdf','docx','txt'])

if uploaded:
    session_id = str(uuid.uuid4())[:8]
    uploads_dir = os.path.join('/mnt/data/uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, f"{session_id}_{uploaded.name}")
    with open(file_path, 'wb') as f:
        f.write(uploaded.getbuffer())
    st.info('File uploaded. Starting processing...')

    progress = st.progress(0)
    status = st.empty()

    status.text('Step 1/5: Extracting...')
    progress.progress(20)
    # run pipeline (blocking) - in production, delegate to background worker / queue for concurrency
    docx_path, pdf_path = run_pipeline(file_path, session_id)

    status.text('Step 5/5: Finished. Preparing downloads...')
    progress.progress(100)

    st.success('Minutes of Meeting generated!')
    with open(docx_path, 'rb') as f:
        st.download_button('Download DOCX', f, file_name=os.path.basename(docx_path))
    with open(pdf_path, 'rb') as f:
        st.download_button('Download PDF', f, file_name=os.path.basename(pdf_path))
