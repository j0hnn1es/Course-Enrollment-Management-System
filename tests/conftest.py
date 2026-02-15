import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import user, course, enrollment


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def clear_db():
    """Clear the in-memory database before each test."""
    user.clear()
    course.clear()
    enrollment.clear()
    yield
    # Cleanup after test
    user.clear()
    course.clear()
    enrollment.clear()


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "role": "student"
    }


@pytest.fixture
def test_admin_data():
    """Test admin data."""
    return {
        "id": 2,
        "name": "Test Admin",
        "email": "admin@example.com",
        "role": "administrator"
    }


@pytest.fixture
def test_course_data():
    """Test course data."""
    return {
        "id": 1,
        "title": "Python 101",
        "code": "PY101",
        "access": "public_access"
    }


@pytest.fixture
def test_enrollment_data():
    """Test enrollment data."""
    return {
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    }


@pytest.fixture
def populated_db(clear_db, test_user_data, test_admin_data, test_course_data, client):
    """Populate database with test data and return the client."""
    # Create test admin 
    client.post("/api/v1/users/", json=test_admin_data)
    
    # Create test course
    client.post("/api/v1/courses/", json=test_course_data)
    
    # Create test user
    client.post("/api/v1/users/", json=test_user_data)
    
    return client
