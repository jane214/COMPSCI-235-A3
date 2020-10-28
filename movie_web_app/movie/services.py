from typing import List, Iterable

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import make_review, Movie, Review, Genre, Actor, Director, User


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(movie_id: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(int(movie_id))
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_review(comment_text, user, movie)

    # Update the repository.
    repo.add_comment(comment)


def add_to_watch_list(movie_id: int, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(int(movie_id))
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    if movie not in user.watch_list:
        repo.add_to_watch_list(user, movie)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(int(movie_id))

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        return None
    return user_to_dict(user)


def get_movies_by_year(year, repo: AbstractRepository):
    # Returns Movies for the target year (empty if no matches), the year of the previous movie (might be null),
    # the date of the next movie (might be null)

    movies = repo.get_movies_by_year(target_year=int(year))
    movies.sort(key=lambda movie: movie.rating, reverse=True)
    movies_dto = list()
    prev_year = next_year = None

    if len(movies) > 0:
        prev_year = repo.get_year_of_previous_movie(movies[0])
        next_year = repo.get_year_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movie_ids_for_year(year, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_year(year)

    return movie_ids


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def remove_from_watch_list(movie_id, username, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(int(movie_id))
    if movie is None:
        raise NonExistentMovieException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    repo.remove_from_watch_list(user, movie)


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Articles to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_search_info(name, repo: AbstractRepository):
    movies = repo.get_movies_for_actor(name)
    movies += repo.get_movies(name)
    movies += repo.get_movies_for_genre(name)
    movies += repo.get_movies_for_director(name)
    movies = set(movies)
    movies = list(movies)
    movies.sort(key=lambda movie: movie.rating, reverse=True)
    return movies_to_dict(movies)


def get_comments_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return comments_to_dict(movie.reviews)


def get_watch_list_for_user(username, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    user.watch_list.watch_list.sort(key=lambda movie:movie.rating, reverse=True)
    return movies_to_dict(user.watch_list)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'year': movie.year,
        'title': movie.title,
        'description': movie.description,
        'hyperlink': None,
        'image_hyperlink': None,
        'comments': comments_to_dict(movie.reviews),
        'genres': genres_to_dict(movie.genres),
        'vote': movie.votes,
        'rate': movie.rating
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(comment: Review):
    comment_dict = {
        'username': comment.user.user_name,
        'movie_id': comment.movie.id,
        'comment_text': comment.review_text,
        'timestamp': comment.timestamp
    }
    return comment_dict


def user_to_dict(user: User):
    user_dict = {
        'username': user.user_name,
        'password': user.password,
        'watch_list': user.watch_list.watch_list
    }
    return user_dict


def comments_to_dict(comments: Iterable[Review]):
    return [comment_to_dict(comment) for comment in comments]


def genre_to_dict(new_g: Genre):
    genre_dict = {
        'name': new_g.genre_name,
        'tagged_movies': [genre.id for genre in new_g.movie_list]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movies(dict):
    movie = Movie(dict.id, dict.year, dict.title)
    movie.description = dict.description
    movie.hyperlink = dict.hyperlink
    # Note there's no comments or tags.
    return movie
