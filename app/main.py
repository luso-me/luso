from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.rest.auth.routes import router as auth_router
from app.adapters.rest.skill.routes import router as skill_router
from app.adapters.rest.user.routes import router as user_router
from app.config import settings


def get_application() -> FastAPI:
    application = FastAPI()

    # TODO: Add logging configuration
    application.add_middleware(middleware_class=CORSMiddleware,
                               allow_origins=settings.cors_allowed_origins,
                               allow_credentials=True,
                               allow_methods=["*"],
                               allow_headers=["*"])

    # TODO: Move to own module
    application.include_router(skill_router)
    application.include_router(user_router)
    application.include_router(auth_router)

    return application


app = get_application()
