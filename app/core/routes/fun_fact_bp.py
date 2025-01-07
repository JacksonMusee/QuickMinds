"""This module defines the a blueprint for routes for managing Fact objects
"""
from flask import Blueprint, current_app, flash, redirect, url_for, request, render_template
from flask_login import login_required
from ..forms import FunFactForm
from app.models import Fact, db, Category

fun_fact_bp = Blueprint("fun_fact_bp", __name__)


@fun_fact_bp.route("/settings/add-fun-fact", methods=["POST"])
@login_required
def add_fun_fact():
    """Create save a new fun fact to database
    """
    fun_fact_form = FunFactForm()
    category_items = Category.query.all()

    fun_fact_form = FunFactForm()
    choices = []
    for item in category_items:
        choice = (item.id, item.name)
        choices.append(choice)
    fun_fact_form.category_id.choices = choices

    if fun_fact_form.validate_on_submit():
        print("Form is valid")
        fact = Fact(fact_body=fun_fact_form.body.data,
                    category_id=fun_fact_form.category_id.data)
        try:
            db.session.add(fact)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            current_app.logger.error(f"Error adding new fun fact: {
                                     error}", exc_info=True)
            flash(message="Adding fun fact failed. Try again later",
                  category="danger")
        else:
            flash(message="Fun fact added successfully", category="success")

    return redirect(request.referrer)


@fun_fact_bp.route("/settings/update-fun-fact/<int:id>", methods=["POST"])
@login_required
def update_fun_fact(id):
    category_items = Category.query.all()

    fun_fact_form = FunFactForm()

    choices = []
    for item in category_items:
        choice = (item.id, item.name)
        choices.append(choice)
    fun_fact_form.category_id.choices = choices

    if fun_fact_form.validate_on_submit():
        fact = Fact.query.filter_by(id=id).first()
        if fact:
            fact.category_id = fun_fact_form.category_id.data
            fact.fact_body = fun_fact_form.body.data
            try:
                db.session.commit()
            except Exception as error:
                current_app.logger.error(f"Error updating fun fact: {
                                         error}", exc_info=True)
                flash(message="Updating failed. Try again later", category="danger")
            else:
                flash(message="Fun fact updated", category="success")
    else:
        flash(
            message=f"Failed. Invalid details", category="danger")
    return redirect(request.referrer)


@fun_fact_bp.route("/settings/delete-fun-fact/<int:id>")
@login_required
def delete_fun_fact(id):
    fact = Fact.query.filter_by(id=id).first()

    if fact:
        try:
            db.session.delete(fact)
            db.session.commit()
        except Exception as error:
            current_app.logger.error(f"Error deleting fun fact: {
                                     error}", exc_info=True)
            flash(message="Delete failed, try again later", category="danger")
        else:
            flash(message="Delete successful", category="success")
    else:
        flash(message="Fun fact not found", category="danger")

    return redirect(request.referrer)
