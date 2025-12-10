import logging
import time
import mlflow
from sqlalchemy import select, and_
from src.db import get_session, Article, init_db
from src.rag import translate_text
from src.tracking import setup_mlflow, log_common_params

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_articles(loop: bool = False, sleep_interval: int = 60):
    """
    Fetches articles from DB with null simplified_text and full_text available,
    translates them, and saves back to DB.
    """
    logger.info("Starting article processing service...")

    tracking_enabled = setup_mlflow()
    
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
                    
                    run_active = False
                    try:
                        start_time = time.time()

                        if tracking_enabled:
                            mlflow.start_run(run_name=f"db:{article.id}")
                            run_active = True
                            log_common_params({"input_source": "db", "article_id": article.id})
                            mlflow.log_param("title", article.title)
                            mlflow.log_param("processing_status_before", article.processing_status)

                        translated_content = translate_text(article.full_text)
                        
                        article.simplified_text = translated_content
                        article.processing_status = 'translated'
                        
                        session.commit()
                        elapsed = time.time() - start_time
                        logger.info(f"Successfully processed article {article.id} in {elapsed:.2f}s")

                        if tracking_enabled:
                            mlflow.log_metric("translation_time_s", elapsed)
                            mlflow.log_metric("full_text_length", len(article.full_text or ""))
                            mlflow.log_metric("simplified_length", len(translated_content or ""))
                            mlflow.log_text(translated_content or "", "summary.md")
                        
                    except Exception as e:
                        logger.error(f"Error processing article {article.id}: {e}")
                        session.rollback()
                        article.processing_status = 'failed_translation'
                        session.commit()
                        if tracking_enabled:
                            mlflow.log_param("processing_status_after", article.processing_status)
                    finally:
                        if run_active:
                            mlflow.end_run()
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
