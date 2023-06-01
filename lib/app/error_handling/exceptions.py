from fastapi import HTTPException
from fastapi.responses import JSONResponse


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail


async def custom_exception_handler(exc):
    return JSONResponse(status_code=exc.status_code, content={
        "detail": exc.detail,
        "error": "Bad request"
    })
