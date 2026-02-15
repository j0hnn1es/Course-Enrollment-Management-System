from app.schemas.user import UserCreate, User
from app.core.db import user
from fastapi import HTTPException, status

class UserService:
    
    @staticmethod
    def create_user(user_create: UserCreate):
        user_id = len(user) + 1
        new_user = User(
            id=user_id,
            name=user_create.name,
            email=user_create.email,
            role=user_create.role
        )
        user[user_id] = new_user
        return new_user
    
    @staticmethod
    def get_user(user_id: int):
        if user_id in user:
            return user[user_id]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")
    
    @staticmethod
    def get_all_users():
        return list(user.values())
    
  
    @staticmethod
    def delete_user(user_id: int):
        if user_id not in user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")
        del user[user_id]
        return {"detail": "User deleted successfully"}