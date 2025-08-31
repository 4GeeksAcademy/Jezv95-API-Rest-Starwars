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
from models import db, User,People,Planet,Favourites_people,Favourites_Planet
from sqlalchemy import select

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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


 # Users Route-------------

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    results = map(lambda user: user.serialize() ,all_users)

    response_body = {
        "msg": "these are all the users:",
        "users": list(results),
       

    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_userid(user_id):
    one_user = User.query.filter_by(id = user_id).first()
  

    return jsonify(one_user.serialize()), 200

@app.route("/user/favorites", methods=["GET"])
def get_user_favorites():
    user_id = request.args.get("user_id", type=int)

    fav_people = db.session.execute(
        select(Favourites_people).where(Favourites_people.user_id == user_id)).scalars().all()

    fav_planets = db.session.execute(
        select(Favourites_Planet).where(Favourites_Planet.user_id == user_id)).scalars().all()

    fav_results = (
        [f.serialize() | {"type": "character"} for f in fav_people] +
        [f.serialize() | {"type": "planet"} for f in fav_planets]
    )
    return jsonify(fav_results), 200

   # People Route------------- 

@app.route('/people', methods=['GET'])
def handle_people():
    all_people = People.query.all()
    people_results = map(lambda people: people.serialize() ,all_people)

    people_response_body = {
        "msg": "these are all the people:",
        "people": list(people_results),
    }
    return jsonify(people_response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_person(people_id):
    person = People.query.filter_by(id = people_id).first()
  

    return jsonify(person.serialize()), 200


@app.route('/people', methods=['POST'])
def add_people():

    person_body =request.get_json()
    
    person = People( 
        name=person_body['name'],
        eye_color=person_body['eye_color'],
        gender=person_body['gender'],
        hair_color=person_body['hair_color'],
        height=person_body['height'],)
    db.session.add(person)
    db.session.commit()
    
    addchar_response_body = {
        "msg": "a new character added succesfully",
        "character" : person.serialize()
        
    }
    return jsonify(addchar_response_body), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.filter_by(id = people_id).first()
  
    db.session.delete(person)
    db.session.commit()
    return jsonify({
        "msg": " Deleted succesfully",
        "character" : person.serialize()
        
    }), 200

 # Favorite People---------------------------------------------------------------
@app.route('/user/favorite/people', methods=['GET'])
def fav_people_list():
    fav_people = Favourites_Planet.query.all()
    favpe_results = map(lambda fav_people : fav_people.serialize() ,fav_people)

    people_Favs_response_body = {
        "msg": "these are all the Favorites characters:",
        "people": list(favpe_results),
    }
    return jsonify(people_Favs_response_body), 200

@app.route("/user/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user_id = int(3)

    person = db.session.get(People, people_id)
    if not person:
        raise APIException("Planet not found", status_code=404)

    exists = db.session.execute(
        select(Favourites_people).where(
            Favourites_people.user_id == user_id,
            Favourites_people.people_id == people_id
        )
    ).scalar_one_or_none()

    if exists:
        return jsonify({"msg": "It was already in favorites"}), 200

    fav = Favourites_people(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize() | {"type": "people"}), 201

@app.route("/user/favorite/people/<int:people_id>", methods=["DELETE"])
def remove_favorite_people(people_id):
    user_id = int(3)

    fav = db.session.execute(
        select(Favourites_people).where(
             Favourites_people.user_id == user_id,
            Favourites_people.people_id == people_id
        )
    ).scalar_one_or_none()

    if not fav:
        raise APIException("That person wasn't in your favorites", status_code=404)

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Person removed from favorites"}), 200


# Planets Route------------- 


@app.route('/planets', methods=['GET'])
def handle_planets():
    all_planets = Planet.query.all()
    planets_results = map(lambda planet : planet.serialize() ,all_planets)

    planets_response_body = {
        "msg": "these are all the planets:",
        "planets": list(planets_results),
    }
    return jsonify(planets_response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id):
    planet = Planet.query.filter_by(id = planet_id).first()
  

    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def add_planets():

    planet_body=request.get_json()
    planet = Planet( 
        name=planet_body['name'],
        diameter=planet_body['diameter'],
        gravity=planet_body['gravity'],
        population=planet_body['population'],
        climate=planet_body['climate'],)
    db.session.add(planet)
    db.session.commit()


    
    addplanet_response_body = {
        "msg": "a new planet added succesfully",
        
    }
    return jsonify(addplanet_response_body), 200


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.filter_by(id = planet_id).first()
  
    db.session.delete(planet)
    db.session.commit()
    return jsonify({
        "msg": " Deleted succesfully",
        "planet" : planet.serialize()
        
    }), 200


    # Favorite Planets---------------------------------------------------------------

@app.route('/user/favorite/planet', methods=['GET'])
def fav_planets_list():
    fav_planets = Favourites_Planet.query.all()
    favpl_results = map(lambda fav_planet : fav_planet.serialize() ,fav_planets)

    planets_Favs_response_body = {
        "msg": "these are all the Favorites planets:",
        "planets": list(favpl_results),
    }
    return jsonify(planets_Favs_response_body), 200

@app.route("/user/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = int(3)

    planet = db.session.get(Planet, planet_id)
    if not planet:
        raise APIException("Planet not found", status_code=404)

    exists = db.session.execute(
        select(Favourites_Planet).where(
            Favourites_Planet.user_id == user_id,
            Favourites_Planet.planet_id == planet_id
        )
    ).scalar_one_or_none()

    if exists:
        return jsonify({"msg": "It was already in favorites"}), 200

    fav = Favourites_Planet(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize() | {"type": "planet"}), 201

@app.route("/user/favorite/planet/<int:planet_id>", methods=["DELETE"])
def remove_favorite_planet(planet_id):
    user_id = int(3)

    fav = db.session.execute(
        select(Favourites_Planet).where(
            Favourites_Planet.user_id == user_id,
            Favourites_Planet.planet_id == planet_id
        )
    ).scalar_one_or_none()

    if not fav:
        raise APIException("That planet wasn't in your favorites", status_code=404)

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Planet removed from favorites"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


