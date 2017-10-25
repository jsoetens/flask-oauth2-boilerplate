from flask_sqlalchemy import SQLAlchemy


# Flask-SQLAlchemy
# The db object contains all the functions and helpers from both sqlalchemy
# and sqlalchemy.orm. Furthermore it provides a class called Model
# that is a declarative base which can be used to declare models.
db = SQLAlchemy()
