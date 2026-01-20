# Chat With Your Docs - RAG System - Complete File Index

## 📊 Project Statistics
- **Total Python Code**: 2,200+ lines
- **Total Files**: 20+
- **Modules**: 11 core modules
- **API Endpoints**: 4
- **LLM Providers**: 3
- **Supported Document Formats**: 3 (PDF, TXT, MD)

---

## 🗂️ File Organization

### CORE APPLICATION MODULES (2,200 lines total)

| File | Lines | Purpose | Key Classes/Functions |
|------|-------|---------|----------------------|
| **config.py** | 80 | Central configuration | Configuration constants, directory paths |
| **logger.py** | 50 | Logging setup | `setup_logger()` |
| **document_loader.py** | 330 | Load documents | `DocumentLoader` class |
| **text_processor.py** | 90 | Text chunking | `TextProcessor` class |
| **embedding.py** | 320 | Embeddings & vectors | `EmbeddingManager`, `VectorStore` classes |
| **retrieval.py** | 200 | Document search | `Retriever` class, `search_docs()` function |
| **ingest.py** | 470 | Ingestion pipeline | `IngestionPipeline` class, `ingest_documents()` |
| **llm.py** | 380 | LLM providers | `OllamaProvider`, `OpenAIProvider`, `RAGChain` |
| **app.py** | 300 | FastAPI backend | FastAPI app, endpoints, request models |
| **ui.py** | 350 | Streamlit frontend | Web UI components and interactions |
| **utils.py** | 80 | Utilities | `JSONHelper`, `FileHelper`, `TimeHelper` |

### TESTING & QUALITY ASSURANCE

| File | Purpose |
|------|---------|
| **test_rag.py** | Comprehensive test suite (7 test categories) |

### INFRASTRUCTURE & DEPLOYMENT

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies (20 packages) |
| **Dockerfile** | Container image for deployment |
| **docker-compose.yml** | Multi-container orchestration |
| **setup.sh** | Automated setup script |
| **.env.example** | Configuration template |
| **.env** | Environment variables (auto-created) |

### DOCUMENTATION

| File | Purpose | Content |
|------|---------|---------|
| **README.md** | Complete user guide | Setup, usage, API docs, troubleshooting |
| **SYSTEM_OVERVIEW.md** | Architecture overview | Components, metrics, deployment options |
| **QUICKSTART.py** | Quick reference guide | Module reference, examples, tips |
| **INDEX.md** | This file | File organization and navigation |

### DATA DIRECTORIES (Auto-created)

