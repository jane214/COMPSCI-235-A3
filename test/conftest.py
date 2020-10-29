import os

import pytest

# import movie_web_app.adapters.Movie_repo as movie_repo
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from movie_web_app import create_app
from movie_web_app.adapters.orm import map_model_to_tables, metadata
from movie_web_app.adapters import Movie_repo, database_repository
from movie_web_app.adapters.Movie_repo import MovieRepo

TEST_DATA_PATH = "C:/Users/zhong/Desktop/COMPSCI-235-A3/test/data/memory"
TEST_DATA_PATH_DATABASE = "C:/Users/zhong/Desktop/COMPSCI-235-A3/test/data/database"
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///covid-19-test.db'


@pytest.fixture
def in_memory_repo():
    repo = MovieRepo()
    Movie_repo.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    datafile = 'Data1000Movies.csv'
    session_factory = sessionmaker(bind=engine)
    database_repository.populate_data(session_factory, TEST_DATA_PATH_DATABASE, datafile)
    database_repository.populate_user(engine, TEST_DATA_PATH_DATABASE)
    # database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
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
    datafile = 'Data1000Movies.csv'
    database_repository.populate_data(session_factory, TEST_DATA_PATH_DATABASE, datafile)
    database_repository.populate_user(engine, TEST_DATA_PATH_DATABASE)
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
    datafile = 'Data1000Movies.csv'
    database_repository.populate_data(session_factory, TEST_DATA_PATH_DATABASE, datafile)
    database_repository.populate_user(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
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
