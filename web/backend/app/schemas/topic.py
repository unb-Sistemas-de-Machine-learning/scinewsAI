from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class TopicCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class TopicResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]

    class Config:
        from_attributes = True