| Directory | Purpose |
|-----------|---------|
| **data/** | Store your PDF, TXT, or MD documents |
| **vector_store/** | FAISS index and embeddings cache |
| **logs/** | Application logs (rag.log) |
| **uploaded_docs/** | Uploaded files from Streamlit UI |

---

## 🔄 Module Dependencies

```
UI Layer (ui.py)
    ↓ (requests)
API Layer (app.py)
    ↓ (imports)
├── retrieval.py
│   ├── embedding.py
│   │   └── config.py
│   └── config.py
├── llm.py
│   ├── config.py
│   └── logger.py
└── ingest.py
    ├── document_loader.py
    │   └── logger.py
    ├── text_processor.py
    │   └── config.py
    ├── embedding.py
    │   └── config.py
    └── config.py

Config & Logging
├── config.py (no dependencies)
└── logger.py
    └── config.py

Utils
├── utils.py (no dependencies)
└── examples.py
    ├── ingest.py
    ├── retrieval.py
    └── llm.py
```

---

## 📖 How to Navigate

### For Understanding the System
1. Start with: **SYSTEM_OVERVIEW.md** - Get the big picture
2. Read: **README.md** - Setup and usage guide
3. Review: **config.py** - See all configuration options

### For Setting Up
1. Run: **setup.sh** - Automated setup
2. Edit: **.env** - Configure for your environment
3. Add documents to: **data/** directory
4. Run: **python ingest.py --source data/**

### For Using the API
1. Start: **app.py** with uvicorn
2. Open: http://localhost:8000/docs (Swagger UI)
3. Or use: **test_rag.py** for examples

### For Using the Web UI
1. Start: **ui.py** with streamlit
2. Open: http://localhost:8501
3. Upload files and ask questions

### For Extending the System
1. For new document formats: Edit **document_loader.py**
2. For different chunking: Edit **text_processor.py**
3. For new LLM: Add class to **llm.py**
4. For new API endpoints: Edit **app.py**

### For Testing
1. Run: **python test_rag.py**
2. Check: **logs/rag.log** for detailed output

---

## 🎯 Key Entry Points

### Command Line
```bash
# Setup
bash setup.sh

# Ingest documents
python ingest.py --source data/
python ingest.py --file data/document.pdf

# Start API
python -m uvicorn app:app --host 127.0.0.1 --port 8000

# Start UI
streamlit run ui.py

# Test system
python test_rag.py

# See quick reference
python QUICKSTART.py
```

### Python API
```python
# Search documents
from retrieval import search_docs
docs = search_docs("your question", top_k=3)

# Generate answer
from llm import generate_answer
answer = generate_answer("question", docs)

# Ingest documents
from ingest import ingest_documents
ingest_documents("data/")

# Full RAG pipeline
from retrieval import get_retriever
from llm import get_rag_chain
retriever = get_retriever()
rag_chain = get_rag_chain()
results = retriever.retrieve("query")
answer = rag_chain.generate_answer("query", [r["content"] for r in results])
```

### REST API
```bash
# Health check
curl http://localhost:8000/health

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is X?","top_k":3}'

# Ingest documents
curl -X POST http://localhost:8000/ingest/sync \
  -H "Content-Type: application/json" \
  -d '{"path":"data/"}'

# Full API docs
curl http://localhost:8000/docs
```

---

## 📚 Class & Function Reference

### DocumentLoader (document_loader.py)
- `load_document(file_path)` - Load single file
- `load_from_directory(directory_path)` - Load all documents
- `is_supported_format(file_path)` - Check if format supported

### TextProcessor (text_processor.py)
- `chunk_documents(documents)` - Split into chunks
- `chunk_text(text)` - Split raw text

### EmbeddingManager (embedding.py)
- `embed_documents(documents)` - Generate embeddings
- `embed_query(query)` - Embed a query

### VectorStore (embedding.py)
- `create_index(embeddings)` - Create FAISS index
- `search(query_embedding, top_k)` - Search index
- `save(documents)` - Save to disk
- `load()` - Load from disk

### Retriever (retrieval.py)
- `retrieve(query, top_k)` - Get results with metadata
- `retrieve_text_only(query, top_k)` - Get just text
- `load_index()` - Load vector store

### IngestionPipeline (ingest.py)
- `ingest_directory(directory_path)` - Ingest all files
- `ingest_file(file_path)` - Ingest single file

### RAGChain (llm.py)
- `generate_answer(question, documents)` - Get answer

### LLM Providers (llm.py)
- `OllamaProvider` - Local LLM
- `OpenAIProvider` - Cloud LLM
- `HuggingFaceProvider` - Open-source LLM

---

## 🔧 Configuration Reference

### In config.py
- `EMBEDDING_MODEL` - Which embeddings to use
- `CHUNK_SIZE` - Document chunk size (default: 500)
- `CHUNK_OVERLAP` - Overlap between chunks (default: 100)
- `TOP_K_RESULTS` - Default retrieval count (default: 3)
- `LLM_TYPE` - "ollama", "openai", or "huggingface"
- `OLLAMA_MODEL` - Which Ollama model (default: "mistral")
- `OPENAI_API_KEY` - OpenAI API key
- `API_HOST` - API server host (default: "127.0.0.1")
- `API_PORT` - API server port (default: 8000)

### In .env file
```
LLM_TYPE=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
API_HOST=127.0.0.1
API_PORT=8000
LOG_LEVEL=INFO
CHUNK_SIZE=500
CHUNK_OVERLAP=100
TOP_K_RESULTS=3
```

---

## 🚀 Recommended Reading Order

1. **INDEX.md** (this file) - Get oriented
2. **SYSTEM_OVERVIEW.md** - Understand architecture
3. **README.md** - Setup and basic usage
4. **config.py** - See what's configurable
5. **app.py** - Understand API endpoints
6. **retrieval.py** - How search works
7. **llm.py** - How generation works
8. **test_rag.py** - See examples
9. **QUICKSTART.py** - Quick reference

---

## 🎓 Learning Path

### Beginner
- Read: README.md
- Run: setup.sh
- Use: UI at http://localhost:8501

### Intermediate
- Read: SYSTEM_OVERVIEW.md
- Run: python ingest.py
- Use: API endpoints
- Read: config.py

### Advanced
- Read: All source code (carefully documented)
- Modify: Extend with new features
- Deploy: Using Docker
- Test: Run test_rag.py

---

## ✅ Quick Checklist

- [x] All 11 core modules implemented
- [x] Full API with 4 endpoints
- [x] Web UI with Streamlit
- [x] 3 LLM provider options
- [x] Comprehensive logging
- [x] Configuration management
- [x] Docker support
- [x] Test suite
- [x] Complete documentation
- [x] Ready for production

---

## 📞 Support & Troubleshooting

### Documentation Files
- General questions → README.md
- Architecture questions → SYSTEM_OVERVIEW.md
- Quick lookup → QUICKSTART.py
- File organization → INDEX.md (this file)

### Code Issues
- Check: logs/rag.log for errors
- Run: python test_rag.py to verify
- Read: Docstrings in source files

### Setup Issues
- Read: README.md "Quick Start" section
- Run: bash setup.sh
- Check: Python version (3.8+)
- Verify: Dependencies installed

---

**Ready to use! Start with: `bash setup.sh`**
