from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.topic import Topic
from app.models.subscription import Subscription
from app.schemas.topic import TopicResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[TopicResponse])
async def list_topics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """List all available topics"""
    topics = db.query(Topic).order_by(Topic.name).all()
    return [TopicResponse.model_validate(t) for t in topics]


@router.post("/{topic_id}/subscribe")
async def subscribe_to_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Subscribe to a topic"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if already subscribed
    existing = db.query(Subscription).filter(
        Subscription.user_id == current_user["user_id"],
        Subscription.topic_id == topic_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed to this topic")
    
    subscription = Subscription(
        user_id=current_user["user_id"],
        topic_id=topic_id
    )
    db.add(subscription)
    db.commit()
    
    return {"message": "Successfully subscribed", "topic": topic.name}


@router.delete("/{topic_id}/unsubscribe")
async def unsubscribe_from_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Unsubscribe from a topic"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user["user_id"],
        Subscription.topic_id == topic_id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    
    return {"message": "Successfully unsubscribed"}


@router.get("/subscriptions/", response_model=List[TopicResponse])
async def get_user_subscriptions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get user's topic subscriptions"""
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user["user_id"]
    ).all()
    
    topic_ids = [sub.topic_id for sub in subscriptions]
    topics = db.query(Topic).filter(Topic.id.in_(topic_ids)).all()
    
    return [TopicResponse.model_validate(t) for t in topics]
