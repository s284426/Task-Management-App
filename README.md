# Task Management System

A Django-based web application for managing tasks and projects with user authentication and role-based access control.

## Features
- User Authentication (Login/Register)
- Role-based access (Admin vs Standard User)
- Create/Update/Delete Tasks & Projects
- Task filtering and categorization
- Responsive UI with Bootstrap
- Docker support

## Technologies
- Python 3.11+
- Django 4.2
- PostgreSQL
- Bootstrap 5
- Gunicorn
- WhiteNoise

## Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional)

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/s284426/Task-Management-1.git
cd task-manager
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create `.env` file:
```bash
cp .env.example .env
```
Edit `.env` with your credentials:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=taskdb
DB_USER=taskuser
DB_PASSWORD=taskpass
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```
Access at: http://localhost:8000

### Docker Setup
```bash
docker-compose up --build
```
Access at: http://localhost:8000

## Testing
```bash
python manage.py test
```

## Deployment
1. **Heroku**:
```bash
heroku create
heroku addons:create heroku-postgresql
git push heroku main
```

2. **Docker Production**:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Project Structure
```
taskmanager/
├── taskmanager/       # Main project config
├── tasks/             # Task management app
├── users/             # User authentication app
├── static/            # Static files
├── templates/         # HTML templates
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## License
MIT License"# Task-Management-App" 
