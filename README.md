# Man I Love Films

A Django movie recommender for browsing a movie collection by genre. Choose one or more genres to get recommendations, with ratings shown out of 5.

## Features

- Filter movies by one or more genres
- View each movie’s description, genres, and rating
- Keep track of the last searched genres
- Cycle through recommendations without repeats until the matching list is exhausted
- Manage movies and genres through Django Admin

## Built with

- Python
- Django
- SQLite
- HTML and CSS

## Run locally

Open a terminal in the folder containing `manage.py`, then run:

```powershell
python -m pip install django
python manage.py migrate
python manage.py seed_movies
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Django Admin

Create an admin account:

```powershell
python manage.py createsuperuser
```

Then open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Seed data

`python manage.py seed_movies` adds the curated movie list without duplicating matching titles.

The `--replace-catalog` option deletes movie records that are not in the seed list. Use it only if you intend to replace your existing catalog.