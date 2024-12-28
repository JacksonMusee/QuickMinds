"""Start application server
"""

if __name__ == "__main__":
    from app import create_app

    application = create_app("config.DevelopmentConfig")
    application.run()
