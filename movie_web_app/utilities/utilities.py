from flask import Blueprint, request, render_template, redirect, url_for, session

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names: # 跟covid 差不多
        genre_urls[genre_name] = url_for('movie_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_selected_movies(quantity = 5):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    for movie in movies:
        movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year = int(movie['release_year']))
    return movies


