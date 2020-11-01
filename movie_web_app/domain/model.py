from typing import List, Iterable
from datetime import date, datetime
class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self._colleague_list = list()
        self._joined_movie = list()
        self._reviews = list()

    @property
    def reviews(self):
        return self._reviews

    @property
    def joined_movie(self):
        return self._joined_movie

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        # TODO
        if not isinstance(other, Actor):
            return False
        if self.__actor_full_name == other.__actor_full_name:
            return True
        else:
            return False
        #pass

    def __lt__(self, other):
        # TODO
        return self.__actor_full_name < other.__actor_full_name

        #pass

    def __hash__(self):
        # TODO
        return hash(self.__actor_full_name)
        #pass

    def add_actor_colleague(self, colleague):
        self._colleague_list += [colleague.__actor_full_name]

    def check_if_this_actor_worked_with(self, colleague):
        if colleague.__actor_full_name in self._colleague_list:
            return True
        else:
            return False

    def add_joined_movie(self, movie: 'Movie'):
        self._joined_movie.append(movie)

    def add_review(self,review):
        self._reviews.append(review)


class Director:
    #class Person:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self._dir_movies = list() # 这个导演导的电影
        self._reviews = list()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def dir_movies(self):
        return self._dir_movies

    @property
    def reviews(self):
        return self._reviews

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        # TODO
        if not isinstance(other, Director):
            return False
        if self.__director_full_name == other.__director_full_name:
            return True
        else:
            return False
        #pass

    def __lt__(self, other):
        # TODO
        return self.__director_full_name < other.__director_full_name

        #pass

    def __hash__(self):
        # TODO
        return hash(self.__director_full_name)
        #pass

    def add_dir_movie(self, movie:'Movie'):
        self._dir_movies.append(movie)

    def add_review(self,review):
        self._reviews.append(review)

class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self._tagged_movies: List[Movie] = list()


    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def tagged_movies(self) -> Iterable['Movie']:
        return self._tagged_movies #covid 不一样

    @property
    def number_of_tagged_movies(self) -> int:
        return len(self._tagged_movies)

    def is_applied_to(self, movie: 'Movie') -> bool:
        return movie in self._tagged_movies

    def add_movie(self, movie: 'Movie'):
        self._tagged_movies.append(movie)


    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        # TODO
        if not isinstance(other, Genre):
            return False
        if self.__genre_name == other.__genre_name:
            return True
        else:
            return False
        #pass

    def __lt__(self, other):
        # TODO
        return self.genre_name < other.genre_name

        #pass

    def __hash__(self):
        # TODO
        return hash(self.__genre_name)

class Movie:
    def __init__(self, id, movie_name: str, release_year = None):
        if movie_name == "" or type(movie_name) is not str:
            self.__title = None
        else:
            self.__title = movie_name.strip()
        if type(release_year) is not int or release_year < 1900:
            self.__release_year = None
        else:
            self.__release_year = release_year
        self._id = id # integer unique id (new one)
        self._description = None
        self._director = None
        self._actors: List['Actor'] = list()
        self._genres: List['Genre'] = list()
        self._runtime_minutes = None
        self._reviews = list()


    @property
    def id(self):
        return self._id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description == "" or type(description) is not str:
            self._description = None
        else:
            self._description = description.strip()

    @property
    def director(self):
        #return self.__director
        return self._director

    @director.setter
    def director(self, director):
        if isinstance(director, Director):
            self._director = director

    @property
    def actors(self) -> list:
        return self._actors

    @property
    def genres(self) -> list:
        return self._genres

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) is int and runtime_minutes > 0:
            self._runtime_minutes = runtime_minutes
        else:
            raise ValueError

    @property
    def reviews(self):
        return self._reviews

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        if self._id == other._id and self.__title == other.__title and self.__release_year == other.__release_year:
            return True
        else:
            return False

    def __lt__(self, other): #这里不确定
        movie_info = str(self.__release_year) + self.__title
        other_movie_info = str(other.__release_year) + other.__title

        # if type(other.__release_year) != int:
        #     other.__release_year = 2020
        return movie_info < other_movie_info

    def __hash__(self):
        the_string = str(self.__title) + str(self.__release_year)
        return hash(the_string)

    def is_tagged_by(self, genre):
        return genre in self._genres


    def add_actor(self, actor):
        if isinstance(actor, Actor):
            self._actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor) and len(self._actors)>0 and actor in self._actors:
            self._actors.remove(actor)


    def add_genre(self, genre):
        if isinstance(genre, Genre):
            self._genres.append(genre)

    def remove_genre(self, genre):
        if isinstance(genre, Genre) and len(self._genres) > 0 and genre in self._genres:
            self._genres.remove(genre)

    def add_review(self, review):
        if isinstance(review, Review):
            self._reviews.append(review)
    def set_des(self, des):
        self.description = des

class Review:
    def __init__(self, user, movie, review_text): #新加的user
        if not isinstance(user, User):
            self.__user = None
        else:
            self.__user = user

        if not isinstance(movie, Movie):
            self.__movie = None
        else:
            self.__movie = movie

        if type(review_text) is str and review_text != "":
            self.__review_text = review_text
        else:
            self.__review_text = None

        # if type(rating) is int and 1 <= rating <= 10:
        #     self.__rating = rating
        # else:
        #     self.__rating = None
        self.__timestamp = datetime.today()

    @property
    def user(self):
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        # return self.actor.actor_full_name + ", " + self.review_text + ", " + self.timestamp
        return self.movie.title + ", " + self.review_text

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        if self.user == other.user and self.movie == other.movie and self.review_text == other.review_text and self.timestamp == other.timestamp:
            return True
        else:
            return False


