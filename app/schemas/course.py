from pydantic import BaseModel, Field, field_validator
from enum import Enum


class CourseAccess(str, Enum):
    ADMIN_ONLY_ACCESS = "admin_only_access"
    PUBLIC_ACCESS = "public_access"

class Course(BaseModel):
    id: int = Field(gt=0, description="Course ID must be positive")
    title: str = Field(min_length=1, max_length=200, description="Course title")
    code: str = Field(min_length=2, max_length=20, pattern="^[A-Z0-9]+$",
                      description="Course code (uppercase alphanumeric)")
    access: CourseAccess
    
    @field_validator('title')
    @classmethod
    def title_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()
    
    @field_validator('code')
    @classmethod
    def code_uppercase(cls, v):
        if not v or not v.strip():
            raise ValueError('Course code cannot be empty')
        return v.upper().strip()
    
class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Course title")
    code: str = Field(min_length=2, max_length=20, pattern="^[A-Z0-9]+$", description="Course code (uppercase alphanumeric)")
    id: int = Field(gt=0, description="Course ID must be positive")
    access: CourseAccess
    
    @field_validator('title')
    @classmethod
    def title_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()
    
    @field_validator('code')
    @classmethod
    def code_uppercase(cls, v):
        if not v or not v.strip():
            raise ValueError('Course code cannot be empty')
        return v.upper().strip()