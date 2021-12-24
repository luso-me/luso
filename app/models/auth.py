from typing import Optional, List

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class JWTPayload(BaseModel):
    sub: str
    exp: Optional[int]
    scopes: List[str] = Field(default_factory=list)
