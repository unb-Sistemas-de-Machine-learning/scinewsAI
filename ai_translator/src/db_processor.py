import logging
import time
from sqlalchemy import select, and_
from src.db import get_session, Article, init_db
from src.rag import translate_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_articles(loop: bool = False, sleep_interval: int = 60):
    """
    Fetches articles from DB with null simplified_text and full_text available,
    translates them, and saves back to DB.
    """
    logger.info("Starting article processing service...")
    
    # Ensure tables exist
    init_db()
    logger.info("Database initialized.")
    
    while True:
        session = get_session()
        try:
            # Query for articles that need processing
            stmt = select(Article).where(
                and_(
                    Article.simplified_text.is_(None),
                    Article.full_text.is_not(None)
                )
            )
            
            result = session.execute(stmt)
            articles = result.scalars().all()
            
            if articles:
                logger.info(f"Found {len(articles)} articles to process.")
                
                for article in articles:
                    logger.info(f"Processing article ID: {article.id} - Title: {article.title[:50]}...")
                    
                    try:
                        start_time = time.time()
                        
                        translated_content = translate_text(article.full_text)
                        
                        article.simplified_text = translated_content
                        article.processing_status = 'translated'
                        
                        session.commit()
                        
                        elapsed = time.time() - start_time
                        logger.info(f"Successfully processed article {article.id} in {elapsed:.2f}s")
                        
                    except Exception as e:
                        logger.error(f"Error processing article {article.id}: {e}")
                        session.rollback()
                        article.processing_status = 'failed_translation'
                        session.commit()
            else:
                if loop:
                    logger.debug(f"No pending articles. Sleeping for {sleep_interval}s...")
            
        except Exception as e:
            logger.error(f"Database error: {e}")
        finally:
            session.close()

        if not loop:
            break
            
        time.sleep(sleep_interval)

if __name__ == "__main__":
    process_articles()
