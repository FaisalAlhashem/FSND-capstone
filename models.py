import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import json

load_dotenv()

db_UserAndPass = os.getenv('DB_USER_AND_PASS', 'postgres:postgres')
db_host = os.getenv('DB_HOST', 'localhost:5432')
db_name = os.getenv('DB_NAME', "trivia")
db_path = "postgresql://{}@{}/{}".format(
    db_UserAndPass, db_host, db_name)

db = SQLAlchemy()
