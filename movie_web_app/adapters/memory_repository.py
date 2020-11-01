import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movie_web_app.adapters.repository import AbstractRepository, RepositoryException

from movie_web_app.domain.model import Actor, Director, Genre, Movie, Review, User, make_review, make_genre_association, ActorReview,DirectorReview
from movie_web_app.domain.model import make_actor_review, make_director_review


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()  # key is movie id, the corresponding value is movie object
        self._genres = list()
        self._users = list()
        self._reviews = list()
        self._directors = list()
        self._actors = list()
        self._actor_review = list()
        self._director_review = list()



    def get_all_movies(self):
        return self._movies # 不知道能不能有这个function

    # def get_movies_index(self):
    #     return self._movies_index


    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    # def get_all_users(self):
    #     return self._users


    def add_movie(self, movie:Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie
        #covid这里有个index

    def get_movies_by_name(self, movie_name):
        matched_list = list()
        for movie in self._movies:
            if (movie.title).lower() == (movie_name).lower():
                matched_list.append(movie)
        return matched_list

        # return 一个list， 可能有重名
        # 和covid不一样 可能有问题

    def get_movie_by_id(self, movie_id):
        movie = None

        try:
           movie = self._movies_index[movie_id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie


    def get_movies_by_year(self, target_year):
        matching_movies = list()
        for movie in self._movies:
            if movie.release_year == target_year:
                matching_movies.append(movie)
        return matching_movies
        #可能有问题

    def get_number_of_movie(self):
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
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the Articles.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies
        #后面可能随机选几个电影的时候会用到这个

    def get_movie_ids_for_genre(self, genre_name):
        the_genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if the_genre is not None:
            movies_ids = [movie.id for movie in the_genre.tagged_movies]
        else:
            # No Tag with name tag_name, so return an empty list.
            movies_ids = list()

        return movies_ids

    def get_year_of_previous_movie(self, movie:Movie):
        previous_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_year = stored_movie.release_year
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_year

    def get_year_of_next_movie(self, movie:Movie):
        next_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_year = stored_movie.release_year
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_year

    def add_genre(self, genre:Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def get_genre_by_name(self, name):
        the_genre = None
        for genre in self._genres:
            if genre.genre_name == name:
                the_genre = genre
                break
        return the_genre

    def add_review(self, review:Review):
        #review.user.add_review(review)  #这里可能有问题
        #review.movie.add_review(review)
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def movie_index(self, movie:Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError

    def get_all_actors(self):
        return self._actors

    def get_all_directors(self):
        return self._directors

    def add_actor(self, actor):
        self._actors.append(actor)

    def add_director(self, director):
        self._directors.append(director)

    def get_movies_by_director(self, director_name):
        matched_list = list()
        for movie in self._movies:
            if (movie.director.director_full_name).lower() == (director_name).lower():
                matched_list.append(movie)
        return matched_list

    def get_movies_by_actor(self, actor_name):
        matched_list = list()
        for movie in self._movies:
            all_actors = movie.actors
            for actor in all_actors:
                if (actor.actor_full_name).lower() == (actor_name).lower():
                    matched_list.append(movie)
        return matched_list

    def add_actor_review(self,review:ActorReview):
        self._actor_review.append(review)

    def add_director_review(self, review: DirectorReview):
        self._director_review.append(review)

    def get_actor(self,name):
        actor = None
        for i in self._actors:
            if i.actor_full_name == name:
                actor = i
        return actor

    def get_director(self,name):
        director = None
        for i in self._directors:
            if i.director_full_name == name:
                director = i
        return director





def load_movies_and_genres(data_path: str, repo: MemoryRepository):
    filename = os.path.join(data_path, 'Data1000Movies.csv')
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)
        genres = dict()
        actors = dict()
        directors = dict()
        for row in movie_file_reader:
            movie_id = int(row['id'])
            movie_title = row['Title']
            release_year = int(row['Year'])

            genre = row["Genre"]
            genres_list = genre.split(",")
            for i in genres_list:
                if i not in genres.keys():
                    genres[i] = list()
                genres[i].append(movie_id)

            movie = Movie(movie_id, movie_title, release_year)
            des = row['Description']
            movie.set_des(des)
            repo.add_movie(movie)
            the_director = row["Director"]
            if the_director not in directors:
                directors[the_director] = [movie_id]
            else:
                directors[the_director] = directors[the_director] + [movie_id]
            actor_list = row["Actors"]
            for actor in actor_list.split(","):
                actor = actor.strip()
                if actor not in actors:
                    actors[actor] = [movie_id]
                else:
                    actors[actor] = actors[actor] + [movie_id]


        for director_name in directors:
            director_obj = Director(director_name)
            all_movie = directors[director_name]
            for movie_id in all_movie:
                movie = repo.get_movie_by_id(movie_id)
                movie.director = director_obj
                director_obj.add_dir_movie(movie)
            repo.add_director(director_obj)

        for actor_name in actors:
            actor_obj = Actor(actor_name)
            all_movie = actors[actor_name]
            for movie_id in all_movie:
                movie = repo.get_movie_by_id(movie_id)
                movie.actors.append(actor_obj)
                actor_obj.add_joined_movie(movie)
            repo.add_actor(actor_obj)

        for genre_name in genres.keys():
            genre = Genre(genre_name)
            for movie_id in genres[genre_name]:
                movie = repo.get_movie_by_id(movie_id)
                make_genre_association(movie, genre)
                # movie.add_genre(genre)
                # genre.add_movie(movie)
            repo.add_genre(genre)

    # print(repo._movies)
    # print(repo._movies_index)

def load_users(data_path:str, repo:MemoryRepository):
    filename = os.path.join(data_path, 'users.csv')
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        user_file_reader = csv.DictReader(csvfile)
        users = dict()
        for row in user_file_reader:
            username = row['username']
            password = generate_password_hash(row['password'])
            user = User(username, password)
            repo.add_user(user)
            user_id = row['id']
            users[user_id] = user
    return users

def load_reviews(data_path: str, repo: MemoryRepository, users):
    filename = os.path.join(data_path, 'reviews.csv')
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        review_file_reader = csv.DictReader(csvfile)
        for row in review_file_reader:
            user_name = row['username']
            user = repo.get_user(user_name)
            movie_id = row['movie_id']
            movie = repo.get_movie_by_id(int(movie_id))
            review_text = row['review_text']
            # rating = int(row['rating'])
            # movie_timestamp = datetime.fromisoformat(row['timestamp'])
            #movie_timestamp = row['timestamp']
            review = make_review(user, movie, review_text)
           # review._timestamp = movie_timestamp
            repo.add_review(review)

def load_actor_reviews(data_path: str, repo: MemoryRepository, users):
    filename = os.path.join(data_path, 'review_on_actor.csv')
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        review_file_reader = csv.DictReader(csvfile)
        for row in review_file_reader:
            user_name = row['username']
            user = repo.get_user(user_name)
            actor_name = row['actor_name']
            actor = repo.get_actor(actor_name)
            review_text = row['review_text']
            review = make_actor_review(user, actor, review_text)
            repo.add_actor_review(review)

def load_director_reviews(data_path: str, repo: MemoryRepository, users):
    filename = os.path.join(data_path, 'review_on_director.csv')
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        review_file_reader = csv.DictReader(csvfile)
        for row in review_file_reader:
            user_name = row['username']
            user = repo.get_user(user_name)
            director_name = row['director_name']
            director = repo.get_director(director_name)
            review_text = row['review_text']
            review = make_director_review(user, director, review_text)
            repo.add_director_review(review)



def populate(data_path: str, repo: MemoryRepository):
    load_movies_and_genres(data_path, repo)

    users = load_users(data_path, repo)

    load_reviews(data_path, repo, users)

    load_actor_reviews(data_path, repo, users)

    load_director_reviews(data_path, repo, users)

#             the_director = row["Director"]
#             director_obj = Director(the_director)
#             if director_obj not in repo._directors:
#                 repo._directors.append(director_obj)
#             movie.director = director_obj
#             director_obj.add_dir_movie(movie)
#
#             actor_list = row["Actors"]
#             for j in actor_list.split(","):
#                 actor_obj = Actor(j)
#                 if j.strip() not in repo._actors:
#                     repo._actors.append(actor_obj)
#                 actor_obj.add_joined_movie(movie)



































