import abc
from typing import List
from datetime import date

from movie_web_app.domain.model import Actor, Director, Genre, Movie,Review, User, ActorReview, DirectorReview

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    # @abc.abstractmethod
    # def get_all_movies(self):
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User: # get user by user name
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, article: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    # 看一下能不能加上movie ID
    # 这个是用电影名的
    def get_movies_by_name(self, movie_name): # there could be more than one movie have this name
        """ Returns movie with movie name from the repository.

        If there is no Movie with the given name, this method returns None.
        """
        # 可能重名，return list
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_id(self, movie_id) -> Movie:
        raise NotImplementedError


    @abc.abstractmethod
    def get_movies_by_year(self):
        #这个不确定
        raise NotImplementedError


    @abc.abstractmethod
    def get_number_of_movie(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self):
        # return the earliest movie
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name):
        raise NotImplementedError
    # return a list contains all the movies that are tagged by this genre

    @abc.abstractmethod
    def get_year_of_previous_movie(self, movie:Movie):
        """ Returns the date of an Article that immediately precedes article.

        If article is the first Article in the repository, this method returns None because there are no Articles
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_next_movie(self, movie:Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the genres stored in the repository. """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_genre_by_name(self):
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review:Review):
        """ Adds a Comment to the repository.

                If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
                RepositoryException and doesn't update the repository.
                """
        # 改一下domain review
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_actors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_directors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor_name):
        raise NotImplementedError




    @abc.abstractmethod
    def movie_index(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor_review(self,review:ActorReview):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director_review(self, review: DirectorReview):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self,name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self,name):
        raise NotImplementedError












