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

from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.domainmodel.model import User, Movie, Review, Genre, Director, Actor
from movie_web_app.adapters.repository import AbstractRepository

genres = None


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
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_genre_list(self) -> List[Genre]:
        genres_list = self._session_cm.session.query(Genre).all()
        return genres_list

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        if target_year is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie._year == target_year).all()
            return movies

    def get_number_of_movies(self):
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

    def get_movie_ids_for_genre(self, new_genre: str):
        movie_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT id FROM tags WHERE name = :tag_name',
                                               {'tag_name': new_genre}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movie_ids = list()
        else:
            genre_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                'SELECT article_id FROM article_tags WHERE tag_id = :tag_id ORDER BY article_id ASC',
                {'genre_id': genre_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_year_of_previous_movie(self, movie: Movie):
        result = None
        prev = self._session_cm.session.query(Movie).filter(Movie._Movie__year < movie.year).order_by(
            desc(Movie._Movie__year)).first()  # might have problem

        if prev is not None:
            result = prev.year

        return result

    def get_year_of_next_movie(self, movie: Movie):
        result = None
        next = self._session_cm.session.query(Movie).filter(Movie._Movie__year > movie.year).order_by(
            asc(Movie._Movie__year)).first()

        if next is not None:
            result = next.year

        return result

    def get_comments(self):
        comments = self._session_cm.session.query(Review).all()
        return comments

    def add_comment(self, review: Review):
        super().add_comment(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        pass

    def get_movies(self, movie_name):
        pass

    def get_movies_for_actor(self, name):
        pass

    def get_movies_for_genre(self, name):
        pass

    def get_movies_for_director(self, name):
        pass

    def add_to_watch_list(self, user: User, movie: Movie):
        pass

    def get_watch_list(self):
        pass

    def movie_index(self, movie: Movie):
        pass

    def remove_from_watch_list(self, user: User, movie: Movie):
        pass

    def get_movie_index(self, new_id):
        pass

    def add_movie_to_year_dict(self, new_movie: Movie, new_year):
        pass

    def add_movie_to_genre_dict(self, movie: Movie, new_g: Genre):
        pass

    def add_movie_to_actor_dict(self, movie: Movie, new_a: Actor):
        pass

    def add_movie_to_director_dict(self, movie: Movie, new_d: Director):
        pass

    def set_actors(self):
        pass

    def set_directors(self):
        pass

    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        pass

    def get_movies_by_genre(self, target_genre: Genre) -> List[Movie]:
        pass

    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        pass

    def get_movie_ids_for_year(self, new_year):
        pass

    def get_year_list(self):
        pass

    def get_genre_dict(self):
        pass


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


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path, data_filename):
    conn = engine.raw_connection()
    cursor = conn.cursor()
    conn.commit()
    conn.close()
    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_comments = """
        INSERT INTO comments (
        id, user_id, movie_id, comment, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_comments, generic_generator(os.path.join(data_path, 'comments.csv')))
    conn.commit()
    conn.close()

    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    session = session_factory()

    for movie in movie_file_reader.dataset_of_movies:
        print(movie)
        session.add(movie)

    for actor in movie_file_reader.dataset_of_actors:
        session.add(actor)

    for genre in movie_file_reader.dataset_of_genres:
        session.add(genre)

    for director in movie_file_reader.dataset_of_directors:
        session.add(director)

    session.commit()
    # pass
