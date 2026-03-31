# FlaskFM - Flask SQLAlchemy Practice

This project is a Flask practice app built with SQLAlchemy and SQLite as part of Codecademy's Build Python Web Apps with Flask course. It focuses on modeling users, playlists, songs, and playlist items, then connecting them through routes and templates so users can browse songs, manage playlists, and update the shared music library.

## Features

- View all user profiles at `/profiles`
- Open a user's profile and see:
  - all available songs
  - that user's playlist
  - add/remove playlist item actions
- Add songs from the dashboard
- View song popularity rankings on the dashboard
- Extra: delete songs from the dashboard and automatically remove related `Item` records
- Extra: redirect after submitting the dashboard form to avoid duplicate POST submissions on refresh

## What I Practiced

- Virtual environment and dependencies
- Database and app configuration with `.env`, `os.getenv()`, and `load_dotenv()`
- Database setup and seed data using Flask application context
- One-to-one and one-to-many SQLAlchemy relationships
- SQLAlchemy 2.0 models and queries
- CRUD operations with Flask routes
- DB Browser for inspecting SQLite data
- Cascade deletes for removing related child records
- Redirect-after-POST

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies from `requirements.txt`.
3. Create a `.env` file using `.env.example` as reference, then add your own `DATABASE_URL` and `SECRET_KEY`.
4. Create the database tables.
5. Run `add_data.py` to seed the database.
6. Start the Flask app.

```text
$ python -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
$ python
>>> from app import app, db
>>> from models import *
>>> with app.app_context():
...     db.create_all()
...
>>> exit()
$ python add_data.py
$ flask run
```
