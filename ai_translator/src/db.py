import os
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    Date,
    ARRAY,
    TIMESTAMP,
    Float,
    Integer
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from src.config import get_settings

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    authors = Column(ARRAY(Text))
    publication_date = Column(Date)
    abstract = Column(Text)
    keywords = Column(ARRAY(Text))
    full_text = Column(Text)
    source_url = Column(Text)
    original_pdf_path = Column(Text)
    processing_status = Column(String(50), default='downloaded')
    simplified_text = Column(Text, nullable=True)
    relevance_score = Column(Float, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now()
    )

    def __repr__(self):
        return f"<Article(id='{self.id}', title='{self.title[:30]}...', score={self.relevance_score})>"

def get_db_engine():
    settings = get_settings()
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in .env or environment")
    return create_engine(settings.DATABASE_URL)

SessionLocal = None

def get_session():
    global SessionLocal
    if SessionLocal is None:
        engine = get_db_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_db():
    """Creates the database tables if they don't exist."""
    engine = get_db_engine()
    Base.metadata.create_all(bind=engine)
