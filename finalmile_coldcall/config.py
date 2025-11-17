"""Configuration settings for the Reddit outreach dashboard."""

import os
from pathlib import Path

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///reddit_outreach.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Reddit scraping settings
    SUBREDDIT_NAME = 'FirstTimeHomeBuyer'
    TARGET_FLAIR = 'GOT THE KEY'
    MAX_POSTS_TO_FETCH = 50
    
    # Dashboard settings
    POSTS_PER_PAGE = 20
    
    # Message template
    DEFAULT_MESSAGE = """Hey!
I just saw your post on r/FirstTimeHomeBuyer. Congrats on your new place that's awesome.
I actually just closed on a house in Dallas too, and it was a pretty wild ride. I've been chatting with a few other recent buyers to hear how their last few weeks before closing went — what parts felt the most stressful or confusing.
If you're up for it, I'd love to have a quick 15 minute chat sometime this week. Totally casual, just trying to learn from others who went through the same craziness so I can figure out how to make the process smoother for people like us.

You can book a time directly here: https://calendly.com/mehul-jainuta/15min"""


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
