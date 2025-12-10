from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.db.supabase import get_supabase
from app.schemas.topic import TopicResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[TopicResponse])
async def list_topics(current_user: dict = Depends(get_current_user)):
    """List all available topics"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("topics").select("*").order("name").execute()
        topics = result.data if result.data else []
        return [TopicResponse.model_validate(t) for t in topics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topics: {str(e)}")


@router.post("/{topic_id}/subscribe")
async def subscribe_to_topic(
    topic_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Subscribe to a topic"""
    supabase = get_supabase()
    
    try:
        # Check if topic exists
        topic_result = supabase.table("topics").select("*").eq("id", topic_id).execute()
        if not topic_result.data:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        topic = topic_result.data[0]
        
        # Check if already subscribed
        existing = supabase.table("subscriptions").select("id").eq("user_id", current_user["user_id"]).eq("topic_id", topic_id).execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="Already subscribed to this topic")
        
        # Create subscription
        supabase.table("subscriptions").insert({
            "user_id": current_user["user_id"],
            "topic_id": topic_id
        }).execute()
        
        return {"message": "Successfully subscribed", "topic": topic.get("name")}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")


@router.delete("/{topic_id}/unsubscribe")
async def unsubscribe_from_topic(
    topic_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Unsubscribe from a topic"""
    supabase = get_supabase()
    
    try:
        supabase.table("subscriptions").delete().eq("user_id", current_user["user_id"]).eq("topic_id", topic_id).execute()
        return {"message": "Successfully unsubscribed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unsubscribe: {str(e)}")


@router.get("/subscriptions/", response_model=List[TopicResponse])
async def get_user_subscriptions(current_user: dict = Depends(get_current_user)):
    """Get user's topic subscriptions"""
    supabase = get_supabase()
    
    try:
        # Get user's subscriptions
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", current_user["user_id"]).execute()
        
        if not subscriptions.data:
            return []
        
        topic_ids = [sub["topic_id"] for sub in subscriptions.data]
        
        # Get topics
        if topic_ids:
            topics = supabase.table("topics").select("*").in_("id", topic_ids).execute()
            return [TopicResponse.model_validate(t) for t in topics.data] if topics.data else []
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscriptions: {str(e)}")
