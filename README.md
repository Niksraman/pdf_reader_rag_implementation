
# Chat With Your Docs (RAG + Ollama)

Serverless-style RAG application using:
- Ollama (open-source LLM)
- FAISS vector store
- FastAPI backend
- Streamlit UI

## How to run locally

1. Install Ollama: https://ollama.ai
2. Pull model:
   ```bash
   ollama pull mistral
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run ingestion:
   ```bash
   python ingest.py --docs data/
   ```

5. Run backend:
   ```bash
   uvicorn app:app --reload
   ```

6. Run UI:
   ```bash
   streamlit run ui.py
   ```
