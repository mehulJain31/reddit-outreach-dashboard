"""Main Flask application for Reddit outreach dashboard."""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db
from config import config
from services.outreach_service import OutreachService


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration name ('development', 'production')
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize services
    outreach_service = OutreachService(app.config)
    
    # Register routes
    register_routes(app, outreach_service)
    
    # Register CLI commands
    register_cli_commands(app, outreach_service)
    
    return app


def register_routes(app: Flask, outreach_service: OutreachService) -> None:
    """Register all application routes."""
    
    @app.route('/')
    def dashboard():
        """Main dashboard showing posts and outreach status."""
        page = request.args.get('page', 1, type=int)
        status_filter = request.args.get('status', 'all')
        auto_refresh = request.args.get('auto_refresh', 'false')
        
        # Auto-refresh posts on first load
        if auto_refresh == 'true':
            try:
                result = outreach_service.refresh_posts()
                flash(
                    f'Auto-refreshed: Added {result["new_posts"]} new posts, '
                    f'updated {result["updated_posts"]}.', 
                    'success'
                )
            except Exception as e:
                flash(f'Auto-refresh error: {str(e)}', 'error')
        
        posts = outreach_service.get_posts(page, status_filter)
        message_content = outreach_service.get_active_message_template()
        
        return render_template(
            'dashboard.html', 
            posts=posts, 
            message_content=message_content, 
            status_filter=status_filter
        )
    
    @app.route('/refresh_posts')
    def refresh_posts():
        """Fetch new posts from Reddit and update database."""
        try:
            result = outreach_service.refresh_posts()
            flash(
                f'Successfully added {result["new_posts"]} new posts and '
                f'updated {result["updated_posts"]} existing posts.', 
                'success'
            )
        except Exception as e:
            flash(f'Error refreshing posts: {str(e)}', 'error')
        
        return redirect(url_for('dashboard'))
    
    @app.route('/mark_sent/<username>')
    def mark_sent(username: str):
        """Mark a user as having been contacted."""
        try:
            if outreach_service.mark_as_sent(username):
                flash(f'Marked {username} as sent.', 'success')
            else:
                flash(f'User {username} not found.', 'error')
        except Exception as e:
            flash(f'Error marking as sent: {str(e)}', 'error')
        
        return redirect(url_for('dashboard'))
    
    @app.route('/mark_not_sent/<username>')
    def mark_not_sent(username: str):
        """Mark a user as not sent (undo)."""
        try:
            if outreach_service.mark_as_not_sent(username):
                flash(f'Marked {username} as not sent.', 'info')
            else:
                flash(f'User {username} not found.', 'error')
        except Exception as e:
            flash(f'Error marking as not sent: {str(e)}', 'error')
        
        return redirect(url_for('dashboard'))
    
    @app.route('/stats')
    def stats():
        """Show outreach statistics."""
        try:
            statistics = outreach_service.get_statistics()
            return jsonify(statistics)
        except Exception as e:
            return jsonify({'error': str(e)}), 500


def register_cli_commands(app: Flask, outreach_service: OutreachService) -> None:
    """Register CLI commands."""
    
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        outreach_service.create_default_template()
        print('Database initialized successfully!')
    
    @app.cli.command()
    def refresh_data():
        """Refresh data from Reddit."""
        try:
            result = outreach_service.refresh_posts()
            print(f'Added {result["new_posts"]} new posts, updated {result["updated_posts"]}')
        except Exception as e:
            print(f'Error: {str(e)}')


# Create application instance
app = create_app()
