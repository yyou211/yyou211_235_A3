from datetime import date, datetime

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, ValidationError

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.utilities as utilities
import movie_web_app.movie.services as services

from movie_web_app.authentication.authentication import login_required

# Configure Blueprint.
movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    # Read query parameters.
    target_year = request.args.get('release_year')
    movies_to_show_reviews = request.args.get('view_reviews_for') # 不确定

    # Fetch the first and last articles in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_year is None:
        target_year = first_movie['release_year']

    else:
        target_year = int(target_year)

    if movies_to_show_reviews is None:
        movies_to_show_reviews = -1

    else:
        movies_to_show_reviews = int(movies_to_show_reviews)

    movies, previous_year, next_year = services.get_movies_by_year(target_year, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        if previous_year is not None:
            prev_movie_url = url_for('movie_bp.movies_by_year', release_year = int(previous_year))
            first_movie_url = url_for('movie_bp.movies_by_year', release_year = int(first_movie['release_year']))

        if next_year is not None:
            next_movie_url = url_for('movie_bp.movies_by_year', release_year = int(next_year))
            last_movie_url = url_for('movie_bp.movies_by_year', release_year = int(last_movie['release_year']))

        for movie in movies:
            movie['view_review_url'] = url_for('movie_bp.movies_by_year', release_year = target_year, view_reviews_for = movie['id'])
            movie['add_review_url'] = url_for('movie_bp.review_on_movie', movie = movie['id'])

        return render_template(
            'movie/movie.html',
            title='Movies',
            movie_title=target_year,
            movies=movies,
            selected_movies=utilities.get_selected_movies(5),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url = first_movie_url,
            last_movie_url = last_movie_url,
            prev_movie_url = prev_movie_url,
            next_movie_url = next_movie_url,
            show_reviews_for_movie = movies_to_show_reviews
        )
    return redirect(url_for('home_bp.home'))


@movie_blueprint.route('/movies_by_genre', methods = ['GET'])
def movies_by_genre():
    movies_per_page = 100
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movies_to_show_reviews = request.args.get('view_reviews_for')

    if movies_to_show_reviews is None:
        movies_to_show_reviews = -1
    else:
        movies_to_show_reviews = int(movies_to_show_reviews)

    if cursor is None:
        cursor = 0

    else:
        cursor = int(cursor)

    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        prev_movie_url = url_for('movie_bp.movies_by_genre', genre= genre_name, cursor = cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_genre', genre = genre_name)

    if cursor + movies_per_page < len(movie_ids):
        next_movie_url = url_for('movie_bp.movies_by_genre', genre = genre_name, cursor = cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_genre', genre = genre_name, cursor = last_cursor)

    for movie in movies:
        movie['view_review_url'] = url_for('movie_bp.movies_by_genre', genre = genre_name, cursor = cursor, view_reviews_for = movie['id'])
        movie['add_review_url'] = url_for('movie_bp.review_on_movie', movie = movie['id'])

    return render_template(
        'movie/movie.html',
        title='movies',
        movie_title='Movies tagged by ' + genre_name,
        movies = movies,
        selected_movies=utilities.get_selected_movies(5),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movies_to_show_reviews
    )

@movie_blueprint.route('/genres_list', methods = ['GET'])
def genres_list():
    return render_template(
        'genres_list.html',
         genre_urls=utilities.get_genres_and_urls(),
        selected_movies=utilities.get_selected_movies(5)
    )



@movie_blueprint.route('/review', methods = ['GET', 'POST'])
@login_required
def review_on_movie():
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        movie_id = int(form.movie_id.data)

        #services.add_review(movie_id, username, form.review.data, repo.repo_instance)
        services.add_review(username, movie_id, form.review.data, repo.repo_instance)

        movie = services.get_movie_by_id(movie_id, repo.repo_instance)

        return redirect(url_for('movie_bp.movies_by_year', release_year = movie['release_year'], view_reviews_for = movie_id))

    if request.method == 'GET':
        #movie_id = int(request.args.get('movie_id'))
        movie_id = int(request.args.get('movie'))
        form.movie_id.data = movie_id

    else:
        movie_id = int(form.movie_id.data)

    movie = services.get_movie_by_id(movie_id, repo.repo_instance)
    return render_template(
        'movie/review_on_movie.html',
        title='Edit movie',
        movie = movie,
        form=form,
        handler_url=url_for('movie_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(5),
        genre_urls=utilities.get_genres_and_urls()
    )

@movie_blueprint.route('/review_actor', methods = ['GET', 'POST'])
@login_required
def review_on_actor():
    username = session['username']

    form = ActorReviewForm()

    if form.validate_on_submit():
        actor_name = form.actor_name.data

        #services.add_review(movie_id, username, form.review.data, repo.repo_instance)
        services.add_actor_review(username, actor_name, form.review.data, repo.repo_instance)

        actor = services.get_actor(actor_name, repo.repo_instance)

        return redirect(url_for('movie_bp.actors_list', view_actor_reviews_for = actor_name))

    if request.method == 'GET':
        #movie_id = int(request.args.get('movie_id'))
        actor_name = request.args.get('actor_name')
        form.actor_name.data = actor_name

    else:
        actor_name = form.actor_name.data

    actor = services.get_actor(actor_name, repo.repo_instance)
    return render_template(
        'actors/review_on_actor.html',
        actor = actor,
        form=form,
        handler_url=url_for('movie_bp.review_on_actor'),
        selected_movies=utilities.get_selected_movies(5),

    )

@movie_blueprint.route('/review_director', methods = ['GET', 'POST'])
@login_required
def review_on_director():
    username = session['username']

    form = DirectorReviewForm()

    if form.validate_on_submit():
        director_name = form.director_name.data

        #services.add_review(movie_id, username, form.review.data, repo.repo_instance)
        services.add_director_review(username, director_name, form.review.data, repo.repo_instance)

        director = services.get_director(director_name, repo.repo_instance)

        return redirect(url_for('movie_bp.directors_list', view_director_reviews_for = director_name))

    if request.method == 'GET':
        #movie_id = int(request.args.get('movie_id'))
        director_name = request.args.get('director_name')
        form.director_name.data = director_name

    else:
        director_name = form.director_name.data

    director = services.get_director(director_name, repo.repo_instance)
    return render_template(
        'directors/review_on_director.html',
        director = director,
        form=form,
        handler_url=url_for('movie_bp.review_on_director'),
        selected_movies=utilities.get_selected_movies(5),

    )




@movie_blueprint.route('/search_movie', methods = ['GET', 'POST'])
def search_movie():
    form = SearchMovieForm()
    if form.validate_on_submit():
        movie_name = form.movie.data
        movies = services.get_movies_by_name(movie_name, repo.repo_instance)
        for movie in movies:
            movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year=int(movie['release_year']))
        if len(movies) == 0:
            movies = None
        return render_template(
            'list_movie.html',
            selected_movies=utilities.get_selected_movies(5),
            movies = movies
        )
    return render_template(
        'search_movie.html',
        selected_movies=utilities.get_selected_movies(5),
        form = form
    )

@movie_blueprint.route('/search_movie_by_director', methods = ['GET', 'POST'])
def search_movie_by_director():
    form = SearchDirectorForm()
    if form.validate_on_submit():
        director_name = form.movie.data
        movies = services.get_movies_by_director(director_name, repo.repo_instance)
        for movie in movies:
            movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year=int(movie['release_year']))
        if len(movies) == 0:
            movies = None
        return render_template(
            'list_movie.html',
            selected_movies=utilities.get_selected_movies(5),
            movies = movies
        )
    return render_template(
        'search_movie_by_director.html',
        selected_movies=utilities.get_selected_movies(5),
        form = form
    )

@movie_blueprint.route('/search_movie_by_actor', methods = ['GET', 'POST'])
def search_movie_by_actor():
    form = SearchActorForm()
    if form.validate_on_submit():
        actor_name = form.movie.data
        movies = services.get_movies_by_actor(actor_name, repo.repo_instance)
        for movie in movies:
            movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year=int(movie['release_year']))
        if len(movies) == 0:
            movies = None
        return render_template(
            'list_movie.html',
            selected_movies=utilities.get_selected_movies(5),
            movies = movies
        )
    return render_template(
        'search_movie_by_actor.html',
        selected_movies=utilities.get_selected_movies(5),
        form = form
    )


@movie_blueprint.route('/actors_list', methods=['GET'])
def actors_list():
    # Read query parameters.
    #target_year = request.args.get('release_year')
    actors_to_show_reviews = request.args.get('view_reviews_for_actor')  # 不确定

    if actors_to_show_reviews is None:
        actors_to_show_reviews = -1

    else:
        actors_to_show_reviews = actors_to_show_reviews

    actors = services.get_all_actors(repo.repo_instance)
    #each_actor_joined_movie = {}
    for actor in actors:
        actor_name = actor['actor_name']
        #print(actor['reviews'])
        joined_movies = services.get_movies_by_actor(actor_name,repo.repo_instance)
        #joined_movies_id = actor['joined_movies']
        for movie in joined_movies:
            movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year=int(movie['release_year']))
        actor['joined_movies'] = joined_movies
        #each_actor_joined_movie[actor] = joined_movies

    if len(actors) > 0:
        for actor in actors:
            actor['view_review_url'] = url_for('movie_bp.actors_list',
                                               view_reviews_for_actor=actor['actor_name'])
            actor['add_review_url'] = url_for('movie_bp.review_on_actor', actor_name=actor['actor_name'])

        return render_template(
            'actors/actors.html',
            title='Movies',
            movie_title='Actors',
            actors=actors,
            selected_movies=utilities.get_selected_movies(5),
            show_reviews_for_actor=actors_to_show_reviews
        )
    return redirect(url_for('home_bp.home'))


