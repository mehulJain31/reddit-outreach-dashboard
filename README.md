# Reddit Outreach Dashboard

A Python Flask application for tracking outreach to Reddit users who have recently purchased homes. Built with Clean Code principles for maintainability and scalability.

## 🎯 Features

- **Reddit Scraping**: Automatically fetches posts from r/FirstTimeHomeBuyer with "GOT THE KEY" flair
- **Location Parsing**: Extracts city/state information from post titles using the `us` library
- **Dashboard UI**: Clean, responsive web interface for managing outreach
- **Status Tracking**: Track which users have been contacted
- **Message Templates**: Pre-filled message templates for easy copying
- **SQLite Database**: Local database for tracking all activities
- **Statistics**: Real-time analytics on outreach progress
- **Clean Architecture**: Modular, testable, and maintainable codebase

## 🏗️ Architecture

```
finalmile_coldcall/
├── app.py                    # Flask application (Factory Pattern)
├── run.py                    # Application entry point
├── config.py                 # Configuration management
├── models.py                 # Database models
├── services/
│   ├── reddit_service.py    # Reddit API operations
│   └── outreach_service.py  # Business logic
├── templates/
│   └── dashboard.html       # Web UI
├── constants.py             # Reddit scraping constants
└── scrape_reddit.py         # Reddit scraping logic
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip or pipenv

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd reddit_scrape
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r finalmile_coldcall/requirements.txt
```

4. **Run the dashboard**
```bash
cd finalmile_coldcall
../.venv/bin/python run.py
```

5. **Open your browser**
Navigate to `http://localhost:5002`

## 📊 Usage

### 1. Refresh Posts
- Click "Refresh Posts" to fetch the latest posts from Reddit
- New posts are automatically added to the database
- Existing posts are updated if titles change

### 2. Review Posts
- Browse posts by status (All, Not Sent, Sent)
- View extracted location information
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

## 🛠️ Configuration

### Environment Variables

```bash
export FLASK_ENV=development  # or production
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///reddit_outreach.db
```

### Customization

Edit `config.py` to modify:
- Target subreddit
- Flair filter
- Message template
- Number of posts to fetch

## 🧪 Testing

```bash
# Run with test configuration
export FLASK_ENV=testing
python run.py

# Initialize test database
flask init-db

# Refresh data manually
flask refresh-data
```

## 📁 Database Schema

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

## 🔧 Development

### Adding New Features

1. **Create new service** in `services/` directory
2. **Add models** to `models.py` if needed
3. **Register routes** in `app.py`
4. **Update templates** if UI changes needed

### Code Style

This project follows Clean Code principles:
- Single Responsibility Principle
- Dependency Injection
- Factory Pattern
- Type Hints
- Comprehensive Error Handling

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /refresh_posts` - Fetch new posts from Reddit
- `GET /mark_sent/<username>` - Mark user as contacted
- `GET /mark_not_sent/<username>` - Undo sent status
- `GET /stats` - Get outreach statistics (JSON)

## 🔒 Security

- Manual message sending ensures Reddit ToS compliance
- No automated messaging
- Local SQLite database for privacy
- Configurable secret key
- SQL injection protection via SQLAlchemy

## 📈 Performance

- Efficient pagination for large datasets
- Optimized database queries
- Minimal external API calls
- Lightweight frontend with Tailwind CSS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is for educational purposes. Please ensure compliance with Reddit's Terms of Service when using.

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port in run.py
app.run(host='0.0.0.0', port=5003)  # Use available port
```

### Database Issues
```bash
# Reset database
rm reddit_outreach.db
flask init-db
```

### Reddit API Limits
- Wait a few minutes between refresh attempts
- Consider reducing `MAX_POSTS_TO_FETCH` in config

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the GitHub repository

---

**Built with Python, Flask, and Clean Code principles** 🐍✨
