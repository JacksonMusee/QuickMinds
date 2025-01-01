"""This module defines blueprint and associated routes for login, signup,
logout, change password
"""

from flask import Blueprint, flash, current_app, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import SignupForm, LoginForm
from app import bcrypt, db
from ...models import User

access_control_bp = Blueprint('access_control_bp', __name__)


@access_control_bp.route("/signup", methods=["POST", "GET"], strict_slashes=False)
def signup():
    """Register a new user
    """
    form = SignupForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        new_user = User(
            name=form.name.data, email=form.email.data, password=hashed_pass, gender=form.gender.data, terms_accepted=form.terms_accepted.data
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            current_app.logger.error(f"Error adding new user: {
                                     error}", exc_info=True)

            flash(
                message="An error occured on our side please try again later", category="danger")
            return render_template("access/signup.html", form=form)
        else:
            flash(message="Sign up successful", category="success")
            return redirect(url_for("access_control_bp.login"))

    return render_template("access/signup.html", form=form, title="Sign up")


@access_control_bp.route("/login", methods=["GET", "POST"])
def login():
    """Provides functionality for loging in a user
    """
    if current_user.is_authenticated:
        return redirect(url_for("ordinary_bp.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            form.email.errors.append("Email does not exist")
            return render_template("access/login.html", form=form)
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            form.password.errors.append("Wrong password")
            return render_template("access/login.html", form=form)
        else:
            try:
                login_user(user)
            except Exception as error:
                current_app.logger.error(f"Error logging in user: {
                                         error}", exc_info=True)
                flash(
                    message="An error occured on our side please try again later", category="danger")
            else:
                flash(message="Login Successful", category="success")

                next_page = request.args.get("next")
                # A function is required to validate next url to avoid crosssite whatever...

                return redirect(next_page) if next_page else redirect(url_for("ordinary_bp.index"))
    return render_template("access/login.html", form=form, title="Login")


@access_control_bp.route("/logout")
@login_required
def logout():
    """Logs out the current user
    """
    logout_user()
    return redirect(url_for("access_control_bp.login"))
