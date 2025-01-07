"""Module defines forms related to core.
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    """Category form object prototype
    """
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])


class FunFactForm(FlaskForm):
    """Fun fact form object prototype
    """
    category_id = SelectField("Category", validators=[
                              DataRequired()], coerce=int)
    body = TextAreaField("Fact", validators=[DataRequired()])


class QuestionForm(FlaskForm):
    """Question form prototype
    """
    category_id = SelectField("Category", validators=[
                              DataRequired()], coerce=int)
    body = TextAreaField("Question", validators=[DataRequired()])
    correct_answer = TextAreaField(
        "Correct Answer", validators=[DataRequired()])
    wrong_1 = TextAreaField("Wrong Answer 1", validators=[DataRequired()])
    wrong_2 = TextAreaField("Wrong Answer 2", validators=[DataRequired()])
    wrong_3 = TextAreaField("Wrong Answer 3", validators=[DataRequired()])
