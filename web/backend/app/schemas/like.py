from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class LikeCreate(BaseModel):
    article_id: str


class LikeResponse(BaseModel):
    id: UUID
    user_id: UUID
    article_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class LikeCountResponse(BaseModel):
    article_id: str
    like_count: int
    is_liked: bool
