"""This module defines blueprint and associated routes for login, signup, pasword reset
logout, change password
"""

from flask import Blueprint, flash, current_app, render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.access.forms import SignupForm, LoginForm, PasswordResetForm, NewPasswordForm
from app import bcrypt, db
from app.models import User
from app.utils import generate_otp, store_otp, send_otp, verify_otp

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
            flash(message="Sign up successful. You can now login",
                  category="success")
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
                flash(message=f"Hey {user.name}, Welcome.", category="success")

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


@access_control_bp.route("/reset-password", methods=["POST", "GET"])
def reset_password():
    """Processes password reset requests
    """
    form = PasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            otp = generate_otp()
            store_otp(otp=otp, email=form.email.data)
            send_otp(email=user.email, otp=otp)
            return render_template("access/otp.html", title="Password Reset")
        else:
            form.email.errors.append("That user doesn't exist")

    return render_template("access/reset-password.html", form=form, title="Password Reset")


@access_control_bp.route("/check-otp", methods=["POST"])
def check_otp():
    """Verifies OTP and sets a new password for user
    """
    data = request.form.to_dict()
    otp = data.get("first") + data.get("second") + data.get("third") + \
        data.get("fourth") + data.get("fifth") + data.get("sixth")

    otp_is_valid, message = verify_otp(otp)

    if otp_is_valid:
        return redirect(url_for("access_control_bp.set_new_password"))
    else:
        flash(message=message, category="danger")
        return render_template("access/otp.html")


@access_control_bp.route("/set-new-password", methods=["POST", "GET"])
def set_new_password():
    form = NewPasswordForm()

    if form.validate_on_submit():
        email = session.get("email")
        user = User.query.filter_by(email=email).first()
        new_pass = bcrypt.generate_password_hash(form.password.data)
        user.password = new_pass
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            current_app.logger.error(f"Error saving new password after reset: {
                                     error}", exc_info=True)
            flash(
                message="Pasword reset failed. Please try again later or contact support", category="danger")
        else:
            flash(message="Password reset successful. Login with the new password",
                  category="success")
            return redirect(url_for("access_control_bp.login"))

    return render_template("access/new-password.html", form=form)
