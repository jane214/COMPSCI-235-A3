import abc
import csv
import os
from bisect import insort_left, bisect_left
from datetime import datetime
from typing import List

from werkzeug.security import generate_password_hash

from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import Movie, Actor, Director, User, Review, Genre, make_review


class MovieRepo(AbstractRepository):

    def __init__(self):
        self._movies_index = {}
        self._movies: List[Movie] = []
        self._actors = []
        self._genres = []
        self._reviews = []
        self._director = []
        self._users = []
        self._genre_dict = {}
        self._actor_dict = {}
        self._director_dict = {}
        self._year_dict = {}
        self._watch_list = []

    @property
    def movies_list(self):
        return self._movies

    @property
    def actors(self):
        return self._actors

    @property
    def year_dict(self):
        return self._year_dict

    @year_dict.setter
    def year_dict(self, new_dict):
        self._year_dict = new_dict

    @property
    def directors(self):
        return self._director

    @property
    def users(self):
        return self._users

    @property
    def genre_list(self):
        return self._genres

    @property
    def genre_dict(self):
        return self.genre_dict

    def remove_from_watch_list(self, user: User, movie: Movie):
        user.watch_list.remove_movie(movie)

    def get_movie_index(self, new_id):
        return self._movies_index[new_id]

    def add_movie_to_year_dict(self, new_movie: Movie, new_year):
        if new_year in self._year_dict:
            if new_movie not in self._year_dict[new_year]:
                self._year_dict[new_year] += [new_movie]
        else:
            self._year_dict[new_year] = [new_movie]

    def add_movie_to_genre_dict(self, movie: Movie, new_g: Genre):
        if new_g in self._genre_dict:
            if movie not in self._genre_dict[new_g]:
                self._genre_dict[new_g] += [movie]
        else:
            self._genre_dict[new_g] = [movie]

    def add_movie_to_actor_dict(self, movie: Movie, new_a: Actor):
        if new_a in self._actor_dict:
            if movie not in self._actor_dict[new_a]:
                self._actor_dict[new_a] += [movie]
        else:
            self._actor_dict[new_a] = [movie]

    def add_movie_to_director_dict(self, movie: Movie, new_d: Director):
        if new_d in self._director_dict:
            if movie not in self._director_dict[new_d]:
                self._director_dict[new_d] += [movie]
        else:
            self._director_dict[new_d] = [movie]

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((hi for hi in self._users if hi.user_name == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def add_genre(self, new_g: Genre):
        if new_g not in self._genres:
            self._genres.append(new_g)

    def add_actor(self, new_a: Actor):
        if new_a not in self._actors:
            self._actors.append(new_a)

    def add_director(self, new_d: Director):
        if new_d not in self._director:
            self._director.append(new_d)

    def get_genre_list(self) -> List[Genre]:
        return self._genres

    def get_year_list(self) -> List[int]:
        year_list = list(self._year_dict.keys())
        year_list.sort()
        return year_list

    def get_genre_dict(self):
        return self._genre_dict

    def get_movie(self, new_id: int) -> Movie:
        movie = None

        try:
            if new_id in self._movies_index:
                movie = self._movies_index[new_id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def set_actors(self, actor_list):
        self._actors = actor_list

    def set_directors(self, new_d_list):
        self._director = new_d_list

    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        matching_movies = list()
        try:
            if target_year in self._year_dict:
                matching_movies = self._year_dict[target_year]
        except KeyError:
            # No movies for specified actor. Simply return an empty list.
            pass

        return matching_movies

    def get_movies_by_actor(self, target_actor: Actor) -> List[Movie]:
        matching_movies = list()
        try:
            if target_actor in self._actor_dict:
                matching_movies = self._actor_dict[target_actor]
        except ValueError:
            # No movies for specified actor. Simply return an empty list.
            pass

        return matching_movies

    def get_movies_by_genre(self, target_genre: Genre) -> List[Movie]:
        matching_movies = list()
        try:
            if target_genre in self._genre_dict:
                matching_movies = self._genre_dict[target_genre]
        except ValueError:
            # No movies for specified actor. Simply return an empty list.
            pass

        return matching_movies

    def get_movies_by_director(self, target_director: Director) -> List[Movie]:
        matching_movies = list()

        try:
            if target_director in self._director_dict:
                matching_movies = self._director_dict[target_director]
        except ValueError:
            # No movie for specified director. Simply return an empty list.
            pass

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [new_id for new_id in id_list if new_id in self._movies_index]

        # Fetch the Articles.
        movies = [self._movies_index[new_id] for new_id in existing_ids]
        return movies

    def get_movie_ids_for_genre(self, new_genre: str):
        # Linear search, to find the first occurrence of a Genre with the name tag_name.
        genre: Genre = next((genre for genre in self._genre_dict if genre.genre_name == new_genre), None)

        # Retrieve the ids of articles associated with the Tag.
        if genre is not None:
            list1 = self._genre_dict[genre]
            list1.sort(key=lambda movie: movie.rating, reverse=True)
            movie_ids = [movie.id for movie in list1]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def get_movie_ids_for_year(self, new_year):
        year = next((year for year in self._year_dict if year == new_year), None)

        # Retrieve the ids of articles associated with the Tag.
        if year is not None:
            list1 = self._year_dict[year]
            list1.sort(key=lambda movie: movie.rating, reverse=True)
            movie_ids = [movie.id for movie in list1]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def get_year_of_previous_movie(self, movie: Movie):
        previous_year = None
        year_list = list(self._year_dict.keys())
        year_list.sort()
        position = year_list.index(movie.year)
        try:
            index = position - 1
            if index >= 0:
                previous_year = year_list[index]
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_year

    def get_year_of_next_movie(self, movie: Movie):
        next_year = None
        year_list = list(self._year_dict.keys())
        year_list.sort()
        position = year_list.index(movie.year)
        try:
            index = position + 1
            if index < len(year_list):
                next_year = year_list[index]
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_year

    def add_comment(self, review: Review):
        super().add_comment(review)
        self._reviews.append(review)

    def get_comments(self):
        return self._reviews

    def add_to_watch_list(self, user: User, movie: Movie):
        # super().add_to_watch_list(user, movie)
        user.add_watch_list(movie)

    def get_watch_list(self):
        return self._watch_list

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._movies):
            raise StopIteration
        else:
            self._current += 1
            return self._movies[self._current - 1]

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].year == movie.year:
            return index
        raise ValueError

    def get_movies(self, movie_name):
        movie_list = []
        movie_name = movie_name.lower()
        for movie in self._movies:
            pattern = movie.title.lower()
            if movie_name == pattern:
                movie_list.append(movie)
        return movie_list

    def get_movies_for_actor(self, name):
        name = name.lower()
        match_list = []
        result = None
        for actor in self._actors:
            pattern = actor.actor_full_name.lower()
            if name == pattern:
                result = actor
        if result is not None:
            match_list = self._actor_dict[result]
        return match_list

    def get_movies_for_genre(self, name):
        name = name.lower()
        match_list = []
        result = None
        for genre in self._genres:
            pattern = genre.genre_name.lower()
            if name == pattern:
                result = genre
        if result is not None:
            match_list = self._genre_dict[result]
        return match_list

    def get_movies_for_director(self, name):
        name = name.lower()
        match_list = []
        result = None
        for director in self._director:
            pattern = director.director_full_name.lower()
            if name == pattern:
                result = director
        if result is not None:
            match_list = self._director_dict[result]
        return match_list


def new_load_movie_actor_and_genre(data_path, repo: MovieRepo):
    filename = os.path.join(data_path, "Data1000Movies.csv")
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)
        for row in movie_file_reader:
            title = row['Title']
            release_year = int(row['Year'])
            run_time = int(row['Runtime (Minutes)'])
            director = Director(row["Director"])
            actor_list = row["Actors"].split(',')
            description = row['Description']
            genre_list = row['Genre'].split(",")
            rating = row['Rating']
            votes = row['Votes']
            rank = int(row['Rank'])

            movie = Movie(title, release_year, new_id=rank)
            movie.description = description
            movie.actors = actor_list
            movie.genres = genre_list
            movie.runtime_minutes = run_time
            movie.rating = rating
            movie.votes = votes

            repo.add_movie(movie)
            repo.add_movie_to_year_dict(movie, release_year)
            for genre in genre_list:
                new_g = Genre(genre)
                new_g.add_movie(movie)
                repo.add_genre(new_g)
                repo.add_movie_to_genre_dict(movie, new_g)

            for actor in actor_list:
                new_a = Actor(actor)
                new_a.movies = movie
                repo.add_actor(new_a)
                repo.add_movie_to_actor_dict(movie, new_a)
            repo.add_movie_to_director_dict(movie, director)
            repo.add_director(director)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: str, repo: MovieRepo):
    users = dict()
    filename = os.path.join(data_path, "users.csv")
    for data_row in read_csv_file(filename):
        user = User(
            name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MovieRepo, users):
    filename = os.path.join(data_path, "comments.csv")
    # 'C:/Users/zhong/Desktop/COMPSCI-235-old-one/covid/adapters/data/comments.csv'
    for data_row in read_csv_file(filename):
        comment = make_review(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MovieRepo):
    # set up all movies repository
    # load_movies(data_path, repo)
    new_load_movie_actor_and_genre(data_path, repo)

    # set up user information
    users = load_users(data_path, repo)

    # set up comments info
    load_comments(data_path, repo, users)




