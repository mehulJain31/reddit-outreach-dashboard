#!/usr/bin/env python3
"""Runner script for the Reddit outreach dashboard."""

from dashboard import app, db

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create default message template if it doesn't exist
        from models import MessageTemplate
        if not MessageTemplate.query.filter_by(name='Default').first():
            from dashboard import DEFAULT_MESSAGE
            default_template = MessageTemplate(
                name='Default',
                content=DEFAULT_MESSAGE,
                is_active=True
            )
            db.session.add(default_template)
            db.session.commit()
            print('Default message template created!')
    
    print('Starting Reddit Outreach Dashboard...')
    print('Open http://localhost:5002 in your browser')
    app.run(debug=True, host='0.0.0.0', port=5002)
