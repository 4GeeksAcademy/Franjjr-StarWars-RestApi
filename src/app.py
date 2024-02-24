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
from models import db, Users


# Instancias de configuracion
app = Flask(__name__)
app.url_map.strict_slashes = False
# Configuracion de la DB
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


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {"msg": "Hello, this is your GET /user response "}
    return jsonify(response_body), 200


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    response_body = {}
    if request.method == 'GET':
        # Logica para consultar la BD y devolver todos los usuarios
        users = db.session.execute(db.select(Users)).scalars()
        # .scalars() -> una lista pero como un objeto SQL Alchemy
        # .scalar() -> un registro pero como un objeto SQL Alchemy
        response_body['results'] = [row.serialize() for row in users]
        response_body['message'] = 'Metodo GET users'
        return response_body, 200
    if request.method == 'POST':
        # debo recibir el body desde el front
        data = request.json
        # Creando una instancia de la clase Users
        user = Users(   email = data['email'],
                        password = data['password'],
                        is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body['results'] = user.serialize() 
        response_body['message'] = 'Metodo POST users'
        return response_body, 200

# Endpoint para un usuario por id
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    response_body = {}
    print(id)
    if request.method == 'GET':
        response_body['message'] = 'Metodo GET de un usuario/id'
        return response_body, 200
    if request.method == 'PUT':
        response_body['message'] = 'Metodo PUT de un usuario/id'
        return response_body, 200
    if request.method == 'DELETE':
        response_body['message'] = 'Metodo DELETE de un usuario/id'
        return response_body, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
