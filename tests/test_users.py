import pytest
from fastapi import status


class TestUserEndpoints:
    """Test cases for user endpoints."""
    
    def test_create_user_success(self, client, clear_db, test_user_data):
        """Test successful user creation."""
        response = client.post("/api/v1/users/", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
        assert data["role"] == test_user_data["role"]
    
    
    def test_create_user_missing_name(self, client, clear_db):
        """Test user creation fails with missing name."""
        invalid_user = {
            "id": 1,
            "name": "",
            "email": "test@example.com",
            "role": "user"
        }
        response = client.post("/api/v1/users/", json=invalid_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_user_invalid_email(self, client, clear_db):
        """Test user creation fails with invalid email."""
        invalid_user = {
            "id": 1,
            "name": "Test User",
            "email": "invalid-email",
            "role": "user"
        }
        response = client.post("/api/v1/users/", json=invalid_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_user_invalid_role(self, client, clear_db):
        """Test user creation fails with invalid role."""
        invalid_user = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "role": "invalid_role"
        }
        response = client.post("/api/v1/users/", json=invalid_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_get_all_users(self, client, clear_db, test_user_data, test_admin_data):
        """Test retrieving all users."""
        # Create test users
        client.post("/api/v1/users/", json=test_user_data)
        client.post("/api/v1/users/", json=test_admin_data)
        
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2
    
    
    def test_get_all_users_empty(self, client, clear_db):
        """Test retrieving users when database is empty."""
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    
    def test_get_user_by_id(self, client, clear_db, test_user_data):
        """Test retrieving a specific user."""
        # Create a user
        client.post("/api/v1/users/", json=test_user_data)
        
        response = client.get("/api/v1/users/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
    
    
    def test_get_user_not_found(self, client, clear_db):
        """Test retrieving a non-existent user."""
        response = client.get("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_get_user_invalid_id(self, client, clear_db):
        """Test retrieving user with invalid ID format."""
        response = client.get("/api/v1/users/invalid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_get_user_negative_id(self, client, clear_db):
        """Test retrieving user with negative ID."""
        response = client.get("/api/v1/users/-1")
        # Negative IDs return 404 instead of 422 when checking if user exists
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
     
    def test_delete_user(self, client, clear_db, test_user_data):
        """Test deleting a user."""
        # Create a user
        client.post("/api/v1/users/", json=test_user_data)
        
        response = client.delete("/api/v1/users/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user is deleted
        get_response = client.get("/api/v1/users/1")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_delete_user_not_found(self, client, clear_db):
        """Test deleting a non-existent user."""
        response = client.delete("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_create_user_negative_id(self, client, clear_db):
        """Test user creation with negative ID."""
        invalid_user = {
            "id": -1,
            "name": "Test User",
            "email": "test@example.com",
            "role": "user"
        }
        response = client.post("/api/v1/users/", json=invalid_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
