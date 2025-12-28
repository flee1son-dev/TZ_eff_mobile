from fastapi import HTTPException, status

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "User not found"
        )

class UserForbidden(HTTPException):
    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN
        detail = "You are not allowed to perform this action"
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class UserEmailAlreadyExists(HTTPException):
    def __init__(self):
        status_code = status.HTTP_409_CONFLICT
        detail = "User with this Email already exists"
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid email or password"
        super().__init__(    
            status_code=status_code,
            detail=detail
        )

class CredentialsException(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials"
        super().__init__(
            status_code=status_code,
            detail=detail
        )