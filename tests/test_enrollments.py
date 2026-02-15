import pytest
from fastapi import status


class TestEnrollmentEndpoints:
    """Test cases for enrollment endpoints."""
    
    def test_enroll_user_success(self, client, clear_db, test_user_data, test_course_data, test_enrollment_data):
        """Test successful user enrollment."""
        # Setup: Create user and course
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        response = client.post("/api/v1/enrollments/", json=test_enrollment_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == test_enrollment_data["user_id"]
        assert data["course_id"] == test_enrollment_data["course_id"]
        assert data["role"] == test_enrollment_data["role"]
    
    
    def test_enroll_user_missing_user_id(self, client, clear_db):
        """Test enrollment fails with missing user_id."""
        invalid_enrollment = {
            "course_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_user_missing_course_id(self, client, clear_db):
        """Test enrollment fails with missing course_id."""
        invalid_enrollment = {
            "user_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_user_missing_role(self, client, clear_db):
        """Test enrollment fails with missing role."""
        invalid_enrollment = {
            "user_id": 1,
            "course_id": 1
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_user_invalid_role(self, client, clear_db, test_user_data, test_course_data):
        """Test enrollment fails with invalid role."""
        # Setup: Create user and course
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        invalid_enrollment = {
            "user_id": 1,
            "course_id": 1,
            "role": "invalid_role"
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_user_negative_user_id(self, client, clear_db):
        """Test enrollment fails with negative user_id."""
        invalid_enrollment = {
            "user_id": -1,
            "course_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_user_negative_course_id(self, client, clear_db):
        """Test enrollment fails with negative course_id."""
        invalid_enrollment = {
            "user_id": 1,
            "course_id": -1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=invalid_enrollment)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_enroll_student_role(self, client, clear_db, test_user_data, test_course_data):
        """Test enrolling user with student role."""
        # Setup: Create user and course
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        enrollment_data = {
            "user_id": 1,
            "course_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=enrollment_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "student"
    
    
    def test_enroll_admin_role(self, client, clear_db, test_admin_data, test_course_data):
        """Test enrolling admin with administrator role."""
        # Setup: Create admin and course
        client.post("/api/v1/users/", json=test_admin_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        enrollment_data = {
            "user_id": 1,
            "course_id": 1,
            "role": "administrator"
        }
        response = client.post("/api/v1/enrollments/", json=enrollment_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "administrator"
    
    
    def test_enroll_duplicate_enrollment(self, client, clear_db, test_user_data, test_course_data, test_enrollment_data):
        """Test duplicate enrollment fails with conflict."""
        # Setup: Create user and course
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        # First enrollment should succeed
        response1 = client.post("/api/v1/enrollments/", json=test_enrollment_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Duplicate enrollment should fail with 409 Conflict
        response2 = client.post("/api/v1/enrollments/", json=test_enrollment_data)
        assert response2.status_code == status.HTTP_409_CONFLICT
    
    
    def test_enroll_nonexistent_user(self, client, clear_db, test_course_data):
        """Test enrollment fails when user doesn't exist."""
        # Create only course
        client.post("/api/v1/courses/", json=test_course_data)
        
        enrollment_data = {
            "user_id": 999,
            "course_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=enrollment_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]
    
    
    def test_enroll_nonexistent_course(self, client, clear_db, test_user_data):
        """Test enrollment fails when course doesn't exist."""
        # Create only user
        client.post("/api/v1/users/", json=test_user_data)
        
        enrollment_data = {
            "user_id": 1,
            "course_id": 999,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=enrollment_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Course not found" in response.json()["detail"]
    
    
    def test_enrollment_data_validation(self, client, clear_db, test_user_data, test_course_data):
        """Test enrollment with valid IDs."""
        # Setup: Create user and course
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/courses/", json=test_course_data)
        
        enrollment_data = {
            "user_id": 1,
            "course_id": 1,
            "role": "student"
        }
        response = client.post("/api/v1/enrollments/", json=enrollment_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Validate response contains id
        assert "id" in data
        assert data["id"] > 0
