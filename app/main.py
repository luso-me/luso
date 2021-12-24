import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api
from app.config import settings


def get_application() -> FastAPI:
    application = FastAPI()

    # TODO: Add logging configuration

    application.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=settings.cors_allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
    )

    # TODO: Move to own module
    application.include_router(api.skill_router, prefix="/skills")
    application.include_router(api.user_router, prefix="/users")
    application.include_router(api.auth_router, prefix='/auth')

    return application


app = get_application()
