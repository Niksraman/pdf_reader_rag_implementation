
"""
Document ingestion pipeline - orchestrates loading, processing, and indexing
"""
from typing import List
from pathlib import Path
from langchain.schema import Document
from document_loader import DocumentLoader
from text_processor import TextProcessor
from embedding import EmbeddingManager, VectorStore
from config import DATA_DIR, TOP_K_RESULTS
from logger import setup_logger

logger = setup_logger(__name__)

class IngestionPipeline:
    """Orchestrate the document ingestion process"""
    
    def __init__(self):
        """Initialize ingestion pipeline"""
        self.loader = DocumentLoader()
        self.processor = TextProcessor()
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        logger.info("Initialized IngestionPipeline")
    
    def ingest_directory(self, directory_path: str) -> None:
        """
        Full ingestion pipeline from directory
        
        Args:
            directory_path: Path to directory containing documents
        """
        try:
            logger.info(f"Starting ingestion from directory: {directory_path}")
            
            # Load documents
            documents = self.loader.load_from_directory(directory_path)
            if not documents:
                logger.warning("No documents loaded from directory")
                return
            
            # Process into chunks
            chunks = self.processor.chunk_documents(documents)
            if not chunks:
                logger.warning("No chunks created from documents")
                return
            
            # Generate embeddings
            chunk_texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embedding_manager.embed_documents(chunk_texts)
            
            # Create and save index
            self.vector_store.create_index(embeddings)
            self.vector_store.save(chunks)
            
            logger.info("Ingestion pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error in ingestion pipeline: {str(e)}")
            raise
    
    def ingest_file(self, file_path: str) -> None:
        """
        Ingest a single file
        
        Args:
            file_path: Path to document file
        """
        try:
            logger.info(f"Starting ingestion of file: {file_path}")
            
            # Load document
            documents = self.loader.load_document(file_path)
            if not documents:
                logger.warning(f"No documents loaded from {file_path}")
                return
            
            # Check if vector store exists and load it
            documents_to_save = documents.copy()
            if not self.vector_store.is_empty():
                try:
                    existing_documents = self.vector_store.load()
                    documents_to_save = existing_documents + documents
                except:
                    logger.warning("Could not load existing vector store, starting fresh")
            
            # Process into chunks
            chunks = self.processor.chunk_documents(documents)
            if not chunks:
                logger.warning("No chunks created from document")
                return
            
            # For new file, we need to re-embed everything
            chunk_texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embedding_manager.embed_documents(chunk_texts)
            
            # Create and save index
            self.vector_store.create_index(embeddings)
            self.vector_store.save(chunks)
            
            logger.info("File ingestion completed successfully")
        except Exception as e:
            logger.error(f"Error ingesting file: {str(e)}")
            raise


def ingest_documents(source_path: str) -> None:
    """
    Convenience function to ingest documents
    
    Args:
        source_path: Path to file or directory
    """
    path = Path(source_path)
    pipeline = IngestionPipeline()
    
    if path.is_dir():
        pipeline.ingest_directory(source_path)
    elif path.is_file():
        pipeline.ingest_file(source_path)
    else:
        raise ValueError(f"Invalid path: {source_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest documents for RAG system")
    parser.add_argument(
        "--source",
        type=str,
        default=str(DATA_DIR),
        help="Path to document file or directory"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Ingest a specific file"
    )
    
    args = parser.parse_args()
    
    source = args.file if args.file else args.source
    ingest_documents(source)
