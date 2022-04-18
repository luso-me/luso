from typing import List

from fastapi.middleware.cors import CORSMiddleware
import structlog

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.adapters.rest.auth.routes import router as auth_router
from app.adapters.rest.skill.routes import router as skill_router
from app.adapters.rest.user.routes import router as user_router
from app.config import settings

log = structlog.get_logger()


def _extract_cors() -> List[str]:
    return settings.cors_allowed_origins.split(",")


def get_application() -> FastAPI:
    application = FastAPI()

    # TODO: Add logging configuration
    application.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=_extract_cors(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # TODO: Move to own module
    application.include_router(skill_router)
    application.include_router(user_router)
    application.include_router(auth_router)

    return application


app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    log.error(f"{request}: {exc_str}")
    content = {"status_code": 422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
