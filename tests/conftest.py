import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from movie_web_app import create_app
from movie_web_app.adapters.orm import metadata, map_model_to_tables
from movie_web_app.adapters import memory_repository, database_repository
from movie_web_app.adapters.memory_repository import MemoryRepository

#TEST_DATA_PATH = '/Users/vivian/Desktop/235Ass2/tests/data/Data1000Movies.csv'
TEST_DATA_PATH_MEMORY = '/Users/vivian/Desktop/yyou211_235_A3/tests/data/memory'
TEST_DATA_PATH_DATABASE = '/Users/vivian/Desktop/yyou211_235_A3/tests/data/database'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///movies.db'

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE,"Data1000Movies.csv")
    database_repository.populate_user_comment(engine, TEST_DATA_PATH_DATABASE)

    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE, "Data1000Movies.csv")
    database_repository.populate_user_comment(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE, "Data1000Movies.csv")
    database_repository.populate_user_comment(engine, TEST_DATA_PATH_DATABASE)

    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',                         # Set to 'memory' or 'database' depending on desired repository.
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,        # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
