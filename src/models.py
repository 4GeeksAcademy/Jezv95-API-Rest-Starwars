from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    favourites_people: Mapped[List["Favourites_people"]] = relationship(back_populates="user")
    favourites_planets: Mapped[List["Favourites_Planet"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return '<User ' + self.username + ' >'


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)

    favourite_planet: Mapped["Favourites_Planet"] = relationship(back_populates="planet", uselist=False)
    
    def __repr__(self):
        return '<Planet ' + self.name + ' >'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
        }



class People (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(120), nullable=False)

    
    favourite_person: Mapped["Favourites_people"] = relationship(back_populates="people", uselist=False)

    def __repr__(self):
        return '<People ' + self.name + ' >'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
        }

        
class Favourites_Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="favourites_planets")
    

    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey("planet.id"), nullable=False)
    planet = relationship("Planet", back_populates="favourite_planet")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize() if self.planet else None
        }

class Favourites_people(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(Integer, ForeignKey("people.id"), nullable=True)

    user = relationship("User", back_populates="favourites_people")
    people = relationship("People", back_populates="favourite_person")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people": self.people.serialize() if self.people else None
        }