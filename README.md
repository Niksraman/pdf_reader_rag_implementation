# Chat With Your Docs - RAG System

A production-ready Retrieval-Augmented Generation (RAG) system for answering questions about document collections. Built with modular Python code, featuring FastAPI backend, Streamlit frontend, and support for multiple LLM providers.

## 🎯 Features

- **📄 Multi-format Document Support**: PDF, TXT, and Markdown files
- **🔍 Semantic Search**: Uses FAISS for efficient vector similarity search
- **🤖 Multiple LLM Providers**: Ollama, OpenAI, HuggingFace transformers
- **⚡ Fast Retrieval**: Real-time document search with embeddings
- **📊 Source Attribution**: See exactly which documents answer your question
- **🏗️ Modular Architecture**: Clean separation of concerns
- **🔄 Easy Integration**: RESTful API with comprehensive documentation
- **📝 Production-Ready**: Logging, error handling, and configuration management

## 📋 Project Structure

```
pdf_reader_rag_implementation/
├── config.py              # Configuration and settings
├── logger.py              # Logging setup
├── document_loader.py     # Document loading from various formats
├── text_processor.py      # Text chunking and processing
├── embedding.py           # Embedding generation and vector store
├── retrieval.py           # Document retrieval logic
├── ingest.py              # Document ingestion pipeline
├── llm.py                 # LLM integration (multiple providers)
├── app.py                 # FastAPI backend
├── ui.py                  # Streamlit frontend
├── utils.py               # Utility functions
├── examples.py            # Example usage
├── requirements.txt       # Python dependencies
└── data/                  # Sample documents directory
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd pdf_reader_rag_implementation

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Documents

Place your documents in the `data/` directory:

```bash
# Create data directory if it doesn't exist
mkdir -p data

# Add your PDF, TXT, or Markdown files
cp /path/to/your/documents/*.pdf data/
```

### 3. Ingest Documents

```bash
# Ingest all documents from data directory
python ingest.py --source data/

# Or ingest a specific file
python ingest.py --file data/document.pdf
```

### 4. Start the API Server

```bash
# Terminal 1: Start FastAPI server
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start the Frontend

```bash
# Terminal 2: Start Streamlit UI
streamlit run ui.py --server.port 8501
```

### 6. Use the Application

Open your browser and navigate to:
- **UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document processing
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 3

# LLM Provider (ollama, openai, huggingface)
LLM_TYPE = "ollama"
OLLAMA_MODEL = "mistral"
```

Or set environment variables:

```bash
export LLM_TYPE=openai
export OPENAI_API_KEY=your-api-key
export OLLAMA_MODEL=mistral
```

## 🧠 LLM Providers

### Ollama (Local, Free)

```bash
# Install Ollama
# https://ollama.ai

# Pull a model
ollama pull mistral

# Start Ollama server
ollama serve

# Configure in app
LLM_TYPE = "ollama"
OLLAMA_MODEL = "mistral"
```

### OpenAI (Cloud-based)

```bash
export OPENAI_API_KEY=sk-...
export LLM_TYPE=openai
```

### HuggingFace (Local, with transformers)

```bash
export LLM_TYPE=huggingface
# Downloads large models automatically
```

## 📚 API Endpoints

### GET `/health`
Health check endpoint
```bash
curl http://localhost:8000/health
```

### POST `/ask`
Ask a question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?", "top_k": 3}'
```

### POST `/ingest`
Ingest documents (asynchronous)
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"path": "data/"}'
```

### POST `/ingest/sync`
Ingest documents (synchronous - waits for completion)
```bash
curl -X POST http://localhost:8000/ingest/sync \
  -H "Content-Type: application/json" \
  -d '{"path": "data/"}'
```

## 💻 Usage Examples

### Python API

```python
from retrieval import search_docs
from llm import generate_answer

# Search documents
query = "What is the main topic?"
documents = search_docs(query, top_k=3)

# Generate answer
answer = generate_answer(query, documents)
print(answer)
```

### Ingest Documents Programmatically

```python
from ingest import ingest_documents

# Ingest from directory
ingest_documents("data/")

# Or ingest a single file
ingest_documents("data/document.pdf")
```

### Full RAG Chain

```python
from retrieval import get_retriever
from llm import get_rag_chain

# Initialize
retriever = get_retriever(top_k=3)
rag_chain = get_rag_chain()

# Query
query = "What is machine learning?"
documents = retriever.retrieve_text_only(query)
answer = rag_chain.generate_answer(query, documents)
print(answer)
```

## 🧪 Testing

Run example scripts:

```bash
# Example: Document ingestion
python examples.py ingest

# Example: Document retrieval
python examples.py retrieve

# Example: Full RAG chain
python examples.py rag
```

## 📊 System Architecture

```
User Input (UI/API)
        ↓
    Router
        ↓
    Retriever ← Vector Store (FAISS)
        ↓      ↗
   Documents
        ↓
  RAG Chain
        ↓
   LLM Provider
        ↓
    Response
```

## 🔍 How RAG Works

1. **Ingestion**: Documents are loaded, chunked, and converted to embeddings
2. **Storage**: Embeddings are stored in FAISS for fast similarity search
3. **Retrieval**: User query is converted to embedding and matched against document embeddings
4. **Generation**: Retrieved documents are provided as context to an LLM
5. **Response**: LLM generates answer grounded in the retrieved documents

## 🛠️ Troubleshooting

### Vector Store Not Found
```bash
# Ensure documents are ingested first
python ingest.py --source data/
```

### API Connection Error
```bash
# Check if API server is running
curl http://localhost:8000/health
```

### Ollama Connection Error
```bash
# Start Ollama service
ollama serve

# Or change LLM_TYPE in config.py
```

### Out of Memory
- Reduce `CHUNK_SIZE` in config.py
- Use a smaller embedding model
- Reduce `TOP_K_RESULTS`

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["sh", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501"]
```

### Environment Variables

```bash
# LLM Configuration
LLM_TYPE=ollama  # or openai, huggingface
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OPENAI_API_KEY=sk-...

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

## 📈 Performance Tips

1. **Batch ingestion**: Ingest multiple documents at once
2. **Tune TOP_K**: Find optimal number of retrieved documents (usually 3-5)
3. **Cache embeddings**: Already embedded in vector store
4. **Use GPU**: Set environment variable for GPU acceleration
5. **Monitor logs**: Check `logs/rag.log` for performance insights

## 🔐 Security Notes

- Store API keys in environment variables (use `.env` file)
- Don't commit `.env` to version control
- Validate input in production
- Use HTTPS for remote deployments
- Implement authentication for production APIs

## 📝 License

MIT

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `logs/rag.log`
3. Check API documentation at `http://localhost:8000/docs`

## 🎓 Learning Resources

- [RAG Architecture](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)
