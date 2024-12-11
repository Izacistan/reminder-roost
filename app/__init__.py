from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from .views import views
        from .auth import auth
        from .models import User, Task

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # Create the database
        db.create_all()

        # Setup Login Manager
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

    return app
