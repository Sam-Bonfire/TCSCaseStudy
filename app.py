from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)

db = SQLAlchemy()


@app.route('/')
def hello_world():
    return 'Hello World!'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_ENGINE + '://' + config.DB_USERNAME + ':' + config.DB_PASSWORD
    '@' + config.DB_HOST + ':' + config.DB_PORT + '/'
    config.DB_NAME

    db.init_app(app)
    return app


if __name__ == '__main__':
    create_app().run()
