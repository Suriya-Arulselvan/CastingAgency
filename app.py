import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import setup_db, Movie, Actor, dbSessionClose, dbSessionRollback
from datetime import date
from auth.auth import AuthError, requires_auth

"""
Create and configure the application
"""


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resource={r"/*": {"origins": "*"}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    GET /movies
    - requires the get:movies permission
    - returns the list of movies in the server with status code 200
    """

    @app.route("/movies")
    @requires_auth("get:movies")
    def getMovies(payload):
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        displayMovies = [movie.format() for movie in movies]

        return jsonify({"success": True, "movies": displayMovies}), 200

    """
    GET /actors
    - requires the get:actors permission
    - returns the list of actors in the server with status code 200
    """

    @app.route("/actors")
    @requires_auth("get:actors")
    def getActors(payload):
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors) == 0:
            abort(404)

        displayActors = [actor.format() for actor in actors]

        return jsonify({"success": True, "actors": displayActors}), 200

    """
    POST /movies
    - requires post:movies permission
    - payload should be json. The release date should be of iso format YYYY-MM-DD
      example payload: {"title":"MovieTitle", "release_date": "2020-12-30"}
    - returns json with id of the newly created movie and status code 200
    """

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def createMovie(payload):
        payload = request.json
        error = False
        body = {}
        try:
            movie = Movie(
                title=payload["title"],
                release_date=date.fromisoformat(payload["release_date"]),
            )
            movie.insert()
            body["id"] = movie.id
            body["success"] = True
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())
        finally:
            dbSessionClose()
        if error:
            abort(400)
        else:
            return jsonify(body), 200

    """
    POST /actors
    - requires post:actors permission
    - payload should be json. 
      example payload: {"name" : "ActorName", "age" : 23, "gender": "Female"} 
    - returns json with id of the newly created actor and status code 200
    """

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def createActor(payload):
        payload = request.json
        body = {}
        error = False
        try:
            actor = Actor(name=payload["name"], age=payload["age"], gender=payload["gender"])
            actor.insert()
            body["id"] = actor.id
            body["success"] = True
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())
        finally:
            dbSessionClose()
        if error:
            abort(400)
        else:
            jsonify(body), 200
        return jsonify(body), 200

    """
    DELETE /movies/<id>
    - requires delete:movie permission
    - if <id> not found, returns a 404 error
    - deletes the corresponding row for <id>
    - returns json with id of deleted movie and status code 200 
    """

    @app.route("/movies/<movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        error = False
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())
        finally:
            dbSessionClose()

        if error:
            abort(400)
        else:
            return jsonify({"success": True, "delete": movie_id}), 200

    """
    DELETE /actors/<id>
    - requires delete:actor permission
    - if <id> not found, returns 404 error
    - deletes the corresponding row for <id>
    - returns json with id of deleted actor and status code 200
    """

    @app.route("/actors/<actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        error = False
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())
        finally:
            dbSessionClose()

        if error:
            abort(400)
        else:
            return jsonify({"success": True, "delete": actor_id}), 200

    """
    PATCH /movies/<id>
    - requires patch:movies permission
    - payload should be json. The release date should be of iso format YYYY-MM-DD
      example payload: {"title":"MovieTitle", "release_date": "2020-12-30"}
    - returns json with details of the modified movie and status code 200
    """

    @app.route("/movies/<int:index>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def editMovie(payload, index):
        movie = Movie.query.get(index)
        if movie is None:
            abort(404)

        data = request.json

        if data is None:
            abort(400)

        error = False
        body = {}
        try:
            movie.title = data["title"]
            movie.release_date = data["release_date"]
            movie.update()
            body = movie.format()
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())
        finally:
            dbSessionClose()

        if error:
            abort(400)
        else:
            return jsonify({"success": True, "movie": body}), 200

    """
    PATCH /actors/<id>
    - requires patch:actors permission
    - payload should be json.
      example paylod: {"name":"ActorName", "age": 56, "gender": "Male"}
    - returns json with details of the modified actor and status code 200
    """

    @app.route("/actors/<int:index>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def editActor(payload, index):
        actor = Actor.query.get(index)
        if actor is None:
            abort(404)

        data = request.json
        error = False
        body = {}
        try:
            actor.name = data["name"]
            actor.age = data["age"]
            actor.gender = data["gender"]
            actor.update()
            body = actor.format()
        except Exception:
            dbSessionRollback()
            error = True
            print(sys.exc_info())

        if error:
            abort(422)
        else:
            return jsonify({"success": True, "actor": body}), 200

    """
    Error handlers
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad Request"}),
            400,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            500,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
