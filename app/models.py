"""This module contains definitions for classes which map
to database tables
"""
from app import db
from flask_login import UserMixin
from datetime import datetime, timezone


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
    created_on = db.Column(db.DateTime(
        timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        """Method called when a User object is printed
        """
        return f"User: {self.name} Email: {self.email}"


class Question(db.Model):
    """This class maps to the Question table in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    question_body = db.Column(db.Text, nullable=False)
    answers = db.Column(db.JSON, nullable=False, default=dict)
    created_on = db.Column(db.DateTime(
        timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        """In case someone prints a Question object
        """
        return f"Question: {self.question_body}"


class Category(db.Model):
    """This class maps to the Category table in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(
        timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    fun_facts = db.relationship("Fact", backref="category")
    questions = db.relationship("Question", backref="category")

    def __repr__(self):
        """In case someone prints a Category object
        """
        return f"Category: {self.name}"


class Fact(db.Model):
    """This class maps to the Fact table in the database
    """
    id = db.Column(db.Integer, primary_key=True)
    fact_body = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    created_on = db.Column(db.DateTime(
        timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        """In case someone prints a Fact object
        """
        return f"Fun fact: {self.fact_body}"
