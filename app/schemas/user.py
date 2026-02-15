from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "administrator"
    USER = "student"


class User(BaseModel):
    id: int = Field(gt=0, description="User ID must be positive")
    name: str = Field(min_length=1, max_length=100, description="User name")
    email: EmailStr
    role: UserRole
    
    @field_validator('name')
    @classmethod
    def name_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()

    
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="User name")
    id: int = Field(gt=0, description="User ID must be positive")
    email: EmailStr
    role: UserRole
    
    @field_validator('name')
    @classmethod
    def name_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()
    