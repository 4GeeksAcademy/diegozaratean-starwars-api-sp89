"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Director
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# INICIO CODIGO

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    # user = User.query.get(1)
    all_users = User.query.all()
    print('prueba donde lo puedo ver]')
    print(all_users)
    results = list(map(lambda user: user.serialize() ,all_users))
    print((results))
    # print(user.serialize())

    response_body = {
        "msg": "ten los usuarios ",
        "results": results
    }

    return jsonify(results), 200

@app.route('/director', methods=['GET'])
def get_directors():
    all_directors = Director.query.all()
    results = list(map(lambda user: user.serialize() ,all_directors))

    return jsonify(results), 200

@app.route('/director/<int:director_id>', methods=['GET'])
def get_director(director_id):
    print(director_id)
    # director = Director.query.get(director_id)
    director = Director.query.filter_by(id=director_id).one()
    print(director)
    print(director.serialize())
    # all_directors = Director.query.all()
    # results = list(map(lambda user: user.serialize() ,all_directors))

    return jsonify(director.serialize()), 200


@app.route('/top/', methods=['GET'])
def top():
    response_body = {
        "msg": "el top 3 de las mejoras pelicul;as de la hisotria ",
        "top": [
            "la vida es bella",
            "el pianista",
            "busqueda implacable"
        ]
    }

    return jsonify(response_body), 200


# FIN CODIGO

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
