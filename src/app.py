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
from models import db, Users, Planets, People, FavoritePeople, FavoritePlanets


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


# Endpoint GET people TODOS
@app.route('/people', methods=['GET'])
def handle_people():
    response_body = {}
    people = db.session.execute(db.select(People)).scalars()
    response_body['results'] = [row.serialize() for row in people]
    response_body['message'] = 'Metodo GET people'
    return jsonify(response_body), 200


# Endpoint GET people por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people_id(people_id):
    response_body = {}
    people = db.session.execute(db.select(People)).scalar()
    response_body['results'] = [row.serialize() for row in people]
    response_body['message'] = 'Metodo GET people for ID'
    return jsonify(response_body), 200


# Endpoint GET planets TODOS
@app.route('/planets', methods=['GET'])
def handle_planet():
    response_body = {}
    planet = db.session.execute(db.select(Planets)).scalars()
    response_body['results'] = [row.serialize() for row in planet]
    response_body['message'] = 'Metodo GET planets'
    return jsonify(response_body), 200


# Endpoint GET planets por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    response_body = {}
    planet = db.session.execute(db.select(Planets)).scalar()
    response_body['results'] = [row.serialize() for row in planet]
    response_body['message'] = 'Metodo GET planets for ID'
    return jsonify(response_body), 200


# Endpoint GET y POST de todos los usuarios
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
                        password = data['password'],)
        db.session.add(user)
        db.session.commit()
        response_body['results'] = user.serialize() 
        response_body['message'] = 'Metodo POST users'
        return response_body, 200


# Endpoint GET de todos los planetas favoritos del usuario actual
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    response_body = {}
    # Buscar todos los planetas favoritos del usuario en la base de datos
    favorites = FavoritePlanets.query.filter_by(users_id=user_id).all()

    if favorites:
        # Preparar la respuesta con los planetas favoritos del usuario solicitado
        favorite_planets = [{'planet_id': fav.planets_id} for fav in favorites]
        response_body['favorite_planets'] = favorite_planets
        response_body['message'] = f'Lista de planetas favoritos para el usuario {user_id}'
        return response_body, 200
    else:
        response_body['message'] = f'No se encontraron planetas favoritos para el usuario {user_id}'
        return response_body, 404


# Endpoint POST planet Favoritos
@app.route('/favorite/<int:user_id>/planets', methods=['POST'])
def add_favorite_planets(user_id):
    response_body = {}
    data = request.json
    print(data)
    # Tomar una instancia de la Base de Datos FavoritePlanets
    favorite = FavoritePlanets(
        users_id = user_id,
        planets_id = data['planets_id'])
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = f'Respode el POST de favorite planets del usuario: {user_id}'
    return response_body, 200


# Endpoint DELETE planet Favoritos
@app.route('/favorites/<int:user_id>/planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    response_body = {}
    # Buscar el planeta favorito en la base de datos
    favorite = FavoritePlanets.query.filter_by(users_id=user_id, planets_id=planet_id).first()
    if favorite:
        # Eliminar el planeta favorito
        db.session.delete(favorite)
        db.session.commit()
        response_body['message'] = f'Planeta favorito {planet_id} eliminado para el usuario {user_id}'
        return response_body, 200
    else:
        response_body['message'] = f'Planeta favorito {planet_id} no encontrado para el usuario {user_id}'
        return response_body, 404


# Endpoint POST de people favoritos
@app.route('/favorite/<int:user_id>/people', methods=['POST'])
def add_favorite_people(user_id):
    response_body = {}
    data = request.json
    print(data)
    # tomamos instancia de la base de datos
    favorite = FavoritePeople(
        users_id = user_id,
        people_id = data['people_id'])
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = f'Respode el POST de favorite people del usuario: {user_id}'
    return response_body, 200


# Endpoint DELETE de people favorito del usuario
@app.route('/favorites/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(user_id, people_id):
    response_body = {}
    # Buscar el planeta favorito en la base de datos
    favorite = FavoritePlanets.query.filter_by(users_id=user_id, people_id=people_id).first()
    if favorite:
        # Eliminar el planeta favorito
        db.session.delete(favorite)
        db.session.commit()
        response_body['message'] = f'People favorito {people_id} eliminado para el usuario {user_id}'
        return response_body, 200
    else:
        response_body['message'] = f'People favorito {people_id} no encontrado para el usuario {user_id}'
        return response_body, 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
