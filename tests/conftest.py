import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before and after each test"""
    # Save original state
    original_activities = copy.deepcopy(activities)
    
    # Yield to test
    yield
    
    # Restore original state
    activities.clear()
    activities.update(original_activities)
