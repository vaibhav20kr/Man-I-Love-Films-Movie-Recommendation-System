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

## Django Admin Screenshots
<img width="300" height="150" alt="Screenshot 2026-10-07 165446" src="https://github.com/user-attachments/assets/701b3811-e04a-4235-b13f-b638d0654b1d" />
<img width="300" height="150" alt="Screenshot 2026-10-07 165519" src="https://github.com/user-attachments/assets/ba5ad4bc-2d19-4d2d-9270-24e3c77bc9aa" />
<img width="300" height="150" alt="Screenshot 2026-10-07 165844" src="https://github.com/user-attachments/assets/4c956f58-823f-47d0-aa31-fb9e577f7c6e" />


## Seed data

`python manage.py seed_movies` adds the curated movie list without duplicating matching titles.

The `--replace-catalog` option deletes movie records that are not in the seed list. Use it only if you intend to replace your existing catalog.
