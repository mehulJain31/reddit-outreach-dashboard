# Reddit Outreach Dashboard

A Flask-based dashboard for tracking outreach to Reddit users who have recently purchased homes.

## Features

- **Post Management**: Fetches and displays posts from r/FirstTimeHomeBuyer with "GOT THE KEY" flair
- **User Profiles**: Direct links to Reddit user profiles
- **Status Tracking**: Mark users as "Sent" or "Not Sent"
- **Message Template**: Pre-filled message template for easy copying
- **Database**: SQLite backend to track all outreach activities
- **Statistics**: Real-time stats on outreach progress
- **Location Data**: Extracts and displays location information from posts

## Setup

1. Install dependencies:
```bash
source .venv/bin/activate
pip install -r finalmile_coldcall/requirements.txt
```

2. Run the dashboard:
```bash
cd finalmile_coldcall
../.venv/bin/python run_dashboard.py
```

3. Open your browser and navigate to:
```
http://localhost:5001
```

## Usage

### 1. Refresh Posts
- Click "Refresh Posts" to fetch the latest posts from Reddit
- New posts are automatically added to the database
- Existing posts are updated if titles change

### 2. Review Posts
- Browse posts by status (All, Not Sent, Sent)
- View location information when available
- See post titles and timestamps

### 3. Send Messages
1. Click on the username link to open their Reddit profile
2. Click "Copy Message" to copy the template to clipboard
3. Paste the message in Reddit's DM
4. Click "Mark Sent" to update the status

### 4. Track Progress
- View statistics in the top bar
- Filter by sent/not sent status
- Monitor completion rate

## Database Schema

### OutreachStatus Table
- `username`: Reddit username (unique)
- `post_title`: Original post title
- `post_url`: Link to user's profile
- `location`: Extracted location from post
- `status`: "Not Sent" or "Sent"
- `created_at`: When post was added
- `sent_at`: When message was marked as sent

### MessageTemplate Table
- `name`: Template name
- `content`: Message content
- `is_active`: Whether template is active
- `created_at`: Creation timestamp

## Customization

### Message Template
Edit the `DEFAULT_MESSAGE` in `dashboard.py` to customize your outreach message.

### Scraping Parameters
Modify the parameters in `refresh_posts()` function:
- `subreddit_name`: Change target subreddit
- `target_flair`: Change flair filter
- `max_posts`: Adjust number of posts to fetch

## Data Privacy

- All data is stored locally in SQLite
- No data is shared with third parties
- Only publicly available Reddit posts are collected
- Users can opt out by not responding to messages

## Compliance

- Manual sending ensures compliance with Reddit's ToS
- No automated messaging
- Users control who they contact
- Easy to track and manage outreach

## Troubleshooting

### Port Already in Use
If port 5001 is in use, modify the port in `run_dashboard.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Change to available port
```

### Database Issues
Reset the database by deleting `reddit_outreach.db` and restarting the dashboard.

### Reddit API Limits
If you hit rate limits, wait a few minutes before refreshing posts again.

## Development

### Adding New Features
- Modify `dashboard.py` for new routes
- Update `templates/dashboard.html` for UI changes
- Add new models in `models.py`

### Database Migrations
For schema changes, delete the database file and restart to recreate tables.

## Security

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive config
- Consider adding authentication for multi-user access
