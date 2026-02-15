from fastapi import APIRouter, Depends, status, Path, HTTPException
from app.schemas.course import Course, CourseCreate, CourseAccess
from app.schemas.user import UserRole
from app.services.course import CourseService
from app.api.deps import is_admin_user, is_student_user

course_router = APIRouter(prefix="/courses", tags=["courses"])



# Create a new course(Admin only)
@course_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Course, responses={
    201: {"description": "Course created successfully"},
    # 400: {"description": "Invalid input data"},
    # 403: {"description": "Admin privileges required"}
})
def create_course(
    course_create: CourseCreate, current_user=Depends(is_admin_user)):
    return CourseService.create_course(course_create)

# Get course by ID (Public: can view PUBLIC_ACCESS courses, Admin: can view all)
@course_router.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=Course, responses={
    200: {"description": "Course retrieved successfully"},
    403: {"description": "Course access restricted"},
    404: {"description": "Course not found"}
})
def get_course(course_id: int, current_user=Depends(is_student_user)):
    course_obj = CourseService.get_course(course_id)
    
    # Check access: ADMIN_ONLY_ACCESS requires admin role
    if course_obj.access == CourseAccess.ADMIN_ONLY_ACCESS and current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This course is admin-only. Access denied."
        )
    
    return course_obj

# Update course(Admin only)
@course_router.put("/{course_id}", status_code=status.HTTP_200_OK, response_model=Course, responses={
    200: {"description": "Course updated successfully"},
   
})
def update_course(
    course_id: int, 
    course_update: CourseCreate = None, 
    current_user=Depends(is_admin_user)):
    return CourseService.update_course(course_id, course_update)

#Delete a course (Admin only)
@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    204: {"description": "Course deleted successfully"},
    # 404: {"description": "Course not found"},
    # 403: {"description": "Admin privileges required"}
})

def delete_course(
    course_id: int, 
    current_user=Depends(is_admin_user)):
    return CourseService.delete_course(course_id)

# Retrieve All courses
@course_router.get("/access/{access}", status_code=status.HTTP_200_OK, response_model=list[Course], responses={
    200: {"description": "Courses retrieved successfully"},
    # 403: {"description": "User privileges required"}
})
def retrieve_all_courses(
    access: CourseAccess, current_user=Depends(is_student_user)):
    
    return CourseService.retrieve_all_courses(access)
