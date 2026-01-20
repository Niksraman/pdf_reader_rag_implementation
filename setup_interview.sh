#!/bin/bash

# Chat With Your Docs - Complete Setup Script
# This script sets up everything needed to run the RAG system

set -e  # Exit on error

echo "=================================================="
echo "Chat With Your Docs - RAG System Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/5] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Create virtual environment
echo -e "${BLUE}[2/5] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo ""

# Install dependencies
echo -e "${BLUE}[3/5] Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ All dependencies installed${NC}"
echo ""

# Create directories
echo -e "${BLUE}[4/5] Creating necessary directories...${NC}"
mkdir -p data vector_store logs uploaded_docs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Test imports
echo -e "${BLUE}[5/5] Testing module imports...${NC}"
python3 -c "
from config import *
from logger import setup_logger
from document_loader import DocumentLoader
from text_processor import TextProcessor
from embedding import EmbeddingManager, VectorStore
from retrieval import Retriever
from llm import get_llm_provider, generate_answer
from ingest import IngestionPipeline
print('✓ All modules imported successfully')
" || {
    echo "Import test failed. Please check your setup."
    exit 1
}
echo -e "${GREEN}✓ All modules working correctly${NC}"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env .env 2>/dev/null || cat > .env << 'EOF'
# LLM Configuration
LLM_TYPE=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_RELOAD=True

# Logging
LOG_LEVEL=INFO

# Document Processing
CHUNK_SIZE=500
CHUNK_OVERLAP=100
TOP_K_RESULTS=3
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Show next steps
echo "=================================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "📚 Sample documents added:"
echo "   - data/python_guide.txt"
echo "   - data/ml_fundamentals.txt"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. ${YELLOW}Ingest the sample documents:${NC}"
echo "   python ingest.py --source data/"
echo ""
echo "2. ${YELLOW}In Terminal 1, start the API:${NC}"
echo "   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload"
echo ""
echo "3. ${YELLOW}In Terminal 2, start the UI:${NC}"
echo "   streamlit run ui.py --server.port 8501"
echo ""
echo "4. ${YELLOW}Open in browser:${NC}"
echo "   - UI: http://localhost:8501"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "💡 For Ollama (free LLM):"
echo "   1. Install: https://ollama.ai"
echo "   2. Run: ollama serve"
echo "   3. In another terminal: ollama pull mistral"
echo ""
echo "📖 For more info, see:"
echo "   - README.md - User guide"
echo "   - SYSTEM_OVERVIEW.md - Technical details"
echo "   - INTERVIEW_GUIDE.md - Interview preparation"
echo ""
echo "=================================================="
