import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api
from app.config import settings

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.include_router(api.skill_router, prefix="/skills")
app.include_router(api.user_router, prefix="/users")
app.include_router(api.auth_router, prefix='/auth')

# todo : dan to add little data populator
