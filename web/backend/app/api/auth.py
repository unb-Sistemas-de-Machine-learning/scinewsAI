from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from uuid import uuid4
from datetime import datetime

from app.db.supabase import get_supabase
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    supabase = get_supabase()
    
    try:
        # Check if user exists
        existing_user = supabase.table("users").select("id").eq("email", user_data.email).execute()
        if existing_user.data and len(existing_user.data) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    # Enforce password length limit for bcrypt compatibility
    user_data.password = user_data.password[:72]
    
    # Create user
    user_id = str(uuid4())
    try:
        user_data_insert = {
            "id": user_id,
            "email": user_data.email,
            "password_hash": get_password_hash(user_data.password),
            "name": user_data.name,
            "profile_type": user_data.profile_type,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        result = supabase.table("users").insert(user_data_insert).execute()
        user = result.data[0] if result.data else None
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user_id, "email": user_data.email})
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=user_id,
                email=user_data.email,
                name=user_data.name,
                profile_type=user_data.profile_type,
                subscribed_topics=[],
                created_at=user.get("created_at"),
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password"""
    supabase = get_supabase()
    
    try:
        # Find user by email
        user_result = supabase.table("users").select("*").eq("email", form_data.username).execute()
        
        if not user_result.data or len(user_result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = user_result.data[0]
        
        # Verify password
        if not verify_password(form_data.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user["id"], "email": user["email"]})
        refresh_token = create_refresh_token(data={"sub": user["id"]})
        
        # Get subscribed topics
        subscriptions = supabase.table("subscriptions").select("topic_id").eq("user_id", user["id"]).execute()
        subscribed_topic_ids = [str(sub["topic_id"]) for sub in subscriptions.data] if subscriptions.data else []
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=user["id"],
                email=user["email"],
                name=user["name"],
                profile_type=user.get("profile_type"),
                subscribed_topics=subscribed_topic_ids,
                created_at=user.get("created_at"),
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    """Refresh access token"""
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")
    supabase = get_supabase()
    
    try:
        user_result = supabase.table("users").select("*").eq("id", user_id).execute()
        if not user_result.data or len(user_result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user = user_result.data[0]
        access_token = create_access_token(data={"sub": user["id"], "email": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    supabase = get_supabase()
    
    try:
        user_result = supabase.table("users").select("*").eq("id", current_user["user_id"]).execute()
        if not user_result.data or len(user_result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}"
        )
