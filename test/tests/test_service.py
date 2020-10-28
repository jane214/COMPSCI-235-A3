from datetime import date

import pytest

from movie_web_app.authentication.services import AuthenticationException
from movie_web_app.domainmodel.model import Movie
from movie_web_app.movie import services as movie_services
from movie_web_app.authentication import services as auth_services
from movie_web_app.movie.services import NonExistentMovieException, UnknownUserException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_id = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    movie_services.add_comment(movie_id, comment_text, username, in_memory_repo)

    # Retrieve the comments for the movie from the repository.
    comments_as_dict = movie_services.get_comments_for_movie(movie_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
        None) is not None


def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie_id = 100000
    comment_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_comment(movie_id, comment_text, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_id = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_comment(movie_id, comment_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movie_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    assert len(movie_as_dict['comments']) == 0
    genre_names = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert 'Mystery' in genre_names
    assert 'Adventure' in genre_names
    assert 'Sci-Fi' in genre_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 1000001

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 966


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 3


def test_get_movies_by_year_with_one_year(in_memory_repo):
    target_year = 2006

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    assert len(movies_as_dict) == 44
    assert movies_as_dict[0]['id'] == 65

    assert prev_year is None
    assert next_year == 2007


def test_get_movies_by_date_with_multiple_dates(in_memory_repo):
    target_year = 2009

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are 3 movies dated 2020-03-01.
    assert len(movies_as_dict) == 51

    # Check that the movie ids for the the movies returned are 3, 4 and 5.
    movies_ids = [movie['id'] for movie in movies_as_dict]
    assert 78 in movies_ids

    # Check that the dates of movies surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_year == 2008
    assert next_year == 2010


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_year = 2023

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are no movies dated 2020-03-06.
    assert len(movies_as_dict) == 0
    assert prev_year is None
    assert next_year is None


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [5, 6, 7, 8]
    movies_as_dict = movie_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 4

    # Check that the movie ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([5, 6]).issubset(movie_ids)


def test_get_comments_for_movie(in_memory_repo):
    comments_as_dict = movie_services.get_comments_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for movie with id 1.
    assert len(comments_as_dict) == 3

    # Check that the comments relate to the movie whose id is 1.
    movie_ids = [comment['movie_id'] for comment in comments_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_comments_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        comments_as_dict = movie_services.get_comments_for_movie(10009, in_memory_repo)


def test_get_comments_for_movie_without_comments(in_memory_repo):
    comments_as_dict = movie_services.get_comments_for_movie(2, in_memory_repo)
    assert len(comments_as_dict) == 0


def test_can_add_or_remove_movie_to_from_watch_list(in_memory_repo):
    movie_id = 3
    username = 'fmercury'
    # Call the service layer to add the comment.
    movie_services.add_to_watch_list(movie_id, username, in_memory_repo)
    watch_list = movie_services.get_watch_list_for_user(username, in_memory_repo)

    assert watch_list[0]['id'] == 3
    movie_services.remove_from_watch_list(movie_id, username, in_memory_repo)
    watch_list = movie_services.get_watch_list_for_user(username, in_memory_repo)
    assert len(watch_list) == 0


def test_can_add_or_remove_movie_to_from_watch_listif_user_is_none(in_memory_repo):
    movie_id = 3
    username = None
    # Call the service layer to add the comment.
    with pytest.raises(UnknownUserException):
        movie_services.add_to_watch_list(movie_id, username, in_memory_repo)

    with pytest.raises(UnknownUserException):
        movie_services.remove_from_watch_list(movie_id, username, in_memory_repo)
