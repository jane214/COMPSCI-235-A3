from flask import Blueprint, request, render_template, redirect, url_for, session

# import movie_web_app.adapters.Movie_repo as repo
import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_year_and_urls():
    years = services.get_years(repo.repo_instance)
    year_urls = dict()
    for year in years:
        year_urls[year] = url_for('movies_bp.movies_by_date', year=year)
    return year_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.movies_by_date', year=int(movie['year']))
    return movies
