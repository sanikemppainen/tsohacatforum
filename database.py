from app import app
from flask import session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"]=getenv("DATABASE_URL")
database=SQLAlchemy(app)
