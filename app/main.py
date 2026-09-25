"""Main FastAPI application for Cloud-Native Text Analytics Microservice."""
import os
import time
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app import __version__
from app.models import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    TextTransformRequest,
    TextTransformResponse,
    HealthStatusResponse,
)
from app.utils import (
    analyze_sentiment,
    count_sentences,
    estimate_reading_time,
    perform_text_transformation,
)

START_TIME = time.time()
REQUEST_COUNTER = 0

app = FastAPI(
    title="Cloud-Native Text Analytics Microservice",
    description="A lightweight, production-ready microservice for real-time text analysis and transformations.",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for cross-origin frontend support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def track_requests(request, call_next):
    global REQUEST_COUNTER
    REQUEST_COUNTER += 1
    response = await call_next(request)
    return response


@app.get("/", tags=["General"])
def root():
    """Root endpoint welcoming clients and directing to interactive documentation."""
    return {
        "service": "Cloud-Native Text Analytics Microservice",
        "status": "online",
        "version": __version__,
        "documentation": "/docs",
        "timestamp": time.time(),
    }


@app.get("/health", response_model=HealthStatusResponse, tags=["Monitoring"])
def health_check():
    """Health check endpoint providing uptime and operational status."""
    uptime = round(time.time() - START_TIME, 2)
    env = os.getenv("ENVIRONMENT", "production")
    return HealthStatusResponse(
        status="healthy",
        version=__version__,
        uptime_seconds=uptime,
        total_requests_processed=REQUEST_COUNTER,
        environment=env,
    )


@app.post("/analyze", response_model=TextAnalysisResponse, tags=["Analytics"])
def analyze_text(payload: TextAnalysisRequest):
    """
    Analyzes input text for word count, character count, sentence count,
    sentiment classification, sentiment score, and estimated reading time.
    """
    raw_text = payload.text.strip()
    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Text content cannot be only whitespace."
        )

    words = raw_text.split()
    word_count = len(words)
    char_count = len(raw_text)
    sentence_count = count_sentences(raw_text)
    sentiment_label, score = analyze_sentiment(raw_text)
    reading_time = estimate_reading_time(word_count)

    return TextAnalysisResponse(
        text=raw_text,
        character_count=char_count,
        word_count=word_count,
        sentence_count=sentence_count,
        sentiment=sentiment_label,
        sentiment_score=score,
        reading_time_seconds=reading_time,
    )


@app.post("/transform", response_model=TextTransformResponse, tags=["Transformations"])
def transform_text(payload: TextTransformRequest):
    """
    Transforms text based on requested operation: uppercase, lowercase, reverse, titlecase.
    """
    try:
        transformed = perform_text_transformation(payload.text, payload.operation)
        return TextTransformResponse(
            original_text=payload.text,
            operation=payload.operation.lower(),
            result=transformed,
            length=len(transformed),
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
