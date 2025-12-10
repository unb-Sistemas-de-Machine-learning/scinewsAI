from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models.like import Like
from app.models.user import User
from app.schemas.like import LikeResponse, LikeCountResponse
from app.core.security import get_current_user
from sqlalchemy import func


router = APIRouter()


@router.post("/articles/{article_id}/like/", response_model=LikeResponse)
async def like_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Like an article"""
    # Extract user_id from current_user dict
    user_id = current_user.get("user_id") or current_user.get("id")
    
    # Check if article exists
    from app.models.article import Article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado"
        )
    
    # Check if user already liked the article
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.article_id == article_id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já curtiu este artigo"
        )
    
    # Create like
    like = Like(
        user_id=user_id,
        article_id=article_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    
    return like


@router.delete("/articles/{article_id}/like/", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Unlike an article"""
    # Extract user_id from current_user dict
    user_id = current_user.get("user_id") or current_user.get("id")
    
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.article_id == article_id
    ).first()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Você não havia curtido este artigo"
        )
    
    db.delete(like)
    db.commit()


@router.get("/articles/{article_id}/like-status/", response_model=LikeCountResponse)
async def get_like_status(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get like count and user's like status for an article"""
    # Extract user_id from current_user dict
    user_id = current_user.get("user_id") or current_user.get("id")
    
    # Count total likes
    like_count = db.query(func.count(Like.id)).filter(
        Like.article_id == article_id
    ).scalar()
    
    # Check if current user liked the article
    user_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.article_id == article_id
    ).first()
    
    return LikeCountResponse(
        article_id=article_id,
        like_count=like_count or 0,
        is_liked=user_like is not None
    )


@router.get("/articles/{article_id}/likes/", response_model=LikeCountResponse)
async def get_like_count_public(
    article_id: str,
    db: Session = Depends(get_db)
):
    """Get like count for an article (public endpoint)"""
    like_count = db.query(func.count(Like.id)).filter(
        Like.article_id == article_id
    ).scalar()
    
    return LikeCountResponse(
        article_id=article_id,
        like_count=like_count or 0,
        is_liked=False
    )
