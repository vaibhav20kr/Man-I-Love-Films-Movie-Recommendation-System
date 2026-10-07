# Man I Love Films

A Django movie recommender for browsing a movie collection by genre. Choose one or more genres to get recommendations, with ratings shown out of 5.

## Features

- Filter movies by one or more genres.
- View each movie's description, genres, and rating.
- Remember the last searched genres and cycle through recommendations without repeats.
- Manage movies and genres through Django Admin.

## Built with

Python · Django · SQLite · HTML and CSS

## Run locally

Requires Python 3.10+ and Git. In Windows PowerShell:

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

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Admin screenshots

<img width="300" alt="Movie catalog in Django Admin" src="https://github.com/user-attachments/assets/701b3811-e04a-4235-b13f-b638d0654b1d" />
<img width="300" alt="Adding a movie in Django Admin" src="https://github.com/user-attachments/assets/ba5ad4bc-2d19-4d2d-9270-24e3c77bc9aa" />
<img width="300" alt="Movie details in Django Admin" src="https://github.com/user-attachments/assets/4c956f58-823f-47d0-aa31-fb9e577f7c6e" />

## Website screenshots
<img width="300" height="150" alt="Screenshot 2026-10-07 183110" src="https://github.com/user-attachments/assets/e62e08e9-f1ba-4c67-a493-fa47d5207fed" />
<img width="300" height="150" alt="Screenshot 2026-10-07 183256" src="https://github.com/user-attachments/assets/81bf3dd4-ed3c-4969-9edd-124c6c86dca3" />


The development server is for local use; production deployment needs separate Django settings.
