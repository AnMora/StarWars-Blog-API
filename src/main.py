"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
import json
import datetime
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Character, Planets, Vehicles

#from models import Person

# ///////////////////////////////////////////////////////////////////////////////////////////////////

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# ///////////////////////////////////////////////////////////////////////////////////////////////////

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    person = People.query.get(id)
    # return jsonify(error.to_dict()), error.status_code
    return jsonify(person), 200

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# DATOS PARA USER
# DATOS PARA USER
# DATOS PARA USER
@app.route('/user', methods=['GET'])
def get_user():
    # response_body = {
    #     "msg": "Hello, this is your GET /user/ response"
    # }
    # return jsonify(response_body), 200
    user = User.query.all()
    # lambda es la funcion flecha anonima de python y enlista los datos que tiene la data
    resultado = list(map(lambda x: x.serialize(),user))
    return jsonify(resultado)

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404() # el first_or_404() capta en el raw el primer id y sino, imprime que no existe
    return jsonify(user.serialize()) # serialize es un metodo reservado para serealizar nuestro objeto

@app.route('/user', methods=['POST'])
def add_user():
    # character = Character(name="angel", hair_color="brown", skin_color="black", eyes_color="blue", birth_day="12/12/12")
    request_body = json.loads(request.data)# loads es para que python entienda en datos json
    # Validar los datos recibidos
    if request_body["name"] == None and request_body["email"] == None and request_body["password"] == None:
        return "Hay datos incompletos, favor completarlos todos!"
    else:
        # return request_body["name"]
        user = User(name=request_body["name"], email=request_body["email"], password=request_body["password"])
        db.session.add(user)
        db.session.commit()
        return "Posteo exitoso"

@app.route('/user/<int:id>', methods=['PUT'])
def update_user():
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)

    request_body = request.get_json()

    if "name" in request_body:
        user.name = request_body["name"]

    db.session.commit()

    return jsonify("All good"), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return("User has been deleted successfully"), 200

# DATOS PARA FAVORITES
# DATOS PARA FAVORITES
# DATOS PARA FAVORITES
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorite = Favorites.query.all()
    resultado = list(map(lambda x: x.serialize(),favorite))
    return jsonify(resultado)

@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorites_by_id(id):
    favorite = Favorites.query.filter_by(id=id).first_or_404() # el first_or_404() capta en el raw el primer id y sino, imprime que no existe
    return jsonify(favorite.serialize()) # serialize es un metodo reservado para serealizar nuestro objeto

@app.route('/favorites', methods=['POST'])
def add_favorites():
    request_body = json.loads(request.data)
    # if request_body["name"] == None and request_body["Type"] == None:
    if request_body["name"] == None:
        return "Hay datos incompletos, favor completarlos todos!"
    else:
        # return request_body["name"]
        # favorite = Favorites(name=request_body["name"], Type=request_body["Type"])
        favorite = Favorites(name=request_body["name"])
        db.session.add(favorite)
        db.session.commit()
        return "Posteo exitoso"

@app.route('/favorites/<int:id>', methods=['PUT'])
def update_favorites(id):
    favorite = Favorites.query.get(id)
    if favorite is None:
        raise APIException('Favorites not found', status_code=404)

    request_body = request.get_json()

    if "name" in request_body:
        favorite = request_body["name"]

    db.session.commit()

    return jsonify("All good"), 200

@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorites_by_id(id):
    favorite = Favorites.query.filter_by(id=id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return("User has been deleted successfully"), 200

# DATOS DE CHARACTER
# DATOS DE CHARACTER
# DATOS DE CHARACTER
@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()
    # lambda es la funcion flecha anonima de python y enlista los datos que tiene la data
    resultado = list(map(lambda x: x.serialize(),character))
    return jsonify(resultado)

@app.route('/character/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = Character.query.filter_by(id=id).first_or_404() # el first_or_404() capta en el raw el primer id y sino, imprime que no existe
    return jsonify(character.serialize()) # serialize es un metodo reservado para serealizar nuestro objeto

# @app.route('/character', methods=['POST'])
# def add_character():
#     # character = Character(name="angel", hair_color="brown", skin_color="black", eyes_color="blue", birth_day="12/12/12")
#     request_body = json.loads(request.data)# loads es para que python entienda en datos json
#     # Validar los datos recibidos
#     if request_body["name"] == None and request_body["hair_color"] == None and request_body["skin_color"] == None and request_body["eyes_color"] == None and request_body["birth_day"] == None:
#         return "Hay datos incompletos, favor completarlos todos!"
#     else:
#         # return request_body["name"]
#         character = Character(name=request_body["name"], hair_color=request_body["hair_color"], skin_color=request_body["skin_color"], eyes_color=request_body["eyes_color"], birth_day=request_body["birth_day"])
#         db.session.add(character)
#         db.session.commit()
#         return "Posteo exitoso"

# @app.route('/character/<int:id>', methods=['DELETE'])
# def delete_character_by_id(id):
#     character = Character.query.filter_by(id=id).first_or_404()
#     db.session.delete(character)
#     db.session.commit()
#     return("User has been deleted successfully"), 200

# DATOS DE PLANETS
# DATOS DE PLANETS
# DATOS DE PLANETS
@app.route('/planets', methods=['GET'])
def get_planet():
    planet = Planets.query.all()
    resultado = list(map(lambda x: x.serialize(), planet))
    return jsonify(resultado)

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.filter_by(id=id).first_or_404() # el first_or_404() capta en el raw el primer id y sino, imprime que no existe
    return jsonify(planet.serialize()) # serialize es un metodo reservado para serealizar nuestro objeto

# DATOS DE CHARACTER
# DATOS DE CHARACTER
# DATOS DE CHARACTER
@app.route('/vehicles', methods=['GET'])
def get_vehicle():
    vehicle = Vehicles.query.all()
    resultado = list(map(lambda x: x.serialize(), vehicle))
    return jsonify(resultado)

@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle_by_id(id):
    vehicle = Vehicles.query.filter_by(id=id).first_or_404() # el first_or_404() capta en el raw el primer id y sino, imprime que no existe
    return jsonify(vehicle.serialize()) # serialize es un metodo reservado para serealizar nuestro objeto

# DATOS DE REGISTER
# DATOS DE REGISTER
# DATOS DE REGISTER
@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({
                "msg": "email is required"
            }), 400
        if not password:
            return jsonify({
                "msg": "password is required"
            }), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({
                "msg": "Username already exists"
            }), 400

        user = User()
        user.email = email
        hashed_password = generate_password_hash(password)
        print(password, hashed_password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": "thanks. your register was successfully", "status": "True"
        }), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)