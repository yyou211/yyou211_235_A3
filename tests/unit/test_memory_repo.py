import unittest
import pytest
from datetime import date, datetime
from typing import List
from movie_web_app.domain.model import Actor, Director, Genre, Movie, MovieWatchingSimulation, Review, User, WatchList, make_review
from movie_web_app.domain.model import ActorReview, DirectorReview, make_actor_review, make_director_review
from movie_web_app.adapters.repository import RepositoryException
from movie_web_app.adapters import memory_repository
from movie_web_app.adapters.memory_repository import MemoryRepository


def test_add_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    #print(in_memory_repo.get_all_users())
    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None



def test_add_movie(in_memory_repo):
    assert in_memory_repo.get_number_of_movie() == 5
    new_movie = Movie(6, 'Harry Potter', 2005)
    in_memory_repo.add_movie(new_movie)
    assert in_memory_repo.get_number_of_movie() == 6

def test_get_number_of_movie(in_memory_repo):
    assert in_memory_repo.get_number_of_movie() == 5

def test_get_movies_by_name(in_memory_repo):
    movie1 = in_memory_repo.get_movie_by_id(1)
    result = [movie1]
    assert in_memory_repo.get_movies_by_name('Guardians of the Galaxy') == result


def test_get_movie_by_id(in_memory_repo):
    movie = in_memory_repo.get_movie_by_id(1)
    assert movie.title == "Guardians of the Galaxy"
    # Check that the Article is commented as expected.
    review_one = [review for review in movie.reviews if review.review_text == 'Like it'][
        0]
    review_two = [review for review in movie.reviews if review.review_text == 'Great movie.'][0]

    assert review_one.user.user_name == 'fmercury'
    assert review_two.user.user_name == "thorke"

    # Check that the Article is tagged as expected.
    assert movie.is_tagged_by(Genre('Action'))
    assert movie.is_tagged_by(Genre('Adventure'))

def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    article = in_memory_repo.get_movie_by_id(101)
    assert article is None


def test_get_movies_by_year(in_memory_repo):
    movie_1 = Movie(6, 'Harry Potter', 2005)
    in_memory_repo.add_movie(movie_1)
    result = in_memory_repo.get_movies_by_year(2005)
    assert (movie_1 in result) == True
    #print(result)


def test_get_first_of_movie(in_memory_repo):
    movie_1 = Movie(6, 'Harry Potter', 2005)
    in_memory_repo.add_movie(movie_1)
    #已知2006最早
    assert in_memory_repo.get_first_movie() == movie_1

def test_get_last_movie(in_memory_repo):
    movie_1 = Movie(6, 'Harry Potter', 2021)
    in_memory_repo.add_movie(movie_1)
    assert in_memory_repo.get_last_movie() == movie_1

def get_movies_by_id(in_memory_repo):
    result = in_memory_repo.get_movies_by_id(['1', '2'])
    movie_1 = in_memory_repo.get_all_movies()[0]
    movie_2 = in_memory_repo.get_all_movies()[1]
    assert result == [movie_1, movie_2]

def test_get_movie_ids_for_genre(in_memory_repo):
    genre_1 = in_memory_repo.get_genre_by_name('Action')
    print(genre_1.tagged_movies)
    movie5 = in_memory_repo.get_movie_by_id(5)
    print(movie5.genres)
    result = in_memory_repo.get_movie_ids_for_genre('Action')
    assert 1 in result
    assert 5 in result




def test_get_year_of_previous_movie(in_memory_repo):
    movie_1 = in_memory_repo.get_movie_by_id(1)
    movie_2 = in_memory_repo.get_movie_by_id(2)
    year_1 = in_memory_repo.get_year_of_previous_movie(movie_1)
    year_2 = in_memory_repo.get_year_of_previous_movie(movie_2)
    assert year_1 == 2012
    assert year_2 is None


