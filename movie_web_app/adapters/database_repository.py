import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_web_app.adapters.repository import AbstractRepository, RepositoryException


from movie_web_app.domain.model import Actor, Director, Genre, Movie, Review, User, make_review, make_genre_association, ActorReview,DirectorReview
from movie_web_app.domain.model import make_actor_review, make_director_review
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

tags = None # ??


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_User__user_name=username).one()


        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie_by_id(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_name(self,name):
        movies = self._session_cm.session.query(Movie).filter(Movie._Movie__title == name).all()
        return movies

    def get_movies_by_year(self, target_year) -> List[Movie]:
        if target_year is None:
            articles = self._session_cm.session.query(Movie).all()
            return articles
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Movie).filter(Movie._Movie__release_year == target_year).all()
            return articles

    def get_number_of_movie(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie._id)).first()
        return movie

    def get_movies_by_id(self, id_list):
        movies = self._session_cm.session.query(Movie).filter(Movie._id.in_(id_list)).all()
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        movie_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name', {'genre_name': genre_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movies_ids = list()
        else:
            genre_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movies_genres WHERE genre_id = :genre_id ORDER BY movie_id ASC',
                    {'genre_id': genre_id}
            ).fetchall()
            movies_ids = [id[0] for id in movie_ids]

        return movies_ids

    def get_year_of_previous_movie(self, movie:Movie):
        result = None
        prev = self._session_cm.session.query(Movie).filter(Movie._Movie__release_year < movie.release_year).order_by(desc(Movie._Movie__release_year)).first()

        if prev is not None:
            result = prev.release_year

        return result

    def get_year_of_next_movie(self, movie:Movie):
        result = None
        next = self._session_cm.session.query(Movie).filter(Movie._Movie__release_year > movie.release_year).order_by(asc(Movie._Movie__release_year)).first()
        if next is not None:
            result = next.release_year

        return result

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(Genre)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_all_actors(self):
        actors = self._session_cm.session.query(Actor).all()
        return actors

    def get_all_directors(self) -> List[Actor]:
        directors = self._session_cm.session.query(Director).all()
        return directors

    def get_movies_by_director(self, director_name):
        pass

    def get_movies_by_actor(self, actor_name):
        pass

    def movie_index(self, movie: Movie):
        pass

    def add_actor_review(self, review: ActorReview):
        pass

    def add_director_review(self, review: DirectorReview):
        pass

    def get_actor(self, name):
        pass

    def get_director(self, name):
        pass




def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(session_factory, data_path, data_filename):
    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    session = session_factory()

    for movie in movie_file_reader.movies:
        session.add(movie)

    for genre in movie_file_reader.genres:
        session.add(genre)
    # for director in movie_file_reader.directors:
    #     session.add(director)
    # for actor in movie_file_reader.actors:
    #     session.add(actor)
    session.commit()

def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row

def populate_user_comment(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_reviews = """
        INSERT INTO reviews (
        id, user_id, movie_id, review,timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()








