from fastapi import HTTPException, status
from app.schemas.enrollment import Enrollment, EnrollmentCreate, Enrollmentrole
from app.schemas.user import UserRole
from app.core.db import enrollment, user, course


# Enrollment management service
class EnrollmentService:
    
    @staticmethod
    def enroll_user_in_course(enrollment_create: EnrollmentCreate) -> Enrollment:
        # Validate user exists
        if enrollment_create.user_id not in user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found")
        
        # Validate course exists
        if enrollment_create.course_id not in course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Course not found")
        
        # Validate user is not already enrolled in the course
        for existing_enrollment in enrollment.values():
            if (existing_enrollment.user_id == enrollment_create.user_id and 
                existing_enrollment.course_id == enrollment_create.course_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="User is already enrolled in this course")
        
        # Create new enrollment
        enrollment_id = len(enrollment) + 1
        new_enrollment = Enrollment(
            id=enrollment_id,
            user_id=enrollment_create.user_id,
            course_id=enrollment_create.course_id,
            role=enrollment_create.role
        )
        enrollment[enrollment_id] = new_enrollment
        return new_enrollment
    
    @staticmethod
    def get_enrollments_for_course(course_id: int) -> list[Enrollment]:
        if course_id not in course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found")
        return [e for e in enrollment.values() if e.course_id == course_id]
    
    @staticmethod
    def get_enrollments_for_user(user_id: int) -> list[Enrollment]:
        if user_id not in user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")
        return [e for e in enrollment.values() if e.user_id == user_id]
    
    @staticmethod
    def deregister_student_from_course(enrollment_id: int):
        if enrollment_id not in enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Enrollment not found")
        
        del enrollment[enrollment_id]
        return {"detail": "Enrollment removed successfully"}
    
    @staticmethod
    def get_all_enrollments() -> list[Enrollment]:
        return list(enrollment.values())
    
    @staticmethod
    def get_enrollment_details(enrollment_id: int) -> Enrollment:
        if enrollment_id not in enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Enrollment not found")
        return enrollment[enrollment_id]
    
    @staticmethod
    def admin_deregister_student_from_course(enrollment_id: int):
        if enrollment_id not in enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Enrollment not found")
        
        del enrollment[enrollment_id]
        return {"detail": "Enrollment removed by admin successfully"}
        
