from flask_sqlalchemy import SQLAlchemy


# Flask-SQLAlchemy
# The db object contains all the functions and helpers from both sqlalchemy
# and sqlalchemy.orm. Furthermore it provides a class called Model
# that is a declarative base which can be used to declare models.

# Set autoflush to False, required for PostgreSQL (not on SQLite)
# http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.params.autoflush
db = SQLAlchemy(session_options={'autoflush': False})
