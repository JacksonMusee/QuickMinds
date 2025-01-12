"""Module defines forms related to app access. Login, Signup
"""
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email


class SignupForm(FlaskForm):
    """Signup form object prototype
    """
    name = StringField("First Name", validators=[
                       DataRequired("Name is required")])
    email = EmailField("Email", validators=[
        Email("Enter a valid email"), DataRequired("Email is required")])
    password = PasswordField("Password", validators=[
                             DataRequired("Password is required")])
    password_confirm = PasswordField("Confirm Password", validators=[
        DataRequired("Re-enter password"), EqualTo("password", message="Your passwords must match")])
    gender = RadioField("Choose Gender", choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[
        DataRequired("Gender is required")])
    terms_accepted = BooleanField("I accept to all Terms and Conditions", validators=[
        DataRequired("You can't proceed without accepting terms and conditions")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """Login form object prototype
    """
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class PasswordResetForm(FlaskForm):
    """Take user email for resetting password
    """
    email = EmailField("Email address", validators=[DataRequired(
        "Email is required"), Email("Enter a valid email address")])


class NewPasswordForm(FlaskForm):
    """Form for setting new password
    """
    password = PasswordField("New password", validators=[DataRequired()])
    password_confirm = PasswordField("Enter new password again", validators=[
                                     DataRequired(), EqualTo("password", message="Passwords must match")])
