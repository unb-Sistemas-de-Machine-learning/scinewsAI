from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List

from app.db.supabase import get_supabase
from app.schemas.article import ArticleResponse, ArticleListResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=ArticleListResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    topic: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """List all articles with pagination and filtering"""
    supabase = get_supabase()
    
    try:
        # Build query
        query = supabase.table("articles").select("*").eq("processing_status", "translated")
        
        if search:
            # Search in title or abstract
            query = query.or_(f"title.ilike.%{search}%,abstract.ilike.%{search}%")
        
        # Get total count
        count_result = supabase.table("articles").select("id", count="exact").eq("processing_status", "translated").execute()
        total = count_result.count if count_result.count else 0
        
        # Get paginated results
        offset = (page - 1) * page_size
        result = query.order("publication_date", desc=True).range(offset, offset + page_size - 1).execute()
        
        articles = result.data if result.data else []
        
        return ArticleListResponse(
            articles=[ArticleResponse.model_validate(a) for a in articles],
            total=total,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch articles: {str(e)}")


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get a specific article by ID"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("articles").select("*").eq("id", article_id).execute()
        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return ArticleResponse.model_validate(result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch article: {str(e)}")


@router.get("/latest/", response_model=List[ArticleResponse])
async def get_latest_articles(
    limit: int = Query(10, ge=1, le=50),
):
    """Get latest articles (public endpoint for newsletter)"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("articles").select("*").eq("processing_status", "completed").order("publication_date", desc=True).limit(limit).execute()
        articles = result.data if result.data else []
        return [ArticleResponse.model_validate(a) for a in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch articles: {str(e)}")
