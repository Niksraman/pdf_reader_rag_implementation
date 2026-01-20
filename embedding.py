"""
Embedding generation and vector store management
"""
import pickle
from typing import List, Tuple
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config import EMBEDDING_MODEL, VECTOR_STORE_FILE, METADATA_FILE
from logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingManager:
    """Manage embeddings and vector operations"""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize embedding manager
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        try:
            self.model_name = model_name
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            logger.info(f"Initialized EmbeddingManager with model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            raise
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of documents
        
        Args:
            documents: List of document texts
            
        Returns:
            numpy array of embeddings
        """
        try:
            if not documents:
                raise ValueError("Document list cannot be empty")
            
            embeddings = self.embeddings.embed_documents(documents)
            embeddings_array = np.array(embeddings).astype('float32')
            logger.info(f"Generated embeddings for {len(documents)} documents")
            return embeddings_array
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a query
        
        Args:
            query: Query text
            
        Returns:
            numpy array of query embedding
        """
        try:
            embedding = self.embeddings.embed_query(query)
            return np.array(embedding).astype('float32')
        except Exception as e:
            logger.error(f"Error embedding query: {str(e)}")
            raise

class VectorStore:
    """Manage vector storage and retrieval using FAISS"""
    
    def __init__(self):
        """Initialize vector store"""
        try:
            import faiss
            self.faiss = faiss
            self.index = None
            self.documents = None
            logger.info("Initialized VectorStore")
        except ImportError:
            logger.error("FAISS not installed. Install with: pip install faiss-cpu")
            raise
    
    def create_index(self, embeddings: np.ndarray) -> None:
        """
        Create FAISS index from embeddings
        
        Args:
            embeddings: numpy array of embeddings
        """
        try:
            dimension = embeddings.shape[1]
            self.index = self.faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            logger.info(f"Created FAISS index with {embeddings.shape[0]} vectors of dimension {dimension}")
        except Exception as e:
            logger.error(f"Error creating index: {str(e)}")
            raise
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[int]:
        """
        Search for similar documents
        
        Args:
            query_embedding: numpy array of query embedding
            top_k: number of top results to return
            
        Returns:
            List of document indices
        """
        try:
            if self.index is None:
                raise ValueError("Index not initialized. Create index first.")
            
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, top_k)
            logger.info(f"Search returned {len(indices[0])} results")
            return indices[0].tolist()
        except Exception as e:
            logger.error(f"Error searching index: {str(e)}")
            raise
    
    def save(self, documents: List[Document]) -> None:
        """
        Save index and documents to disk
        
        Args:
            documents: List of documents to save
        """
        try:
            if self.index is None:
                raise ValueError("Index not initialized")
            
            VECTOR_STORE_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(VECTOR_STORE_FILE, 'wb') as f:
                pickle.dump(self.index, f)
            
            with open(METADATA_FILE, 'wb') as f:
                pickle.dump(documents, f)
            
            logger.info(f"Saved vector store to {VECTOR_STORE_FILE}")
            logger.info(f"Saved metadata to {METADATA_FILE}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load(self) -> List[Document]:
        """
        Load index and documents from disk
        
        Returns:
            List of documents
        """
        try:
            if not VECTOR_STORE_FILE.exists():
                raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_FILE}")
            
            if not METADATA_FILE.exists():
                raise FileNotFoundError(f"Metadata file not found at {METADATA_FILE}")
            
            with open(VECTOR_STORE_FILE, 'rb') as f:
                self.index = pickle.load(f)
            
            with open(METADATA_FILE, 'rb') as f:
                documents = pickle.load(f)
            
            logger.info(f"Loaded vector store from {VECTOR_STORE_FILE}")
            logger.info(f"Loaded {len(documents)} documents from {METADATA_FILE}")
            return documents
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
    
    def is_empty(self) -> bool:
        """Check if vector store is empty"""
        return self.index is None or self.index.ntotal == 0
