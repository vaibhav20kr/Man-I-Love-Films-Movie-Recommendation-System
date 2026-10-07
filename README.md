## Man I Love Films

A Django-based movie recommender for browsing a curated film collection by genre. Choose one or more genres to get a fresh set of matching movies, compare ratings out of 5, and keep exploring without seeing the same recommendations again until that genre cycle is complete.

## Features

- Filter the movie catalog by one or more genres.
- See movie descriptions, poster images when available, genre tags, and ratings out of 5.
- Remember the most recently selected genres between visits in the same browser session.
- Show up to 12 recommendations at a time, ordered by rating and title.
- Cycle back to the beginning when all matching movies have been shown.
- Add and manage movies and genres in Django Admin.
- Use a responsive dark interface with a comic-inspired style.

Recommendations are based on the selected genres and the ratings in the catalog; this project does not use a machine-learning model.

## Built with

- Python 3.10+
- Django 5.2.18
- SQLite
- Django templates, HTML, and CSS

## Project structure

```text
mov/
├── manage.py
├── README.md
├── movie_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── recommender/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── migrations/
    ├── management/commands/seed_movies.py
    └── templates/recommender/home.html
```

## Run locally

### Requirements

- Python 3.10 or newer
- pip
- Git (to clone the repository)

### Windows PowerShell

Clone the repository and enter the folder containing `manage.py`:

```powershell
git clone https://github.com/vaibhav20kr/Man-I-Love-Films-Movie-Recommendation-System.git
cd Man-I-Love-Films-Movie-Recommendation-System
```

Create and activate a virtual environment, then install Django:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "Django==5.2.18"
```

Create the database tables, add the starter catalog, and start the development server:

```powershell
python manage.py migrate
python manage.py seed_movies
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. Stop the server with `Ctrl+C` in the terminal.

If PowerShell blocks virtual-environment activation, open a new Command Prompt and activate it with:

```bat
.venv\Scripts\activate.bat
```

### macOS or Linux

After cloning and entering the project folder, create and activate the virtual environment, then install Django:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "Django==5.2.18"
```

Then run the same three `manage.py` commands shown above.

## Seed the movie catalog

The `seed_movies` command adds the starter movie data. By default, it creates missing movies and leaves existing matching titles unchanged, so it can be run more than once without duplicating titles.

Update existing seeded titles as well:

```powershell
python manage.py seed_movies --update-existing
```

Replace the catalog with only the movies in the seed list:

```powershell
python manage.py seed_movies --replace-catalog
```

**Caution:** `--replace-catalog` deletes movie records that are not included in the seed list. Back up your database before using it if you need to keep your current catalog.

Seed ratings use a 0–5 scale and are sample catalog ratings; they are not intended to reproduce anyone's personal Letterboxd ratings.

## Django Admin

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Start the server and visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to manage movies and genres.

## Data models

- **Genre**: a genre name, such as Horror, Comedy, or Superhero.
- **Movie**: a title, description, poster image URL, rating, and one or more genres.

The local database uses SQLite and is stored in `db.sqlite3` after migrations are applied.

## Deployment note

This repository is configured for local development. Django's `runserver` is not intended for production. Before deploying publicly, configure a production server, database, and static-file serving; load `SECRET_KEY` from an environment variable; set `DEBUG=False`; and configure `ALLOWED_HOSTS`. See the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).
