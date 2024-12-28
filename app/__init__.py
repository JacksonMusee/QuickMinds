"""This module initialize the application and applies configuration
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(configs):
    """Creates and return a flask app object
    """
    # app initialization and configuration
    app = Flask(__name__)
    app.config.from_object(configs)

    db.init_app(app)
    login_manager.init_app(app)

    # import register blueprints
    from app.core.routes.main import core_main_bp

    app.register_blueprint(core_main_bp)

    return app
