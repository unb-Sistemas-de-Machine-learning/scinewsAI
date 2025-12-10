from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ArticleCreate(BaseModel):
    id: str
    title: str
    authors: List[str] = []
    publication_date: Optional[date] = None
    abstract: Optional[str] = None
    keywords: List[str] = []
    source_url: Optional[str] = None


class ArticleResponse(BaseModel):
    id: str
    title: str
    authors: List[str]
    publication_date: Optional[date]
    abstract: Optional[str]
    keywords: List[str]
    source_url: Optional[str]
    processing_status: str
    simplified_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    articles: List[ArticleResponse]
    total: int
    page: int
    page_size: int
