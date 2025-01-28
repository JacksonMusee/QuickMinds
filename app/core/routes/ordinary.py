from flask import Blueprint, render_template, request, current_app, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Question, Fact
from app import db
import random
import math
from datetime import datetime

ordinary_bp = Blueprint("ordinary_bp", __name__)


@ordinary_bp.route("/")
def index():
    fun_facts = Fact.query.limit(3).all()
    current_year = datetime.now().year
    return render_template("core/index.html", fun_facts=fun_facts, current_year=current_year, title="Home")


@ordinary_bp.route("/profile")
@login_required
def get_profile():
    """Fetch and render current user's profile details
    """
    return render_template("core/profile.html", title="Profile")


@ordinary_bp.route("/take-quiz")
@login_required
def get_quiz():
    """Take random questions from the database
    """
    questions = Question.query.order_by(func.random()).limit(10).all()

    for question in questions:
        answers = question.answers.get("wrong_answers")
        answers.append(question.answers.get("correct_answer"))
        new_answers = answers[:]
        random.shuffle(new_answers)
        question.answers = new_answers

    return render_template("core/take-quiz.html", questions=questions, quiz_len=len(questions), title="Quiz")


@ordinary_bp.route("/mark-quiz/<int:quiz_len>", methods=["POST"])
@login_required
def mark_quiz(quiz_len):
    """Marks user answer and returns feedback
    """
    points = 0
    response = request.form.to_dict()

    for key, value in response.items():
        question = Question.query.filter_by(id=key).first()
        if value == question.answers.get("correct_answer"):
            points += 1

    try:
        current_user.total_points += points
        current_user.quizes_taken += 1
        current_user.average_score = math.floor(
            ((current_user.total_points + points) / (current_user.quizes_taken + 1)) * 100)
        db.session.commit()
    except Exception as error:
        current_app.logger.error(f"Error saving quiz results: {
                                 error}", exc_info=True)
        db.session.rollback()

    score = math.floor((points/quiz_len) * 100)

    return render_template("core/feedback.html", score=score, title="Quiz feedback")
