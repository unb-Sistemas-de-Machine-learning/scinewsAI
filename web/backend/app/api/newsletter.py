from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.article import Article
from app.models.topic import Topic
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.article import ArticleResponse

router = APIRouter()


@router.get("/weekly-digest")
async def get_weekly_digest(
    db: Session = Depends(get_db),
):
    """
    Get articles for weekly newsletter digest
    Called by n8n workflow
    """
    from datetime import datetime, timedelta
    
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    
    articles = (
        db.query(Article)
        .filter(
            Article.processing_status == "completed",
            Article.created_at >= one_week_ago
        )
        .order_by(Article.created_at.desc())
        .limit(20)
        .all()
    )
    
    return {
        "articles": [ArticleResponse.model_validate(a) for a in articles],
        "total": len(articles),
        "week_start": one_week_ago.isoformat(),
        "week_end": datetime.utcnow().isoformat(),
    }


@router.get("/article/{article_id}/subscribers")
async def get_article_subscribers(
    article_id: str,
    db: Session = Depends(get_db),
):
    """
    Get list of subscribers interested in an article's topics
    Called by n8n workflow for notifications
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Get all subscriptions for topics matching article keywords
    topics = db.query(Topic).filter(Topic.slug.in_(article.keywords or [])).all()
    topic_ids = [t.id for t in topics]
    
    if not topic_ids:
        return {"subscribers": [], "article_id": article_id}
    
    subscriptions = db.query(Subscription).filter(
        Subscription.topic_id.in_(topic_ids)
    ).all()
    
    user_ids = list(set([sub.user_id for sub in subscriptions]))
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    
    return {
        "article_id": article_id,
        "article_title": article.title,
        "subscribers": [
            {
                "user_id": str(user.id),
                "email": user.email,
                "name": user.name,
                "profile_type": user.profile_type.value,
            }
            for user in users
        ],
        "total": len(users),
    }


@router.get("/social-post/{article_id}")
async def get_social_post_content(
    article_id: str,
    db: Session = Depends(get_db),
):
    """
    Get formatted content for social media posting
    Called by n8n workflow for Twitter/LinkedIn
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Format for different platforms
    base_url = "https://scinewsai.com/article"
    
    return {
        "article_id": article.id,
        "title": article.title,
        "abstract": article.abstract[:200] + "..." if article.abstract and len(article.abstract) > 200 else article.abstract,
        "url": f"{base_url}/{article.id}",
        "source_url": article.source_url,
        "keywords": article.keywords,
        "twitter_format": f"📚 New research simplified!\n\n{article.title[:200]}\n\nRead the simplified version: {base_url}/{article.id}\n\n#Research #ComputerScience #AI",
        "linkedin_format": f"🔬 Latest Research Insight\n\n{article.title}\n\n{article.abstract[:300]}...\n\nRead the full simplified analysis: {base_url}/{article.id}\n\n#Research #Technology #Innovation",
    }
