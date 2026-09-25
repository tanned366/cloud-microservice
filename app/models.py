"""Data models and schemas for the Text Analytics Microservice."""
from pydantic import BaseModel, Field
from typing import Dict, Optional


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="The input text to analyze")
    language: Optional[str] = Field("en", description="Language code (e.g. en)")


class TextAnalysisResponse(BaseModel):
    text: str
    character_count: int
    word_count: int
    sentence_count: int
    sentiment: str
    sentiment_score: float
    reading_time_seconds: float


class TextTransformRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="The text to transform")
    operation: str = Field(..., description="Transformation type: uppercase, lowercase, reverse, titlecase")


class TextTransformResponse(BaseModel):
    original_text: str
    operation: str
    result: str
    length: int


class HealthStatusResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    total_requests_processed: int
    environment: str
