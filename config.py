"""
Configuration module for RAG system
"""
import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"

# Vector store configuration
VECTOR_STORE_FILE = VECTOR_STORE_DIR / "vector_store.pkl"
METADATA_FILE = VECTOR_STORE_DIR / "metadata.pkl"

# Embedding model configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Document processing configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 3


# LLM configuration (default: Ollama)
LLM_TYPE = os.getenv("LLM_TYPE", "ollama")  # ollama, openai, or huggingface
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# API configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# Streamlit configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "rag.log"

# Create necessary directories
for directory in [DATA_DIR, VECTOR_STORE_DIR, LOG_FILE.parent]:
    directory.mkdir(parents=True, exist_ok=True)
