from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date
from datetime import date
import os

db = SQLAlchemy()

database_path = os.getenv("DATABASE_PATH").replace("\r", "")


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def dbSessionClose():
    db.session.close()


def dbSessionRollback():
    db.session.rollback()


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date, nullable=False, default=date.today())

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "title": self.title, "release_date": self.release_date}

    def __repr__(self):
        return f"<Movie {self.id} {self.title} {self.release_date}>"


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name, "age": self.age, "gender": self.gender}

    def __repr__(self):
        return f"<Actor {self.id} {self.name} {self.age} {self.gender}>"
