from fastapi import HTTPException, status
from app.schemas.course import Course, CourseCreate, CourseAccess
from app.schemas.user import UserRole
from app.core.db import course


class CourseService:
    @staticmethod
    def create_course(course_create: CourseCreate):
        # Validation: Title must not be empty
        if not course_create.title or len(course_create.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Title must not be empty.")
        
        # Validation: Code must not be empty
        if not course_create.code or len(course_create.code.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code must not be empty.")
        
        # Validation: Code must be unique
        for existing_course in course.values():
            if existing_course.code.lower() == course_create.code.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Code must be unique.")
        
        course_id = len(course) + 1
        new_course = Course(
            id=course_id,
            title=course_create.title,
            code=course_create.code,
            access=course_create.access
        )
        course[course_id] = new_course
        return new_course
    
    @staticmethod
    def get_course(course_id: int):
        if course_id in course:
            return course[course_id]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found.")
    
    @staticmethod
    def update_course(course_id: int, course_update: CourseCreate):
        if course_id not in course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found.")
        
        # Validation: Title must not be empty
        if not course_update.title or len(course_update.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Title must not be empty.")
        
        # Validation:  Code must not be empty
        if not course_update.code or len(course_update.code.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Code must not be empty.")
        
        # Validation: Code must be unique (excluding current course)
        for existing_course_id, existing_course in course.items():
            if existing_course_id != course_id and existing_course.code.lower() == course_update.code.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Code must be unique.")
        
        updated_course = Course(
            id=course_id,
            title=course_update.title,
            code=course_update.code,
            access=course_update.access
        )
        course[course_id] = updated_course
        return updated_course
    
    @staticmethod
    def delete_course(course_id: int):
        if course_id in course:
            del course[course_id]
            return {"detail": "Course deleted successfully."}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found.")
    
    @staticmethod
    def retrieve_courses(access: CourseAccess):
        if access == CourseAccess.PUBLIC_ACCESS:
            return [c for c in course.values()
                    if c.access == CourseAccess.PUBLIC_ACCESS]
        elif access == CourseAccess.ADMIN_ONLY_ACCESS:
            return [c for c in course.values()
                    if c.access == CourseAccess.ADMIN_ONLY_ACCESS]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access type.")
    
    @staticmethod
    def retrieve_all_courses(access: CourseAccess):
        return [c for c in course.values() 
                if c.access == access]