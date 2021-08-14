import os
import flask_migrate
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from dotenv import load_dotenv
import json

load_dotenv()

db_UserAndPass = os.getenv('DB_USER_AND_PASS', 'postgres:postgres')
db_host = os.getenv('DB_HOST', 'localhost:5432')
db_name = os.getenv('DB_NAME', "capstone")
db_path = os.getenv("DATABASE_URL", "postgresql://{}@{}/{}".format(
    db_UserAndPass, db_host, db_name))
# db_path = "postgresql://{}@{}/{}".format(
#     db_UserAndPass, db_host, db_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    # db.create_all()


'''

Movies

'''


class Movie(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    release_date = Column(String)

    def __init__(self, title, release_date, id=None):
        if id != None:
            self.id = id
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
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date
        }


'''

Actors

'''


class Actor(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender, id=None):
        if id != None:
            self.id = id
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
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
