
#Comentarios sobre el proyecto:
#1.- He hecho el extra que pidió Álvaro si queríamos que es de que planeta era cada personaje.
#2.- He tenido que buscar informacion por IA para DateTime ya que no sabia cómo hacerlo

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relación de uno a muchos (user ==> Favoritos)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    # Relación de character con Planets (Cada personaje a qué planeta pertenece)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=False)

    # Relacion de uno a muchos
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="character")

    # Relación de character con Planets (Cada personaje a qué planeta pertenece)
    planet: Mapped["Planet"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "planet_id": self.planet_id
        }


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(100), nullable=False)
    length: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "length": self.length,
            "model": self.model
        }


class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

    # Relación
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")
    # Relación con Characters
    characters: Mapped[list["Character"]] = relationship(
        back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Relación de muchos a uno (Favoritos ==> Usuario), no va List porque cada favorito pertenece a un solo usuario
    user: Mapped["User"] = relationship(back_populates="favorites")
    # Siguientes relaciones iguales
    character: Mapped["Character"] = relationship(back_populates="favorites")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,
            "planet_id": self.planet_id,
            "created_at": self.created_at.isoformat()
        }
