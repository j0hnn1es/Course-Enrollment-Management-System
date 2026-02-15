from fastapi import Depends, HTTPException, status
from app.schemas.user import UserRole

def is_admin_user():
    """Dependency for admin-only endpoints."""
    return {"role": UserRole.ADMIN}
    
def is_student_user():
    """Dependency for authenticated student endpoints."""
    return {"role": UserRole.USER}

