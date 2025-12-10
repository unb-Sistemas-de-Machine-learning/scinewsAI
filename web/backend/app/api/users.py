from fastapi import APIRouter, Depends, HTTPException

from app.db.supabase import get_supabase
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me/", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    supabase = get_supabase()
    
    try:
        user_result = supabase.table("users").select("*").eq("id", current_user["user_id"]).execute()
        if not user_result.data or len(user_result.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = user_result.data[0]
        
        # Get subscribed topics
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", user["id"]).execute()
        subscribed_topic_ids = [str(sub["topic_id"]) for sub in subscriptions.data] if subscriptions.data else []
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            profile_type=user.get("profile_type"),
            subscribed_topics=subscribed_topic_ids,
            created_at=user.get("created_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    updates: UserUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update user profile"""
    supabase = get_supabase()
    
    try:
        user_id = current_user["user_id"]
        
        # Prepare update data
        update_data = {}
        if updates.name:
            update_data["name"] = updates.name
        if updates.profile_type:
            update_data["profile_type"] = updates.profile_type
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update user
        result = supabase.table("users").update(update_data).eq("id", user_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = result.data[0]
        
        # Get subscribed topics
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", user["id"]).execute()
        subscribed_topic_ids = [str(sub["topic_id"]) for sub in subscriptions.data] if subscriptions.data else []
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            profile_type=user.get("profile_type"),
            subscribed_topics=subscribed_topic_ids,
            created_at=user.get("created_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.delete("/")
async def delete_account(current_user: dict = Depends(get_current_user)):
    """Delete user account"""
    supabase = get_supabase()
    
    try:
        user_id = current_user["user_id"]
        supabase.table("users").delete().eq("id", user_id).execute()
        return {"message": "Account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")


@router.post("/me/topics/{topic_id}/subscribe/", response_model=UserResponse)
async def subscribe_to_topic(
    topic_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Subscribe user to a topic"""
    supabase = get_supabase()
    
    try:
        user_id = current_user["user_id"]
        
        # Check if topic exists
        topic_result = supabase.table("topics").select("id").eq("id", topic_id).execute()
        if not topic_result.data:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        # Check if already subscribed
        existing = supabase.table("subscriptions").select("id").eq("user_id", user_id).eq("topic_id", topic_id).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Already subscribed to this topic")
        
        # Create subscription
        supabase.table("subscriptions").insert({
            "user_id": user_id,
            "topic_id": topic_id
        }).execute()
        
        # Return updated user
        user_result = supabase.table("users").select("*").eq("id", user_id).execute()
        user = user_result.data[0] if user_result.data else None
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", user["id"]).execute()
        subscribed_topic_ids = [str(sub["topic_id"]) for sub in subscriptions.data] if subscriptions.data else []
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            profile_type=user.get("profile_type"),
            subscribed_topics=subscribed_topic_ids,
            created_at=user.get("created_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")


@router.delete("/me/topics/{topic_id}/subscribe/", response_model=UserResponse)
async def unsubscribe_from_topic(
    topic_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Unsubscribe user from a topic"""
    supabase = get_supabase()
    
    try:
        user_id = current_user["user_id"]
        
        # Find and delete subscription
        supabase.table("subscriptions").delete().eq("user_id", user_id).eq("topic_id", topic_id).execute()
        
        # Return updated user
        user_result = supabase.table("users").select("*").eq("id", user_id).execute()
        user = user_result.data[0] if user_result.data else None
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", user["id"]).execute()
        subscribed_topic_ids = [str(sub["topic_id"]) for sub in subscriptions.data] if subscriptions.data else []
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            profile_type=user.get("profile_type"),
            subscribed_topics=subscribed_topic_ids,
            created_at=user.get("created_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unsubscribe: {str(e)}")
