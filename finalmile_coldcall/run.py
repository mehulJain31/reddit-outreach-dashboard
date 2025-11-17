#!/usr/bin/env python3
"""Clean runner script for the Reddit outreach dashboard."""

import os
from app import create_app
from models import db


def main():
    """Main entry point for the application."""
    # Determine environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Initialize database
    with app.app_context():
        db.create_all()
        print('Database initialized!')
    
    # Print startup info
    port = 5002
    print(f'Starting Reddit Outreach Dashboard in {env} mode...')
    print(f'Open http://localhost:{port} in your browser')
    
    # Run application
    app.run(
        debug=(env == 'development'),
        host='0.0.0.0',
        port=port
    )


if __name__ == '__main__':
    main()
