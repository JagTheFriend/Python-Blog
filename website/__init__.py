from os import path
import logging as log

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

log.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(name)s - %(levelname)s: %(message)s',
    level=log.DEBUG
)


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "HelloWorld"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # initialize the database

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User
    create_database(app=app)
    login_manager = LoginManager()
    # redirect the user to the login page
    # if the user tries to visit a page without logging in
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """Allows to access the information about the user
        with that specific user ID"""
        return User.query.get(int(id))

    return app


def create_database(*, app: Flask):
    """Creates the database if it doesn't already exists"""
    if not path.exists(f"website/{DB_NAME}"):
        db.create_all(app=app)
        log.info(f"Created database called {DB_NAME!r}")
    log.info(f"Database called {DB_NAME!r} already exists")
