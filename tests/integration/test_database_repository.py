from datetime import date, datetime

import pytest

from movie_web_app.adapters.database_repository import SqlAlchemyRepository
from movie_web_app.adapters.repository import RepositoryException
from movie_web_app.domain.model import Actor, Director, Genre, Movie, Review, User, make_review, make_genre_association, ActorReview,DirectorReview
from movie_web_app.domain.model import make_actor_review, make_director_review

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_article_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movie()

    # Check that the query returned 177 Articles.
    assert number_of_movies == 5

def test_repository_can_add_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movie()

    new_movie_id = number_of_movies + 1

    movie = Movie(6, "aaaa", 2020)
    movie.description = "good it"
    #movie._id = new_movie_id
    repo.add_movie(movie)

    assert repo.get_movie_by_id(new_movie_id) == movie

def test_repository_can_retrieve_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie_by_id(1)

    # Check that the Article has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # # Check that the Article is commented as expected.
    # comment_one = [comment for comment in article.comments if comment.comment == 'Oh no, COVID-19 has hit New Zealand'][
    #     0]
    # comment_two = [comment for comment in article.comments if comment.comment == 'Yeah Freddie, bad news'][0]
    #
    # assert comment_one.user.username == 'fmercury'
    # assert comment_two.user.username == "thorke"
    #
    # # Check that the Article is tagged as expected.
    # assert article.is_tagged_by(Tag('Health'))
    # assert article.is_tagged_by(Tag('New Zealand'))

def test_repository_does_not_retrieve_a_non_existent_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie_by_id(1001)
    assert movie is None

def test_repository_can_retrieve_articles_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_year(2012)

    assert len(articles) == 1

    # these articles are no jokes...
    movies = repo.get_movies_by_year(2014)

    assert len(articles) == 1

def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_year(2020)
    assert len(articles) == 0

def test_repository_can_retrieve_tags(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tags = repo.get_genres()

    assert len(tags) == 10

def test_repository_can_get_first_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_first_movie()
    assert movie.release_year == 2014
    # assert article.title == 'Coronavirus: First case of virus in New Zealand'

def test_repository_can_get_last_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_last_movie()
    assert movie.release_year == 2016
    # assert article.title == 'Covid 19 coronavirus: Kiwi mum on the heartbreak of losing her baby in lockdown'

def test_repository_can_get_articles_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([1, 2])

    assert len(articles) == 2
    # assert articles[
    #            0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    # assert articles[1].title == "Australia's first coronavirus fatality as man dies in Perth"
    # assert articles[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'

def test_repository_does_not_retrieve_article_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([2, 1002])

    assert len(articles) == 1
    # assert articles[
    #            0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([0, 1099])

    assert len(articles) == 0

# def test_repository_returns_article_ids_for_existing_tag(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article_ids = repo.get_article_ids_for_tag('Health')
#
#     assert article_ids == [1, 2]

def test_repository_returns_an_empty_list_for_non_existent_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article_ids = repo.get_movie_ids_for_genre('United States')

    assert len(article_ids) == 0


# def test_repository_returns_date_of_previous_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(6)
#     previous_date = repo.get_date_of_previous_article(article)
#
#     assert previous_date.isoformat() == '2020-03-01'
#
#
# def test_repository_returns_none_when_there_are_no_previous_articles(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(1)
#     previous_date = repo.get_date_of_previous_article(article)
#
#     assert previous_date is None
#
#
# def test_repository_returns_date_of_next_article(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(3)
#     next_date = repo.get_date_of_next_article(article)
#
#     assert next_date.isoformat() == '2020-03-05'
#
#
# def test_repository_returns_none_when_there_are_no_subsequent_articles(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(177)
#     next_date = repo.get_date_of_next_article(article)
#
#     assert next_date is None
#
#
# def test_repository_can_add_a_tag(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     tag = Tag('Motoring')
#     repo.add_tag(tag)
#
#     assert tag in repo.get_tags()
#
#
# def test_repository_can_add_a_comment(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     user = repo.get_user('thorke')
#     article = repo.get_article(2)
#     comment = make_comment("Trump's onto it!", user, article)
#
#     repo.add_comment(comment)
#
#     assert comment in repo.get_comments()
#
#
# def test_repository_does_not_add_a_comment_without_a_user(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     article = repo.get_article(2)
#     comment = Comment(None, article, "Trump's onto it!", datetime.today())
#
#     with pytest.raises(RepositoryException):
#         repo.add_comment(comment)
#
#
# def test_repository_can_retrieve_comments(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     assert len(repo.get_comments()) == 3
#
#
# def make_article(new_article_date):
#     article = Article(
#         new_article_date,
#         'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
#         'The self-isolation deadline has been pushed back',
#         'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800',
#         'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
#     )
#     return article
#
# def test_can_retrieve_an_article_and_add_a_comment_to_it(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     # Fetch Article and User.
#     article = repo.get_article(5)
#     author = repo.get_user('thorke')
#
#     # Create a new Comment, connecting it to the Article and User.
#     comment = make_comment('First death in Australia', author, article)
#
#     article_fetched = repo.get_article(5)
#     author_fetched = repo.get_user('thorke')
#
#     assert comment in article_fetched.comments
#     assert comment in author_fetched.comments

