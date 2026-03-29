class AppError(Exception):
    def __init__(self, message: str, status_code: int, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code

class NotFoundError(AppError):
    def __init__(self, message: str = "Not found", code: str | None = None):
        super().__init__(message, 404, code or "NOT_FOUND")

class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request", code: str | None = None):
        super().__init__(message, 400, code or "BAD_REQUEST")

class ConflictError(AppError):
    def __init__(self, message: str = "Conflict", code: str | None = None):
        super().__init__(message, 409, code or "CONFLICT")

class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized", code: str | None = None):
        super().__init__(message, 401, code or "UNAUTHORIZED")

class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden", code: str | None = None):
        super().__init__(message, 403, code or "FORBIDDEN")

class ServerError(AppError):
    def __init__(self, message: str = "Server error", code: str | None = None):
        super().__init__(message, 500, code or "SERVER_ERROR")
