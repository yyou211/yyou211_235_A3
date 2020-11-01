import csv
from typing import List
from movie_web_app.domain.model import Actor, Director, Genre, Movie

class MovieFileCSVReader:
    def __init__(self,file_name):
        self.__file_name = file_name
        self.__movies = set()
        self.__movies_index = set()  # key is movie id, the corresponding value is movie object
        self.__genres = set()
        self.__reviews = set()
        self.__directors = set()
        self.__actors = set()
        # self._actor_review = list()
        # self._director_review = list()


    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            #index = 0
            genre_dict = {}
            director_dict = {}
            actor_dict = {}
            for row in movie_file_reader:
                movie_id = int(row['id'])
                movie_title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(movie_id, movie_title, release_year)
                self.__movies.add(movie)
                genre = row["Genre"]
                genres_list = genre.split(",")
                for genre_name in genres_list:
                    if genre_name not in genre_dict:
                        genre_dict[genre_name] = [movie]
                    else:
                        genre_dict[genre_name] = genre_dict[genre_name] + [movie]
                des = row['Description']
                movie.set_des(des)
                the_director = row["Director"]
                if the_director not in director_dict:
                    director_dict[the_director] = [movie]
                else:
                    director_dict[the_director] = director_dict[the_director] + [movie]
                actor_list = row["Actors"]
                for actor in actor_list.split(","):
                    actor = actor.strip()
                    if actor not in actor_dict:
                        actor_dict[actor] = [movie]
                    else:
                        actor_dict[actor] = actor_dict[actor] + [movie]
            for genre_name in genre_dict:
                genre = Genre(genre_name)
                for movie in genre_dict[genre_name]:
                    genre.add_movie(movie)
                    movie.add_genre(genre)
                self.__genres.add(genre)
            for director_name in director_dict:
                director = Director(director_name)
                for movie in director_dict[director_name]:
                    director.add_dir_movie(movie)
                    movie.director = director
                self.__directors.add(director)
            for actor_name in actor_dict:
                actor = Actor(actor_name)
                for movie in actor_dict[actor_name]:
                    actor.add_joined_movie(movie)
                    movie.add_actor(actor)
                self.__actors.add(actor)


    @property
    def movies(self):
        return self.__movies
    @property
    def actors(self):
        return self.__actors
    @property
    def directors(self):
        return self.__directors
    @property
    def genres(self):
        return self.__genres

filename = '/Users/vivian/Desktop/235Ass2_version4/movie_web_app/datafiles/Data1000Movies.csv'
movie_file_reader = MovieFileCSVReader(filename)
movie_file_reader.read_csv_file()

all_directors_sorted = sorted(movie_file_reader.directors)
print(f'first 3 unique directors of sorted dataset: {all_directors_sorted[0:3]}')

# for movie in movie_file_reader.movies:
#     print(movie)
# for genre in movie_file_reader.genres:
#     print(genre)











