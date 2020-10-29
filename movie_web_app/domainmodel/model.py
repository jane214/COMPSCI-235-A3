from datetime import datetime
from typing import List, Iterable


class ModelException(Exception):
    pass


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.colleague = []
        self._movies = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, value):
        if value == "" or type(value) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = value.strip()

    @property
    def movies(self):
        return self._movies

    @movies.setter
    def movies(self, new_list):
        self._movies = new_list

    def add_movies(self, movie):
        self._movies.append(movie)

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other):
        if not (isinstance(other, Actor) or other.actor_full_name is None):
            return False
        else:
            return self.actor_full_name == other.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague: "Actor"):
        self.colleague.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: "Actor"):
        return colleague in self.colleague


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self._movies = []

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def movies(self):
        return self._movies

    def add_movies(self, movie):
        self._movies.append(movie)

    def __repr__(self):
        return f"<Director {self.director_full_name}>"

    def __eq__(self, other):
        if not (isinstance(other, Director) or other.director_full_name is None):
            return False
        else:
            return self.director_full_name == other.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.director_full_name)


class Movie:
    def __init__(self, movie_name, release_year=None, new_id=None, hyperlink=None):
        if movie_name == "" or type(movie_name) is not str:
            self.__movie_name = None
        else:
            self.__movie_name = movie_name.strip()
        if type(release_year) is not int or release_year < 1900:
            self.__year = None
        else:
            self.__year = release_year
        self._description = None
        self._director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes = None
        self._id = new_id
        self._review = []
        self._hyperlink = hyperlink
        self._rating = None
        self._votes = None

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, new_rate):
        self._rating = new_rate

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, new_vote):
        self._votes = new_vote

    @property
    def year(self):
        return self.__year

    @property
    def title(self):
        return self.__movie_name

    @property
    def hyperlink(self):
        return self._hyperlink

    @hyperlink.setter
    def hyperlink(self, new_link):
        self.hyperlink = new_link

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_string: str):
        if new_string == "" or type(new_string) is not str:
            self._description = None
        else:
            self._description = new_string.strip()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, new_direct: Director):
        if isinstance(new_direct, Director):
            self._director = new_direct

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, new_actor_list):
        actor_list = []
        for actor in new_actor_list:
            actor_list += [Actor(actor)]
        self._actors = actor_list

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, new_genre_list):
        genre_list = []
        for genre in new_genre_list:
            genre_list += [Genre(genre)]
        self._genres = genre_list

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @property
    def reviews(self):
        return self._review

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime: int):
        if isinstance(new_runtime, int):
            if new_runtime > 0:
                self._runtime_minutes = new_runtime
            else:
                raise ValueError
        else:
            raise ValueError

    def concate(self) -> str:
        return str(self.__movie_name) + str(self.__year)

    def __repr__(self):
        return f"<Movie {self.__movie_name}, {self.__year}, {self.id}>"

    def __eq__(self, other: "Movie"):
        if not isinstance(other, Movie):
            return False
        else:
            string1 = self.concate()
            string2 = other.concate()
            return string1 == string2

    def __lt__(self, other):
        return self.year < other.year

    def __str__(self):
        return f"<Movie {self.__movie_name}, {self.__year}, {self.id}>"

    def __hash__(self):
        string1 = self.concate()
        return hash(string1)

    def add_actor(self, new_actor: Actor):
        if isinstance(new_actor, Actor):
            self._actors.append(new_actor)

    def remove_actor(self, new_actor: Actor):
        if isinstance(new_actor, Actor) and new_actor in self._actors and (len(self._actors) > 0):
            self._actors.remove(new_actor)

    def add_genre(self, new_genre: 'Genre'):
        if isinstance(new_genre, Genre):
            self._genres.append(new_genre)

    def add_review(self, review: 'Review'):
        self._review.append(review)

    def remove_genre(self, new_genre: 'Genre'):
        if isinstance(new_genre, Genre) and new_genre in self._genres and (len(self._genres) > 0):
            self._genres.remove(new_genre)

    def is_genred_by(self, genre: 'Genre'):
        return genre in self._genres


