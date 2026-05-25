from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.api.base import router as base_router
from src.api.categories import router as categories_router
from src.api.locations import router as locations_router
from src.api.comment import router as comments_router
from src.api.user import router as users_router
from src.api.auth import router as auth_router
from src.middleware import LoggingMiddleware
from src.exceptions import ValidationError, NotFoundError, UniqueConstraintError

from fastapi.staticfiles import StaticFiles

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(LoggingMiddleware)

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        logger.warning(f"Validation error: {exc.field} - {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation Error",
                "field": exc.field,
                "message": exc.message,
                "value": exc.value,
            },
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        logger.warning(f"Not found: {exc.entity_name} id={exc.entity_id}")
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "entity": exc.entity_name,
                "id": exc.entity_id,
            },
        )

    @app.exception_handler(UniqueConstraintError)
    async def unique_constraint_error_handler(
        request: Request, exc: UniqueConstraintError
    ):
        logger.warning(f"Conflict: {exc.entity_name} {exc.field}={exc.value}")
        return JSONResponse(
            status_code=409,
            content={
                "error": "Conflict",
                "entity": exc.entity_name,
                "field": exc.field,
                "value": exc.value,
            },
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, tags=["Authentication"])
    app.include_router(base_router, prefix="/base", tags=["Base APIs"])
    app.include_router(categories_router, tags=["Categories"])
    app.include_router(locations_router, tags=["Locations"])
    app.include_router(comments_router, tags=["Comments"])
    app.include_router(users_router, tags=["Users"])

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    return app
