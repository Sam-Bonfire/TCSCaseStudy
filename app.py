from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_ENGINE + '://' + config.DB_USERNAME + ':' + config.DB_PASSWORD + \
        '@' + config.DB_HOST + ':' + config.DB_PORT + '/' + config.DB_NAME

    from routes import app as app_blueprint
    app.register_blueprint(app_blueprint)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'app.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_login):
        return User.query.get(user_login)

    return app


if __name__ == '__main__':
    create_app().run()
