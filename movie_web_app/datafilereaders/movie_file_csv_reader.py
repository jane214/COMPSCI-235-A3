import csv
from typing import Set

from movie_web_app.domainmodel.model import Movie, Director, Actor, Genre

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self._dataset_of_movies = []
        self._genre_dict = {}
        self._actor_list = []
        self._director_list = []
        self._genre_list = []
        self._dataset_of_actors: Set[Actor] = set()
        self._dataset_of_genres = list()
        self._dataset_of_directors = set()
        self._actor_dict = {}
        self._director_dict = {}

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                run_time = int(row['Runtime (Minutes)'])
                actor_list = row["Actors"].split(',')
                description = row['Description']
                genre_list = row['Genre'].split(",")
                rating = float(row['Rating'])
                votes = int(row['Votes'])

                movie = Movie(title, release_year)
                movie.description = description
                movie.actors = actor_list
                movie.genres = genre_list
                movie.runtime_minutes = run_time
                movie.rating = rating
                movie.votes = votes
                self._dataset_of_movies.append(movie)

                for genre in genre_list:
                    new_g = Genre(genre.strip())
                    if new_g not in self.dataset_of_genres:
                        self._dataset_of_genres.append(new_g)
                        new_g.add_movie(movie)
                    else:
                        index = self._dataset_of_genres.index(new_g)
                        self._dataset_of_genres[index].add_movie(movie)
                    if new_g in self._genre_dict:
                        if movie not in self._genre_dict[new_g]:
                            self._genre_dict[new_g] += [movie]
                    else:
                        self._genre_dict[new_g] = [movie]
                movie.genres = genre_list

                for actor in actor_list:
                    new_a = Actor(actor.strip())
                    if new_a not in self._actor_dict:
                        self._actor_dict[new_a] = [movie]
                    else:
                        if movie not in self._actor_dict[new_a]:
                            self._actor_dict[new_a] += [movie]
                    self._dataset_of_actors.add(new_a)

                movie.actors = actor_list

                director = row["Director"]
                new_d = Director(director.strip())
                new_d.add_movies(movie)
                self._dataset_of_directors.add(new_d)

    @property
    def dataset_of_movies(self):
        self._dataset_of_movies.sort(key=lambda movie: movie.year)
        for i in range(len(self._dataset_of_movies)):
            self._dataset_of_movies[i].id = i + 1
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self):
        actor_list = list(self._dataset_of_actors)
        for i in range(len(actor_list)):
            if actor_list[i] in self._actor_dict.keys():
                actor_list[i].movies = self._actor_dict[actor_list[i]]
        return actor_list

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres
        # genre_list = list(self.dataset_of_genres)
        # for i in range(len(genre_list)):
        #     if genre_list[i] in self._genre_dict.keys():
        #         genre_list[i].movies = self._genre_dict[genre_list[i]]
        # return genre_list

    @property
    def genres_dict(self):
        return self._genre_dict

    @property
    def actor_dict(self):
        return self._actor_dict

    @property
    def director_dict(self):
        return self._director_dict

#
# filename = 'Data1000Movies.csv'
# movie_file_reader1 = MovieFileCSVReader(filename)
# movie_file_reader1.read_csv_file()
# print("hi")
# for movie in movie_file_reader1.dataset_of_movies:
#     print(movie)
# for genre in movie_file_reader1.dataset_of_genres:
#     for movie in genre.tagged_movies:
#         print(genre, movie, end = ", ")
#
#     print()
#
# print()
# print()

# print("hi")
# movie_file = movie_file_reader1.dataset_of_movies
# for movie in movie_file:
#     print(movie, movie.id, movie.year, movie.description)
#     print("movie actor", movie.actors, "movie genre", movie.genres, "movie director",  movie.director)
#

# movie_file = movie_file_reader1.genres_dict
# for genre in movie_file:
#     print(genre, movie_file[genre])

# movie_file = movie_file_reader1.actor_dict
# for actor in movie_file:
#     print(actor, movie_file[actor])

# movie_file = movie_file_reader1.director_dict
# for director in movie_file:
#     print(director, movie_file[director])

# movie_file = movie_file_reader1.dataset_of_directors
# for director in movie_file:
#     print(director, director.movies)

# movie_file = movie_file_reader1.genres_dict
# for genre in movie_file.keys():
#     print(genre, movie_file[genre])
# print(movie_file_reader1.dataset_of_actors)
# print(f'number of unique movies: {len(movie_file_reader1.dataset_of_movies)}')
# print(f'number of unique actors: {len(movie_file_reader1.dataset_of_actors)}')
# print(f'number of unique directors: {len(movie_file_reader1.dataset_of_directors)}')
# print(f'number of unique genres: {len(movie_file_reader1.dataset_of_genres)}')
