"""This module contains definition for classes which map
to database tables
"""
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """User object class. Maps to User table in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    terms_accepted = db.Column(db.Boolean, nullable=False)
    total_points = db.Column(db.Integer, nullable=False, default=0)
    quizes_taken = db.Column(db.Integer, nullable=False, default=0)
    average_score = db.Column(db.Float, nullable=False, default=0.0)
    average_quiz_duration = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """Method called when a User object is printed
        """
        return f"User: {self.name} Email: {self.email}"


class Question:
    """This class maps to the Question table in the database
    """
