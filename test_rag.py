#!/usr/bin/env python
"""
Test script for RAG system
Run: python test_rag.py
"""

import sys
import json
from pathlib import Path

def test_imports():
    """Test all module imports"""
    print("\n" + "="*60)
    print("TEST 1: Checking Module Imports")
    print("="*60)
    
    modules_to_test = [
        ("config", "Configuration module"),
        ("logger", "Logger module"),
        ("document_loader", "Document loader"),
        ("text_processor", "Text processor"),
        ("embedding", "Embedding manager"),
        ("retrieval", "Retrieval module"),
        ("ingest", "Ingestion pipeline"),
        ("llm", "LLM integration"),
        ("app", "FastAPI application"),
    ]
    
    failed = []
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {description:30} [{module_name}]")
        except ImportError as e:
            print(f"✗ {description:30} [{module_name}]")
            print(f"  Error: {str(e)}")
            failed.append(module_name)
    
    if failed:
        print(f"\n❌ {len(failed)} module(s) failed to import")
        return False
    else:
        print(f"\n✅ All modules imported successfully!")
        return True

def test_config():
    """Test configuration"""
    print("\n" + "="*60)
    print("TEST 2: Checking Configuration")
    print("="*60)
    
    try:
        from config import (
            PROJECT_ROOT, DATA_DIR, VECTOR_STORE_DIR,
            EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP,
            LLM_TYPE, OLLAMA_MODEL, API_HOST, API_PORT
        )
        
        print(f"Project Root:         {PROJECT_ROOT}")
        print(f"Data Directory:       {DATA_DIR}")
        print(f"Vector Store Dir:     {VECTOR_STORE_DIR}")
        print(f"Embedding Model:      {EMBEDDING_MODEL}")
        print(f"Chunk Size:           {CHUNK_SIZE}")
        print(f"Chunk Overlap:        {CHUNK_OVERLAP}")
        print(f"LLM Type:             {LLM_TYPE}")
        print(f"Ollama Model:         {OLLAMA_MODEL}")
        print(f"API Host:             {API_HOST}")
        print(f"API Port:             {API_PORT}")
        
        print(f"\n✅ Configuration loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error loading configuration: {str(e)}")
        return False

def test_directories():
    """Test directory structure"""
    print("\n" + "="*60)
    print("TEST 3: Checking Directory Structure")
    print("="*60)
    
    from config import PROJECT_ROOT, DATA_DIR, VECTOR_STORE_DIR
    
    dirs_to_check = [
        (PROJECT_ROOT, "Project Root"),
        (DATA_DIR, "Data Directory"),
        (VECTOR_STORE_DIR, "Vector Store"),
    ]
    
    all_ok = True
    for dir_path, description in dirs_to_check:
        if dir_path.exists():
            print(f"✓ {description:25} {dir_path}")
        else:
            print(f"✗ {description:25} {dir_path} (creating...)")
            dir_path.mkdir(parents=True, exist_ok=True)
            if dir_path.exists():
                print(f"  ✓ Created successfully")
            else:
                print(f"  ✗ Failed to create")
                all_ok = False
    
    if all_ok:
        print(f"\n✅ All directories OK!")
    else:
        print(f"\n⚠️  Some directories needed creation")
    
    return all_ok

def test_logger():
    """Test logging functionality"""
    print("\n" + "="*60)
    print("TEST 4: Testing Logger")
    print("="*60)
    
    try:
        from logger import setup_logger
        
        logger = setup_logger("test")
        logger.info("Test info message")
        logger.warning("Test warning message")
        
        print(f"✓ Logger initialized")
        print(f"✓ Logging statements executed")
        print(f"\n✅ Logger working correctly!")
        return True
    except Exception as e:
        print(f"✗ Logger error: {str(e)}")
        return False

def test_embeddings():
    """Test embedding manager"""
    print("\n" + "="*60)
    print("TEST 5: Testing Embedding Manager")
    print("="*60)
    
    try:
        from embedding import EmbeddingManager
        
        print("Initializing embedding manager...")
        em = EmbeddingManager()
        print("✓ EmbeddingManager initialized")
        
        # Test document embedding
        print("Testing document embedding...")
        docs = ["Hello world", "This is a test"]
        embeddings = em.embed_documents(docs)
        print(f"✓ Embedded {len(docs)} documents")
        print(f"  Embedding shape: {embeddings.shape}")
        
        # Test query embedding
        print("Testing query embedding...")
        query_emb = em.embed_query("Hello")
        print(f"✓ Embedded query")
        print(f"  Embedding shape: {query_emb.shape}")
        
        print(f"\n✅ Embedding manager working correctly!")
        return True
    except Exception as e:
        print(f"✗ Embedding error: {str(e)}")
        print(f"  Note: This requires sentence-transformers to be installed")
        return False

def test_document_loader():
    """Test document loader"""
    print("\n" + "="*60)
    print("TEST 6: Testing Document Loader")
    print("="*60)
    
    try:
        from document_loader import DocumentLoader
        from config import DATA_DIR
        
        # Check supported formats
        supported = DocumentLoader.SUPPORTED_FORMATS
        print(f"Supported formats: {list(supported.keys())}")
        
        # Check if data directory has documents
        if DATA_DIR.exists():
            files = list(DATA_DIR.glob("*"))
            if files:
                print(f"\nFound {len(files)} files in {DATA_DIR}:")
                for f in files[:5]:  # Show first 5
                    print(f"  - {f.name}")
            else:
                print(f"\nNo documents found in {DATA_DIR}")
                print("(This is OK - add documents to test ingestion)")
        
        print(f"\n✅ Document loader initialized!")
        return True
    except Exception as e:
        print(f"✗ Document loader error: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n" + "="*60)
    print("TEST 7: Testing API Endpoints")
    print("="*60)
    
    try:
        from app import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        print("Testing GET /health...")
        response = client.get("/health")
        if response.status_code == 200:
            print(f"✓ Health check passed: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
        
        print(f"\n✅ API endpoints working!")
        return True
    except Exception as e:
        print(f"✗ API test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RAG SYSTEM TEST SUITE")
    print("="*60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Directories", test_directories),
        ("Logger", test_logger),
        ("Embeddings", test_embeddings),
        ("Document Loader", test_document_loader),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n⚠️  Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
