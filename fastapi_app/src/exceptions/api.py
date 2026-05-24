from fastapi import HTTPException, status


class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail)


class NotFoundHTTPError(APIError):
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with id {entity_id} not found",
            error_code="NOT_FOUND",
        )


class ConflictHTTPError(APIError):
    def __init__(self, entity_name: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{entity_name} with {field} '{value}' already exists",
            error_code="CONFLICT",
        )


class BadRequestHTTPError(APIError):
    def __init__(self, message: str, field: str = None):
        detail = f"{field}: {message}" if field else message
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BAD_REQUEST",
        )


class UnprocessableEntityHTTPError(APIError):
    def __init__(self, errors: list):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"validation_errors": errors},
            error_code="VALIDATION_ERROR",
        )
