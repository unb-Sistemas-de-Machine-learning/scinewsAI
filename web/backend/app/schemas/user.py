from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class ProfileType(str, Enum):
    student = "student"
    educator = "educator"
    enthusiast = "enthusiast"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    profile_type: ProfileType = ProfileType.student


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    profile_type: ProfileType
    subscribed_topics: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile_type: Optional[ProfileType] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
