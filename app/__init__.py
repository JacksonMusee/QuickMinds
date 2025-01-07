"""This module initialize the application and applies configuration
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import active_configs


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


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

    @login_manager.user_loader
    def load_user(user_id):
        """Required by login_manager to load user from session
        """
        from app.models import User
        return User.query.get(int(user_id))

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
