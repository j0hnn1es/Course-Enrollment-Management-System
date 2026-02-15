from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import is_admin_user
from schemas.course import Course, CourseCreate, CourseAccess
from services.course_service import CourseService



course_router = APIRouter(prefix="/courses", tags=["courses"])

# Create a new course (Admin only)

@course_router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, current_user = Depends(is_admin_user)):
    """
    course_created = {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "access": course.access
        
    }
    """
    new_course = Course(id=course.id, title=course.title, code=course.code,access=CourseAccess.PUBLIC_ACCESS)
    
    return CourseService.create_course(new_course)