import abc
from typing import List

from movie_web_app.domainmodel.model import Movie, Actor, Director, User, Review, Genre

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, new_user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_index(self, new_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, new_movie: Movie):
        """ Adds an movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, new_g: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, new_a: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, new_d: Director):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_to_year_dict(self, new_movie: Movie, year):
        """ Adds an movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_to_genre_dict(self, movie: Movie, new_g:Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_to_actor_dict(self, movie: Movie, new_a:Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_to_director_dict(self, movie: Movie, new_d:Director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, new_id: int) -> Movie:
        """ Returns Movie with id from the repository.

        If there is no Movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_list(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_list(self) -> List[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_dict(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        """ Returns a list of Movies that were directed by target_director.

        If there are no Movies direct by this director, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        """ Returns a list of Movies that were acted by target_actor.

        If there are no Movies act by this actor, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        """ Returns a list of Movies that were directed by target_director.

        If there are no Movies direct by this director, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by year, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_previous_movie(self, movie: Movie):
        """ Returns the date of an Movie that immediately precedes article.

        If article is the first Movie in the repository, this method returns None because there are no Articles
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_next_movie(self, movie: Movie):
        """ Returns the date of an Movie that immediately follows Movie.

        If article is the last Movie in the repository, this method returns None because there are no Movie
        on a later date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, review: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self, movie_name):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_for_actor(self, name):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_for_genre(self, name):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_for_director(self, name):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_watch_list(self, user: User, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_watch_list(self, user: User, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_watch_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_year(self, year):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, new_genre: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self) -> Movie:
        raise NotImplementedError
