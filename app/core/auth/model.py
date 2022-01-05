from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class JWTPayload(BaseModel):
    sub: str
    exp: Optional[datetime]
    scopes: List[str] = Field(default_factory=list)
