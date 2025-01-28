from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Category, Fact, Question
from app.core.forms import CategoryForm, FunFactForm, QuestionForm
from app.utils import admin_required

settings_bp = Blueprint("settings_bp", __name__)


@settings_bp.route("/settings", methods=["GET"])
@login_required
@admin_required
def settings():
    """Loads the settings page with all the required forms embedded.
    """
    active_tab = request.args.get("active_tab", "categories")
    category_items = Category.query.all()
    fun_fact_items = Fact.query.all()
    question_items = Question.query.all()

    category_form = CategoryForm()
    fun_fact_form = FunFactForm()
    question_form = QuestionForm()
    choices = []
    for item in category_items:
        choice = (item.id, item.name)
        choices.append(choice)
    fun_fact_form.category_id.choices = choices
    question_form.category_id.choices = choices

    categories = []
    for category in category_items:
        form = CategoryForm()
        form.name.data = category.name
        form.description.data = category.description
        item = (category, form)
        categories.append(item)

    fun_facts = []
    for fun_fact in fun_fact_items:
        form = FunFactForm()
        form.category_id.choices = choices
        form.category_id.data = fun_fact.category_id
        form.body.data = fun_fact.fact_body
        item = (fun_fact, form)
        fun_facts.append(item)

    questions = []
    for question in question_items:
        form = QuestionForm()
        form.category_id.choices = choices
        form.category_id.data = question.category_id
        form.body.data = question.question_body
        form.correct_answer.data = question.answers.get("correct_answer")
        form.wrong_1.data = question.answers.get("wrong_answers")[0]
        form.wrong_2.data = question.answers.get("wrong_answers")[1]
        form.wrong_3.data = question.answers.get("wrong_answers")[2]
        item = (question, form)
        questions.append(item)

    return render_template("core/settings.html", title="settings", active_tab=active_tab,
                           categories=categories, category_form=category_form,
                           fun_fact_form=fun_fact_form, fun_facts=fun_facts,
                           question_form=question_form, questions=questions)
