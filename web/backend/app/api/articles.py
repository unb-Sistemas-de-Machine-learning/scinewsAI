from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleResponse, ArticleListResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=ArticleListResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """List all articles with pagination and filtering"""
    query = db.query(Article).filter(Article.processing_status == "completed")
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Article.title.ilike(search_filter)) |
            (Article.abstract.ilike(search_filter))
        )
    
    if topic:
        query = query.filter(Article.keywords.contains([topic]))
    
    total = query.count()
    articles = query.order_by(Article.publication_date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return ArticleListResponse(
        articles=[ArticleResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a specific article by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article)


@router.get("/latest/", response_model=List[ArticleResponse])
async def get_latest_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Get latest articles (public endpoint for newsletter)"""
    articles = (
        db.query(Article)
        .filter(Article.processing_status == "completed")
        .order_by(Article.created_at.desc())
        .limit(limit)
        .all()
    )
    return [ArticleResponse.model_validate(a) for a in articles]
