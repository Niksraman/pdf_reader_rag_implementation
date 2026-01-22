
"""
FastAPI application for RAG system
"""
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from retrieval import search_docs
from llm import generate_answer
from ingest import ingest_documents
from config import API_HOST, API_PORT
from logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Chat With Your Docs - RAG System",
    description="A Retrieval-Augmented Generation system for document Q&A",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Request/Response Models ============

class QueryRequest(BaseModel):
    """Query request model"""
    question: str = Field(..., min_length=1, description="The question to ask")
    top_k: int = Field(3, ge=1, le=10, description="Number of top documents to retrieve")

class QueryResponse(BaseModel):
    """Query response model"""
    answer: str = Field(..., description="The generated answer")
    sources: List[str] = Field(..., description="List of source documents used")
    num_sources: int = Field(..., description="Number of sources used")

class IngestRequest(BaseModel):
    """Ingestion request model"""
    path: str = Field(..., description="Path to file or directory to ingest")

class IngestResponse(BaseModel):
    """Ingestion response model"""
    status: str = Field(..., description="Status of ingestion")
    message: str = Field(..., description="Status message")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

# ============ API Endpoints ============

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - service health check"""
    return HealthResponse(status="healthy", version="1.0.0")

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Ask a question and get an answer from documents
    
    Args:
        request: Query request with question
        
    Returns:
        QueryResponse with answer and sources
    """
    try:
        logger.info(f"Processing question: {request.question}")
        
        # Retrieve relevant documents
        documents = search_docs(request.question, top_k=request.top_k)
        
        if not documents:
            logger.warning(f"No documents found for query: {request.question}")
            return QueryResponse(
                answer="No relevant documents found to answer this question.",
                sources=[],
                num_sources=0
            )
        
        # Generate answer
        answer = generate_answer(request.question, documents)
        
        logger.info(f"Generated answer ({len(answer)} chars) with {len(documents)} sources")
        
        return QueryResponse(
            answer=answer,
            sources=documents,
            num_sources=len(documents)
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    """
    Ingest documents from a file or directory
    
    Args:
        request: Ingest request with path
        background_tasks: Background tasks for async processing
        
    Returns:
        IngestResponse with status
    """
    try:
        if not os.path.exists(request.path):
            raise ValueError(f"Path does not exist: {request.path}")
        
        logger.info(f"Starting ingestion from: {request.path}")
        
        # Add ingestion task to background
        background_tasks.add_task(ingest_documents, request.path)
        
        return IngestResponse(
            status="processing",
            message=f"Ingestion started for path: {request.path}"
        )
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ingest/sync", response_model=IngestResponse)
async def ingest_sync(request: IngestRequest):
    """
    Synchronously ingest documents (waits for completion)
    
    Args:
        request: Ingest request with path
        
    Returns:
        IngestResponse with status
    """
    try:
        if not os.path.exists(request.path):
            raise ValueError(f"Path does not exist: {request.path}")
        
        logger.info(f"Starting synchronous ingestion from: {request.path}")
        ingest_documents(request.path)
        
        return IngestResponse(
            status="completed",
            message=f"Successfully ingested documents from: {request.path}"
        )
    except Exception as e:
        logger.error(f"Error in ingest/sync endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ============ Main ============

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting RAG API server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )
