from fastapi import APIRouter, Depends
from v1.deps import get_user_role
from schemas.user import User, UserCreate




user_router = APIRouter(prefix="/users", tags=["users"])

# Create a new user
@user_router.post("/")
def create_user(user: UserCreate, role: UserRole = Depends(get_user_role)):
    
    return {"message": "User created successfully", "user": user}