@movie_blueprint.route('/directors_list', methods=['GET'])
def directors_list():
    # Read query parameters.
    #target_year = request.args.get('release_year')
    directors_to_show_reviews = request.args.get('view_reviews_for_director')  # 不确定

    if directors_to_show_reviews is None:
        directors_to_show_reviews = -1

    else:
        directors_to_show_reviews = directors_to_show_reviews

    directors= services.get_all_directors(repo.repo_instance)
    for director in directors:
        director_name = director['director_name']
        #print(["hhhhhhh"] + director['reviews'])
        dir_movies = services.get_movies_by_director(director_name,repo.repo_instance)
        #joined_movies_id = actor['joined_movies']
        for movie in dir_movies:
            movie['hyperlink'] = url_for('movie_bp.movies_by_year', release_year=int(movie['release_year']))
        director['dir_movies'] = dir_movies

    if len(directors) > 0:
        for director in directors:
            director['view_review_url'] = url_for('movie_bp.directors_list',
                                               view_reviews_for_director=director['director_name'])
            director['add_review_url'] = url_for('movie_bp.review_on_director', director_name=director['director_name'])

        return render_template(
            'directors/directors.html',
            title='Movies',
            movie_title='directors',
            directors=directors,
            selected_movies=utilities.get_selected_movies(5),
            show_reviews_for_director=directors_to_show_reviews
        )
    return redirect(url_for('home_bp.home'))



class SearchMovieForm(FlaskForm):
    movie = StringField('type movie name', [DataRequired(message='movie name is required')])
    submit = SubmitField('Find')

class SearchDirectorForm(FlaskForm):
    movie = StringField('type director name to find movies', [DataRequired(message='movie name is required')])
    submit = SubmitField('Find')

class SearchActorForm(FlaskForm):
    movie = StringField('type actor name to find movies', [DataRequired(message='movie name is required')])
    submit = SubmitField('Find')


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review text is too short'),
        ProfanityFree(message='Your review text must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')

class ActorReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review text is too short'),
        ProfanityFree(message='Your review text must not contain profanity')])
    actor_name = HiddenField("Actor name")
    submit = SubmitField('Submit')

class DirectorReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review text is too short'),
        ProfanityFree(message='Your review text must not contain profanity')])
    director_name = HiddenField("Director name")
    submit = SubmitField('Submit')






















