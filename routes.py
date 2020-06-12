from . import db
from flask import Blueprint, render_template

app = Blueprint('app', __name__)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("base.html", index=True)
