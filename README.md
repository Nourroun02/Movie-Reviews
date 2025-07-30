# 🎬 Movie-Reviews - Django & Docker Powered Movie Review Platform

Transform movie reviews into community masterpieces with this scalable web application built using Django, Docker, and modern web technologies

Tech Stack: Django · Python · Docker · Nginx · JavaScript · HTML5 · CSS3


## Features

# Django-Powered Backend:

-Robust database models for movies, reviews, and users

-Authentication & authorization (login, signup, profiles)

-Admin dashboard for content management

# Dockerized Development & Production:

-"docker-compose.yml" for easy local development

-Optimized "Dockerfile" for production deployments

-Nginx reverse proxy for static files and load balancing

# Modern Frontend:

-Responsive UI with HTML5, CSS3, and JavaScript
-User-friendly review system with ratings

 #DevOps & CI/CD Ready:

-Pre-configured for GitHub Actions / GitLab CI

-Automated testing & deployment workflows

## Installation

Clone the repository:


```bash
git clone https://github.com/Nourroun02/Movie-Reviews.git
cd Movie-Reviews
```

Set up environment variables:
```bash
cp .env.example .env  # Edit with your settings
```
Run with Docker (Recommended):
```bash
docker-compose up --build
```
Access at: http://localhost:8001

Or run locally:
```bash
python -m venv venv
source venv/bin/activate  # Windows: `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


