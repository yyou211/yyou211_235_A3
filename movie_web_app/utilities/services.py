from typing import Iterable
import random

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genres_names = [genre.genre_name for genre in genres]
    return genres_names

def get_all_actors(repo: AbstractRepository):
    all_actors = repo.get_all_actors()
    actors_names = [actor.actor_full_name for actor in all_actors]
    return actors_names

def get_all_directors(repo: AbstractRepository):
    all_directors = repo.get_all_directors()
    directors_names = [director.director_full_name for director in all_directors]
    return directors_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movie()
    if quantity >= movie_count:
        quantity = movie_count -1

    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# convert model entities to dicts


def movie_to_dict(movie:Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        # 'director': movie.director,
        # 'actors': movie.actors,
        'hyperlink': None,
        'genres': movie.genres, # 原来是genre
        'reviews': movie.reviews # 原来是review
    }
    return movie_dict


def movies_to_dict(movies):
    return [movie_to_dict(movie) for movie in movies]