def test_get_year_of_next_movie(in_memory_repo):
    movie_1 = in_memory_repo.get_movie_by_id(1)
    movie_2 = in_memory_repo.get_movie_by_id(2)
    movie_3 = in_memory_repo.get_movie_by_id(3)
    year_1 = in_memory_repo.get_year_of_next_movie(movie_1)
    year_2 = in_memory_repo.get_year_of_next_movie(movie_2)
    year_3 = in_memory_repo.get_year_of_next_movie(movie_3)
    assert year_1 == 2016
    assert year_2 == 2014
    assert year_3 is None



def test_add_genres(in_memory_repo):
    new_genre = Genre("unknown")
    in_memory_repo.add_genre(new_genre)
    assert (new_genre in in_memory_repo.get_genres()) == True

def test_get_genres(in_memory_repo):
    result = in_memory_repo.get_genres()
    genre_1 = Genre('Action')
    #print(in_memory_repo.get_movie_ids_for_tag('Action'))
    assert (genre_1 in result) == True


def test_get_genre_by_name(in_memory_repo):
    genre_1 = in_memory_repo.get_genre_by_name('Action')
    assert genre_1 == Genre('Action')


def test_add_review(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    movie_1 = in_memory_repo.get_movie_by_id(1)
    #review_1 = Review(user, movie_1, "Good!", 8.8)
    review_1 = make_review(user, movie_1, "Good!")
    in_memory_repo.add_review(review_1)
    assert len(in_memory_repo.get_reviews()) ==4
    #  有问题 ??

def test_get_reviews(in_memory_repo):
    all_reviews = in_memory_repo.get_reviews()
    assert len(all_reviews) == 3

def test_movie_index(in_memory_repo):
    movie_1 = Movie(2001, 'Harry Potter', 2021)
    in_memory_repo.add_movie(movie_1)
    index = in_memory_repo.movie_index(movie_1)
    assert in_memory_repo.get_number_of_movie() == 6
    assert index == 5


def test_get_all_actors(in_memory_repo):
    all_actors = in_memory_repo.get_all_actors()
    print(all_actors)
    movie1 = in_memory_repo.get_movie_by_id(1)
    print(movie1.actors)

    assert Actor('Chris Pratt') in all_actors

def test_get_movies_by_actor(in_memory_repo):
    movie1 = in_memory_repo.get_movie_by_id(1)
    #actor = in_memory_repo.get_actor('Chris Pratt')
    result = in_memory_repo.get_movies_by_actor('Chris Pratt')
    assert movie1 in result

def test_get_movies_by_director(in_memory_repo):
    movie1 = in_memory_repo.get_movie_by_id(1)
    result = in_memory_repo.get_movies_by_director('James Gunn')
    assert movie1 in result

def test_add_actor_review(in_memory_repo):
    actor = in_memory_repo.get_actor('Bradley Cooper')
    assert len(actor.reviews) == 2
    user = in_memory_repo.get_user('thorke')
    make_actor_review(user, actor, "Good actor!")
    assert len(actor.reviews) == 3

def test_add_director_review(in_memory_repo):
    director = in_memory_repo.get_director('James Gunn')
    assert len(director.reviews) == 1
    user = in_memory_repo.get_user('thorke')
    make_director_review(user, director, "Good director!")
    assert len(director.reviews) == 2









# def fun1(in_memory_repo):
#     all_genre = in_memory_repo.get_genres()
#     print(all_genre)
#     # movie_1 = in_memory_repo.get_movie_by_id(1)
#     # print(movie_1)
#     all_movies = in_memory_repo.get_all_movies()
#     print(all_movies)
#     movie_1 = all_movies[0]
#     print(movie_1)
#     print(movie_1.title)
#     print(movie_1.genres)
#     genre_1 = all_genre[0]
#     print(genre_1)
#     print(genre_1.genre_name)
#     print(len(genre_1.tagged_movies))
#     print(in_memory_repo.get_movies_index())
#     user = User('Dave', '123456789')
#     in_memory_repo.add_user(user)
#     print(in_memory_repo.get_all_users())
#



if __name__ == '__main__':
    unittest.main()
