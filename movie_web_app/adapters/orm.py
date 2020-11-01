from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('release_year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('hyperlink', String(255), nullable=True),
    # Column('director', ForeignKey('directors.id'))
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movies_genres = Table(
    'movies_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

# directors = Table(
#     'directors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String(64), nullable=False)
# )

# directors_movies = Table(
#     'directors_movies', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('movie_id', ForeignKey('movies.id')),
#     Column('director_id', ForeignKey('directors.id'))
# )

# actors = Table(
#     'actors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String(64), nullable=False)
# )
#
# actors_movies = Table(
#     'actors_movies', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('movie_id', ForeignKey('movies.id')),
#     Column('actors_id', ForeignKey('actors.id'))
# )


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_User__user_name': users.c.username,
        '_User__password': users.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user')
    })
    mapper(model.Review, reviews, properties={
        '_Review__review_text': reviews.c.review,
        '_Review__timestamp': reviews.c.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_Movie__release_year': movies.c.release_year,
        '_Movie__title': movies.c.title,
        '_description': movies.c.description,
        '_hyperlink': movies.c.hyperlink,
        '_reviews': relationship(model.Review, backref='_Review__movie'),

    })
    mapper(model.Genre, genres, properties={
        '_Genre__genre_name': genres.c.name,
        '_tagged_movies': relationship(
            movies_mapper,
            secondary=movies_genres,
            backref="_genres"
        )
    })



