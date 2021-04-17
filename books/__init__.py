import os

from flask import Flask, g
from flask_session import Session
from flask_restplus import Resource, Api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = "769f213c4ea89e980132232fb84a528755cd1029110f2d274dfeabd6b404896a"
    app.config["DATABASE_URL"] = "postgresql://postgres:niko1122@localhost/BookAPI"
    Session(app)

    # engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
    # conn = engine.connect()
    # db = scoped_session(sessionmaker(bind=engine))

    # from books.utils import db_helper

    # from . import db
    # db.init_app(app)

    from . import api
    # from . import views
    app.register_blueprint(api.api)
    # app.register_blueprint(views.view_bp)
    # a simple page that says hello

    return app
