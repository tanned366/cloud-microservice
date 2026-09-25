"""Test suite verifying endpoints, validations, sentiment analysis, and transformations."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_1_root_endpoint():
    """Test 1: Root endpoint returns 200 OK and valid service metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Cloud-Native Text Analytics Microservice"
    assert data["status"] == "online"
    assert "version" in data
    assert "documentation" in data


def test_2_health_check_endpoint():
    """Test 2: Health check endpoint returns 200 OK and uptime metrics."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["uptime_seconds"] >= 0
    assert data["total_requests_processed"] >= 1
    assert "environment" in data


def test_3_analyze_positive_sentiment():
    """Test 3: Valid positive text payload returns correct sentiment and word counts."""
    payload = {
        "text": "FastAPI and Docker make building cloud microservices amazing, awesome, and great!"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 11
    assert data["character_count"] > 0
    assert data["sentiment"] == "positive"
    assert data["sentiment_score"] > 0.15
    assert data["reading_time_seconds"] > 0


def test_4_analyze_negative_sentiment():
    """Test 4: Negative text returns negative sentiment classification."""
    payload = {
        "text": "This server is experiencing terrible slow response and awful horrible failure."
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"
    assert data["sentiment_score"] < -0.15


def test_5_analyze_empty_payload_validation():
    """Test 5: Empty payload or only whitespace triggers 422 Unprocessable Entity."""
    response = client.post("/analyze", json={"text": "   "})
    assert response.status_code == 422


def test_6_transform_uppercase():
    """Test 6: Transform endpoint correctly converts text to uppercase."""
    payload = {
        "text": "cloud computing",
        "operation": "uppercase"
    }
    response = client.post("/transform", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "CLOUD COMPUTING"
    assert data["operation"] == "uppercase"
    assert data["length"] == 15


def test_7_transform_reverse():
    """Test 7: Transform endpoint reverses input string."""
    payload = {
        "text": "docker",
        "operation": "reverse"
    }
    response = client.post("/transform", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "rekcod"


def test_8_transform_invalid_operation():
    """Test 8: Invalid transformation operation returns 400 Bad Request."""
    payload = {
        "text": "hello",
        "operation": "invalid_op_code"
    }
    response = client.post("/transform", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Unsupported operation" in data["detail"]
