#!/usr/bin/env python
"""
Quick start guide and module reference for Chat With Your Docs RAG System
"""

QUICK_START = """
╔════════════════════════════════════════════════════════════════════════════╗
║          CHAT WITH YOUR DOCS - RAG SYSTEM QUICK START GUIDE               ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 PROJECT OVERVIEW
==================
A production-ready Retrieval-Augmented Generation (RAG) system that allows you to
ask questions about a collection of documents (PDFs, TXT, Markdown) and get 
answers powered by LLMs with cited sources.

🏗️ MODULAR ARCHITECTURE
=======================
The system is divided into independent modules that work together:

  ┌─────────────────────────────────────────────────────────┐
  │              USER INTERFACE LAYER                        │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  UI (Streamlit) <-> API (FastAPI)               │   │
  │  └──────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────┘
                           ↓
  ┌─────────────────────────────────────────────────────────┐
  │          ORCHESTRATION & PROCESSING LAYER               │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Ingest Pipeline | Retrieval | LLM Chain       │   │
  │  └──────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────┘
                           ↓
  ┌─────────────────────────────────────────────────────────┐
  │        CORE MODULES (MODULAR & REUSABLE)                │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Loader | Processor | Embeddings | Vector Store │   │
  │  └──────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────┘
                           ↓
  ┌─────────────────────────────────────────────────────────┐
  │        DATA & CONFIGURATION LAYER                       │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │  Config | Logger | Utils                        │   │
  │  └──────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────┘

📁 FILE STRUCTURE
=================
pdf_reader_rag_implementation/
│
├── Core Modules (Document & Data Processing)
│   ├── document_loader.py    # Load PDFs, TXT, Markdown files
│   ├── text_processor.py     # Chunk and process documents
│   ├── embedding.py          # Generate embeddings & manage vector store
│   └── retrieval.py          # Search and retrieve documents
│
├── Processing Pipeline
│   ├── ingest.py             # Orchestrate ingestion workflow
│   └── llm.py                # LLM integration (Ollama, OpenAI, HF)
│
├── Application Layer
│   ├── app.py                # FastAPI backend API
│   └── ui.py                 # Streamlit web interface
│
├── Utilities & Configuration
│   ├── config.py             # Centralized configuration
│   ├── logger.py             # Logging setup
│   ├── utils.py              # Helper functions
│   └── examples.py           # Example usage
│
├── Testing & Deployment
│   ├── test_rag.py           # System test suite
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Container image
│   ├── docker-compose.yml    # Multi-container setup
│   ├── setup.sh              # Setup automation
│   └── .env.example          # Configuration template
│
├── Documentation
│   └── README.md             # Complete documentation
│
└── Data Directories (auto-created)
    ├── data/                 # Store your documents here
    ├── vector_store/         # FAISS index & embeddings
    └── logs/                 # Application logs

🚀 GETTING STARTED (5 MINUTES)
==============================

1. SETUP
   bash setup.sh
   
2. ADD DOCUMENTS
   cp /path/to/your/*.pdf data/
   
3. INGEST DOCUMENTS
   python ingest.py --source data/
   
4. START API (Terminal 1)
   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   
5. START UI (Terminal 2)
   streamlit run ui.py --server.port 8501
   
6. OPEN BROWSER
   http://localhost:8501

🔑 KEY FEATURES
===============

✓ MULTI-FORMAT SUPPORT
  Supports PDF, TXT, and Markdown files
  
✓ SEMANTIC SEARCH
  Uses state-of-the-art embeddings for accurate document retrieval
  
✓ MULTIPLE LLM OPTIONS
  - Local: Ollama (free, no API keys needed)
  - Cloud: OpenAI (GPT-3.5, GPT-4)
  - Open-source: HuggingFace transformers
  
✓ SOURCE ATTRIBUTION
  Every answer shows which documents were used
  
✓ PRODUCTION-READY
  Full logging, error handling, and configuration management
  
✓ MODULAR DESIGN
  Each module can be used independently or combined

📚 MODULE REFERENCE
===================

DOCUMENT_LOADER (document_loader.py)
  Purpose: Load documents from disk
  Class: DocumentLoader
  Methods:
    - load_document(file_path) -> List[Document]
    - load_from_directory(dir_path) -> List[Document]
    - is_supported_format(file_path) -> bool
  Usage:
    from document_loader import DocumentLoader
    docs = DocumentLoader.load_document("file.pdf")

TEXT_PROCESSOR (text_processor.py)
  Purpose: Split documents into chunks
  Class: TextProcessor
  Methods:
    - chunk_documents(docs) -> List[Document]
    - chunk_text(text) -> List[str]
  Usage:
    from text_processor import TextProcessor
    processor = TextProcessor(chunk_size=500, chunk_overlap=100)
    chunks = processor.chunk_documents(documents)

EMBEDDING (embedding.py)
  Purpose: Generate embeddings and manage vector store
  Classes: EmbeddingManager, VectorStore
  Methods:
    - embed_documents(docs) -> np.ndarray
    - embed_query(query) -> np.ndarray
    - create_index(embeddings) -> None
    - search(query_embedding, top_k) -> List[int]
    - save/load() for persistence
  Usage:
    from embedding import EmbeddingManager, VectorStore
    em = EmbeddingManager()
    embeddings = em.embed_documents(texts)

RETRIEVAL (retrieval.py)
  Purpose: Retrieve relevant documents
  Class: Retriever
  Functions:
    - search_docs(query, top_k) -> List[str]
    - get_retriever() -> Retriever
  Usage:
    from retrieval import search_docs
    results = search_docs("What is X?", top_k=3)

INGEST (ingest.py)
  Purpose: Orchestrate document ingestion
  Class: IngestionPipeline
  Functions:
    - ingest_documents(path) -> None
  Usage:
    from ingest import ingest_documents
    ingest_documents("data/")

LLM (llm.py)
  Purpose: Generate answers using LLMs
  Classes: OllamaProvider, OpenAIProvider, HuggingFaceProvider, RAGChain
  Functions:
    - generate_answer(question, documents) -> str
    - get_rag_chain() -> RAGChain
  Usage:
    from llm import generate_answer
    answer = generate_answer("Question?", documents)

🔧 CONFIGURATION
================

All settings are in config.py. Override with environment variables:

  export LLM_TYPE=ollama
  export OLLAMA_MODEL=mistral
  export CHUNK_SIZE=500
  export TOP_K_RESULTS=3

Or edit .env file:
  LLM_TYPE=ollama
  OLLAMA_MODEL=mistral
  # etc...

📡 API ENDPOINTS
================

Health Check
  GET /health
  Response: {"status": "healthy", "version": "1.0.0"}

Ask Question
  POST /ask
  Request: {"question": "What is X?", "top_k": 3}
  Response: {"answer": "...", "sources": [...], "num_sources": 3}

Ingest (Async)
  POST /ingest
  Request: {"path": "data/"}
  Response: {"status": "processing", "message": "..."}

Ingest (Sync)
  POST /ingest/sync
  Request: {"path": "data/"}
  Response: {"status": "completed", "message": "..."}

Full API docs: http://localhost:8000/docs

💻 PYTHON API USAGE
===================

from retrieval import search_docs
from llm import generate_answer

# Simple usage
query = "What is the main topic?"
documents = search_docs(query, top_k=3)
answer = generate_answer(query, documents)
print(answer)

# Advanced usage
from retrieval import get_retriever
from llm import get_rag_chain

retriever = get_retriever(top_k=3)
rag_chain = get_rag_chain()

results = retriever.retrieve(query)  # With metadata
answer = rag_chain.generate_answer(query, documents)

🐳 DOCKER DEPLOYMENT
====================

Build and run with Docker Compose:

  docker-compose up --build

This will start:
  - RAG application on ports 8000 (API) and 8501 (UI)
  - Ollama service on port 11434 (optional)

Access:
  - UI: http://localhost:8501
  - API: http://localhost:8000
  - Ollama: http://localhost:11434

🧪 TESTING
==========

Run the test suite:
  python test_rag.py

This tests:
  ✓ Module imports
  ✓ Configuration loading
  ✓ Directory structure
  ✓ Logger functionality
  ✓ Embedding manager
  ✓ Document loader
  ✓ API endpoints

🛠️ TROUBLESHOOTING
==================

Problem: "Vector store not found"
Solution: Ingest documents first
  python ingest.py --source data/

Problem: "Cannot connect to Ollama"
Solution: Start Ollama or configure different LLM
  ollama serve
  OR edit config.py, set LLM_TYPE="openai"

Problem: "Out of memory"
Solution: Reduce chunk size or use smaller model
  In config.py: CHUNK_SIZE=250

Problem: "Slow inference"
Solution: Reduce TOP_K_RESULTS or use faster model
  In config.py: TOP_K_RESULTS=2

📊 PERFORMANCE TUNING
====================

For Better Accuracy:
  - Increase CHUNK_SIZE (e.g., 1000)
  - Increase TOP_K_RESULTS (e.g., 5)
  - Use larger LLM model (e.g., "neural-chat")

For Better Speed:
  - Decrease CHUNK_SIZE (e.g., 250)
  - Decrease TOP_K_RESULTS (e.g., 2)
  - Use smaller embedding model
  - Use faster LLM (e.g., "orca-mini")

For Better Memory Usage:
  - Decrease CHUNK_SIZE
  - Use CPU instead of GPU (CUDA disabled)
  - Use smaller embedding model

🔐 SECURITY NOTES
=================

✓ Store API keys in .env (never commit to git)
✓ Use environment variables for sensitive config
✓ Enable HTTPS in production
✓ Add authentication to production APIs
✓ Validate all user inputs
✓ Use firewall rules for internal services

📖 LEARNING RESOURCES
====================

RAG Concepts:
  - RAG Architecture: https://docs.llamaindex.ai
  - Embeddings: https://www.sbert.net
  - Vector Search: https://github.com/facebookresearch/faiss

Frameworks:
  - FastAPI: https://fastapi.tiangolo.com
  - Streamlit: https://docs.streamlit.io
  - LangChain: https://docs.langchain.com

LLMs:
  - Ollama: https://ollama.ai
  - OpenAI: https://platform.openai.com
  - HuggingFace: https://huggingface.co

╔════════════════════════════════════════════════════════════════════════════╗
║                      READY TO USE!                                        ║
║                      Next: Run setup.sh or add documents to data/          ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(QUICK_START)
