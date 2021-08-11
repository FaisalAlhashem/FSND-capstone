import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor

NUM_OF_ITEMS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response

    def paginate_movies(request, movies=[]):
        page = request.args.get('page', 1, type=int)
        start = (page-1) * NUM_OF_ITEMS_PER_PAGE
        if len(movies) == 0:
            movies = Movie.query.order_by(Movie.id).limit(
                NUM_OF_ITEMS_PER_PAGE).offset(start).all()
        end = start + NUM_OF_ITEMS_PER_PAGE

        movies = [movie.format() for movie in movies]

        return movies

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = paginate_movies(request)
        return jsonify({
            'success': True,
            'movies': movies,
            'total movies': Movie.query.count()
        })

    def paginate_actors(request, actors=[]):
        page = request.args.get('page', 1, type=int)
        start = (page-1) * NUM_OF_ITEMS_PER_PAGE
        if len(actors) == 0:
            actors = Actor.query.order_by(Actor.id).limit(
                NUM_OF_ITEMS_PER_PAGE).offset(start).all()
        end = start + NUM_OF_ITEMS_PER_PAGE

        actors = [actor.format() for actor in actors]

        return actors

    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = paginate_actors(request)
        return jsonify({
            'success': True,
            'actors': actors,
            'total actors': Actor.query.count()
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
