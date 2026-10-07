# Man I Love Films

A Django movie recommender for browsing a curated collection by genre. Ratings are out of 5.

## Features

- Get movie recommendations by one or more genres.
- See each movie’s rating, description, and genres.
- Recommendations cycle through matching movies without repeats until the list is exhausted.
- Manage movies and genres in Django Admin.

## Run locally

Requires Python 3.10+ and Git. In PowerShell:

```powershell
git clone https://github.com/vaibhav20kr/Man-I-Love-Films-Movie-Recommendation-System.git
cd Man-I-Love-Films-Movie-Recommendation-System
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "Django==5.2.18"
python manage.py migrate
python manage.py seed_movies
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Admin Screenshots
<img width="1475" height="812" alt="Screenshot 2026-10-07 165743" src="https://github.com/user-attachments/assets/9895b698-1dc5-4c59-8d5b-a3ce6b52f961" />
