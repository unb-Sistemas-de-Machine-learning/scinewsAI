from fastapi import APIRouter, Depends, HTTPException, status

from app.db.supabase import get_supabase
from app.schemas.like import LikeResponse, LikeCountResponse
from app.core.security import get_current_user
from uuid import uuid4
from datetime import datetime

router = APIRouter()


@router.post("/articles/{article_id}/like/", response_model=LikeResponse)
async def like_article(
    article_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Like an article"""
    supabase = get_supabase()
    user_id = current_user.get("user_id") or current_user.get("id")
    
    try:
        # Check if article exists
        article = supabase.table("articles").select("id").eq("id", article_id).execute()
        if not article.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado"
            )
        
        # Check if user already liked the article
        existing_like = supabase.table("likes").select("id").eq("user_id", user_id).eq("article_id", article_id).execute()
        
        if existing_like.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já curtiu este artigo"
            )
        
        # Create like
        like_data = {
            "id": str(uuid4()),
            "user_id": user_id,
            "article_id": article_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        result = supabase.table("likes").insert(like_data).execute()
        return result.data[0] if result.data else like_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to like article: {str(e)}")


@router.delete("/articles/{article_id}/like/", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_article(
    article_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Unlike an article"""
    supabase = get_supabase()
    user_id = current_user.get("user_id") or current_user.get("id")
    
    try:
        # Find and delete the like
        like = supabase.table("likes").select("id").eq("user_id", user_id).eq("article_id", article_id).execute()
        
        if not like.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Você não havia curtido este artigo"
            )
        
        supabase.table("likes").delete().eq("user_id", user_id).eq("article_id", article_id).execute()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unlike article: {str(e)}")


@router.get("/articles/{article_id}/like-status/", response_model=LikeCountResponse)
async def get_like_status(
    article_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get like count and user's like status for an article"""
    supabase = get_supabase()
    user_id = current_user.get("user_id") or current_user.get("id")
    
    try:
        # Count total likes
        all_likes = supabase.table("likes").select("id", count="exact").eq("article_id", article_id).execute()
        like_count = all_likes.count if all_likes.count else 0
        
        # Check if current user liked the article
        user_like = supabase.table("likes").select("id").eq("user_id", user_id).eq("article_id", article_id).execute()
        is_liked = bool(user_like.data)
        
        return LikeCountResponse(
            article_id=article_id,
            like_count=like_count,
            is_liked=is_liked
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get like status: {str(e)}")


@router.get("/articles/{article_id}/likes/", response_model=LikeCountResponse)
async def get_like_count_public(article_id: str):
    """Get like count for an article (public endpoint)"""
    supabase = get_supabase()
    
    try:
        # Count total likes
        all_likes = supabase.table("likes").select("id", count="exact").eq("article_id", article_id).execute()
        like_count = all_likes.count if all_likes.count else 0
        
        return LikeCountResponse(
            article_id=article_id,
            like_count=like_count,
            is_liked=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get like count: {str(e)}")
