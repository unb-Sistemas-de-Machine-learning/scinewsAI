import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.db import Article, Base

# Override DATABASE_URL for seeding if needed, or use the one from env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/scinews")

print(f"Connecting to {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    
    session = Session()
    
    # Check if article exists
    existing = session.query(Article).filter_by(id="test_article_1").first()
    if existing:
        print("Test article already exists.")
        return

    print("Inserting test article...")
    article = Article(
        id="test_article_1",
        title="The Effects of Caffeine on Coding Speed",
        full_text="""
        Abstract: This study explores the correlation between caffeine intake and coding velocity.
        
        Introduction:
        Programmers often consume coffee. We wanted to see if more coffee equals faster code.
        
        Methodology:
        We gave 10 developers varying amounts of espresso and measured their typing speed and bug rate.
        
        Results:
        Participants who drank 3 cups showed a 20% increase in typing speed but a 15% increase in syntax errors. 
        However, subjective feelings of productivity increased by 50%.
        
        Conclusion:
        Caffeine boosts speed but may reduce accuracy. Use with caution.
        """,
        simplified_text=None,
        processing_status="downloaded"
    )
    
    session.add(article)
    session.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
