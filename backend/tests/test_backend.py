import os
import json
import pytest
import httpx
from httpx import AsyncClient
from app import app, HISTORY_FILE, FEEDBACK_FILE

# Use a clean, isolated setup for testing data persistence
@pytest.fixture(autouse=True)
def setup_and_teardown_test_data():
    """Fixture to ensure a pristine data environment for each test run."""
    history_bak = f"{HISTORY_FILE}.bak"
    feedback_bak = f"{FEEDBACK_FILE}.bak"
    
    if os.path.exists(HISTORY_FILE):
        os.rename(HISTORY_FILE, history_bak)
    if os.path.exists(FEEDBACK_FILE):
        os.rename(FEEDBACK_FILE, feedback_bak)
        
    yield  # Run the actual test cases here
    
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)
        
    if os.path.exists(history_bak):
        os.rename(history_bak, HISTORY_FILE)
    if os.path.exists(feedback_bak):
        os.rename(feedback_bak, FEEDBACK_FILE)

@pytest.mark.asyncio
async def test_health_endpoint():
    """Validates backend readiness and health check endpoint."""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "services" in response.json()

@pytest.mark.asyncio
async def test_fact_check_endpoint():
    """Validates Wikipedia API processing pipeline."""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"query": "Artificial Intelligence", "max_summary_length": 100}
        response = await ac.post("/fact-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert "summary" in data

@pytest.mark.asyncio
async def test_analyze_event_endpoint():
    """Validates NLP Zero-Shot theme extraction formatting constraints."""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "event_description": "Green energy systems and solar panel integration workshop",
            "top_k": 2,
            "threshold": 0.05
        }
        response = await ac.post("/analyze-event", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "primary_theme" in data
    assert isinstance(data["extracted_themes"], list)

@pytest.mark.asyncio
async def test_generate_and_retrieve_history_workflow():
    """Validates data pipeline: content generation to automatic JSON logging."""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        gen_payload = {
            "event_description": "Fintech Disruptors Summit 2026",
            "themes": ["blockchain", "finance"],
            "interests": ["banking", "security"],
            "num_starters": 2
        }
        gen_response = await ac.post("/generate-conversation", json=gen_payload)
        assert gen_response.status_code == 200
        
        history_response = await ac.get("/history")
        assert history_response.status_code == 200
        history_data = history_response.json()
        assert history_data["total_entries"] > 0

@pytest.mark.asyncio
async def test_feedback_submission_persistence():
    """Validates metrics tracking storage framework."""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        feedback_payload = {
            "item_id": "starter_test_99",
            "feedback_type": "thumbs_up",
            "notes": "Extremely relevant starter framework"
        }
        response = await ac.post("/feedback", json=feedback_payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Feedback recorded successfully"