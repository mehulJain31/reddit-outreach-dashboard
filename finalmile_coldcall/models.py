"""Database models for the Reddit outreach dashboard."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class OutreachStatus(db.Model):
    """Track outreach status for each Reddit user."""
    __tablename__ = 'outreach_status'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    post_title = db.Column(db.Text, nullable=False)
    post_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Not Sent')  # Not Sent, Sent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<OutreachStatus {self.username}: {self.status}>'
    
    def mark_as_sent(self):
        """Mark the outreach as sent."""
        self.status = 'Sent'
        self.sent_at = datetime.utcnow()
        db.session.commit()

class MessageTemplate(db.Model):
    """Store message templates for outreach."""
    __tablename__ = 'message_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MessageTemplate {self.name}>'
