
from application import app 
from flask import render_template

#@app.route('/')
#def hello_world():
#    return 'Hello World!'


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

