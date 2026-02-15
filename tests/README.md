# API Tests

This directory contains comprehensive test suites for all API endpoints.

## Test Structure

- **conftest.py** - Pytest fixtures and configuration
- **test_users.py** - User endpoint tests (CRUD operations)
- **test_courses.py** - Course endpoint tests (CRUD operations)
- **test_enrollments.py** - Enrollment endpoint tests

## Running Tests

```bash
pip install -r requirements-test.txt
```

### Run all tests

```bash
pytest
```

### Run with verbose output

```bash
pytest -v
```

### Run specific test file

```bash
pytest tests/test_users.py
```

### Run specific test class

```bash
pytest tests/test_users.py::TestUserEndpoints
```

### Run specific test

```bash
pytest tests/test_users.py::TestUserEndpoints::test_create_user_success
```

### Run with coverage report

```bash
pytest --cov=app --cov-report=html
```

## Test Coverage

### User Endpoints (16 tests)

- ✅ Create user (success, with validation errors)
- ✅ Get all users (success, empty database)
- ✅ Get user by ID (success, not found, invalid ID)
- ✅ Update user (success, partial, not found)
- ✅ Delete user (success, not found)

### Course Endpoints (17 tests)

- ✅ Create course (success, validation for title/code/access)
- ✅ Get course by ID (success, not found, invalid ID)
- ✅ Get courses by access level (public, admin-only)
- ✅ Update course (success, not found)
- ✅ Delete course (success, not found)

### Enrollment Endpoints (14 tests)

- ✅ Enroll user (success, validation, role types)
- ✅ Duplicate enrollment (conflict handling)
- ✅ Enrollment validation (user/course existence, IDs)

## Test Coverage Summary

### Total Tests: 47

### Status Codes Tested

- 201 Created
- 200 OK
- 204 No Content
- 400 Bad Request
- 404 Not Found
- 409 Conflict
- 422 Unprocessable Entity
- 403 Forbidden

### Validation Tested

- ✅ Data type validation
- ✅ Field length constraints
- ✅ Email format validation
- ✅ Enum validation
- ✅ Positive integer validation
- ✅ Non-empty string validation
- ✅ Code pattern validation (uppercase alphanumeric)

### Edge Cases Tested

- ✅ Missing required fields
- ✅ Invalid data types
- ✅ Negative IDs
- ✅ Empty strings
- ✅ Non-existent resources
- ✅ Duplicate enrollments
- ✅ Field length limits
- ✅ Special characters in fields

## Fixtures

### clear_db

Clears all in-memory databases before and after each test.

### client

FastAPI TestClient for making HTTP requests.

### test_user_data, test_admin_data

Sample user data for testing.

### test_course_data

Sample course data for testing.

### test_enrollment_data

Sample enrollment data for testing.

### populated_db

Pre-populated database with sample data.

## Best Practices

- Each test tests a single behavior
- Tests are independent (no shared state)
- Database is cleared between tests
- Both success and failure paths are tested
- Response codes and data are validated
- Edge cases are covered
