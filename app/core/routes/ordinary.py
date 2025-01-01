from flask import Blueprint, render_template

ordinary_bp = Blueprint("ordinary_bp", __name__)


@ordinary_bp.route("/")
def index():
    return render_template("core/index.html", page_title="Whatever")
