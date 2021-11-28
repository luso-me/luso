import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.include_router(api.skill_router, prefix="/skills")
app.include_router(api.user_router, prefix="/users")
app.include_router(api.auth_router, prefix='/auth')

app = CORSMiddleware(
        app=app,
        allow_origins=["http://localhost:7000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

# todo : dan to add little data populator
