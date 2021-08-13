import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from psycopg2 import IntegrityError
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

    @app.route('/movies', methods=['POST'])
    def create_movie():
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release date', None)
            if not (title and release_date):
                raise ValueError(
                    'Some information is missing, unable to create question')
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
        except ValueError as Value_error:
            print(Value_error.with_traceback(Value_error.__traceback__))
            abort(422)
        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            abort(400)

        return jsonify({
            'success': True,
            'movieID': movie.id,
            'movie': movie.format()
        })

    @app.route("/movie/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            "success": True,
            "deleted": movie_id
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

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            "success": True,
            "deleted": actor_id
        })

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if not (name and age and gender):
            abort(422)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'actorID': actor.id,
            'actor': actor.format()
        })


# Error Handling
# error handling for unprocessable entity

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

# error handling for an entity that can't be found

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
