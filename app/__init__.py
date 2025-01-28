"""This module initialize the application and applies configuration
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from werkzeug.exceptions import HTTPException
from config import active_configs
import pymysql


pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()


def create_app():
    """Creates and return a flask app object
    """
    # app initialization and configuration
    app = Flask(__name__)
    app.config.from_object(active_configs)

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
        print(error)
        code = 500
        description = "A technical errror occurred on the server. Please try again later."

        if isinstance(error, HTTPException):
            code = error.code
            description = error.description
        return render_template("error.html", description=description, title="Error"), code

    # import register blueprints
    from app.core.routes.ordinary import ordinary_bp
    from app.core.routes.settings_bp import settings_bp
    from app.core.routes.category_bp import category_bp
    from app.core.routes.fun_fact_bp import fun_fact_bp
    from app.core.routes.question_bp import question_bp
    from app.access.routes.access_control import access_control_bp

    app.register_blueprint(ordinary_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(fun_fact_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(access_control_bp)

    return app
