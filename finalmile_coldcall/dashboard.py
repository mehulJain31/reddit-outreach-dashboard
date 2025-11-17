"""Flask dashboard for Reddit outreach tracking."""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, OutreachStatus, MessageTemplate
from scrape_reddit import get_recent_posts_with_user_and_location
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reddit_outreach.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Default message template
DEFAULT_MESSAGE = """Hey!
I just saw your post on r/FirstTimeHomeBuyer. Congrats on your new place that's awesome.
I actually just closed on a house in Dallas too, and it was a pretty wild ride. I've been chatting with a few other recent buyers to hear how their last few weeks before closing went — what parts felt the most stressful or confusing.
If you're up for it, I'd love to have a quick 15 minute chat sometime this week. Totally casual, just trying to learn from others who went through the same craziness so I can figure out how to make the process smoother for people like us."""

@app.route('/')
def dashboard():
    """Main dashboard showing posts and outreach status."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status_filter = request.args.get('status', 'all')
    auto_refresh = request.args.get('auto_refresh', 'false')
    
    # Auto-refresh posts on first load
    if auto_refresh == 'true':
        try:
            reddit_posts = get_recent_posts_with_user_and_location(
                "FirstTimeHomeBuyer", 
                target_flair="GOT THE KEY", 
                max_posts=50
            )
            
            new_posts_count = 0
            updated_posts_count = 0
            
            for title, location, username in reddit_posts:
                existing = OutreachStatus.query.filter_by(username=username).first()
                post_url = f"https://www.reddit.com/user/{username}/"
                
                if existing:
                    if existing.post_title != title:
                        existing.post_title = title
                        existing.location = location
                        updated_posts_count += 1
                else:
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
            flash(f'Auto-refreshed: Added {new_posts_count} new posts, updated {updated_posts_count}.', 'success')
            
        except Exception as e:
            flash(f'Auto-refresh error: {str(e)}', 'error')
    
    query = OutreachStatus.query.order_by(OutreachStatus.created_at.desc())
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    posts = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get active message template
    template = MessageTemplate.query.filter_by(is_active=True).first()
    message_content = template.content if template else DEFAULT_MESSAGE
    
    return render_template('dashboard.html', posts=posts, message_content=message_content, status_filter=status_filter)

@app.route('/refresh_posts')
def refresh_posts():
    """Fetch new posts from Reddit and update database."""
    try:
        # Get fresh posts from Reddit
        reddit_posts = get_recent_posts_with_user_and_location(
            "FirstTimeHomeBuyer", 
            target_flair="GOT THE KEY", 
            max_posts=50
        )
        
        new_posts_count = 0
        updated_posts_count = 0
        
        for title, location, username in reddit_posts:
            # Check if user already exists
            existing = OutreachStatus.query.filter_by(username=username).first()
            
            post_url = f"https://www.reddit.com/user/{username}/"
            
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
        
        flash(f'Successfully added {new_posts_count} new posts and updated {updated_posts_count} existing posts.', 'success')
        
    except Exception as e:
        flash(f'Error refreshing posts: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/mark_sent/<username>')
def mark_sent(username):
    """Mark a user as having been contacted."""
    user_status = OutreachStatus.query.filter_by(username=username).first_or_404()
    user_status.mark_as_sent()
    flash(f'Marked {username} as sent.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/mark_not_sent/<username>')
def mark_not_sent(username):
    """Mark a user as not sent (undo)."""
    user_status = OutreachStatus.query.filter_by(username=username).first_or_404()
    user_status.status = 'Not Sent'
    user_status.sent_at = None
    db.session.commit()
    flash(f'Marked {username} as not sent.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/stats')
def stats():
    """Show outreach statistics."""
    total_posts = OutreachStatus.query.count()
    sent_posts = OutreachStatus.query.filter_by(status='Sent').count()
    not_sent_posts = OutreachStatus.query.filter_by(status='Not Sent').count()
    
    # Get unique locations
    locations = db.session.query(OutreachStatus.location).filter(
        OutreachStatus.location != 'Unknown',
        OutreachStatus.location.isnot(None)
    ).distinct().all()
    location_count = len(locations)
    
    return jsonify({
        'total_posts': total_posts,
        'sent_posts': sent_posts,
        'not_sent_posts': not_sent_posts,
        'unique_locations': location_count,
        'sent_percentage': round((sent_posts / total_posts * 100) if total_posts > 0 else 0, 1)
    })

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    
    # Create default message template
    if not MessageTemplate.query.filter_by(name='Default').first():
        default_template = MessageTemplate(
            name='Default',
            content=DEFAULT_MESSAGE,
            is_active=True
        )
        db.session.add(default_template)
        db.session.commit()
    
    print('Database initialized successfully!')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
