import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.item_router, prefix="/items")
app.include_router(api.user_router)
