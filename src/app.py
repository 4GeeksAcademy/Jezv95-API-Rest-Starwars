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
from models import db, User,People,Planet
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
        "planets_fav":[],
        "people_fav":[],

    }

    return jsonify(response_body), 200



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



# Planets Route------------- 


@app.route('/planets', methods=['GET'])
def handle_planets():
    all_planets = Planet.query.all()
    planets_results = map(lambda planet : planet.serialize() ,all_planets)

    planets_response_body = {
        "msg": "these are all the people:",
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


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
