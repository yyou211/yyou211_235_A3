from typing import List, Iterable

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import make_review, Movie, Review, Genre,ActorReview, DirectorReview, Actor,Director
from movie_web_app.domain.model import make_actor_review, make_director_review

class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(user_name: str, movie_id: int, review_text:str, repo: AbstractRepository):
    movie = repo.get_movie_by_id(int(movie_id))

    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(user, movie, review_text)

    repo.add_review(review)

def add_actor_review(user_name: str, actor_name: str, review_text:str, repo: AbstractRepository):
    actor = repo.get_actor(actor_name)
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    review = make_actor_review(user, actor, review_text)
    repo.add_actor_review(review)

def add_director_review(user_name: str, director_name: str, review_text:str, repo: AbstractRepository):
    director = repo.get_director(director_name)
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    review = make_director_review(user, director, review_text)
    repo.add_director_review(review)



def get_movie_by_id(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)

# 可能需要get_movies_by_name
def get_movies_by_name(name, repo: AbstractRepository):
    movie = repo.get_movies_by_name(name)
    # if len(movie) == 0:
    #     raise NonExistentMovieException
    # else:
    #     return movies_to_dict(movie)
    return movies_to_dict(movie)

def get_movies_by_director(director_name, repo: AbstractRepository):
    movie = repo.get_movies_by_director(director_name)
    return movies_to_dict(movie)

def get_movies_by_actor(actor_name, repo: AbstractRepository):
    movie = repo.get_movies_by_actor(actor_name)
    return movies_to_dict(movie)

def get_actor(name,repo:AbstractRepository):
    actor = repo.get_actor(name)
    return actor_to_dict(actor)

def get_director(name,repo:AbstractRepository):
    director = repo.get_director(name)
    return director_to_dict(director)

def get_all_actors(repo:AbstractRepository):
    actors = repo.get_all_actors()
    return actors_to_dict(actors)

def get_all_directors(repo:AbstractRepository):
    directors = repo.get_all_directors()
    return directors_to_dict(directors)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)

def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)

def get_movies_by_year(year, repo: AbstractRepository):
    movies = repo.get_movies_by_year(target_year = year)

    movies_dto = list()
    prev_year = next_year = None

    if len(movies) > 0:
        prev_year = repo.get_year_of_previous_movie(movies[0]) #可能要改
        next_year = repo.get_year_of_next_movie(movies[0])

        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year

def get_movie_ids_for_genre(genre_name, repo:AbstractRepository):
    movies_ids = repo.get_movie_ids_for_genre(genre_name)
    return movies_ids

def get_movies_by_id(id_list, repo:AbstractRepository):
    movies = repo.get_movies_by_id(id_list)
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict

def get_reviews_for_movie(movie_id, repo:AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)
    if movie is None:
        raise NonExistentMovieException
    return reviews_to_dict(movie.reviews)

def get_reviews_for_actor(actor_name, repo:AbstractRepository):
    actor = repo.get_actor(actor_name)
    return actor_reviews_to_dict(actor.reviews)

def get_reviews_for_director(director_name, repo:AbstractRepository):
    director = repo.get_director(director_name)
    return director_reviews_to_dict(director.reviews)


#functions to convert model entities to dicts

def movie_to_dict(movie:Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        # 'actors': movie.actors,
        # 'director': movie.director,
        'hyperlink': None,
        'genres': movie.genres,
        'reviews': movie.reviews,
        'description': movie.description
    }
    return movie_dict


def movies_to_dict(movies):
    return [movie_to_dict(movie) for movie in movies]

def review_to_dict(review:Review):
    review_dict = {
        'user': review.user,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        #'rating':review.rating,
        'timestamp': review.timestamp
    }
    return review_dict

def reviews_to_dict(reviews):
    return [review_to_dict(review) for review in reviews]

def genre_to_dict(genre:Genre):
    genre_dict = {
        'genre_name': genre.genre_name,
        'tagged_movies': [movie.id for movie in genre.tagged_movies]
    }
    return genre_dict

def genres_to_dict(genres):
    return [genre_to_dict(genre) for genre in genres]

def dict_to_movie(dict):
    movie = Movie(dict.id, dict.title, dict.release_year)
    return movie

def actor_review_to_dict(review:ActorReview):
    review_dict = {
        'user': review.user,
        'actor': review.actor.actor_full_name,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict

def actor_reviews_to_dict(reviews):
    return [actor_review_to_dict(review) for review in reviews]

def director_review_to_dict(review:DirectorReview):
    review_dict = {
        'user': review.user,
        'director': review.director.director_full_name,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict

def director_reviews_to_dict(reviews):
    return [director_review_to_dict(review) for review in reviews]


def actor_to_dict(actor:Actor):
    actor_dict = {
        'actor_name': actor.actor_full_name,
        'joined_movies': [movie for movie in actor.joined_movie],
        'reviews': actor.reviews
    }
    return actor_dict

def actors_to_dict(actors):
    return [actor_to_dict(actor) for actor in actors]

def director_to_dict(director:Director):
    director_dict = {
        'director_name': director.director_full_name,
        'dir_movies': [movie for movie in director.dir_movies],
        'reviews': director.reviews
    }
    return director_dict

def directors_to_dict(directors):
    return [director_to_dict(director) for director in directors]

