# Todo API - Flask Application

A full-stack todo application built with Flask, featuring both REST API endpoints and a web interface.

## Features

- ✅ Create, read, update, and delete todos
- 🎯 Toggle completion status
- 🌐 REST API endpoints
- 💻 Web interface with HTML templates
- 📱 Responsive design

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Open http://localhost:5000 in your browser

## API Endpoints

- `GET /todos` - Get all todos
- `POST /todo` - Create a new todo
- `GET /todo/<id>` - Get specific todo
- `PATCH /todo/<id>` - Update todo
- `DELETE /todo/<id>` - Delete todo

## Deployment Options

### 1. Heroku Deployment

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-todo-app-name

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key-here"

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 2. Railway Deployment

1. Connect your GitHub repository to Railway
2. Railway will auto-detect your Flask app
3. Set environment variables:
   - `SECRET_KEY`: Your secret key
   - `FLASK_DEBUG`: false

### 3. Docker Deployment

```dockerfile
# Dockerfile is ready - build and run:
docker build -t todo-app .
docker run -p 5000:5000 todo-app
```

## Environment Variables

- `PORT`: Port to run the application (default: 5000)
- `SECRET_KEY`: Secret key for Flask sessions
- `DATABASE_URL`: Database connection string (default: SQLite)
- `FLASK_DEBUG`: Enable debug mode (default: False)

## Project Structure

```
todo-api/
├── main.py              # Main Flask application
├── templates/
│   └── index.html       # Web interface template
├── static/
│   └── style.css        # Styles for web interface
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku process file
├── runtime.txt         # Python version specification
└── README.md           # This file
```

## Technologies Used

- **Backend**: Flask, Flask-RESTful, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Heroku, Railway, Docker