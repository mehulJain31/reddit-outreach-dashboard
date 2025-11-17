#!/usr/bin/env python3
"""Script to update the message template in the database."""

from app import create_app
from models import db, MessageTemplate
from config import Config

def update_message_template():
    """Update the default message template in the database."""
    app = create_app()
    
    with app.app_context():
        # Get or create the default template
        template = MessageTemplate.query.filter_by(name='Default').first()
        
        if template:
            template.content = Config.DEFAULT_MESSAGE
            print("Updated existing message template")
        else:
            template = MessageTemplate(
                name='Default',
                content=Config.DEFAULT_MESSAGE,
                is_active=True
            )
            db.session.add(template)
            print("Created new message template")
        
        db.session.commit()
        print("Message template updated successfully!")
        
        print("\nNew message template:")
        print("=" * 50)
        print(template.content)
        print("=" * 50)

if __name__ == '__main__':
    update_message_template()
