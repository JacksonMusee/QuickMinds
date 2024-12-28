"""This modules contains configurations variables for differnt emviroment
"""


class DefaultConfig:
    """Configurations whih apply accross
    """
    SECRET_KEY = "9382714629836764"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"


class DevelopmentConfig(DefaultConfig):
    """Configurations for development environment
    """
    DEBUG = True


class ProductionConfig(DefaultConfig):
    """Configurations for production environment
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""
