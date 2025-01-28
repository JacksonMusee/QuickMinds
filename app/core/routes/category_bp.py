from flask import Blueprint, render_template, current_app, flash, request, redirect
from flask_login import login_required
from app.models import Category
from app import db
from app.core.forms import CategoryForm

category_bp = Blueprint("category_bp", __name__)

'''
@category_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    """Loads the settings page with all the required forms embedded
    """
    category_form = CategoryForm()
    categories = Category.query.all()

    return render_template("core/settings.html", page_title="settings", category_form=category_form, categories=categories)
'''


@category_bp.route("/settings/add-category", methods=["POST"])
@login_required
def add_category():
    """Saves a category to database. This includes editing existing categories
    """
    category_form = CategoryForm()

    if category_form.validate_on_submit():
        category = Category(name=category_form.name.data,
                            description=category_form.description.data)

        try:
            db.session.add(category)
            db.session.commit()
        except Exception as error:
            current_app.logger.error(f"Error adding category: {
                                     error}", exc_info=True)
            db.session.rollback()
            flash(message="Adding category failed. Try again later",
                  category="danger")
        else:
            flash(message="Category added successfully", category="success")
    else:
        flash(message="Failed, Invalid details", category="danger")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=categories")


@category_bp.route("/update-category/<int:id>", methods=["POST"])
@login_required
def update_category(id):
    """Updates an existing category
    """
    category_form = CategoryForm()

    if category_form.validate_on_submit():
        category = Category.query.filter_by(
            id=id).first()
        if category:
            category.name = category_form.name.data
            category.description = category_form.description.data
            try:
                db.session.commit()
            except Exception as error:
                current_app.logger.error(f"Error updating category: {
                                         error}", exc_info=True)
                flash(message="Updating failed. Try again later", category="danger")
            else:
                flash(message="Category updated", category="success")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=categories")


@category_bp.route("/delete-category/<int:id>")
@login_required
def delete_category(id):
    """Deletes a category from database
    """
    category = Category.query.filter_by(id=id).first()

    if category:
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as error:
            current_app.logger.error(f"Error deleting category: {
                                     error}", exc_info=True)
            flash(message="Delete failed, try again later", category="danger")
        else:
            flash(message="Delete successful", category="success")
    else:
        flash(message="Category not found", category="danger")

    referrer = request.referrer.split("?active_tab=")[0]
    return redirect(f"{referrer}?active_tab=categories")
