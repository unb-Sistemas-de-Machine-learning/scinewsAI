from sqlalchemy.orm import Session
import logging
from app.models.article import Article
from app.models.subscription import Subscription
from app.models.topic import Topic
from app.models.user import User
from app.services.email import send_email

logger = logging.getLogger(__name__)

def process_notifications(db: Session):
    """
    Check for processed articles that haven't been notified yet,
    find interested users based on topics, and send emails.
    """
    # 1. Find candidates
    articles = db.query(Article).filter(
        Article.processing_status == "completed",
        Article.notification_sent == False
    ).all()
    
    if not articles:
        return 0

    logger.info(f"Found {len(articles)} articles to process for notifications")
    
    count = 0
    for article in articles:
        try:
            # 2. Match topics
            if not article.keywords:
                # If no keywords, we can't match subscriptions (unless we implement 'subscribe to all')
                # Just mark as notified to avoid getting stuck
                article.notification_sent = True
                db.add(article)
                continue
                
            # Get Topic objects ensuring we match slugs
            topics = db.query(Topic).filter(Topic.slug.in_(article.keywords)).all()
            topic_ids = [t.id for t in topics]
            
            if not topic_ids:
                article.notification_sent = True
                db.add(article)
                continue
            
            # 3. Find unique users interested in these topics
            subscriptions = db.query(Subscription).filter(
                Subscription.topic_id.in_(topic_ids)
            ).all()
            
            user_ids = set(sub.user_id for sub in subscriptions)
            if not user_ids:
                article.notification_sent = True
                db.add(article)
                continue
                
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            
            # 4. Send emails
            for user in users:
                subject = f"New AI Summary: {article.title}"
                # content = generate_email_content(user, article) # extracted for clarity
                content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2c3e50;">New Article Processed</h2>
                    <p>Hi {user.name},</p>
                    <p>An article matching your interests has just been processed by our AI.</p>
                    
                    <div style="border: 1px solid #eee; padding: 15px; border-radius: 5px; background: #f9f9f9;">
                        <h3 style="margin-top: 0;">{article.title}</h3>
                        <p style="color: #666; font-style: italic; font-size: 0.9em;">
                            {article.abstract[:200]}...
                        </p>
                        <a href="http://localhost:5173/article/{article.id}" 
                           style="display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">
                           Read Simplified Version
                        </a>
                    </div>
                    
                    <p style="font-size: 0.8em; color: #999; margin-top: 20px;">
                        You received this because you are subscribed to: {', '.join([t.name for t in topics])}
                    </p>
                </div>
                """
                send_email(user.email, subject, content)
            
            # 5. Mark done
            article.notification_sent = True
            db.add(article)
            count += 1
            
        except Exception as e:
            logger.error(f"Error processing notifications for article {article.id}: {e}")
            continue
            
    db.commit()
    return count
