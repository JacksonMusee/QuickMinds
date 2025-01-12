"""This module defines the a blueprint for routes for managing Question objects
"""
from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_login import login_required
from ..forms import QuestionForm
from ....app.models import Question, db, Category

question_bp = Blueprint("question_bp", __name__)


@question_bp.route("/settings/add-question", methods=["POST"])
@login_required
def add_question():
    """Create save a new question in the database
    """
    question_form = QuestionForm()
    category_items = Category.query.all()

    choices = []
    for item in category_items:
        choice = (item.id, item.name)
        choices.append(choice)
    question_form.category_id.choices = choices

    if question_form.validate_on_submit():
        answers = {"correct_answer": question_form.correct_answer.data,
                   "wrong_answers": [
                       question_form.wrong_1.data,
                       question_form.wrong_2.data,
                       question_form.wrong_3.data
                   ]}
        question = Question(question_body=question_form.body.data,
                            category_id=question_form.category_id.data,
                            answers=answers)
        try:
            db.session.add(question)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            current_app.logger.error(f"Error adding new question: {
                                     error}", exc_info=True)
            flash(message="Adding question failed. Try again later",
                  category="danger")
        else:
            flash(message="Question added successfully", category="success")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=questions")


@question_bp.route("/settings/update-question/<int:id>", methods=["POST"])
@login_required
def update_question(id):
    category_items = Category.query.all()

    question_form = QuestionForm()

    choices = []
    for item in category_items:
        choice = (item.id, item.name)
        choices.append(choice)
    question_form.category_id.choices = choices

    if question_form.validate_on_submit():
        question = Question.query.filter_by(id=id).first()
        answers = {"correct_answer": question_form.correct_answer.data,
                   "wrong_answers": [
                       question_form.wrong_1.data,
                       question_form.wrong_2.data,
                       question_form.wrong_3.data
                   ]}

        if question:
            question.category_id = question_form.category_id.data
            question.question_body = question_form.body.data
            question.answers = answers
            try:
                db.session.commit()
            except Exception as error:
                current_app.logger.error(f"Error updating question: {
                                         error}", exc_info=True)
                flash(message="Updating failed. Try again later", category="danger")
            else:
                flash(message="Question updated sucessfully", category="success")
    else:
        flash(
            message=f"Failed. Invalid details", category="danger")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=questions")


@question_bp.route("/settings/delete-question/<int:id>")
@login_required
def delete_question(id):
    question = Question.query.filter_by(id=id).first()

    if question:
        try:
            db.session.delete(question)
            db.session.commit()
        except Exception as error:
            current_app.logger.error(f"Error deleting question: {
                                     error}", exc_info=True)
            flash(message="Delete failed, try again later", category="danger")
        else:
            flash(message="Delete successful", category="success")
    else:
        flash(message="Question not found", category="danger")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=questions")
