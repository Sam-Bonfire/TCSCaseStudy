from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#db = SQLAlchemy()


if __name__ == '__main__':
    app.run()

from application import routes
