from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app.schemas.user import UserRole
from app.services.enrollment import EnrollmentService


Enrollment_router = APIRouter(prefix="/enrollments", tags=["enrollments"])

from app.api.deps import is_student_user

# Enroll a user in a course 
@Enrollment_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Enrollment, responses={
    201: {"description": "User enrolled successfully"},
    400: {"description": "Invalid input data"},
    404: {"description": "User or course not found"},
    409: {"description": "User already enrolled in this course"}
})
def enroll_user_in_course(
    enrollment_create: EnrollmentCreate, current_user=Depends(is_student_user)):
    return EnrollmentService.enroll_user_in_course(enrollment_create)


