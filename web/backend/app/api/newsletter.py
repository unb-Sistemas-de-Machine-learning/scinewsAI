from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta

from app.db.supabase import get_supabase
from app.schemas.article import ArticleResponse

router = APIRouter()


@router.get("/weekly-digest")
async def get_weekly_digest():
    """
    Get articles for weekly newsletter digest
    Called by n8n workflow
    """
    supabase = get_supabase()
    
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Query articles created in the last week with completed status
        result = supabase.table("articles").select("*").eq("processing_status", "completed").gte("created_at", one_week_ago.isoformat()).order("created_at", desc=True).limit(20).execute()
        
        articles = result.data if result.data else []
        
        return {
            "articles": [ArticleResponse.model_validate(a) for a in articles],
            "total": len(articles),
            "week_start": one_week_ago.isoformat(),
            "week_end": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch digest: {str(e)}")


@router.get("/article/{article_id}/subscribers")
async def get_article_subscribers(article_id: str):
    """
    Get list of subscribers interested in an article's topics
    Called by n8n workflow for notifications
    """
    supabase = get_supabase()
    
    try:
        # Get article
        article_result = supabase.table("articles").select("*").eq("id", article_id).execute()
        if not article_result.data:
            raise HTTPException(status_code=404, detail="Article not found")
        
        article = article_result.data[0]
        keywords = article.get("keywords", [])
        
        # Get topics matching article keywords
        if not keywords:
            return {"subscribers": [], "article_id": article_id}
        
        # Query topics by slug
        topics_result = supabase.table("topics").select("id").in_("slug", keywords).execute()
        topic_ids = [t["id"] for t in topics_result.data] if topics_result.data else []
        
        if not topic_ids:
            return {"subscribers": [], "article_id": article_id}
        
        # Get subscriptions for these topics
        subscriptions_result = supabase.table("subscriptions").select("user_id").in_("topic_id", topic_ids).execute()
        user_ids = list(set([sub["user_id"] for sub in subscriptions_result.data])) if subscriptions_result.data else []
        
        if not user_ids:
            return {"subscribers": [], "article_id": article_id}
        
        # Get user details
        users_result = supabase.table("users").select("id,email,name,profile_type").in_("id", user_ids).execute()
        subscribers = [
            {
                "user_id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "profile_type": user.get("profile_type", "researcher"),
            }
            for user in users_result.data
        ] if users_result.data else []
        
        return {
            "article_id": article_id,
            "article_title": article.get("title"),
            "subscribers": subscribers,
            "total": len(subscribers),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscribers: {str(e)}")


@router.get("/social-post/{article_id}")
async def get_social_post_content(article_id: str):
    """
    Get formatted content for social media posting
    Called by n8n workflow for Twitter/LinkedIn
    """
    supabase = get_supabase()
    
    try:
        # Get article
        article_result = supabase.table("articles").select("*").eq("id", article_id).execute()
        if not article_result.data:
            raise HTTPException(status_code=404, detail="Article not found")
        
        article = article_result.data[0]
        
        # Format for different platforms
        base_url = "https://scinewsai.com/article"
        abstract = article.get("abstract", "")
        abstract_short = abstract[:200] + "..." if abstract and len(abstract) > 200 else abstract
        
        return {
            "article_id": article["id"],
            "title": article.get("title"),
            "abstract": abstract_short,
            "url": f"{base_url}/{article['id']}",
            "source_url": article.get("source_url"),
            "keywords": article.get("keywords", []),
            "twitter_format": f"📚 New research simplified!\n\n{article.get('title', '')[:200]}\n\nRead the simplified version: {base_url}/{article['id']}\n\n#Research #ComputerScience #AI",
            "linkedin_format": f"🔬 Latest Research Insight\n\n{article.get('title')}\n\n{article.get('abstract', '')[:300]}...\n\nRead the full simplified analysis: {base_url}/{article['id']}\n\n#Research #Technology #Innovation",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch social post content: {str(e)}")
