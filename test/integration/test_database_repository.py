from datetime import date, datetime

import pytest

from movie_web_app.adapters.database_repository import SqlAlchemyRepository
from movie_web_app.domainmodel.model import User, Movie, Genre, make_review, Review
from movie_web_app.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_article_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_number_of_movies()

    # Check that the query returned 177 Articles.
    assert number_of_articles == 1000


def test_repository_can_add_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_number_of_movies()

    new_article_id = number_of_articles + 1

    movie = Movie(
        "hahahha",
        2020,
        1001
    )
    movie.description = "sdhabcd"
    movie.rating = 10
    movie.votes = 1000
    repo.add_movie(movie)
    movie.runtime_minutes = 130

    assert repo.get_movie(new_article_id) == movie


def test_repository_can_retrieve_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the Article has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in movie.reviews if comment.review_text == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in movie.reviews if comment.review_text == 'Yeah Freddie, bad news'][0]

    assert comment_one.user.user_name == 'fmercury'
    assert comment_two.user.user_name == "thorke"

    # Check that the Article is tagged as expected.
    assert movie.is_genred_by(Genre('Action'))
    assert movie.is_genred_by(Genre('Adventure'))


def test_repository_does_not_retrieve_a_non_existent_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_movie(1001)
    assert article is None


def test_repository_can_retrieve_articles_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_year(2006)

    # Check that the query returned 3 Articles.
    assert len(articles) == 44

    # these articles are no jokes...
    articles = repo.get_movies_by_year(2017)

    # Check that the query returned 5 Articles.
    assert len(articles) == 0


def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_year(2023)
    assert len(articles) == 0


# def test_repository_can_retrieve_tags(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     genres = repo.get_genre_list()
#
#     assert len(genres) == 10
#
#     tag_one = [tag for tag in genres if tag.genre_name == 'Action'][0]
#     tag_two = [tag for tag in genres if tag.genre_name == 'Adventure'][0]
#     tag_three = [tag for tag in genres if tag.genre_name == 'Drama'][0]
#     tag_four = [tag for tag in genres if tag.genre_name == 'Fantasy'][0]
#
#     assert tag_one.number_of_movies() == 53
#     assert tag_two.number_of_movies() == 2
#     assert tag_three.number_of_movies() == 64
#     assert tag_four.number_of_movies() == 1


def test_repository_can_get_first_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_first_movie()
    assert article.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_last_movie()
    assert article.title == 'Nine Lives'


def test_repository_can_get_articles_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([2, 5, 6])

    assert len(articles) == 3
    assert articles[
               0].title == 'Prometheus'
    assert articles[1].title == "Suicide Squad"
    assert articles[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_article_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([2, 209])

    assert len(articles) == 2
    assert articles[
               0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_movies_by_id([0, 199])

    assert len(articles) == 1


def test_repository_returns_article_ids_for_existing_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('Action')

    assert len(movie_ids) == 303


def test_repository_returns_an_empty_list_for_non_existent_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article_ids = repo.get_movie_ids_for_genre('hahaha')

    assert len(article_ids) == 0


def test_repository_returns_date_of_previous_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_movie(6)
    previous_date = repo.get_year_of_previous_movie(article)

    assert previous_date == 2015


def test_repository_returns_none_when_there_are_no_previous_articles(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_first_movie()
    previous_date = repo.get_year_of_previous_movie(article)

    assert previous_date is None


def test_repository_returns_date_of_next_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_movie(3)
    next_date = repo.get_year_of_next_movie(article)

    assert next_date == 2007


def test_repository_returns_none_when_there_are_no_subsequent_articles(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_movie(1000)
    next_date = repo.get_year_of_next_movie(article)

    assert next_date is None


def test_repository_can_add_a_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motoring')
    repo.add_genre(genre)

    assert genre in repo.get_genre_list()


def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    article = repo.get_movie(2)
    comment = make_review("Trump's onto it!", user, article)

    repo.add_comment(comment)

    assert comment in repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_movie(2)
    comment = Review(article, "Trump's onto it!", 10, None)

    with pytest.raises(RepositoryException):
        repo.add_comment(comment)


def test_repository_can_retrieve_comments(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_comments()) == 3


# def make_article(new_article_date):
#     article = Movie(
#         new_article_date,
#         'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
#         'The self-isolation deadline has been pushed back',
#         'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800',
#         'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
#     )
#     return article


def test_can_retrieve_an_article_and_add_a_comment_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Article and User.
    article = repo.get_movie(5)
    author = repo.get_user('thorke')

    # Create a new Comment, connecting it to the Article and User.
    comment = make_review('First death in Australia', author, article)

    article_fetched = repo.get_movie(5)
    author_fetched = repo.get_user('thorke')

    assert comment in article_fetched.reviews
    assert comment in author_fetched.reviews
