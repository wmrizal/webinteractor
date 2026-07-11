from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@dataclass(slots=True)
class ApiError(Exception):
    code: str
    message: str
    status_code: int


class NotFoundError(ApiError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(code="not_found", message=message, status_code=404)


class ConflictError(ApiError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(code="conflict", message=message, status_code=409)


class BadRequestError(ApiError):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(code="bad_request", message=message, status_code=400)


async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": "Request validation failed",
            "details": jsonable_encoder(exc.errors()),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
