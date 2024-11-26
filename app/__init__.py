from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        db.create_all()

    return app
