import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    Date,
    ARRAY,
    TIMESTAMP,
    Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
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

def init_db():
    print("Inicializando o banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso.")

if __name__ == "__main__":
    init_db()
    