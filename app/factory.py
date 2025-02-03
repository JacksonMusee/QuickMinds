import os
import json
import dotenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from app import db, login_manager, bcrypt, migrate, mail
from app.core.routes.ordinary import ordinary_bp
from app.core.routes.settings_bp import settings_bp
from app.core.routes.category_bp import category_bp
from app.core.routes.fun_fact_bp import fun_fact_bp
from app.core.routes.question_bp import question_bp
from app.access.routes.access_control import access_control_bp


def from_json():
    """A helper function to convert a app configurations json string to an object.
    """
    class config:
        pass

    dotenv.load_dotenv(override=True)
    config_str = os.getenv("QUICKMINDS_ENV_ACTIVE")
    config_obj = config()
    config_dict = json.loads(config_str)
    for key, value in config_dict.items():
        setattr(config_obj, key, value)

    return config_obj


def create_app():
    """Creates and return a flask app object
    """
    app = Flask(__name__)
    app.config.from_object(from_json())

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "access_control_bp.login"
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Required by login_manager to load user from session
        """
        from app.models import User
        return User.query.get(int(user_id))

    @app.errorhandler(Exception)
    def handle_all_errors(error):
        code = 500
        description = "A technical errror occurred on the server. Please try again later."

        if isinstance(error, HTTPException):
            code = error.code
            description = error.description
        return render_template("error.html", description=description, title="Error"), code

    app.register_blueprint(ordinary_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(fun_fact_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(access_control_bp)

    return app
