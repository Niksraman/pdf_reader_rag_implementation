"""
Text chunking and processing module
"""
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP
from logger import setup_logger

logger = setup_logger(__name__)

class TextProcessor:
    """Handle text chunking and processing"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialize text processor
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        logger.info(f"Initialized TextProcessor with chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        try:
            chunks = self.splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking documents: {str(e)}")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split raw text into chunks
        
        Args:
            text: Raw text to chunk
            
        Returns:
            List of text chunks
        """
        try:
            chunks = self.splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            raise
