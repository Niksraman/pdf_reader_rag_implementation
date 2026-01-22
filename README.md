# Chat With Your Docs - RAG System

A professional Retrieval-Augmented Generation (RAG) system for answering questions about document collections. Built with modular Python code, featuring a FastAPI backend, professional Streamlit frontend, and HuggingFace LLM integration.

## 🎯 Features

- **📄 Multi-format Document Support**: PDF, TXT, and Markdown files
- **🔍 Semantic Search**: FAISS-based efficient vector similarity search
- **🤖 LLM Integration**: HuggingFace (default), with support for OpenAI and Ollama
- **⚡ Fast Retrieval**: Real-time document search with embeddings
- **📊 Source Attribution**: See exactly which documents answer your question
- **🎨 Professional UI**: Modern Streamlit interface with custom styling
- **📚 RESTful API**: Comprehensive FastAPI backend with Swagger documentation
- **🔐 Production-Ready**: Error handling, logging, and configuration management

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

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Documents

Place your documents in the `data/` directory:

```bash
# Documents in data/ directory are automatically loaded
# Supports: .pdf, .txt, .md files
cp /path/to/your/documents/*.pdf data/
```

### 3. Start Both Services (Recommended)

```bash
# Terminal 1: Start FastAPI backend (port 8000)
python app.py

# Terminal 2: Start Streamlit UI (port 8501)
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
```

### 4. Access the Application

- **Web UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Upload and Chat

