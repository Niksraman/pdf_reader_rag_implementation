"""
Document loading and processing module
"""
from pathlib import Path
from typing import List, Optional
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
from logger import setup_logger

logger = setup_logger(__name__)

class DocumentLoader:
    """Handle loading documents from various formats"""
    
    SUPPORTED_FORMATS = {
        '.pdf': PyPDFLoader,
        '.txt': TextLoader,
        '.md': TextLoader,
    }
    
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        """
        Load a single document file
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_ext = path.suffix.lower()
        
        if file_ext not in DocumentLoader.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {list(DocumentLoader.SUPPORTED_FORMATS.keys())}"
            )
        
        try:
            loader_class = DocumentLoader.SUPPORTED_FORMATS[file_ext]
            loader = loader_class(file_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} pages from {path.name}")
            return documents
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def load_from_directory(directory_path: str) -> List[Document]:
        """
        Load all supported documents from a directory
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of all loaded Document objects
        """
        dir_path = Path(directory_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        documents = []
        supported_extensions = list(DocumentLoader.SUPPORTED_FORMATS.keys())
        
        # Find all supported files
        for ext in supported_extensions:
            files = list(dir_path.glob(f"*{ext}"))
            logger.info(f"Found {len(files)} files with extension {ext}")
            
            for file_path in files:
                try:
                    docs = DocumentLoader.load_document(str(file_path))
                    documents.extend(docs)
                except Exception as e:
                    logger.warning(f"Skipped file {file_path.name}: {str(e)}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """
        Check if a file format is supported
        
        Args:
            file_path: Path to check
            
        Returns:
            True if format is supported, False otherwise
        """
        ext = Path(file_path).suffix.lower()
        return ext in DocumentLoader.SUPPORTED_FORMATS
