"""Reddit service for fetching and managing posts."""

from typing import List, Tuple
from scrape_reddit import get_recent_posts_with_user_and_location
from config import Config


class RedditService:
    """Service class for Reddit operations."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def fetch_recent_posts(self) -> List[Tuple[str, str, str]]:
        """
        Fetch recent posts from Reddit.
        
        Returns:
            List of tuples: (title, location, username)
        """
        try:
            return get_recent_posts_with_user_and_location(
                subreddit_name=self.config.SUBREDDIT_NAME,
                target_flair=self.config.TARGET_FLAIR,
                max_posts=self.config.MAX_POSTS_TO_FETCH
            )
        except Exception as e:
            raise Exception(f"Failed to fetch posts from Reddit: {str(e)}")
    
    def create_post_url(self, username: str) -> str:
        """
        Create Reddit user profile URL.
        
        Args:
            username: Reddit username
            
        Returns:
            Full URL to user's profile
        """
        return f"https://www.reddit.com/user/{username}/"
    
    def is_valid_username(self, username: str) -> bool:
        """
        Check if username is valid.
        
        Args:
            username: Reddit username to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not username or username == '[deleted]':
            return False
        
        # Basic validation - Reddit usernames are 3-20 chars, alphanumeric + underscores + dashes
        return 3 <= len(username) <= 20 and username.replace('_', '').replace('-', '').isalnum()
