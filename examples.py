"""
Example usage and testing module
"""
from ingest import IngestionPipeline
from retrieval import get_retriever
from llm import get_rag_chain
from logger import setup_logger

logger = setup_logger(__name__)

def example_ingest():
    """Example: Ingest documents from data directory"""
    print("\n" + "="*50)
    print("EXAMPLE: Document Ingestion")
    print("="*50)
    
    pipeline = IngestionPipeline()
    pipeline.ingest_directory("data")
    print("✅ Ingestion completed")

def example_retrieve():
    """Example: Retrieve documents for a query"""
    print("\n" + "="*50)
    print("EXAMPLE: Document Retrieval")
    print("="*50)
    
    retriever = get_retriever(top_k=3)
    
    query = "What is machine learning?"
    print(f"\nQuery: {query}")
    
    results = retriever.retrieve(query)
    
    print(f"\nFound {len(results)} relevant documents:\n")
    for i, result in enumerate(results, 1):
        print(f"--- Source {i} ---")
        print(result["content"][:200] + "...\n")

def example_rag():
    """Example: Full RAG chain"""
    print("\n" + "="*50)
    print("EXAMPLE: Full RAG Chain")
    print("="*50)
    
    # Retrieve documents
    retriever = get_retriever(top_k=3)
    query = "What is the main topic?"
    documents = retriever.retrieve_text_only(query)
    
    print(f"\nQuery: {query}")
    print(f"Retrieved {len(documents)} documents")
    
    # Generate answer
    rag_chain = get_rag_chain()
    answer = rag_chain.generate_answer(query, documents)
    
    print(f"\nAnswer:\n{answer}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        if example == "ingest":
            example_ingest()
        elif example == "retrieve":
            example_retrieve()
        elif example == "rag":
            example_rag()
        else:
            print(f"Unknown example: {example}")
    else:
        print("Usage: python examples.py [ingest|retrieve|rag]")
