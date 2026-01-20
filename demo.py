#!/usr/bin/env python3
"""
Interactive Demo - Chat With Your Docs
Shows how to use the RAG system programmatically
"""

import sys
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_section(text):
    """Print a formatted section"""
    print(f"\n>>> {text}")
    print("-" * 60)

def demo_basic_usage():
    """Demonstrate basic RAG usage"""
    print_header("RAG System Interactive Demo")
    
    try:
        from ingest import IngestionPipeline
        from retrieval import Retriever
        from llm import generate_answer
        from logger import setup_logger
        
        logger = setup_logger(__name__)
        
        # Step 1: Check if documents are ingested
        print_section("Step 1: Checking Document Store")
        
        from embedding import VectorStore
        vector_store = VectorStore()
        
        try:
            documents = vector_store.load()
            print(f"✓ Found {len(documents)} documents in vector store")
            print("\nDocuments in index:")
            for i, doc in enumerate(documents[:5], 1):
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. {preview}...")
            if len(documents) > 5:
                print(f"  ... and {len(documents) - 5} more documents")
        except Exception as e:
            print(f"✗ No documents found. Ingesting sample documents...")
            print("\nTo ingest documents, run:")
            print("  python ingest.py --source data/")
            return
        
        # Step 2: Retrieve relevant documents
        print_section("Step 2: Document Retrieval")
        
        question = "What is Python?"
        print(f"Question: {question}\n")
        
        retriever = Retriever(top_k=3)
        retriever.load_index()
        
        results = retriever.retrieve(question, top_k=3)
        print(f"✓ Retrieved {len(results)} relevant documents:\n")
        
        for i, result in enumerate(results, 1):
            preview = result['content'][:150].replace('\n', ' ')
            print(f"  [{i}] {preview}...")
        
        # Step 3: Generate answer
        print_section("Step 3: Answer Generation")
        
        try:
            # Check if Ollama is available
            import requests
            try:
                requests.get("http://localhost:11434/api/tags", timeout=2)
                print("✓ Ollama is running\n")
                
                # Generate answer using LLM
                print(f"Question: {question}\n")
                print("Generating answer...")
                
                answer = generate_answer(question, results)
                print(f"\nAnswer:\n{answer}\n")
                
            except requests.ConnectionError:
                print("⚠ Ollama is not running. Showing retrieval-only results:\n")
                print(f"Question: {question}\n")
                context = "\n\n".join([r['content'][:200] for r in results])
                print(f"Retrieved Context:\n{context}\n")
                print("\nTo enable LLM answers:")
                print("  1. Install Ollama: https://ollama.ai")
                print("  2. Run: ollama serve")
                print("  3. In another terminal: ollama pull mistral")
                
        except Exception as e:
            print(f"⚠ Could not generate answer: {e}")
            print("Showing retrieved documents as fallback.\n")
        
        # Step 4: Try more questions
        print_section("Step 4: Try Different Questions")
        
        sample_questions = [
            "What is machine learning?",
            "How does Python compare to other languages?",
            "What are the main types of learning in ML?"
        ]
        
        print("Sample questions you can ask:\n")
        for q in sample_questions:
            print(f"  • {q}")
        
        print("\n")
        
        # Step 5: API Usage
        print_section("Step 5: Using the REST API")
        
        print("You can also query the system via REST API:\n")
        print("curl -X POST 'http://localhost:8000/api/query' \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{")
        print('    "question": "What is Python?",')
        print('    "top_k": 3')
        print("  }'")
        
        print("\n\nAPI Documentation:")
        print("  http://localhost:8000/docs")
        
        print("\n")
        
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def demo_ingest_flow():
    """Show the ingestion flow"""
    print_header("Document Ingestion Flow")
    
    try:
        from ingest import IngestionPipeline
        
        print("The ingestion pipeline follows these steps:\n")
        
        steps = [
            ("Document Loading", "Load PDFs, TXT, Markdown files from specified directory"),
            ("Text Processing", "Split documents into chunks (500 tokens, 100 token overlap)"),
            ("Embedding Generation", "Convert text chunks to 384-dimensional vectors"),
            ("Vector Indexing", "Store vectors in FAISS index for fast retrieval"),
            ("Metadata Storage", "Save document metadata for later reference"),
        ]
        
        for i, (step, description) in enumerate(steps, 1):
            print(f"{i}. {step}")
            print(f"   {description}\n")
        
        print("To ingest documents:")
        print("  python ingest.py --source data/")
        print("\nOr ingest a single file:")
        print("  python ingest.py --file data/document.pdf")
        
    except Exception as e:
        print(f"Error: {e}")

def demo_architecture():
    """Show system architecture"""
    print_header("System Architecture")
    
    architecture = """
PRESENTATION LAYER
├── FastAPI REST API (app.py)
│   ├── POST /api/query        - Query documents
│   ├── POST /api/ingest       - Ingest documents
│   └── GET /api/health        - Health check
│
└── Streamlit Web UI (ui.py)
    ├── File Upload
    ├── Query Interface
    └── Results Display

ORCHESTRATION LAYER
├── Ingestion Pipeline (ingest.py)
│   ├── Load Documents
│   ├── Process Text
│   ├── Generate Embeddings
│   └── Build Index
│
├── Query Pipeline
│   ├── Retrieve (retrieval.py)
│   ├── LLM Generate (llm.py)
│   └── Format Answer
│
└── Components
    ├── DocumentLoader (document_loader.py)
    ├── TextProcessor (text_processor.py)
    ├── EmbeddingManager (embedding.py)
    ├── Retriever (retrieval.py)
    └── LLMProvider (llm.py)

DATA LAYER
├── Document Store (Pickle files)
├── Vector Store (FAISS)
└── Embeddings (Sentence-Transformers)

LLM PROVIDERS
├── Ollama (Local, Free)
├── OpenAI (Cloud-based)
└── HuggingFace (Open-source)
"""
    
    print(architecture)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Interactive demo for Chat With Your Docs RAG system"
    )
    parser.add_argument(
        "--demo",
        choices=["basic", "ingest", "architecture", "all"],
        default="all",
        help="Which demo to run"
    )
    
    args = parser.parse_args()
    
    try:
        if args.demo in ["basic", "all"]:
            demo_basic_usage()
        
        if args.demo in ["ingest", "all"]:
            demo_ingest_flow()
        
        if args.demo in ["architecture", "all"]:
            demo_architecture()
        
        print_header("Demo Complete!")
        print("Next steps:")
        print("  1. Start the API: python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload")
        print("  2. Start the UI: streamlit run ui.py --server.port 8501")
        print("  3. Open http://localhost:8501 in your browser")
        print("")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted.")
        sys.exit(0)
