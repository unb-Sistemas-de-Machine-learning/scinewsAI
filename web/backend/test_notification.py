import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.services.notification import process_notifications
from app.models.article import Article
from app.models.topic import Topic
from app.models.subscription import Subscription
from app.models.user import User

class TestNotification(unittest.TestCase):
    @patch("app.services.notification.send_email")
    def test_process_notifications(self, mock_send_email):
        # Mock DB session
        db = MagicMock()
        
        # Mock Data
        article = Article(
            id="1", 
            title="Test Article", 
            abstract="Summary", 
            keywords=["ai"], 
            processing_status="completed",
            notification_sent=False
        )
        topic = Topic(id="t1", name="AI", slug="ai")
        subscription = Subscription(user_id="u1", topic_id="t1")
        user = User(id="u1", email="test@example.com", name="Test User")
        
        # The query chain is complex: db.query(Model).filter(...).all()
        # We need to mock return values based on the Model passed to query
        
        def query_side_effect(model):
            query_mock = MagicMock()
            if model == Article:
                query_mock.filter.return_value.all.return_value = [article]
            elif model == Topic:
                query_mock.filter.return_value.all.return_value = [topic]
            elif model == Subscription:
                query_mock.filter.return_value.all.return_value = [subscription]
            elif model == User:
                query_mock.filter.return_value.all.return_value = [user]
            else:
                query_mock.filter.return_value.all.return_value = []
            return query_mock
            
        db.query.side_effect = query_side_effect
        
        # Run
        count = process_notifications(db)
        
        # Verify
        self.assertEqual(count, 1)
        self.assertTrue(article.notification_sent)
        
        # Verify db.add(article) was called
        db.add.assert_called_with(article)
        db.commit.assert_called_once()
        
        # Verify email sent
        mock_send_email.assert_called_once()
        args = mock_send_email.call_args[0]
        self.assertEqual(args[0], "test@example.com")
        self.assertIn("Test Article", args[1])

if __name__ == "__main__":
    unittest.main()
