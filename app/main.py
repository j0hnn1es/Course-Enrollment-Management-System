from fastapi import FastAPI
from app.router.course import course_router
from app.router.user import user_router
from app.router.enrollment import Enrollment_router

app = FastAPI(
    title="Course Management API",
    description="API for managing users, courses, and enrollments",
    version="1.0.0"
)


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint - API information and documentation."""
    return {
        "message": "Welcome to Course Management API"
        }



app.include_router(course_router, prefix="/api/v1", tags=["course"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])
app.include_router(Enrollment_router, prefix="/api/v1", tags=["enrollment"])



