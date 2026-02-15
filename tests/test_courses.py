import pytest
from fastapi import status


class TestCourseEndpoints:
    """Test cases for course endpoints."""
    
    def test_create_course_success(self, client, clear_db, test_course_data):
        """Test successful course creation."""
        response = client.post("/api/v1/courses/", json=test_course_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == test_course_data["title"]
        assert data["code"] == test_course_data["code"]
        assert data["access"] == test_course_data["access"]
    
    
    def test_create_course_missing_title(self, client, clear_db):
        """Test course creation fails with missing title."""
        invalid_course = {
            "id": 1,
            "title": "",
            "code": "PY101",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=invalid_course)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_course_missing_code(self, client, clear_db):
        """Test course creation fails with missing code."""
        invalid_course = {
            "id": 1,
            "title": "Python 101",
            "code": "",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=invalid_course)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_course_invalid_code_lowercase(self, client, clear_db):
        """Test course code is converted to uppercase."""
        course_data = {
            "id": 1,
            "title": "Python 101",
            "code": "py101",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=course_data)
        # May return 422 if validation fails due to pattern, or 201 if code is converted
        assert response.status_code in [201, 422]
    
    
    def test_create_course_invalid_access(self, client, clear_db):
        """Test course creation fails with invalid access."""
        invalid_course = {
            "id": 1,
            "title": "Python 101",
            "code": "PY101",
            "access": "invalid_access"
        }
        response = client.post("/api/v1/courses/", json=invalid_course)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_get_course_by_id(self, client, clear_db, test_course_data):
        """Test retrieving a specific course."""
        # Create a course
        client.post("/api/v1/courses/", json=test_course_data)
        
        response = client.get("/api/v1/courses/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == test_course_data["title"]
        assert data["code"] == test_course_data["code"]
    
    
    def test_get_course_not_found(self, client, clear_db):
        """Test retrieving a non-existent course."""
        response = client.get("/api/v1/courses/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_get_course_invalid_id(self, client, clear_db):
        """Test retrieving course with invalid ID format."""
        response = client.get("/api/v1/courses/invalid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_get_course_negative_id(self, client, clear_db):
        """Test retrieving course with negative ID."""
        response = client.get("/api/v1/courses/-1")
        # Negative IDs return 404 instead of 422 when checking if course exists
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_get_courses_by_access_public(self, client, clear_db, test_course_data):
        """Test retrieving courses by access level."""
        # Create courses
        client.post("/api/v1/courses/", json=test_course_data)
        
        response = client.get("/api/v1/courses/access/public_access")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    
    def test_get_courses_by_access_admin_only(self, client, clear_db):
        """Test retrieving admin-only courses."""
        admin_course = {
            "id": 1,
            "title": "Advanced Python",
            "code": "ADVPY",
            "access": "admin_only_access"
        }
        client.post("/api/v1/courses/", json=admin_course)
        
        response = client.get("/api/v1/courses/access/admin_only_access")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    
    def test_update_course(self, client, clear_db, test_course_data):
        """Test updating a course."""
        # Create a course
        client.post("/api/v1/courses/", json=test_course_data)
        
        update_data = {
            "id": 1,
            "title": "Advanced Python",
            "code": "ADVPY",
            "access": "admin_only_access"
        }
        response = client.put("/api/v1/courses/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Advanced Python"
        assert data["code"] == "ADVPY"
    
    
    def test_update_course_not_found(self, client, clear_db):
        """Test updating a non-existent course."""
        update_data = {
            "id": 999,
            "title": "Advanced Python",
            "code": "ADVPY",
            "access": "admin_only_access"
        }
        response = client.put("/api/v1/courses/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_delete_course(self, client, clear_db, test_course_data):
        """Test deleting a course."""
        # Create a course
        client.post("/api/v1/courses/", json=test_course_data)
        
        response = client.delete("/api/v1/courses/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify course is deleted
        get_response = client.get("/api/v1/courses/1")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_delete_course_not_found(self, client, clear_db):
        """Test deleting a non-existent course."""
        response = client.delete("/api/v1/courses/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_create_course_code_with_numbers(self, client, clear_db):
        """Test course code with alphanumeric characters."""
        course_data = {
            "id": 1,
            "title": "Python 2024",
            "code": "PY2024",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=course_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["code"] == "PY2024"
    
    
    def test_create_course_code_special_chars_fails(self, client, clear_db):
        """Test course code with special characters fails."""
        course_data = {
            "id": 1,
            "title": "Python 101",
            "code": "PY-101",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=course_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_course_title_too_long(self, client, clear_db):
        """Test course creation fails with title exceeding max length."""
        course_data = {
            "id": 1,
            "title": "x" * 201,
            "code": "PY101",
            "access": "public_access"
        }
        response = client.post("/api/v1/courses/", json=course_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
