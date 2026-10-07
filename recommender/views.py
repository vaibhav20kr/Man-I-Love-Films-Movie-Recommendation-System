from django.shortcuts import render

from .models import Genre, Movie


LAST_GENRES_SESSION_KEY = "movie_recommender_last_genres"
SHOWN_MOVIES_SESSION_KEY = "movie_recommender_shown_movies"
RECOMMENDATION_LIMIT = 12


def _integer_ids(values):
    """Return unique integer IDs, ignoring invalid session or query values."""
    result = []
    for value in values:
        try:
            value = int(value)
        except (TypeError, ValueError):
            continue
        if value not in result:
            result.append(value)
    return result


def home(request):
    genres = Genre.objects.all().order_by("name")
    valid_genre_ids = {genre.id for genre in genres}

    if request.GET.get("clear") == "1":
        request.session.pop(LAST_GENRES_SESSION_KEY, None)
        request.session.pop(SHOWN_MOVIES_SESSION_KEY, None)
        selected_genres = []
    elif request.GET.get("search") == "1" or "genres" in request.GET:
        selected_genres = [
            genre_id
            for genre_id in _integer_ids(request.GET.getlist("genres"))
            if genre_id in valid_genre_ids
        ]
        previous_genres = [
            genre_id
            for genre_id in _integer_ids(
                request.session.get(LAST_GENRES_SESSION_KEY, [])
            )
            if genre_id in valid_genre_ids
        ]

        # A new genre search starts a fresh recommendation history.
        if set(selected_genres) != set(previous_genres):
            request.session[SHOWN_MOVIES_SESSION_KEY] = []
        request.session[LAST_GENRES_SESSION_KEY] = selected_genres
    else:
        # Going back to the homepage keeps using the last searched genre(s).
        selected_genres = [
            genre_id
            for genre_id in _integer_ids(
                request.session.get(LAST_GENRES_SESSION_KEY, [])
            )
            if genre_id in valid_genre_ids
        ]

    matching_movies = Movie.objects.all().prefetch_related("genres")
    if selected_genres:
        matching_movies = matching_movies.filter(
            genres__id__in=selected_genres
        ).distinct()
    else:
        # Do not show the entire catalog before the user chooses a genre.
        matching_movies = matching_movies.none()

    shown_ids = _integer_ids(
        request.session.get(SHOWN_MOVIES_SESSION_KEY, [])
    )
    unseen_movies = matching_movies.exclude(id__in=shown_ids)
    movies = list(
        unseen_movies.order_by("-rating", "title")[:RECOMMENDATION_LIMIT]
    )

    # Once every matching movie has been shown, start the recommendation cycle
    # over instead of displaying an end-of-list message.
    if not movies and shown_ids and matching_movies.exists():
        shown_ids = []
        movies = list(
            matching_movies.order_by("-rating", "title")[:RECOMMENDATION_LIMIT]
        )

    if movies:
        request.session[SHOWN_MOVIES_SESSION_KEY] = shown_ids + [
            movie.id for movie in movies
        ]

    selected_genre_names = list(
        Genre.objects.filter(id__in=selected_genres)
        .order_by("name")
        .values_list("name", flat=True)
    )

    if selected_genre_names:
        recommendation_heading = "Recommended: " + ", ".join(
            selected_genre_names
        )
        if not movies:
            empty_message = "There are no movies in the selected genre yet."
        else:
            empty_message = ""
    else:
        recommendation_heading = "Recommended movies"
        empty_message = "Choose one or more genres to get recommendations."

    context = {
        "genres": genres,
        "movies": movies,
        "selected_genres": selected_genres,
        "selected_genre_names": selected_genre_names,
        "recommendation_heading": recommendation_heading,
        "empty_message": empty_message,
    }
    return render(request, "recommender/home.html", context)