class ActorReview:
    def __init__(self, user, actor, review_text):
        if not isinstance(user, User):
            self.__user = None
        else:
            self.__user = user

        if not isinstance(actor, Actor):
            self.__actor = None
        else:
            self.__actor = actor

        if type(review_text) is str and review_text != "":
            self.__review_text = review_text
        else:
            self.__review_text = None

        self.__timestamp = datetime.today()

    @property
    def actor(self):
        return self.__actor

    @property
    def user(self):
        return self.__user

    @property
    def review_text(self):
        return self.__review_text

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        #return self.actor.actor_full_name + ", " + self.review_text + ", " + self.timestamp
        return self.actor.actor_full_name + ", " + self.review_text

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        if self.user == other.user and self.actor == other.actor and self.review_text == other.review_text and self.timestamp == other.timestamp:
            return True
        else:
            return False



class DirectorReview:
    def __init__(self, user, director, review_text):
        if not isinstance(user, User):
            self.__user = None
        else:
            self.__user = user

        if not isinstance(director, Director):
            self.__director = None
        else:
            self.__director = director

        if type(review_text) is str and review_text != "":
            self.__review_text = review_text
        else:
            self.__review_text = None

        self.__timestamp = datetime.today()

    @property
    def director(self):
        return self.__director

    @property
    def user(self):
        return self.__user

    @property
    def review_text(self):
        return self.__review_text
    # @property
    # def rating(self):
    #     return self.__rating
    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return self.director.director_full_name + ", " + self.review_text
        #return self.director.director_full_name + ", " + self.review_text + ", " + self.timestamp


    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        if self.user == other.user and self.director == other.director and self.review_text == other.review_text and self.timestamp == other.timestamp:
            return True
        else:
            return False

class User:
    def __init__(self, user_name, password):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.lower()
        if password == "" or type(user_name) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies: List[Movie] = list()
        self.__reviews: List[Review] = list()
        self.__time_spent_watching_movies_minutes = 0
        self.__watchList: List[Movie] = list()
    @property
    def user_name(self):
        return self.__user_name
    @property
    def password(self):
        return self.__password
    @property
    def watched_movies(self):
        return self.__watched_movies
    @property
    def reviews(self):
        return self.__reviews
    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, value):
        self.__time_spent_watching_movies_minutes += value

    @property
    def watchList(self):
        return self.__watchList

    def __repr__(self):
        return "<User " + self.__user_name + ">"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.__user_name == other.__user_name:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        if isinstance(movie, Movie) and movie not in self.__watched_movies:
            self.__watched_movies.append(movie)
            #print("****")
            if type(movie.runtime_minutes) is int:
                #print("runtime")
                #print(movie.runtime_minutes)
                self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def add_watchList(self, new_movie):
        if isinstance(new_movie, Movie) and (new_movie not in self.__watchList):
            self.__watchList.append(new_movie)

class WatchList:
    def __init__(self):
        self.__watch_list: List[Movie] = list()

    def add_movie(self, movie):
        if isinstance(movie, Movie) and movie not in self.__watch_list:
            self.__watch_list.append(movie)

    def remove_movie(self, movie):
        if isinstance(movie, Movie) and movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def select_movie_to_watch(self, index):
        if type(index) != int or index < 0 or index >= len(self.__watch_list):
            return None
        else:
            return self.__watch_list[index]

    def size(self):
        return len(self.__watch_list)

    def first_movie_in_watchlist(self):
        if len(self.__watch_list) == 0:
            return None
        else:
            return self.__watch_list[0]

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count < len(self.__watch_list):
            the_movie = self.__watch_list[self.count]
            self.count +=1
            return the_movie
        else:
            raise StopIteration


class MovieWatchingSimulation:
    def __init__(self, users, movie):
        if len(users) > 1:
            self.__users: List[User] = users
        if isinstance(movie, Movie):
            self.__the_movie = movie
        else:
            self.__the_movie = None
        self.__reviews = {}
        self.__finish_watch = False;


   #def __repr__(self):
        #return "{ Watching Simulation:" + self.__the_movie + self.__users + "}"

    @property
    def users(self):
        return self.__users
    @users.setter
    def users(self, value):
        self.__users = value

    @property
    def the_movie(self):
        return self.__the_movie

    @property
    def reviews(self):
        return self.__reviews

    @property
    def finish_watch(self):
        return self.__finish_watch

    def add_user(self, new_user):
        if new_user not in self.__users:
            self.__users.append(new_user)

    def change_movie(self, new_movie):
        if isinstance(new_movie, Movie) and new_movie != self.__the_movie:
            self.__the_movie = new_movie

    def done_watching(self):
        self.__finish_watch = True
        for i in self.__users:
            if self.__the_movie in i.watchList:
                i.watchList.remove(self.__the_movie)

    def add_review(self, user, review):
        if (self.__finish_watch == True) and (user in self.__users ) and (isinstance(review, Review)):
            if review.movie == self.__the_movie:
                self.__reviews[user] = review

class ModelException(Exception):
    pass

def make_review(user:User, movie:Movie, review_text:str):
    review = Review(user, movie, review_text)
    user.add_review(review)
    movie.add_review(review)
    return review

def make_actor_review(user:User, actor:Actor, review_text:str):
    review = ActorReview(user, actor, review_text)
    user.add_review(review)
    actor.add_review(review)
    return review

def make_director_review(user:User, director:Director, review_text:str):
    review = DirectorReview(user, director, review_text)
    user.add_review(review)
    director.add_review(review)
    return review

def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Movie "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)

