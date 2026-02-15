from pydantic import BaseModel, Field, field_validator
from enum import Enum 



class Enrollmentrole(str, Enum):
    STUDENT = "student"
    ADMIN = "administrator"



class Enrollment(BaseModel):
    id: int = Field(gt=0, description="Enrollment ID must be positive")
    user_id: int = Field(gt=0, description="User ID must be positive")
    course_id: int = Field(gt=0, description="Course ID must be positive")
    role: Enrollmentrole
    
    @field_validator('user_id', 'course_id')
    @classmethod
    def validate_ids(cls, v):
        if v <= 0:
            raise ValueError('IDs must be positive integers')
        return v

class EnrollmentCreate(BaseModel):
    user_id: int = Field(gt=0, description="User ID must be positive")
    course_id: int = Field(gt=0, description="Course ID must be positive")
    role: Enrollmentrole
    
    @field_validator('user_id', 'course_id')
    @classmethod
    def validate_ids(cls, v):
        if v <= 0:
            raise ValueError('IDs must be positive integers')
        return v