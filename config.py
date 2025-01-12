"""This module contains configuration variables for differnt environments
"""


class DevelopmentConfig:
    """Configurations for development environment
    """
    SECRET_KEY = "9382714629836764"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_DATABASE_URI = "mysql://quickmindsuser:QuickMinds&1121@localhost/quickminds"
    DEBUG = True

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "realjmusee@gmail.com"
    MAIL_PASSWORD = "zkcnsfeeqmtboili"
    MAIL_DEFAULT_SENDER = "QuickMinds <realjmusee@gmail.com>"


class ProductionConfig:
    """Configurations for production environment
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""


active_configs = DevelopmentConfig()
