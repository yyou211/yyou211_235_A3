from datetime import date

import pytest

from movie_web_app.authentication.services import AuthenticationException
from movie_web_app.movie import services as movie_services
from movie_web_app.authentication import services as auth_services
from movie_web_app.movie.services import NonExistentMovieException

# -------------------
# authentication test
# -------------------

def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')  #不确定


def test_cannot_add_user_with_existing_name(in_memory_repo):
    # new_username = 'thorke'
    # new_password = 'abcd1A23'
    # auth_services.add_user(new_username, new_password, in_memory_repo)
    # user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    # assert user_as_dict['username'] == new_username

    #再次加入相同用户
    new_username = 'thorke'
    new_password = 'abcd1A23'
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(new_username, new_password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):#这个不确定
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)





# -------------------
# movie test
# -------------------


def test_can_add_review(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    # rating = 8
    #username = 'fmercury'
    username = 'pmccartney'
    password = 'abcd1A23'
    # add user
    auth_services.add_user(username, password, in_memory_repo)

    # Call the service layer to add the comment.
    movie_services.add_review(username, movie_id, review_text, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 7
    review_text = "COVID-19 - what's that?"

    username = 'pmccartney'
    password = 'abcd1A23'
    # add user
    auth_services.add_user(username, password, in_memory_repo)

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_review(username, movie_id, review_text, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael' # unknown user

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_review(username, movie_id, review_text, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movie_services.get_movie_by_id(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['release_year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    #assert article_as_dict['first_para'] == 'US President Trump tweeted on Saturday night (US time) that he has asked the Centres for Disease Control and Prevention to issue a ""strong Travel Advisory"" but that a quarantine on the New York region"" will not be necessary.'
    assert movie_as_dict['hyperlink'] == None
    #assert movie_as_dict['image_hyperlink'] == 'https://www.nzherald.co.nz/resizer/159Vi4ELuH2fpLrv1SCwYLulzoM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/XQOAY2IY6ZEIZNSW2E3UMG2M4U.jpg'
    assert len(movie_as_dict['reviews']) == 0

    # all_genres = movie_as_dict['genre']
    # genres_dict = movie_services.genres_to_dict(all_genres)
    # genres_names = [Dictionary['genre_name'] for Dictionary in genres_dict]
    genres_names = [Dictionary['genre_name'] for Dictionary in movie_services.genres_to_dict(movie_as_dict['genres'])]
    assert 'Adventure' in genres_names
    assert 'Mystery' in genres_names
    assert 'Sci-Fi' in genres_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie_by_id(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)
    #print(movie_as_dict)

    assert movie_as_dict['id'] == 2


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 5


def test_get_movies_by_date_with_one_year(in_memory_repo):
    target_year = 2016
    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    assert len(movies_as_dict) == 3
    assert movies_as_dict[0]['id'] == 4

    assert prev_year ==  2014
    assert next_year is None


def test_get_movies_by_year_with_multiple_years(in_memory_repo):
    target_year = 2016

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are 3 articles dated 2020-03-01.
    assert len(movies_as_dict) == 3

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([3, 4, 5]).issubset(movie_ids)

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_year == 2014
    assert next_year is None


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_year = 2020

    movies_as_dict, prev_date, next_date = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are no articles dated 2020-03-06.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [1,2,3,4]
    movies_as_dict = movie_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 4

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([1,2,3,4]).issubset(movie_ids)

def test2_get_movies_by_id(in_memory_repo):
    target_movie_ids = [4,5,6,7]
    movies_as_dict = movie_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([4,5]).issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 3 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 3

    # Check that the comments relate to the article whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    new_movie_ids = set(movie_ids)
    assert 1 in new_movie_ids and len(new_movie_ids) == 1


def test_get_review_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movie_services.get_reviews_for_movie(7, in_memory_repo)


def test_get_review_for_movie_without_review(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0




