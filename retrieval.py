
"""
Retrieval module - search and retrieve documents
"""
from typing import List
import numpy as np
from embedding import EmbeddingManager, VectorStore
from config import TOP_K_RESULTS
from logger import setup_logger

logger = setup_logger(__name__)

class Retriever:
    """Handle document retrieval from vector store"""
    
    def __init__(self, top_k: int = TOP_K_RESULTS):
        """
        Initialize retriever
        
        Args:
            top_k: Number of top results to return
        """
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        self.top_k = top_k
        self.documents = None
        logger.info(f"Initialized Retriever with top_k={top_k}")
    
    def load_index(self) -> bool:
        """
        Load vector store and documents
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.documents = self.vector_store.load()
            logger.info(f"Loaded {len(self.documents)} documents from vector store")
            return True
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return False
    
    def retrieve(self, query: str, top_k: int = None) -> List[dict]:
        """
        Retrieve top-k relevant documents for a query
        
        Args:
            query: Query text
            top_k: Number of results to return (overrides default)
            
        Returns:
            List of dictionaries with document content and metadata
        """
        try:
            if self.documents is None:
                if not self.load_index():
                    raise RuntimeError("Vector store not available")
            
            k = top_k or self.top_k
            
            # Generate query embedding
            query_embedding = self.embedding_manager.embed_query(query)
            
            # Search vector store
            indices = self.vector_store.search(query_embedding, top_k=k)
            
            # Retrieve documents
            results = []
            for idx in indices:
                if 0 <= idx < len(self.documents):
                    doc = self.documents[idx]
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata if hasattr(doc, 'metadata') else {},
                        "index": idx
                    })
            
            logger.info(f"Retrieved {len(results)} documents for query")
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
    
    def retrieve_text_only(self, query: str, top_k: int = None) -> List[str]:
        """
        Retrieve only the text content of top-k relevant documents
        
        Args:
            query: Query text
            top_k: Number of results to return
            
        Returns:
            List of document texts
        """
        try:
            results = self.retrieve(query, top_k)
            return [result["content"] for result in results]
        except Exception as e:
            logger.error(f"Error in retrieve_text_only: {str(e)}")
            raise


# Global retriever instance
_retriever = None

def get_retriever(top_k: int = TOP_K_RESULTS) -> Retriever:
    """
    Get or create global retriever instance
    
    Args:
        top_k: Number of top results
        
    Returns:
        Retriever instance
    """
    global _retriever
    if _retriever is None:
        _retriever = Retriever(top_k=top_k)
    return _retriever

def search_docs(query: str, top_k: int = TOP_K_RESULTS) -> List[str]:
    """
    Convenience function to search documents
    
    Args:
        query: Query text
        top_k: Number of results
        
    Returns:
        List of relevant document texts
    """
    retriever = get_retriever(top_k=top_k)
    return retriever.retrieve_text_only(query, top_k=top_k)
