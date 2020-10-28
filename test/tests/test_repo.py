from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.adapters.repository import RepositoryException
from movie_web_app.domainmodel.model import User, Movie, Genre, Director, Actor, make_review, Review


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Jane', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('jane') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 movies.
    assert number_of_articles == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Moana", 1900, 7)
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(7) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in movie.reviews if comment.review_text == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in movie.reviews if comment.review_text == 'Yeah Freddie, bad news'][0]

    assert comment_one.user.user_name == 'fmercury'
    assert comment_two.user.user_name == "thorke"

    # Check that the movie is genred as expected.
    assert not movie.is_genred_by(Genre('Mystery'))
    assert not movie.is_genred_by(Genre('Thriller'))


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(10001)
    assert movie is None


def test_repository_can_retrieve_movies_by_actor(in_memory_repo):
    movies = in_memory_repo.get_movies_by_actor(Actor("Noomi Rapace"))

    assert len(movies) == 5


def test_repository_can_retrieve_movies_by_director(in_memory_repo):
    movies = in_memory_repo.get_movies_by_director(Director("Adam Wingard"))

    assert len(movies) == 2


def test_repository_can_retrieve_movies_by_genre(in_memory_repo):
    movies = in_memory_repo.get_movies_by_genre(Genre("War"))

    assert len(movies) == 13


def test_repository_does_not_retrieve_a_movie_when_there_are_no_articles_for_a_given_actor(in_memory_repo):
    movies = in_memory_repo.get_movies_by_actor(Actor("a"))
    assert len(movies) == 0


def test_repository_does_not_retrieve_a_movie_when_there_are_no_articles_for_a_given_director(in_memory_repo):
    movies = in_memory_repo.get_movies_by_director(Director("a"))
    assert len(movies) == 0


def test_repository_does_not_retrieve_a_movie_when_there_are_no_articles_for_a_given_genre(in_memory_repo):
    movies = in_memory_repo.get_movies_by_actor(Genre("a"))
    assert len(movies) == 0


def test_repository_can_retrieve_genre(in_memory_repo):
    tags: List[Genre] = in_memory_repo.get_genre_list()

    assert len(tags) == len(in_memory_repo.genre_list)


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Inland Empire'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Split'


def test_repository_can_get_movie_by_ids(in_memory_repo):
    movie = in_memory_repo.get_movies_by_id([2, 5, 6])

    assert len(movie) == 3
    assert movie[0].title == "Prometheus"
    assert movie[1].title == 'Suicide Squad'
    assert movie[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 9])

    assert len(movies) == 2
    assert movies[0].title == "Prometheus"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_movies_by_id([0, 9])

    assert len(articles) == 1


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    article_ids = in_memory_repo.get_movie_ids_for_genre('War')

    assert article_ids == [78, 231, 714, 511, 114, 241, 644, 763, 895, 821, 480, 187, 161]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    article_ids = in_memory_repo.get_movie_ids_for_genre('United States')

    assert len(article_ids) == 0


def test_repository_returns_year_of_previous_article(in_memory_repo):

    year_list = list(in_memory_repo._year_dict.keys())
    year_list.sort()
    movie = in_memory_repo._year_dict[year_list[1]][0]
    movie = in_memory_repo.get_movie(movie.id)
    previous_year = in_memory_repo.get_year_of_previous_movie(movie)

    assert previous_year == 2006


def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    previous_year = in_memory_repo.get_year_of_previous_movie(movie)
    assert previous_year is None


def test_repository_returns_year_of_next_article(in_memory_repo):
    year_list = list(in_memory_repo._year_dict.keys())
    year_list.sort()
    movie = in_memory_repo._year_dict[year_list[1]][0]
    movie = in_memory_repo.get_movie(movie.id)
    next_year = in_memory_repo.get_year_of_next_movie(movie)

    assert next_year == 2008


def test_repository_returns_none_when_there_are_no_subsequent_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    next_year = in_memory_repo.get_year_of_next_movie(movie)

    assert next_year is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Motoring')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genre_list()



def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = make_review("Trump's onto it!", user, movie)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    comment = Review(movie, "Trump's onto it!", None, None)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = Review(None, "Trump's onto it!", None, user)

    user.add_review(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_add_or_remove_movie_to_or_from_watch_list(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    movie = Movie("Hello")
    in_memory_repo.add_to_watch_list(user, movie)
    assert len(user.watch_list.watch_list) == 1
    assert user.watch_list.watch_list[0].title == "Hello"
    in_memory_repo.remove_from_watch_list(user, movie)
    assert len(user.watch_list.watch_list) == 0

