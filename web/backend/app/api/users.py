from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.models.subscription import Subscription
from app.models.topic import Topic
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me/", response_model=UserResponse)
async def get_me(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get current user info"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscribed_topic_ids = [str(sub.topic_id) for sub in user.subscriptions]
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_type=user.profile_type,
        subscribed_topics=subscribed_topic_ids,
        created_at=user.created_at,
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update user profile"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if updates.name:
        user.name = updates.name
    if updates.profile_type:
        user.profile_type = updates.profile_type
    
    db.commit()
    db.refresh(user)
    
    subscribed_topic_ids = [str(sub.topic_id) for sub in user.subscriptions]
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_type=user.profile_type,
        subscribed_topics=subscribed_topic_ids,
        created_at=user.created_at,
    )


@router.delete("/")
async def delete_account(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete user account"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "Account deleted successfully"}


@router.post("/me/topics/{topic_id}/subscribe/", response_model=UserResponse)
async def subscribe_to_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Subscribe user to a topic"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if already subscribed
    existing = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.topic_id == topic_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed to this topic")
    
    # Create subscription
    subscription = Subscription(user_id=user.id, topic_id=topic_id)
    db.add(subscription)
    db.commit()
    db.refresh(user)
    
    subscribed_topic_ids = [str(sub.topic_id) for sub in user.subscriptions]
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_type=user.profile_type,
        subscribed_topics=subscribed_topic_ids,
        created_at=user.created_at,
    )


@router.delete("/me/topics/{topic_id}/subscribe/", response_model=UserResponse)
async def unsubscribe_from_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Unsubscribe user from a topic"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find and delete subscription
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.topic_id == topic_id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    db.refresh(user)
    
    subscribed_topic_ids = [str(sub.topic_id) for sub in user.subscriptions]
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_type=user.profile_type,
        subscribed_topics=subscribed_topic_ids,
        created_at=user.created_at,
    )