1. Go to the Streamlit UI (http://localhost:8501)
2. Upload documents from the sidebar (PDF, TXT, or Markdown)
3. Click **💾 Save Files** then **🚀 Ingest**
4. Ask questions in the main area
5. View answers with source references

## 🔧 Configuration

### Default Configuration

The system is configured to use **HuggingFace LLM (distilgpt2)** by default, which:
- ✅ Works out-of-the-box without external services
- ✅ Runs locally on CPU
- ✅ Requires no API keys
- ✅ Automatically downloads the lightweight model

Edit `config.py` to customize:

```python
# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document processing
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 3

# LLM Provider (default: huggingface)
LLM_TYPE = "huggingface"  # or "openai", "ollama"
```

### Environment Variables

```bash
# Change LLM provider
export LLM_TYPE=openai
export OPENAI_API_KEY=sk-your-key-here

# Or use Ollama
export LLM_TYPE=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=mistral
```

## 🧠 LLM Providers

### HuggingFace (Default, Recommended)

- **Best For**: Out-of-the-box usage, no API keys needed
- **Model**: distilgpt2 (lightweight, ~300MB)
- **Pros**: Free, local, privacy-friendly, no external dependencies
- **Cons**: Less powerful than enterprise models

```bash
export LLM_TYPE=huggingface
# No additional setup needed!
```

### OpenAI (Enterprise-Grade)

- **Best For**: Production applications, highest quality answers
- **Model**: gpt-3.5-turbo (default)
- **Pros**: Powerful, reliable, supports multiple models
- **Cons**: Requires API key and payment

```bash
export LLM_TYPE=openai
export OPENAI_API_KEY=sk-your-api-key
```

### Ollama (Self-Hosted)

- **Best For**: Privacy-focused, custom models
- **Model**: mistral (default)
- **Pros**: Open-source, local, customizable
- **Cons**: Requires additional installation and setup

```bash
# Install Ollama: https://ollama.ai
ollama pull mistral
ollama serve

# Configure
export LLM_TYPE=ollama
export OLLAMA_BASE_URL=http://localhost:11434
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

### Web UI

Simply upload documents and ask questions through the professional Streamlit interface:

1. Upload documents from the sidebar
2. Click **Ingest** to process documents
3. Ask questions in the main chat area
4. Review answers with source citations

### Python API

```python
from retrieval import search_docs
from llm import generate_answer

# Search documents
query = "What is machine learning?"
documents = search_docs(query, top_k=3)

# Generate answer
answer = generate_answer(query, documents)
print(answer)
```

### REST API

```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?", "top_k": 3}'

# Ingest documents
curl -X POST http://localhost:8000/ingest/sync \
  -H "Content-Type: application/json" \
  -d '{"path": "data/"}'

# Health check
curl http://localhost:8000/health
```

## 🧪 Testing

Test the system with sample documents:

```bash
# Sample documents are included in data/
# They are automatically processed when you start the app

# Test via API
curl http://localhost:8000/health

# Test via Streamlit
# Go to http://localhost:8501 and ask a question
```

## 📁 Project Structure

```
pdf_reader_rag_implementation/
├── Core Application
│   ├── app.py                 # FastAPI backend
│   ├── ui.py                  # Streamlit frontend
│   └── config.py              # Configuration settings
│
├── Document Processing
│   ├── document_loader.py     # Load PDF, TXT, MD files
│   ├── text_processor.py      # Chunk and process text
│   └── ingest.py              # Document ingestion pipeline
│
├── AI Components
│   ├── embedding.py           # Embeddings and vector store (FAISS)
│   ├── retrieval.py           # Document retrieval
│   └── llm.py                 # LLM providers (HuggingFace, OpenAI, Ollama)
│
├── Utilities
│   ├── logger.py              # Logging configuration
│   ├── utils.py               # Helper functions
│   └── requirements.txt       # Python dependencies
│
└── Data & Logs
    ├── data/                  # Sample documents
    ├── vector_store/          # FAISS index and metadata
    ├── logs/                  # Application logs
    └── uploaded_docs/         # User-uploaded documents
```

## 🔍 How RAG Works

1. **Ingestion**: Documents are loaded, split into chunks, and converted to embeddings
2. **Storage**: Embeddings stored in FAISS vector database for fast retrieval
3. **Query**: User question is converted to embedding
4. **Retrieval**: Similar document chunks are found using vector similarity
5. **Generation**: Retrieved chunks are passed as context to the LLM
6. **Response**: LLM generates an answer grounded in the documents

## 🛠️ Troubleshooting

### Common Issues

**Q: Application won't start**
- Ensure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`
- Check port availability (8000, 8501)

**Q: "No documents found"**
- Place documents in `data/` directory
- Supported formats: PDF, TXT, Markdown
- Restart the application after adding documents

**Q: "LLM Error" or slow responses**
- HuggingFace model loads slowly on first use (normal)
- For faster responses, use OpenAI: `export LLM_TYPE=openai`
- Check available memory (model requires ~500MB)

**Q: Vector store issues**
- Delete `vector_store/` directory to reset
- Re-ingest documents from the UI or API
- Check that `data/` contains documents

### Check Logs

```bash
# View application logs
tail -f logs/rag.log

# Clear logs
rm logs/rag.log
```

## 🚀 Deployment

### Using Docker

```bash
# Build image
docker build -t rag-system .

# Run container
docker run -p 8000:8000 -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/vector_store:/app/vector_store \
  rag-system
```

### Environment Variables

```bash
# LLM Configuration
LLM_TYPE=huggingface              # or openai, ollama (default: huggingface)
OPENAI_API_KEY=sk-...             # Required if using OpenAI
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

## 📈 Performance Tips

- **Batch Processing**: Upload multiple documents at once
- **Tune TOP_K**: Optimal is usually 3-5 documents
- **Monitor Memory**: First LLM load caches the model
- **Check Logs**: Review `logs/rag.log` for performance insights

## � API Endpoints

### Health Check
```bash
GET /health
# Returns API status and version
```

### Ask Question
```bash
POST /ask
{
  "question": "What is machine learning?",
  "top_k": 3
}
```

### Ingest Documents (Async)
```bash
POST /ingest
{
  "path": "data/"
}
```

### Ingest Documents (Sync)
```bash
POST /ingest/sync
{
  "path": "data/"
}
# Waits for completion
```

## 📝 License

MIT

## 🤝 Support & Feedback

- **Issues**: Check troubleshooting section first
- **Logs**: Review `logs/rag.log` for detailed information
- **API Docs**: Visit http://localhost:8000/docs for interactive documentation
- **Questions**: Refer to the examples and configuration guide

---

**Status**: ✅ Ready for Production | **Last Updated**: January 2026

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
