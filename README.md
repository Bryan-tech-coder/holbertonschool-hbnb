# HBnB - Holberton School Project

## Overview
This project is a full-stack web application for booking and reviewing places to stay, inspired by Airbnb. It includes a modern frontend (HTML/CSS/JS) and a RESTful backend API (Flask, SQLAlchemy, JWT).

## Features
- User authentication (JWT-based login/logout)
- Browse, filter, and view places
- Place details with amenities and reviews
- Add reviews (authenticated users)
- Responsive, modern UI
- Docker and requirements for easy setup

## Technologies
- **Backend:** Python, Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-CORS
- **Frontend:** HTML5, CSS3 (responsive, modern), Vanilla JS
- **Database:** SQLite (default), SQLAlchemy ORM
- **Other:** Docker, Alembic (migrations), pytest (tests)

## Quick Start

### 1. Clone the repository
```
git clone https://github.com/Bryan-tech-coder/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

### 2. Set up Python environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r part3/requirements.txt
```

### 3. Initialize the database and create admin user
```
cd part3
python create_user.py
```

### 4. Run the backend server
```
python run.py
```
The API will be available at [http://127.0.0.1:5002](http://127.0.0.1:5002)

### 5. Open the frontend
Open `part4/index.html` in your browser (or use the backend to serve static files).

## Demo Credentials
- **Email:** admin@example.com
- **Password:** supersecretpassword

## Project Structure
```
part3/   # Backend (Flask API, models, scripts)
part4/   # Frontend (HTML, CSS, JS, images)
```

## Author
Bryan Ramos

## Documentation & Comments
- All code is documented in English for easy explanation and demo.
- See comments in HTML, JS, and CSS for structure and logic.

## License
MIT

---

## HBnB Database ER Diagram

```mermaid
erDiagram

USER {
    int id
    string email
    string first_name
    string last_name
    string password
    boolean is_admin
    datetime created_at
    datetime updated_at
}

PLACE {
    int id
    string name
    string description
    float price
    float latitude
    float longitude
    int owner_id
}

REVIEW {
    int id
    string text
    int rating
    int user_id
    int place_id
}

AMENITY {
    int id
    string name
    string description
}

PLACE_AMENITY {
    int place_id
    int amenity_id
}

USER ||--o{ PLACE : owns
USER ||--o{ REVIEW : writes
PLACE ||--o{ REVIEW : receives
PLACE ||--o{ PLACE_AMENITY : has
AMENITY ||--o{ PLACE_AMENITY : included_in
```
## Docker (quick start)

To build and run the API (part3) and the frontend static site (part4) using Docker and docker-compose:

1. Build and start containers:

```bash
docker-compose build --pull
docker-compose up -d
```

2. Open the frontend at: http://localhost:8080
    - The API will be available at: http://localhost:5002

3. Stop and remove containers:

```bash
docker-compose down --volumes
```

Notes:
- The API `Dockerfile` installs dependencies from `part3/requirements.txt`. If a pinned dependency fails during build (for example an unavailable exact version of `Flask-CORS`), the Dockerfile also installs a compatible `flask-cors` afterwards.
- If you prefer to run only the API locally (no Docker), continue using your virtualenv.

Production notes:
- The `part3/Dockerfile` now runs the API under `gunicorn` (non-root user) and exposes `/health` for container healthchecks.
- To build production images and run:

```bash
docker-compose build --pull
docker-compose up -d
docker-compose ps
```

To view API logs:

```bash
docker-compose logs -f api
```
