from sqlalchemy import Column, String, Text, Date, DateTime, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)  # arXiv ID
    title = Column(Text, nullable=False)
    authors = Column(ARRAY(Text), nullable=True)
    publication_date = Column(Date, nullable=True)
    abstract = Column(Text, nullable=True)
    keywords = Column(ARRAY(Text), nullable=True)
    full_text = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    original_pdf_path = Column(Text, nullable=True)
    processing_status = Column(String(50), default="pending")
    simplified_text = Column(Text, nullable=True)
    notification_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
