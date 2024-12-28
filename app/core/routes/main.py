from flask import Blueprint, render_template

core_main_bp = Blueprint("core_main_bp", __name__)


@core_main_bp.route("/")
def index():
    return render_template("access/signup.html", page_title="Whatever")
