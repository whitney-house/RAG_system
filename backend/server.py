from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import time
import os
from dotenv import load_dotenv

# Import the RAG system
from rag_system import RecipeRAGSystem

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Recipe Assistant API",
    description="An API for a Recipe RAG (Retrieval-Augmented Generation) system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User's recipe-related question")
    top_k: Optional[int] = Field(3, description="Number of recipes to retrieve")

class FeedbackRequest(BaseModel):
    query_id: str = Field(..., description="Unique ID of the query")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5)")
    feedback: Optional[str] = Field(None, description="Optional feedback text")

# Response models
class ChatResponse(BaseModel):
    answer: str = Field(..., description="Generated answer to the user's question")
    sources: List[str] = Field(..., description="Recipe sources used for the answer")
    query_id: str = Field(..., description="Unique ID for this query")
    response_time: float = Field(..., description="Processing time in seconds")

# Request ID middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred", "type": type(exc).__name__},
    )

# Initialize the RAG system (with lazy loading)
_rag_system = None

def get_rag_system():
    """
    Lazily initialize the RAG system.
    This helps with faster API startup and better resource management.
    """
    global _rag_system
    if _rag_system is None:
        logger.info("Initializing RAG system")
        _rag_system = RecipeRAGSystem(
            embedding_model="sentence-transformers/all-MiniLM-L6-v2", 
            llm_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",  
            temperature=0.7
        )
    return _rag_system
   

# API endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, rag_system: RecipeRAGSystem = Depends(get_rag_system)):
    """
    Process a user query about recipes and return a generated response with sources.
    """
    start_time = time.time()
    query_id = f"query-{int(start_time)}"
    logger.info(f"Processing chat request {query_id}: {request.message}")
    
    try:
        # Retrieve relevant recipes
        retrieval_result = rag_system.retrieve(request.message, request.top_k)
        sources = retrieval_result["sources"]
        
        # Generate answer based on retrieved context
        answer = rag_system.generate_answer(request.message, sources)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        return {
            "answer": answer,
            "sources": sources,
            "query_id": query_id,
            "response_time": response_time
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback", status_code=201)
async def feedback_endpoint(request: FeedbackRequest):
    """
    Collect user feedback about the quality of responses.
    In a real implementation, this would store feedback in a database.
    """
    logger.info(f"Received feedback for query {request.query_id}: rating={request.rating}")
    # In a production system, you would store this feedback in a database
    return {"status": "Feedback received", "query_id": request.query_id}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {"status": "healthy", "timestamp": time.time()}
@app.get("/")
async def root():
    return {
        "message": "Welcome to Recipe Assistant API",
        "endpoints": {
            "/api/chat": "POST - Submit recipe questions",
            "/api/feedback": "POST - Submit feedback",
            "/health": "GET - Service health check",
            "/docs": "API documentation"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    logger.info(f"Starting API server on port {port}")
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=port, 
        log_level=log_level,
        reload=os.getenv("ENVIRONMENT", "production") == "development"
    )