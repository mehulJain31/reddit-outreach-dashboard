"""Outreach service for managing user outreach data."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from models import db, OutreachStatus, MessageTemplate
from services.reddit_service import RedditService
from config import Config


class OutreachService:
    """Service class for outreach operations."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.reddit_service = RedditService(config)
    
    def refresh_posts(self) -> Dict[str, int]:
        """
        Refresh posts from Reddit and update database.
        
        Returns:
            Dictionary with counts of new and updated posts
        """
        try:
            reddit_posts = self.reddit_service.fetch_recent_posts()
            
            new_posts_count = 0
            updated_posts_count = 0
            
            for title, location, username in reddit_posts:
                if not self.reddit_service.is_valid_username(username):
                    continue
                
                existing = OutreachStatus.query.filter_by(username=username).first()
                post_url = self.reddit_service.create_post_url(username)
                
                if existing:
                    # Update existing record if post title changed
                    if existing.post_title != title:
                        existing.post_title = title
                        existing.location = location
                        updated_posts_count += 1
                else:
                    # Create new record
                    new_post = OutreachStatus(
                        username=username,
                        post_title=title,
                        post_url=post_url,
                        location=location,
                        status='Not Sent'
                    )
                    db.session.add(new_post)
                    new_posts_count += 1
            
            db.session.commit()
            
            return {
                'new_posts': new_posts_count,
                'updated_posts': updated_posts_count
            }
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to refresh posts: {str(e)}")
    
    def get_posts(self, page: int = 1, status_filter: str = 'all', per_page: int = 20) -> List[OutreachStatus]:
        """
        Get posts with pagination and filtering.
        
        Args:
            page: Page number
            status_filter: Filter by status ('all', 'Sent', 'Not Sent')
            per_page: Posts per page
            
        Returns:
            Paginated list of posts
        """
        query = OutreachStatus.query.order_by(OutreachStatus.created_at.desc())
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        return query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
    
    def mark_as_sent(self, username: str) -> bool:
        """
        Mark a user as having been contacted.
        
        Args:
            username: Reddit username
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_status = OutreachStatus.query.filter_by(username=username).first()
            if not user_status:
                return False
            
            user_status.status = 'Sent'
            user_status.sent_at = datetime.utcnow()
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to mark as sent: {str(e)}")
    
    def mark_as_not_sent(self, username: str) -> bool:
        """
        Mark a user as not sent (undo).
        
        Args:
            username: Reddit username
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_status = OutreachStatus.query.filter_by(username=username).first()
            if not user_status:
                return False
            
            user_status.status = 'Not Sent'
            user_status.sent_at = None
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to mark as not sent: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get outreach statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_posts = OutreachStatus.query.count()
        sent_posts = OutreachStatus.query.filter_by(status='Sent').count()
        not_sent_posts = OutreachStatus.query.filter_by(status='Not Sent').count()
        
        # Get unique locations (excluding Unknown)
        locations = db.session.query(OutreachStatus.location).filter(
            OutreachStatus.location != 'Unknown',
            OutreachStatus.location.isnot(None)
        ).distinct().all()
        location_count = len(locations)
        
        return {
            'total_posts': total_posts,
            'sent_posts': sent_posts,
            'not_sent_posts': not_sent_posts,
            'unique_locations': location_count,
            'sent_percentage': round((sent_posts / total_posts * 100) if total_posts > 0 else 0, 1)
        }
    
    def get_active_message_template(self) -> Optional[str]:
        """
        Get the active message template.
        
        Returns:
            Message content or None if no template exists
        """
        template = MessageTemplate.query.filter_by(is_active=True).first()
        return template.content if template else self.config.DEFAULT_MESSAGE
    
    def create_default_template(self) -> None:
        """Create the default message template if it doesn't exist."""
        if not MessageTemplate.query.filter_by(name='Default').first():
            default_template = MessageTemplate(
                name='Default',
                content=self.config.DEFAULT_MESSAGE,
                is_active=True
            )
            db.session.add(default_template)
            db.session.commit()
