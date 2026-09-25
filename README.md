# PocketSmart AI

PocketSmart AI is a GenAI-powered budget and recommendation assistant.

The application supports:

- Home Interior Planning
- Party Planning
- Jewelry Recommendations
- Optional outfit image analysis
- Gemini AI integration
- Fallback recommendations
- User registration
- User login
- Logout
- JWT authentication
- Session management
- Recommendation history
- Responsive frontend

---

## Project Architecture

PocketSmartAI/

app/

    main.py
    config.py
    db.py
    security.py

    models/

        schemas.py

    routes/

        api.py
        pages.py

    services/

        auth.py
        catalog.py
        fallback.py
        gemini_utils.py

    templates/

        base.html
        home.html
        login.html
        register.html
        dashboard.html
        planner_home.html
        planner_party.html
        planner_jewelry.html
        history.html
        testimonials.html

    static/

        css/

            style.css

        js/

            app.js

data/

uploads/

tests/

run.py

requirements.txt

.env

---

# Installation

Create a virtual environment:

Windows:

    py -3.11 -m venv .venv

Activate it:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

---

# Environment Variables

Create a file named:

    .env

Example:

    APP_NAME=PocketSmart AI

    SECRET_KEY=my-secret-key

    GEMINI_API_KEY=YOUR_API_KEY

    GEMINI_MODEL=gemini-3.8-flash

    ACCESS_TOKEN_EXPIRE_MINUTES=60

    MAX_UPLOAD_MB=5

---

# Run

Run:

    uvicorn app.main:app --reload

Or:

    python run.py

Open:

    http://127.0.0.1:8000

---

# Pages

Home:

    /

Register:

    /register

Login:

    /login

Dashboard:

    /dashboard

Home Planner:

    /planner/home

Party Planner:

    /planner/party

Jewelry Planner:

    /planner/jewelry

History:

    /history

Testimonials:

    /testimonials

---

# API Endpoints

POST /register

POST /login

POST /logout

POST /token

GET /session-info

GET /session-data

GET /history

POST /generate-home

POST /generate-party

POST /generate-jewelry

POST /recommendations-details

GET /startup

GET /health

---

# Testing

Run:

    python -m unittest discover -s tests -v

---

# Gemini

The Gemini API key must remain on the backend.

Do not put the API key inside JavaScript.

If the Gemini API key is not configured,
PocketSmart AI automatically uses the
built-in fallback recommendation system.

This allows the application UI and core
workflow to be tested without an API key.