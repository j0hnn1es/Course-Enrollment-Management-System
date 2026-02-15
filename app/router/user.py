from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.schemas.user import User, UserCreate, UserRole
from app.api.deps import is_admin_user, is_student_user
from app.services.user import UserService

user_router = APIRouter(prefix="/users", tags=["users"])

# Create a user 
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=User, responses={
    201: {"description": "User created successfully"},
    400: {"description": "Invalid input data"}
})
def create_user(
    user_create: UserCreate, current_user=Depends(is_admin_user)):
    
    return UserService.create_user(user_create)


# Retrieve all users 
@user_router.get("/", status_code=status.HTTP_200_OK, response_model=list[User], responses={
    200: {"description": "List of users retrieved successfully"},
})
def get_all_users(current_user=Depends(is_student_user)):
    
    return UserService.get_all_users()

#Retrieve a user by ID
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User, responses={
    200: {"description": "User retrieved successfully"},
    404: {"description": "User not found"}
})
def get_user(user_id: int, current_user=Depends(is_student_user)):
    
    return UserService.get_user(user_id)

# Delete user (Admin only)
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    204: {"description": "User deleted successfully"},
    404: {"description": "User not found"},
    403: {"description": "Admin privileges required"}
})
def delete_user(
    user_id: int,
    current_user=Depends(is_admin_user)):
    
    return UserService.delete_user(user_id)
