"""
Config file to initialize the db.
"""

from flask_sqlalchemy import SQLAlchemy


# Configures the SQLite database, relative to the app instance folder.
DATABASE_URI = "sqlite:///movies-collection.db"

db = SQLAlchemy()


def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)


def create_app(app):
    # Creates the database tables using the SQLAlchemy ORM and the application context
    with app.app_context():
        db.create_all()
