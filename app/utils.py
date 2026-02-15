"""Utility functions for validation and checking"""
from fastapi import HTTPException, status
from app.database import db


def check_admin_role(role: str) -> None:
    """Check if user has admin role"""
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action"
        )


def check_student_role(role: str) -> None:
    """Check if user has student role"""
    if role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action"
        )


def get_and_validate_user(user_id: int):
    """Get user and validate it exists"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


def get_and_validate_course(course_id: int):
    """Get course and validate it exists"""
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course
