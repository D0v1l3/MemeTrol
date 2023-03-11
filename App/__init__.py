from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from App.home.home_blueprints import home_blueprints

        app.register_blueprint(home_blueprints)

        from App.login.login_blueprints import login_blueprints

        app.register_blueprint(login_blueprints)

        from App.signup.signup_blueprints import signup_blueprints

        app.register_blueprint(signup_blueprints)

        db.create_all()
        db.session.commit()

    return app
