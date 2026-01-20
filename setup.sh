#!/bin/bash

# Chat With Your Docs - RAG System Startup Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Chat With Your Docs - RAG System${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1)
echo "✓ $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install/update dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
echo -e "\n${YELLOW}Creating necessary directories...${NC}"
mkdir -p data vector_store logs uploaded_docs
echo "✓ Directories created"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "\n${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo "✓ .env file created (please update with your configuration)"
fi

# Display startup instructions
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}Quick Start:${NC}"
echo -e "1. ${YELLOW}Ingest documents:${NC}"
echo "   python ingest.py --source data/"
echo ""
echo -e "2. ${YELLOW}Start API server (Terminal 1):${NC}"
echo "   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload"
echo ""
echo -e "3. ${YELLOW}Start UI (Terminal 2):${NC}"
echo "   streamlit run ui.py --server.port 8501"
echo ""
echo -e "4. ${YELLOW}Open in browser:${NC}"
echo "   http://localhost:8501"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "   - Edit config.py for settings"
echo "   - Edit .env for environment variables"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   - See README.md for detailed information"
echo "   - API docs: http://localhost:8000/docs"
echo ""
