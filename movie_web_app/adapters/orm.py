from sqlalchemy import (
    Table, MetaData, Column, Integer, String, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('hyperlink', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('voting', Integer, nullable=False),
    Column('director_id', ForeignKey('directors.id')),
    Column('running_time', Integer, nullable=False)
    # Column('image_hyperlink', String(255), nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_User__user_name': users.column.username,
        '_User__password': users.column.password,
        '_reviews': relationship(model.Review, backref='_user')
        # _watch_list # add later
    })
    mapper(model.Review, comments, properties={
        '_Review__review_text': comments.column.comment, # what is the difference of c and column
        '_Review__timestamp': comments.column.timestamp
    })

    mapper(model.Director, directors, properties={
        '_Director__director_full_name': directors.c.name,
        '_movies': relationship(model.Movie, backref='_director')
    })

    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.column.id,
        '_Movie__year': movies.column.year,
        '_Movie__movie_name': movies.column.title,
        '_description': movies.column.description,
        '_hyperlink': movies.column.hyperlink,
        '_review': relationship(model.Review, backref='_movie'),
        '_rating': movies.column.rating,
        '_voting': movies.column.voting,
        '_runtime_minutes': movies.column.running_time,
        # _runtime_minutes
    })

    mapper(model.Genre, genres, properties={
        '_Genre__genre_name': genres.column.name,
        '_movie': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref="_genres"
        )
    })

    mapper(model.Actor, actors, properties={
        '_Actor__actor_full_name': actors.column.name,
        '_movies': relationship(
            movies_mapper,
            secondary=movie_actors,
            backref="_actors"
        )
    })
