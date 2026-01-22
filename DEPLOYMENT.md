# 🚀 Deployment Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Application
**Option A: Using separate terminals (Recommended)**

```bash
# Terminal 1: Start backend API (port 8000)
python app.py

# Terminal 2: Start frontend UI (port 8501)
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
```

**Option B: Using shell script**
```bash
# Create a simple start script
#!/bin/bash
python app.py &
sleep 3
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
```

### Step 3: Access the Application
- **Web UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## Usage

### Upload Documents
1. Go to http://localhost:8501
2. Use the sidebar to upload documents (PDF, TXT, or Markdown)
3. Click **💾 Save Files**
4. Click **🚀 Ingest** to process

### Ask Questions
1. Enter your question in the text area
2. Click **🔍 Ask**
3. View the answer with source references

## LLM Configuration

### Default (HuggingFace - No Setup Needed)
- Uses lightweight distilgpt2 model
- Runs locally on CPU
- No API keys required
- First load takes 1-2 minutes to download model

### OpenAI (Recommended for Production)
```bash
export OPENAI_API_KEY=sk-your-api-key-here
export LLM_TYPE=openai
```

### Ollama (For Advanced Users)
```bash
# Install Ollama from https://ollama.ai
ollama pull mistral
ollama serve

# In another terminal
export LLM_TYPE=ollama
python app.py
```

## System Requirements

| Component | Requirement |
|-----------|-------------|
| **RAM** | 4GB minimum (8GB recommended) |
| **Storage** | 1GB for dependencies + space for documents |
| **CPU** | Any modern processor |
| **GPU** | Optional (accelerates LLM) |

## Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports 8000 and 8501
lsof -i :8000  # Find PID
kill -9 <PID>

lsof -i :8501
kill -9 <PID>
```

### LLM Model Download Slow
- First load downloads ~350MB model (normal, takes 1-2 min)
- Model is cached for subsequent runs
- For faster response, use OpenAI instead

### Documents Not Being Found
1. Ensure documents are in `data/` directory
2. Supported formats: .pdf, .txt, .md
3. Click **🚀 Ingest** in the UI to process

### Vector Store Error
```bash
# Reset vector store (deletes cached embeddings)
rm -rf vector_store/

# Re-ingest documents through UI
```

## Monitoring

### View Application Logs
```bash
tail -f logs/rag.log
```

### Check API Health
```bash
curl http://localhost:8000/health
```

## Docker Deployment

### Build Image
```bash
docker build -t rag-system .
```

### Run Container
```bash
docker run -p 8000:8000 -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/vector_store:/app/vector_store \
  -v $(pwd)/logs:/app/logs \
  rag-system
```

## Performance Optimization

| Setting | Recommendation |
|---------|---|
| **TOP_K** | 3-5 documents (default: 3) |
| **CHUNK_SIZE** | 500 tokens (default) |
| **CHUNK_OVERLAP** | 100 tokens (default) |

## Production Checklist

- [ ] Test with sample documents
- [ ] Configure LLM provider (default is sufficient for testing)
- [ ] Set up logging in `config.py`
- [ ] Use environment variables for sensitive data
- [ ] Set `LOG_LEVEL = "INFO"` in production
- [ ] Monitor `logs/rag.log` regularly
- [ ] Set up regular backups of `vector_store/`

## Support

For issues:
1. Check `logs/rag.log` for error messages
2. Review the main `README.md`
3. Visit http://localhost:8000/docs for API help

---

**Version**: 1.0 | **Last Updated**: January 2026
