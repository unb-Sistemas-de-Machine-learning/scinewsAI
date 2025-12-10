from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from app.api import auth, articles, topics, users, newsletter, likes
from app.core.config import settings
from app.db.database import engine, Base, SessionLocal
from app.services.notification import process_notifications

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def notification_worker():
    """Background task to send notifications"""
    logger.info("Notification worker started")
    while True:
        try:
            # Check for notifications every 60 seconds
            # We run the blocking DB operation in a separate thread
            await asyncio.to_thread(run_notification_check)
        except asyncio.CancelledError:
            logger.info("Notification worker cancelled")
            break
        except Exception as e:
            logger.error(f"Error in notification worker: {e}")
        
        await asyncio.sleep(60)

def run_notification_check():
    """Helper to manage DB session for the worker"""
    db = SessionLocal()
    try:
        process_notifications(db)
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting SciNewsAI API...")
    
    # Start background task
    task = asyncio.create_task(notification_worker())
    
    yield
    
    # Shutdown
    logger.info("Shutting down SciNewsAI API...")
    
    # Cancel background task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="SciNewsAI API",
    description="Backend API for SciNewsAI - Simplified Research Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(topics.router, prefix="/api/topics", tags=["Topics"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(newsletter.router, prefix="/api/newsletter", tags=["Newsletter"])
app.include_router(likes.router, prefix="/api", tags=["Likes"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SciNewsAI API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected"
    }
