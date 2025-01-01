"""Module defines forms related to core.
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional


class CategoryForm(FlaskForm):
    """Category form object prototype
    """
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
