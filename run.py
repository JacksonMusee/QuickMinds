"""Start application server
"""
from app import create_app, db
# from .app.models import *

application = create_app()

# if __name__ == "__main__":
# with application.app_context():
#   print("App context active:", application.app_context().g is not None)
#   print("Database URI:", application.config.get("SQLALCHEMY_DATABASE_URI"))
#   db.create_all()
# application.run()
