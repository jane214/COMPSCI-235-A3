import csv

from movie_web_app.domainmodel.model import Movie, Director, Actor, Genre


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self._dataset_of_movies = []
        self._genre_dict = {}
        self._actor_list = []
        self._director_list = []
        self._genre_list = []
        self._dataset_of_actors = set()
        self._dataset_of_genres = set()
        self._dataset_of_directors = set()
        self._actor_dict = {}
        self._director_dict = {}

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year)
                movie.director = Director(row["Director"])
                actor_list = row["Actors"].split(',')
                movie.actors = actor_list
                self._dataset_of_movies.append(movie)
                genre_list = row['Genre'].split(",")
                description= row['Description']
                movie.description = description
                for genre in genre_list:
                    new_g = Genre(genre)
                    new_g.add_movie(movie)
                    self._dataset_of_genres.add(new_g)
                    if new_g in self._genre_dict:
                        if movie not in self._genre_dict[new_g]:
                            self._genre_dict[new_g] += [movie]
                    else:
                        self._genre_dict[new_g] = [movie]
                movie.genres = genre_list
                self._actor_list += actor_list
                for actor in actor_list:
                    new_a = Actor(actor)
                    new_a.add_movies(movie)
                    if new_a not in self._actor_dict:
                        self._actor_dict[new_a] = [movie]
                    else:
                        if movie not in self._actor_dict[new_a]:
                            self._actor_dict[new_a] += [movie]
                    self._dataset_of_actors.add(new_a)


                director_list = row["Director"].split(',')
                for director in director_list:
                    new_d = Director(director)
                    new_d.movies = movie
                    if new_d not in self._director_dict:
                        self._director_dict[new_d] = [movie]
                    else:
                        if movie not in self._director_dict:
                            self._director_dict[new_d] += [movie]
                    self._dataset_of_directors.add(new_d)


    @property
    def dataset_of_movies(self):
        self._dataset_of_movies.sort(key=lambda movie: movie.year)
        for i in range(len(self._dataset_of_movies)):
            self._dataset_of_movies[i].id = i + 1
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self._dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres

    @property
    def genres_dict(self):
        return self._genre_dict

    @property
    def actor_dict(self):
        return self._actor_dict

    @property
    def director_dict(self):
        return self._director_dict

# filename = 'Data1000Movies.csv'
# movie_file_reader1 = MovieFileCSVReader(filename)
# movie_file_reader1.read_csv_file()
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
