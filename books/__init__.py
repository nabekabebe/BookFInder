from flask import Flask
from flask_session import Session

from .views import view_bp
from .api import api_bp
from .db import db
from .init_api import API


def create_app(config='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    Session(app)

    API.init_app(api_bp)
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    @app.route('/start')
    def start():
        return "Hello"

    return app