class Review:
    def __init__(self, movie1: Movie, text, rating_number, user):
        if movie1 == "" or type(movie1) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie1
        if text == "" or type(text) is not str:
            self.__review_text = None
        else:
            self.__review_text = text
        if type(rating_number) is not int or rating_number < 1 or rating_number > 10:
            self.__rating_number = None
        else:
            self.__rating_number = rating_number
        self.__timestamp = datetime.today()
        self._user = user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def user(self):
        return self._user

    @property
    def rating(self):
        return self.__rating_number

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, new_stamp):
        self.__timestamp = new_stamp

    def __repr__(self):
        return f"<Review: {self.__movie} Time: {self.__timestamp}>"

    def __eq__(self, other):
        if not (isinstance(other, Review)):
            return False
        else:
            return (self.__movie == other.__movie and
                    self.__review_text == other.__review_text and
                    # self.__rating_number == other.__rating_number and
                    self.__timestamp == other.__timestamp)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self._tagged_movies = []

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @genre_name.setter
    def genre_name(self, value):
        if value == "" or type(value) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = value.strip()

    @property
    def movie_list(self):
        return self._tagged_movies

    @movie_list.setter
    def movie_list(self, new_list):
        self._tagged_movies = new_list

    @property
    def tagged_movies(self) -> Iterable[Movie]:
        return iter(self._tagged_movies)

    def add_movie(self, new_movie: Movie):
        if new_movie not in self._tagged_movies:
            self._tagged_movies.append(new_movie)

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if not (isinstance(other, Genre) or other.genre_name is None):
            return False
        else:
            return self.genre_name == other.genre_name

    def __lt__(self, other):
        return self.genre_name < other.genre_name

    def __hash__(self):
        return hash(self.genre_name)

    def number_of_movies(self):
        return len(self._tagged_movies)


class User:
    def __init__(self, name: str, password: str):
        if name == "" or type(name) is not str:
            self.__user_name = None
        else:
            self.__user_name = name.strip().lower()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self._watched_movies = []
        self._reviews = []
        self._time_spent = 0
        self._watch_list = WatchList()

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def watch_list(self):
        return self._watch_list

    @watch_list.setter
    def watch_list(self, list1):
        self._watch_list = list1

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, value):
        if (type(value) is not int) or value < 0:
            self._time_spent = None
        else:
            self._time_spent = value

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self.__user_name == other.__user_name

    def __lt__(self, other):
        if isinstance(other, User):
            return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie1: Movie):
        if isinstance(movie1, Movie) and movie1 not in self._watched_movies:
            self._watched_movies.append(movie1)
            if type(movie1.runtime_minutes) is int:
                self._time_spent += movie1.runtime_minutes

    def add_review(self, review1):
        if isinstance(review1, Review) and review1 not in self._reviews:
            self._reviews.append(review1)

    def add_watch_list(self, new_movie: Movie):
        if isinstance(new_movie, Movie):
            self._watch_list.add_movie(new_movie)

    def remove_watch_list(self, new_movie: Movie):
        if isinstance(new_movie, Movie):
            self._watch_list.remove_movie(new_movie)


class WatchList:
    def __init__(self):
        self.__watchlist: List[Movie] = []
        self.__user = None

    @property
    def watch_list(self):
        return self.__watchlist

    @property
    def user(self):
        return self.__user

    @watch_list.setter
    def watch_list(self, new_list: list):
        self.__watchlist = new_list

    @user.setter
    def user(self, new_user: User):
        self.__user = new_user

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if isinstance(movie, Movie) and movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if type(index) is not int or index >= len(self.__watchlist):
            return None
        else:
            return self.__watchlist[index]

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if len(self.__watchlist) == 0:
            return None
        else:
            return self.__watchlist[0]

    def __repr__(self):
        return ", ".join(str(x) for x in self.__watchlist)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.__watchlist):
            result = self.__watchlist[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


def make_review(comment_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    comment = Review(movie, comment_text, -1, user)
    comment.timestamp = timestamp
    user.add_review(comment)
    movie.add_review(comment)

    return comment
