"""
Main FastAPI Application
Personalized Networking Assistant Backend

Integrates all NLP services (event analyzer, topic generator, fact checker)
and provides REST API endpoints with local JSON persistence for history and feedback.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import our core services
from fact_checker import create_fact_checker, FactChecker
from event_analyzer import create_event_analyzer, EventAnalyzer
from topic_generator import create_topic_generator, TopicGenerator

# Initialize your real service class objects
fact_checker = create_fact_checker() if 'create_fact_checker' in globals() else FactChecker()
event_analyzer = create_event_analyzer() if 'create_event_analyzer' in globals() else EventAnalyzer()
topic_generator = create_topic_generator() if 'create_topic_generator' in globals() else TopicGenerator()
# ==================== CONFIGURATION ====================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data persistence paths
DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "history.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# ==================== PYDANTIC MODELS ====================

class AnalyzeEventRequest(BaseModel):
    """Request model for event analysis endpoint."""
    event_description: str = Field(..., min_length=5, max_length=1000)
    top_k: Optional[int] = Field(3, ge=1, le=10)
    threshold: Optional[float] = Field(0.1, ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_description": "AI for Sustainable Cities",
                "top_k": 3,
                "threshold": 0.1
            }
        }


class GenerateConversationRequest(BaseModel):
    """Request model for conversation generation endpoint."""
    event_description: str = Field(..., min_length=5, max_length=1000)
    themes: List[str] = Field(..., min_items=1, max_items=5)
    interests: List[str] = Field(..., min_items=1, max_items=10)
    num_starters: Optional[int] = Field(3, ge=1, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_description": "AI for Sustainable Cities",
                "themes": ["artificial intelligence", "sustainability"],
                "interests": ["climate change", "urban planning", "innovation"],
                "num_starters": 3
            }
        }


class FactCheckRequest(BaseModel):
    """Request model for fact-checking endpoint."""
    query: str = Field(..., min_length=3, max_length=200)
    max_summary_length: Optional[int] = Field(300, ge=50, le=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "blockchain in healthcare",
                "max_summary_length": 300
            }
        }


class FeedbackRequest(BaseModel):
    """Request model for feedback submission endpoint."""
    item_id: str = Field(..., min_length=1)
    feedback_type: str = Field(..., pattern="^(thumbs_up|thumbs_down)$")
    notes: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "item_id": "conv_12345",
                "feedback_type": "thumbs_up",
                "notes": "Great conversation starter!"
            }
        }


# ==================== RESPONSE MODELS ====================

class ThemeResult(BaseModel):
    """Individual theme result."""
    label: str
    score: float


class AnalyzeEventResponse(BaseModel):
    """Response model for event analysis."""
    event_description: str
    extracted_themes: List[ThemeResult]
    primary_theme: Optional[str]
    error: Optional[str]


class ConversationStarter(BaseModel):
    """Individual conversation starter."""
    id: str
    starter: str
    generated_at: str


class GenerateConversationResponse(BaseModel):
    """Response model for conversation generation."""
    conversation_id: str
    event_description: str
    themes: List[str]
    interests: List[str]
    conversation_starters: List[ConversationStarter]
    num_generated: int
    generated_at: str
    error: Optional[str]


class FactCheckResult(BaseModel):
    """Response model for fact-checking."""
    found: bool
    title: Optional[str]
    summary: Optional[str]
    url: Optional[str]
    error: Optional[str]


class HistoryEntry(BaseModel):
    """Individual history entry."""
    id: str
    type: str
    event_description: str
    themes: Optional[List[str]]
    interests: Optional[List[str]]
    content: Dict[str, Any]
    created_at: str


class HistoryResponse(BaseModel):
    """Response model for history retrieval."""
    total_entries: int
    entries: List[HistoryEntry]


class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    feedback_id: str
    item_id: str
    feedback_type: str
    submitted_at: str
    message: str


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    services: Dict[str, bool]


# ==================== JSON FILE HANDLERS ====================

class JSONPersistence:
    """
    Handles reading and writing JSON files with robust error handling.
    Manages edge cases like missing files, corrupted JSON, etc.
    """
    
    @staticmethod
    def ensure_file_exists(file_path: Path, default_data: Any = None) -> None:
        """
        Ensure a JSON file exists; create with default data if it doesn't.
        
        Args:
            file_path (Path): Path to JSON file
            default_data (Any): Data to write if file doesn't exist (default: empty list)
        """
        if not file_path.exists():
            logger.info(f"Creating new file: {file_path}")
            if default_data is None:
                default_data = []
            try:
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
                logger.info(f"Successfully created {file_path}")
            except Exception as e:
                logger.error(f"Failed to create {file_path}: {str(e)}")
                raise
    
    @staticmethod
    def read_json(file_path: Path, default_data: Any = None) -> Any:
        """
        Read JSON file with error handling for corruption/missing files.
        
        Args:
            file_path (Path): Path to JSON file
            default_data (Any): Data to return if file cannot be read
        
        Returns:
            Any: Parsed JSON data or default_data on error
        """
        if default_data is None:
            default_data = []
        
        # Ensure file exists
        JSONPersistence.ensure_file_exists(file_path, default_data)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.debug(f"Successfully read {file_path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON in {file_path}: {str(e)}")
            logger.info(f"Returning default data for {file_path}")
            return default_data
        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")
            return default_data
    
    @staticmethod
    def write_json(file_path: Path, data: Any) -> bool:
        """
        Write data to JSON file with error handling.
        
        Args:
            file_path (Path): Path to JSON file
            data (Any): Data to write
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.debug(f"Successfully wrote to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing to {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def append_to_json(file_path: Path, new_entry: Dict[str, Any]) -> bool:
        """
        Append a new entry to a JSON array file.
        
        Args:
            file_path (Path): Path to JSON file
            new_entry (Dict[str, Any]): Entry to append
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing data
            data = JSONPersistence.read_json(file_path, [])
            
            # Ensure data is a list
            if not isinstance(data, list):
                logger.warning(f"{file_path} contains non-list data. Resetting to list.")
                data = []
            
            # Append new entry
            data.append(new_entry)
            
            # Write back
            return JSONPersistence.write_json(file_path, data)
        
        except Exception as e:
            logger.error(f"Error appending to {file_path}: {str(e)}")
            return False


# ==================== SERVICE INITIALIZATION ====================

def initialize_services():
    """
    Initialize all NLP services with error handling.
    
    Returns:
        tuple: (fact_checker, event_analyzer, topic_generator) instances
    
    Raises:
        RuntimeError: If critical services fail to initialize
    """
    logger.info("Initializing NLP services...")
    
    try:
        fact_checker = create_fact_checker()
        logger.info("✓ FactChecker initialized")
    except Exception as e:
        logger.error(f"Failed to initialize FactChecker: {str(e)}")
        raise RuntimeError(f"FactChecker initialization failed: {str(e)}")
    
    try:
        event_analyzer = create_event_analyzer()
        logger.info("✓ EventAnalyzer initialized")
    except Exception as e:
        logger.error(f"Failed to initialize EventAnalyzer: {str(e)}")
        raise RuntimeError(f"EventAnalyzer initialization failed: {str(e)}")
    
    try:
        topic_generator = create_topic_generator()
        logger.info("✓ TopicGenerator initialized")
    except Exception as e:
        logger.error(f"Failed to initialize TopicGenerator: {str(e)}")
        raise RuntimeError(f"TopicGenerator initialization failed: {str(e)}")
    
    logger.info("All services initialized successfully")
    return fact_checker, event_analyzer, topic_generator


# ==================== FASTAPI APPLICATION ====================

app = FastAPI(
    title="Personalized Networking Assistant API",
    description="AI-powered conversation starters for networking events",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    fact_checker, event_analyzer, topic_generator = initialize_services()
    services_ready = True
except Exception as e:
    logger.error(f"Service initialization failed: {str(e)}")
    services_ready = False


# ==================== UTILITY FUNCTIONS ====================

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix."""
    unique_id = str(uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id


# ==================== HEALTH CHECK ENDPOINT ====================

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify all services are operational.
    
    Returns:
        HealthCheckResponse: Status of all services
    """
    return HealthCheckResponse(
        status="healthy" if services_ready else "degraded",
        timestamp=get_current_timestamp(),
        services={
            "fact_checker": True if fact_checker else False,
            "event_analyzer": True if event_analyzer else False,
            "topic_generator": True if topic_generator else False,
        }
    )


# ==================== ANALYZE EVENT ENDPOINT ====================

@app.post("/analyze-event", response_model=AnalyzeEventResponse)
async def analyze_event(request: AnalyzeEventRequest):
    """
    Analyze an event description and extract relevant themes.
    
    Uses DistilBERT for zero-shot classification to identify themes
    aligned with the event description.
    
    Args:
        request (AnalyzeEventRequest): Event description and parameters
    
    Returns:
        AnalyzeEventResponse: Extracted themes with confidence scores
    
    Raises:
        HTTPException: If services are unavailable or analysis fails
    """
    if not services_ready or not event_analyzer:
        logger.error("EventAnalyzer service not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Event analyzer service is not available"
        )
    
    try:
        logger.info(f"Analyzing event: '{request.event_description[:50]}...'")
        
        # Call the event analyzer service
        result = event_analyzer.analyze_event(
            event_description=request.event_description,
            top_k=request.top_k,
            threshold=request.threshold
        )
        
        # Check for errors
        if result['error']:
            logger.warning(f"Event analysis error: {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['error']
            )
        
        # Transform themes for response
        themes = [
            ThemeResult(label=t['label'], score=t['score'])
            for t in result['extracted_themes']
        ]
        
        logger.info(f"Successfully analyzed event. Themes: {[t.label for t in themes]}")
        
        return AnalyzeEventResponse(
            event_description=result['event_description'],
            extracted_themes=themes,
            primary_theme=result['primary_theme'],
            error=None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing event: {str(e)}"
        )


# ==================== GENERATE CONVERSATION ENDPOINT ====================

@app.post("/generate-conversation", response_model=GenerateConversationResponse)
async def generate_conversation(request: GenerateConversationRequest):
    """
    Generate conversation starters based on event themes and user interests.
    
    Uses GPT-2 text generation to create natural, contextual conversation
    prompts. Results are automatically logged to history.json.
    
    Args:
        request (GenerateConversationRequest): Event and user details
    
    Returns:
        GenerateConversationResponse: Generated conversation starters with ID
    
    Raises:
        HTTPException: If services unavailable or generation fails
    """
    if not services_ready or not topic_generator:
        logger.error("TopicGenerator service not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Topic generator service is not available"
        )
    
    try:
        logger.info(
            f"Generating conversation for event: '{request.event_description[:50]}...'"
        )
        
        # Call the topic generator service
        result = topic_generator.generate_starters(
            themes=request.themes,
            interests=request.interests,
            num_starters=request.num_starters
        )
        
        # Check for errors (but continue even if there was an error)
        if result['error']:
            logger.warning(f"Generation warning: {result['error']}")
        
        # Generate unique conversation ID and timestamp
        conversation_id = generate_id("conv")
        timestamp = get_current_timestamp()
        
        # Create conversation starter objects with IDs
        conversation_starters = [
            ConversationStarter(
                id=generate_id("starter"),
                starter=starter,
                generated_at=timestamp
            )
            for starter in result['conversation_starters']
        ]
        
        # Prepare history entry
        history_entry = {
            "id": conversation_id,
            "type": "conversation_generation",
            "event_description": request.event_description,
            "themes": request.themes,
            "interests": request.interests,
            "content": {
                "conversation_starters": [
                    {"id": cs.id, "starter": cs.starter}
                    for cs in conversation_starters
                ],
                "num_generated": len(conversation_starters)
            },
            "created_at": timestamp
        }
        
        # Log to history.json
        if JSONPersistence.append_to_json(HISTORY_FILE, history_entry):
            logger.info(f"Conversation logged with ID: {conversation_id}")
        else:
            logger.warning(f"Failed to log conversation {conversation_id}")
        
        logger.info(
            f"Successfully generated {len(conversation_starters)} conversation starters"
        )
        
        return GenerateConversationResponse(
            conversation_id=conversation_id,
            event_description=request.event_description,
            themes=request.themes,
            interests=request.interests,
            conversation_starters=conversation_starters,
            num_generated=len(conversation_starters),
            generated_at=timestamp,
            error=result.get('error')
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating conversation: {str(e)}"
        )


# ==================== FACT CHECK ENDPOINT ====================

@app.post("/fact-check", response_model=FactCheckResult)
async def fact_check(request: FactCheckRequest):
    """
    Retrieve and summarize factual information from Wikipedia.
    
    Quick fact verification for networking preparation using Wikipedia API.
    
    Args:
        request (FactCheckRequest): Topic to fact-check
    
    Returns:
        FactCheckResult: Wikipedia summary with URL and status
    
    Raises:
        HTTPException: If services unavailable
    """
    if not services_ready or not fact_checker:
        logger.error("FactChecker service not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fact checker service is not available"
        )
    
    try:
        logger.info(f"Fact-checking: '{request.query}'")
        
        # Call the fact checker service
        result = fact_checker.check_fact(
            query=request.query,
            max_summary_length=request.max_summary_length
        )
        
        logger.info(
            f"Fact-check result: found={result['found']}, title={result.get('title')}"
        )
        
        return FactCheckResult(
            found=result['found'],
            title=result.get('title'),
            summary=result.get('summary'),
            url=result.get('url'),
            error=result.get('error')
        )
    
    except Exception as e:
        logger.error(f"Error in fact_check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fact-checking: {str(e)}"
        )


# ==================== HISTORY ENDPOINT ====================

@app.get("/history", response_model=HistoryResponse)
async def get_history():
    """
    Retrieve all entries from conversation history.
    
    Returns all previously generated conversations and actions from history.json.
    
    Returns:
        HistoryResponse: All history entries with metadata
    """
    try:
        logger.info("Retrieving conversation history")
        
        # Read history file
        history_data = JSONPersistence.read_json(HISTORY_FILE, [])
        
        # Validate and transform data
        entries = []
        if isinstance(history_data, list):
            for entry in history_data:
                if isinstance(entry, dict):
                    try:
                        history_entry = HistoryEntry(
                            id=entry.get('id', ''),
                            type=entry.get('type', ''),
                            event_description=entry.get('event_description', ''),
                            themes=entry.get('themes', []),
                            interests=entry.get('interests', []),
                            content=entry.get('content', {}),
                            created_at=entry.get('created_at', '')
                        )
                        entries.append(history_entry)
                    except Exception as e:
                        logger.warning(f"Skipping invalid history entry: {str(e)}")
                        continue
        
        logger.info(f"Retrieved {len(entries)} history entries")
        
        return HistoryResponse(
            total_entries=len(entries),
            entries=entries
        )
    
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {str(e)}"
        )


# ==================== FEEDBACK ENDPOINT ====================

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback (thumbs up/down) on generated content.
    
    Appends feedback entries to feedback.json for continuous improvement.
    
    Args:
        request (FeedbackRequest): Feedback with item ID and type
    
    Returns:
        FeedbackResponse: Confirmation of feedback submission
    
    Raises:
        HTTPException: If feedback cannot be recorded
    """
    try:
        logger.info(
            f"Submitting feedback: item_id={request.item_id}, "
            f"type={request.feedback_type}"
        )
        
        # Generate feedback entry
        feedback_id = generate_id("feedback")
        timestamp = get_current_timestamp()
        
        feedback_entry = {
            "id": feedback_id,
            "item_id": request.item_id,
            "feedback_type": request.feedback_type,
            "notes": request.notes or "",
            "submitted_at": timestamp
        }
        
        # Append to feedback file
        if not JSONPersistence.append_to_json(FEEDBACK_FILE, feedback_entry):
            logger.error(f"Failed to write feedback {feedback_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to record feedback"
            )
        
        logger.info(f"Feedback recorded with ID: {feedback_id}")
        
        return FeedbackResponse(
            feedback_id=feedback_id,
            item_id=request.item_id,
            feedback_type=request.feedback_type,
            submitted_at=timestamp,
            message="Feedback recorded successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting feedback: {str(e)}"
        )


# ==================== ROOT ENDPOINT ====================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Personalized Networking Assistant API",
        "version": "1.0.0",
        "status": "running" if services_ready else "degraded",
        "endpoints": {
            "health": "/health",
            "analyze_event": "POST /analyze-event",
            "generate_conversation": "POST /generate-conversation",
            "fact_check": "POST /fact-check",
            "history": "GET /history",
            "feedback": "POST /feedback",
            "docs": "/docs"
        }
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler with logging."""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": get_current_timestamp()
    }


# ==================== STARTUP EVENTS ====================

@app.on_event("startup")
async def startup_event():
    """Initialize data persistence files on startup."""
    logger.info("Starting up Personalized Networking Assistant API")
    
    # Ensure history and feedback files exist
    JSONPersistence.ensure_file_exists(HISTORY_FILE, [])
    JSONPersistence.ensure_file_exists(FEEDBACK_FILE, [])
    
    logger.info("Data persistence files initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Personalized Networking Assistant API")


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI server on http://localhost:8000")
    logger.info("API documentation available at http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
